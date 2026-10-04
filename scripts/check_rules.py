"""Check current templates, protected routes and changes to known classifications."""
from pathlib import Path
from itertools import combinations
import argparse
import fnmatch
import json
import os
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--data-root', type=Path, default=ROOT)
parser.add_argument('--audit-output', type=Path, default=ROOT / 'routing-audit.json')
parser.add_argument('--accept-routing-changes', action='store_true')
args = parser.parse_args()
RULE_ROOT = args.data_root / 'rules'
PERSONAL = {'polymarket', 'personal-sites'}

def lines(path):
    return [s.strip() for s in path.read_text(encoding='utf-8-sig').splitlines()
            if s.strip() and not s.lstrip().startswith('#')]

def template_rules(path):
    text = path.read_text(encoding='utf-8')
    block = text.split('\nrules:\n', 1)[1]
    return [json.loads(s.strip()[2:]) for s in block.splitlines() if s.strip().startswith('- ')]

files = sorted((ROOT / 'templates').glob('*_v3.yaml'))
assert len(files) == 2, 'Exactly two stable templates required'
routes = template_rules(files[0])
assert routes == template_rules(files[1]), 'Template routing differs'
assert routes[-1] == 'MATCH,兜底', 'Final fallback changed'
order = [(r.split(',')[1], r.split(',')[2]) for r in routes if r.startswith('RULE-SET,')]
assert order[0:2] == [('polymarket', 'Polymarket'), ('personal-sites', '自用网站')]
assert dict(order).get('googlefcm-ip') == 'Google', 'FCM IPs must follow Google'

patterns = {}
for name, _ in order:
    if name.endswith('-ip'): continue
    path = ROOT / 'rules' / f'{name}.list' if name in PERSONAL else RULE_ROOT / 'compat' / f'{name}.list'
    exact, suffix, wildcard = set(), set(), []
    for rule in lines(path):
        kind, domain = rule.split(',')
        domain = domain.lower()
        if kind == 'DOMAIN': exact.add(domain)
        elif kind == 'DOMAIN-SUFFIX': suffix.add(domain)
        elif kind == 'DOMAIN-WILDCARD' and name not in PERSONAL: wildcard.append(domain)
        else: raise ValueError(f'Unexpected domain rule: {name}: {rule}')
    patterns[name] = (exact, suffix, wildcard)

def hit(domain, name):
    exact, suffix, wildcard = patterns[name]
    parts = domain.lower().strip('.').split('.')
    return domain in exact or any('.'.join(parts[i:]) in suffix for i in range(len(parts))) or any(
        fnmatch.fnmatchcase(domain, p) for p in wildcard)

def route(domain):
    if domain == 'localhost' or any(domain.endswith('.' + d) for d in ['local', 'lan', 'home.arpa', 'internal']):
        return 'DIRECT', [('private', 'DIRECT')]
    matched = [(name, policy) for name, policy in order if name in patterns and hit(domain, name)]
    return (matched[0][1] if matched else '兜底'), matched

checks = json.loads((ROOT / 'checks.json').read_text(encoding='utf-8'))
failed = [{'domain': host, 'expected': expected, 'actual': route(host)[0]}
          for host, expected in checks.items() if route(host)[0] != expected]
assert not failed, f'Protected routes changed: {json.dumps(failed, ensure_ascii=False)}'

# Audit overseas roots and representative suffix children, plus personal/protected hosts.
# This is a finite regression corpus, not a proof over all possible future domains.
candidates = set(checks)
for name, policy in order:
    if name not in patterns or policy == 'DIRECT': continue
    exact, suffix, _ = patterns[name]
    candidates.update(exact)
    candidates.update(suffix)
    candidates.update('probe.' + d for d in suffix)
winners, pairs, overlaps = {}, set(), []
for host in sorted(candidates):
    winner, matched = route(host)
    winners[host] = winner
    groups = sorted({policy for _, policy in matched if policy != 'DIRECT'})
    if winner != 'DIRECT' and len(groups) > 1:
        pairs.update(combinations(groups, 2))
        overlaps.append({'domain': host, 'winner': winner, 'groups': groups})

baseline_path = ROOT / 'routing-audit.json'
if baseline_path.exists() and not args.accept_routing_changes:
    baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
    changes = [{'domain': host, 'old': old, 'new': route(host)[0]}
               for host, old in baseline['domain_winners'].items()
               if route(host)[0] != old and route(host)[0] not in ['Polymarket', '自用网站']]
    new_pairs = pairs - {tuple(p) for p in baseline['allowed_group_pairs']}
    assert not changes, f'Known classifications changed; update held: {json.dumps(changes[:30], ensure_ascii=False)}'
    assert not new_pairs, f'New cross-group overlaps; update held: {sorted(new_pairs)}'
elif not args.accept_routing_changes:
    raise RuntimeError('Routing baseline missing; initialize it explicitly after review')

core = os.environ['MIHOMO_BINARY']
with tempfile.TemporaryDirectory(prefix='mmw-check-') as temp:
    home = Path(temp)
    for file in files:
        text = file.read_text(encoding='utf-8')
        text = text.replace('proxies: null', 'proxies:\n  - name: "验证节点"\n    type: socks5\n    server: 127.0.0.1\n    port: 49198')
        text = text.replace('__PROXY_NODES__', '验证节点').replace('include-all-proxies: true', 'include-all-proxies: false')
        text = text.replace('type: "http"', 'type: "file"')
        def local_path(match):
            filename = Path(json.loads(match.group(1))).name
            name = Path(filename).stem
            if name in PERSONAL: path = ROOT / 'rules' / filename
            elif filename.endswith('.mrs'): path = RULE_ROOT / 'mihomo' / filename
            else: path = RULE_ROOT / 'compat' / filename
            assert path.exists(), path
            local = home / 'rules' / filename
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_bytes(path.read_bytes())
            return '    path: ' + json.dumps(str(local), ensure_ascii=False)
        text = re.sub(r'^    path: (.+)$', local_path, text, flags=re.MULTILINE)
        expanded = home / file.name
        expanded.write_text(text, encoding='utf-8')
        result = subprocess.run([core, '-t', '-d', str(home), '-f', str(expanded)], capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(f'Mihomo rejected {file.name}: {result.stdout}\n{result.stderr}')

report = {'protected_checks': len(checks), 'domain_winners': winners,
          'allowed_group_pairs': sorted([list(p) for p in pairs]),
          'overlap_count': len(overlaps), 'overlap_examples': overlaps[:30],
          'limits': 'Finite roots/subdomain regression; new dependencies still need connection logs.'}
args.audit_output.parent.mkdir(parents=True, exist_ok=True)
args.audit_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'{len(checks)} protected routes, {len(winners)} audit hosts, both Mihomo templates passed.')
