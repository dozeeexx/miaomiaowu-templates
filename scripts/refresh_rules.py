"""Stage, check and refresh public rules; preserve personal files and templates."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--accept-routing-changes', action='store_true',
                    help='Accept reviewed classification changes; protected checks still apply')
args = parser.parse_args()
CORE = os.environ['MIHOMO_BINARY']
POLICY = json.loads((ROOT / 'policy.json').read_text(encoding='utf-8'))
MANIFEST = json.loads((ROOT / 'source-manifest.json').read_text(encoding='utf-8'))

def get(item):
    request = urllib.request.Request(item['url'], headers={'User-Agent': 'mmw-v3-2026-rules/1.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    if not data or b'<html' in data[:300].lower(): raise ValueError(f'Invalid source: {item["name"]}')
    values = [x.strip() for x in data.decode('utf-8-sig').splitlines() if x.strip() and not x.startswith('#')]
    if len(values) < 5: raise ValueError(f'Unexpected short source: {item["name"]}')
    return item, data, values

def sanitize(name, values):
    removed, kept = [], []
    for line in values:
        domain = line.removeprefix('+.')
        reason = None
        if line.startswith('+.') and domain in POLICY['shared_suffixes']:
            reason = 'Shared CDN / infrastructure suffix is not exclusive to this service'
        elif re.fullmatch(r'execute-api\.[a-z0-9-]+\.amazonaws\.com', domain):
            reason = 'Shared regional AWS API endpoint'
        elif domain == POLICY['attribution_marker']:
            reason = 'Upstream attribution marker, not a service domain'
        elif line in POLICY['remove_by_set'].get(name, []):
            reason = 'Shared vendor domain has a more specific classification elsewhere'
        if reason: removed.append({'set': name, 'line': line, 'reason': reason})
        else: kept.append(line)
    kept = list(dict.fromkeys(kept + POLICY.get('add_by_set', {}).get(name, [])))
    return kept, removed

def domain_rule(line):
    if line.startswith('+.'): return 'DOMAIN-SUFFIX,' + line[2:]
    if '*' in line: return 'DOMAIN-WILDCARD,' + line
    return 'DOMAIN,' + line

with ThreadPoolExecutor(max_workers=4) as pool:
    # Download every source before writing artifacts; a failed download aborts the run.
    downloads = list(pool.map(get, MANIFEST))

new_manifest, removals = [], []
with tempfile.TemporaryDirectory() as temp:
    stage = Path(temp)
    datasets, source_urls = {}, {}
    for item, data, values in downloads:
        kind, filename = item['name'].split('/')
        name = filename.removesuffix('.list')
        if kind == 'domain':
            values, removed = sanitize(name, values)
            removals.extend(removed)
        elif kind != 'ipcidr': raise ValueError(f'Unsupported source kind: {kind}')
        datasets[(kind, name)] = values
        source_urls[(kind, name)] = item['url']
        new_manifest.append({'name': item['name'], 'url': item['url'], 'bytes': len(data),
                             'sha256': hashlib.sha256(data).hexdigest(), 'ok': True})
    merged = POLICY.get('merged_sets', {})
    for name, members in merged.items():
        datasets[('domain', name)] = list(dict.fromkeys(
            value for member in members for value in datasets[('domain', member)]))
        source_urls[('domain', name)] = 'policy.json merged_sets: ' + ', '.join(members)
    merged_members = {member for members in merged.values() for member in members}
    for (kind, name), values in datasets.items():
        if kind == 'domain' and name in merged_members: continue
        compiled_name = name if kind == 'domain' else name + '-ip'
        if kind == 'domain':
            classical = list(dict.fromkeys(domain_rule(v) for v in values))
        else:
            classical = [('IP-CIDR6' if ':' in v else 'IP-CIDR') + ',' + v +
                         (',no-resolve' if name in ['telegram', 'googlefcm'] else '') for v in values]
        rule_text = stage / 'rules' / 'mihomo' / (compiled_name + '.list')
        rule_text.parent.mkdir(parents=True, exist_ok=True)
        rule_text.write_text('\n'.join(values) + '\n', encoding='utf-8')
        subprocess.run([CORE, 'convert-ruleset', kind, 'text', str(rule_text),
                        str(rule_text.with_suffix('.mrs'))], check=True)
        output = stage / 'rules' / 'compat' / (compiled_name + '.list')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(f'# Generated from {source_urls[(kind, name)]}\n# Domain/IP rules only.\n' +
                          '\n'.join(classical) + '\n', encoding='utf-8')
    # Validate the staged snapshots before overwriting current artifacts.
    check_command = [sys.executable, str(ROOT / 'scripts' / 'check_rules.py'),
                     '--data-root', str(stage), '--audit-output', str(stage / 'routing-audit.json')]
    if args.accept_routing_changes: check_command.append('--accept-routing-changes')
    subprocess.run(check_command, check=True)
    for file in (stage / 'rules').rglob('*'):
        if file.is_file():
            # Compiler inputs stay temporary; clients use MRS or true classical text.
            if file.parent.name == 'mihomo' and file.suffix == '.list': continue
            destination = ROOT / file.relative_to(stage)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(file.read_bytes())
    (ROOT / 'routing-audit.json').write_bytes((stage / 'routing-audit.json').read_bytes())
(ROOT / 'source-manifest.json').write_text(json.dumps(new_manifest, ensure_ascii=False, indent=2), encoding='utf-8')
(ROOT / 'sanitization.json').write_text(json.dumps(removals, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Refreshed {len(downloads)} public sources; personal rules and templates preserved.')
