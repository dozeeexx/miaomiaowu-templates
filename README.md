# 妙妙屋 V3 日常模板

面向中国大陆用户：国内服务优先直连，海外服务按用途选择节点。适配 FlClash、Clash Verge Rev，以及通过妙妙屋转换的小火箭完整配置。

此仓库从零建立，只维护这次的新模板、规则和更新脚本。

## 两份固定模板

| 文件 | 用途 |
|---|---|
| [DailyClash_v3.yaml](templates/DailyClash_v3.yaml) | FlClash / Clash Verge Rev；公共规则用 Mihomo MRS |
| [Dailyxhj_v3.yaml](templates/Dailyxhj_v3.yaml) | 妙妙屋转换小火箭完整配置；使用 classical 文本规则 |

原始地址：

- Clash：`https://raw.githubusercontent.com/dozeeexx/miaomiaowu-templates/main/templates/DailyClash_v3.yaml`
- 小火箭入口：`https://raw.githubusercontent.com/dozeeexx/miaomiaowu-templates/main/templates/Dailyxhj_v3.yaml`

在妙妙屋 V3 中上传或导入对应模板，选择节点并生成订阅。小火箭选择完整配置输出。两份模板本身没有真实节点，不能直接作为客户端最终配置使用；纯节点订阅不带这些分流规则。

模板名称保持稳定，后续更新文件内容即可。妙妙屋中保存的模板主体需要同步新版；规则集会按下述机制更新。

## 16 个分组

节点选择、自动选择、AI、加密货币、Polymarket、自用网站、Google、YouTube、Telegram、海外社交、GitHub、海外流媒体、TikTok、Spotify、Apple、兜底。

- AI、加密货币、Polymarket 只手选实际节点，首次使用请选定合适节点。
- 一般服务默认跟随“节点选择”；手选实际节点后使用该组自己的选择。
- 自用网站、Apple、兜底也可选择 DIRECT。
- 海外流媒体包含 Netflix、Disney+、Prime Video、HBO、Twitch；TikTok、Spotify 各自独立。
- 普通 Microsoft 服务直连；Copilot 走 AI，GitHub 单独分流。
- Apple 分组仅控制 apple-proxy 海外子集；普通 Apple、大陆子集优先直连。
- 不设国家、广告拦截、游戏或 FCM 独立分组。

### FCM 跟随 Google

FCM 的 mtalk、安装注册等域名已被 Google 集合覆盖。另保留 26 个精确推送 IP 的小型补充集合，也指向 Google，不增加分组。

因此切换 Google 分组会影响经过代理的新 FCM 连接。已有推送长连接可能需要重连。若既删掉 FCM 专用 IP 规则，也没有域名信息，直接连接推送 IP 的流量通常落入兜底；不能保证跟随你另选的 Google 节点。

FCM 是否能推送还取决于安卓 Google Play 服务、应用支持、后台运行及连接是否经过代理。iOS 推送使用 APNs。

## 个人规则

| 文件 | 当前内容 | 分组 |
|---|---|---|
| [polymarket.list](rules/polymarket.list) | polymarket.com 及子域，覆盖主站、API、WebSocket | Polymarket |
| [personal-sites.list](rules/personal-sites.list) | 精确 cdn.jucode.cn；shlii.io 及子域 | 自用网站 |

在 GitHub 编辑这两个文件即可长期维护。每行使用 DOMAIN 或 DOMAIN-SUFFIX，不附分组名称：

```text
DOMAIN,cdn.jucode.cn
DOMAIN-SUFFIX,shlii.io
```

两个集合排在大陆规则之前。cdn.jucode.cn 默认走自用网站；整个 jucode.cn 不会因此被代理。Polymarket 优先于加密货币集合。公共更新脚本保留两个个人文件及模板。

Polymarket 使用第三方钱包、RPC、验证码时，请用连接日志确认依赖；初期可将 Polymarket 与加密货币选到同一适用节点。共享云/CDN 后缀不宜归到个人组。

## 匹配顺序与重叠

Mihomo 从上到下匹配，首个命中生效：

1. 局域网、环回、私有地址直连。
2. Polymarket、自用网站。
3. 中国大陆域名、Apple/Microsoft 大陆子集、国内游戏/下载子集直连。
4. AI、加密货币、YouTube、Telegram、TikTok、Spotify。
5. 海外社交、GitHub、Apple 海外子集、海外流媒体。
6. 普通 Microsoft/Apple 直连，普通 Google 走 Google。
7. Telegram 专用 IP → Telegram；FCM 精确 IP → Google；大陆 IP 直连。
8. MATCH → 兜底。

当前仍有上游集合的正常交集，结果由顺序明确决定：

| 重叠 | 生效策略 |
|---|---|
| Polymarket / crypto | Polymarket |
| YouTube / Google | YouTube |
| Telegram / 海外社交 | Telegram |
| Fragment / Telegram / crypto | 加密货币 |
| Grok、Meta AI / 海外社交 | AI |
| MarsCode、Trae / TikTok | AI |

YouTube 集合中的 gvt1.com、gvt2.com、ggpht.com 等共用后缀已收窄，普通 Google 下载/图片回到 Google；保留 yt3.ggpht.com 和 yt3.googleusercontent.com 归 YouTube。已清理 20 条共享或过宽规则，策略保存在 [policy.json](policy.json)。

分组选择对命中该组的新连接有效。旧 HTTP/2、QUIC、WebSocket、推送连接可能继续使用旧出口；必要时重连。共享登录、验证、CDN 请求按自己的规则走，不保证整个应用的所有第三方请求同出口。

## 自动更新

有两层更新：

- **仓库**：GitHub Actions 每日 UTC+8 08:30 尝试拉取上游、清理、检查并生成 MRS/文本。GitHub 可能排队延迟。也可在 [Actions](https://github.com/dozeeexx/miaomiaowu-templates/actions) 手动运行。
- **桌面客户端**：公共规则每 24 小时检查，个人规则每小时检查；需要客户端运行且下载成功。模板主体、分组与规则顺序不会因 provider 更新而改变。

更新前执行 69 个受保护域名检查、5,575 个初始根域/代表子域的分类回归，以及两份 Mihomo 配置检查。已知域名的策略改变，或出现新的未确认跨分组重叠类型时，停止发布公共产物，保留上次版本。审计记录为 [routing-audit.json](routing-audit.json)。

这些检查减少自动更新引入误分流的风险，无法证明未来所有域名、路径、第三方依赖永远正确。检查失败可在 Actions 日志查看原因；确认属于有意调整后，再修改检查/策略并更新审计基线。

小火箭的远程规则刷新方式/间隔由小火箭及妙妙屋转换结果控制，不直接继承 Mihomo 的 interval。仓库规则会更新，iOS 是否及时拉取需检查客户端设置。

## 速度与效率

已采用：国内优先直连与国内 DNS/CDN、海外 Fake-IP、节点域名独立解析、TCP 并发、仅一个按需测速组、24 份公共 MRS 总计约 649 KiB。

模板不强制开启 TUN、系统代理或监听端口；不全局封 QUIC/UDP，不增加广告、进程或国家规则。国内游戏继续直连，海外游戏由加速器处理。TUN 与加速器的路由/DNS 冲突需在客户端按实际情况处理。

这是一份开销较低、可维护的配置，**没有真实节点与运营商线路测试，不能称为速度最优解**。速度主要取决于节点线路、拥塞、丢包、吞吐和 CDN。url-test 延迟最低不等于大文件/视频最快；更换更适合的线路通常比继续堆模板参数更有效。

默认保留 IPv6；若实测存在 IPv6 丢包/绕路，再按网络调整。国内解析效果不佳时再比较本地运营商 DNS 与当前 DoH。没有实测证据时不继续增加测速组、并行解析或额外分组。

## DNS 与小火箭边界

桌面主模板：国内域名返回真实 IP，使用国内 DoH；DIRECT 出站用国内 DNS。节点域名独立解析。普通海外 DNS 经节点选择；AI、加密货币、Polymarket、自用网站分别使用对应策略。个人 DNS 策略优先于大陆集合，已验证 cdn.jucode.cn 覆盖生效。

系统代理不会接管所有 DNS/应用流量。客户端覆写可能修改模板行为。

妙妙屋依赖的 proxyparser v0.2.9 只把 MRS URL 后缀替换成 list，不翻译纯域名文本，所以 Dailyxhj 提供真正的 classical 规则。转换器也不移植 Mihomo 的 Fake-IP、nameserver-policy、direct-nameserver。兼容版默认 DNS 不带 Mihomo #分组 后缀；iOS DNS 需实测，不能照搬桌面验证结论。

转换器可能自动插入 Google Rewrite/MITM 段，导入后检查。确认每个分组有小火箭支持的节点。

## 验证与维护文件

本地 Mihomo v1.19.32：两份展开 YAML 通过；各 16 组、44 条顶层规则、26 个 provider，加载各 132,713 条；各 129 次本地路由/节点切换与 12 次 DNS 检查通过。

刷新脚本离线验证：48 份公共产物一致；个人新增内容和两份模板保持不变；模拟新的 Crypto/Google 重叠后，刷新被拦截，原文件完全保留。

验证使用本地 SOCKS/DNS 模拟服务器；尚无真实节点速度、远程 DoH、游戏加速器、客户端覆写或 iOS 实机测试。

- templates/：两份长期模板。
- rules/：两份个人规则，以及公共 MRS/兼容文本。
- scripts/refresh_rules.py：下载、暂存、验证、生成公共产物。
- scripts/check_rules.py、checks.json、routing-audit.json：更新检查与审计基线。
- source-manifest.json、policy.json、sanitization.json：来源快照和清理策略。

## 上游来源

AI/crypto 直接采用 HenryChiao 的聚合规则，清理后统一生成两种格式：

| 分类 | Henry 文档列出的聚合来源 | 范围 |
|---|---|---|
| AI | MetaCubeX、SukkaW、ConnersHua、ACL4SSR | OpenAI、Gemini、Claude、Copilot、Groq、Perplexity、xAI、Cursor 等 |
| 加密货币 | blackmatrix7、MetaCubeX、ACL4SSR | Binance、OKX、Bybit、Bitget、钱包、RPC、行情等 |

- [妙妙屋](https://github.com/iluobei/miaomiaowu)
- [Henry 规则说明](https://github.com/HenryChiao/MIHOMO_YAMLS/blob/main/THEDOC/RULESET_README.md)
- [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat)：独立 Telegram 域名与 IP。
- [Mihomo](https://github.com/MetaCubeX/mihomo)：规则内核与编译器。

具体 URL 与校验值在 source-manifest.json。公共来源的许可与使用声明仍适用；规则分类不改变各服务的地区、账号或访问政策。
