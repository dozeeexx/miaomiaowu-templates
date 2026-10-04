# 妙妙屋 V3 日常模板

阅读导航：[项目用途](#项目用途) · [分流方案](#分流方案) · [导入与使用](#导入与使用) · [长期维护](#长期维护) · [验证与使用边界](#验证与使用边界)

## 项目用途

这是以个人日常使用为目标、长期维护的 Clash/Mihomo 规则与订阅模板仓库。面向中国大陆网络环境，通过妙妙屋 V3 生成 FlClash、Clash Verge Rev 配置，并提供小火箭导入用的 Clash YAML 兼容版。两端的 DNS 与连接效果需分别验收。

| 使用需求 | 当前方案 |
|---|---|
| 国内访问与下载顺畅 | 大陆域名/IP、厂商大陆服务和已收录的游戏/下载域名优先直连 |
| 海外日常服务按用途选节点 | 覆盖 AI、加密货币、社交、开发、视频和音乐等分类 |
| 特定服务保持独立出口 | AI、加密货币、自定义1 可手动选择实际节点 |
| 个人网站持续补充 | 两份个人规则文件提供固定入口，不在 README 展示自用网站清单 |
| 模板简单、维护成本低 | 保留 16 个分组、18 个 provider、37 条顶层规则；仅一个测速组 |
| 规则长期更新且便于恢复 | 公共规则定时刷新、检查后发布；固定模板名、Git 提交与回滚说明 |

国内直连与必要的用途分类是主要目标；不设国家、广告拦截、游戏、Microsoft 或 FCM 独立组。具体出口由节点选择和客户端设置决定，模板不保证某条线路的实际速度。

## 分流方案

### 分组与默认行为

共 16 组，不设国家、广告拦截、游戏、Microsoft 或 FCM 独立组。

| 分组 | 默认与用途 |
|---|---|
| 🎯 节点选择 | 默认自动选择；也可手选实际节点 |
| ⚡ 自动选择 | 唯一测速组；按需每 600 秒测可用性/延迟，容差 80 ms |
| 🤖 AI、💰 加密货币、🧩 自定义1 | 默认跟随节点选择；可手动指定实际节点 |
| 🔖 自定义2 | 默认节点选择；也可选 DIRECT 或实际节点 |
| 🌐 Google、📺 YouTube、✈️ Telegram、💬 海外社交、🐙 GitHub、🎬 海外流媒体、🎵 TikTok、🎧 Spotify | 默认节点选择；可各自手选实际节点 |
| 🍎 Apple | 仅控制 `apple-proxy` 海外子集；默认节点选择，也可选 DIRECT |
| 🧭 兜底 | 未分类流量默认节点选择；可选 DIRECT 或实际节点 |

所有服务选择组都提供 `🎯 节点选择` 和实际节点，默认跟随全局选择，之后可逐组手选。`⚡ 自动选择` 只包含实际节点，避免与全局选择形成循环。图标是分组名称的一部分。`🧩 自定义1` 沿用 Polymarket 规则，`🔖 自定义2` 沿用个人网站规则；规则文件名、来源和优先级不变。

海外流媒体合并 Netflix、Disney+、Prime Video、HBO、Twitch。TikTok、Spotify 独立。普通 Microsoft/Apple 服务与其大陆子集直连；Copilot 归 AI，GitHub 单独分流。Apple 分组不能切换所有 Apple 请求的出口。

### 常用软件、网站与场景

以下按当前域名规则与优先级说明主要请求的归属，不按整个应用进程分类：

| 分组 / 策略 | 常用软件、网站、场景 | 范围或例外 |
|---|---|---|
| 🎯 节点选择 | 多数海外服务的默认出口入口 | 默认自动选择；服务组另选实际节点后，不再跟随这里 |
| ⚡ 自动选择 | 自动选可用、延迟较低的节点 | 不单独匹配网站；供节点选择使用，延迟不代表吞吐 |
| 🤖 AI | ChatGPT/OpenAI、Claude、Gemini、Copilot、Cursor、Perplexity、Grok、Meta AI | 专用 AI 域名优先；不是整个 Google、Microsoft、X、Facebook 都归 AI |
| 💰 加密货币 | Binance、OKX、Bybit、Bitget，集合内的钱包、RPC、行情网站；Fragment | Polymarket 主域另归专用组；第三方依赖按自己的规则 |
| 🧩 自定义1 | Polymarket 主站、CLOB、Gamma/Data API、主域下 WebSocket | `polymarket.com` 及全部子域 |
| 🔖 自定义2 | 个人常用网站与小众服务 | 清单自行维护；公开说明不列举实际域名 |
| 🌐 Google | 搜索、Gmail、Google Drive、Maps、Play、普通 Google API、安卓 FCM | Gemini → AI；YouTube → YouTube；大陆子集先直连，Play 控制接口有精确例外 |
| 📺 YouTube | YouTube 视频、直播、视频 CDN；YouTube Music 的同域请求 | `youtube.com`、`googlevideo.com` 等；通用 Google 登录/资源可走 Google |
| ✈️ Telegram | Telegram、`t.me`、Bot API、集合内服务器 IP | Fragment → 加密货币 |
| 💬 海外社交 | X/Twitter、Facebook、Instagram、Threads、Messenger、WhatsApp、Discord、LINE、Signal | 含 twimg、fbcdn、cdninstagram 等专用资源；Grok/Meta AI 专用域名 → AI |
| 🐙 GitHub | GitHub 网页/Raw/发布下载、GitLab、GitBook、npm 官方仓库 | 名称虽为 GitHub，范围是 `gits` 开发服务集合；Gitee → DIRECT，Copilot 专用域名 → AI |
| 🎬 海外流媒体 | Netflix、Disney+、Prime Video、HBO/Max、Twitch | 不包含所有海外视频网站；TikTok、Spotify、YouTube 另分 |
| 🎵 TikTok | TikTok 与集合内视频资源 | 国内抖音 → DIRECT；MarsCode/Trae 的 AI 域名 → AI |
| 🎧 Spotify | Spotify 音乐、播客与专用资源 | `spotify.com`、`scdn.co` 等 |
| 🍎 Apple | Apple Developer、TestFlight、`tv.apple.com`、指定 Apple 海外服务主机 | 仅命中 `apple-proxy` 且未被大陆规则抢先匹配的请求 |
| DIRECT（非新增分组） | 微信/QQ、支付宝、淘宝/京东、B 站、抖音、小红书、知乎；普通 Microsoft/Apple 域名；局域网 | 例如 Outlook/Office/OneDrive/Teams 主要域名、App Store/iCloud/APNs；Steam 等已收录下载域名也直连 |
| 🧭 兜底 | 当前没有专门收录的海外网站、论坛、购物和工具 | 如 Reddit、Quora、LinkedIn、Pinterest、Amazon/eBay、Notion 的主域通常在这里；Steam/Epic 商店主要域名也没有游戏专属组 |

Grok/Meta AI 使用独立域名时归 AI；如果某个内嵌功能的请求仍使用 `x.com` / `facebook.com`，则按海外社交处理，域名规则不能按 URL 路径区分。海外游戏加速器流量是否进入本模板，取决于加速器及客户端接管方式。

未分类域名若随后命中大陆 IP 规则则直连，否则走兜底。兜底默认也跟随节点选择，因此“没有专门分类”不会让普通海外请求失去代理。整个应用的共享登录、验证码、通话 IP 和其他依赖仍需看连接日志。

### 规则顺序与冲突处理

Mihomo 从上到下匹配，首个命中决定分组：

1. 局域网、环回、私有地址直连。
2. 🧩 自定义1（Polymarket）、🔖 自定义2（个人网站）。
3. Play 控制接口 `services.googleapis.cn` 精确匹配 Google；随后 `domestic` 的大陆域名、Apple/Microsoft 大陆子集、国内游戏/下载子集直连。
4. AI → 加密货币 → YouTube → Telegram → TikTok → Spotify。
5. 海外社交 → GitHub → Apple 海外子集 → 海外流媒体。
6. `vendor-direct`：普通 Microsoft/Apple 直连；随后普通 Google 走 Google。
7. Telegram 专用 IP → Telegram；FCM 精确 IP → Google；大陆 IP → DIRECT。
8. `MATCH` → 兜底。

正常交集不必全部删除，优先级决定它们的用途：

| 交集或共用域名 | 当前结果与处理 |
|---|---|
| Polymarket / crypto | 🧩 自定义1 |
| YouTube / Google | YouTube；通用 Google 集合放后面 |
| Telegram / 海外社交 | Telegram |
| Fragment / Telegram / crypto | 加密货币 |
| Grok、Meta AI / 海外社交 | AI |
| MarsCode、Trae / TikTok | AI |
| 大陆子集 / 海外集合 | 大陆直连优先，个人规则和 Play 精确例外除外 |
| Apple Siri/Intelligence 共用 `guzzoni.apple.com` | 大陆直连优先；仅靠同一域名无法区分功能 |

YouTube 的通用 `gvt1.com`、`gvt2.com`、`ggpht.com` 等后缀已收窄，普通 Google 下载/图片回到 Google；`yt3.ggpht.com`、`yt3.googleusercontent.com` 仍归 YouTube。共清理 20 条共享、过宽或非服务规则，清理策略见 [policy.json](policy.json)，实际记录见 [sanitization.json](sanitization.json)。

**不要将 `vendor-direct` 提前合入 `domestic`。** 两者虽然都走 DIRECT，但提前会抢走 Copilot、Apple 海外子集等专门分流。只有相邻、同策略的集合适合直接合并。

分组选择对命中该组的新连接有效。排查“选了节点但没生效”时，在客户端连接列表查看实际命中的规则、策略链和主机；再关闭相关旧连接或重启应用。HTTP/2、QUIC、WebSocket、推送长连接可能继续用旧出口。登录、验证码、共享 CDN 的请求可能属于其他组。

### 精简与效率

本次只合并同策略且连续的域名集合，两份模板保持相同的分组和路由：

| 新集合 | 原集合 | 策略 |
|---|---|---|
| `domestic` | cn、apple-cn、microsoft-cn、games-cn | DIRECT，位于海外分类之前 |
| `streaming` | netflix、disney、primevideo、hbo、twitch | 海外流媒体 |
| `vendor-direct` | microsoft、apple | DIRECT，位于专门分类之后 |

| 项目 | 精简前 | 当前 |
|---|---:|---:|
| 用户分组 | 16 | 16 |
| provider | 26 | 18（16 公共 + 2 个人） |
| 顶层规则 | 44 | 37（含 Play 精确例外） |
| 公共 MRS 文件 | 24 | 16 |
| 公共产物（MRS + 文本） | 48 | 32 |
| 公共 MRS 总大小 | 约 649 KiB | 约 647 KiB |

合并减少客户端下载规则集的次数、provider 管理和顶层匹配步骤；去除同集合重复项。仍追踪 24 个上游来源，来源信息没有丢失。域名与 IP 保持独立，适配 MRS 类型和 DNS 策略。

MRS 域名集合使用内核的索引结构匹配，并非每个连接逐行遍历全部约 13 万条规则。为减少文件大小删掉大陆覆盖，可能让国内请求落入代理，得不偿失。

当前设计在保留上述分类和国内覆盖的前提下开销较低。**不存在脱离实际网络的“理论最快模板”；本次没有证明真实访问速度提升。** 节点线路、拥塞、丢包、吞吐和 CDN 通常更影响速度；测速延迟最低不代表下载或视频最快。

已采用国内 DNS/CDN、海外 Fake-IP、节点域名独立解析、TCP 并发和唯一按需测速组。保留 IPv6，不全局封 QUIC/UDP，不额外堆测速、广告、进程或国家规则。只有实测发现 IPv6 绕路、国内 DNS 不合适等问题，再调整对应选项。海外游戏由加速器处理；TUN 与加速器的路由/DNS 兼容性需按实际客户端验证。

### Google Play 的窄范围例外

`services.googleapis.cn` 在大陆与 Google 集合中重叠。模板在个人规则之后、大陆直连之前加一条精确 Google 规则，使它与 Play API、图片和下载 CDN 同组；没有把整个 Google 集合提前，也没有将 `googleapis.cn` 全部代理。`fonts.googleapis.cn` 仍直连。

Mihomo 中，下列必要接口和下载域族的 DNS 经 Google 组发出：`services.googleapis.cn`、`clientservices.googleapis.com`、`play.googleapis.com`、`play.google.com`、`play-lh.googleusercontent.com`，以及 `xn--ngstr-lra8j.com`、`gvt1.com` 根域与子域。Google 独立选节点后，这些解析也跟随它；无新增分组或 provider。普通海外 DNS 仍跟随节点选择，YouTube 与 AI 的现有策略不变。

这是针对已发现的出口不一致风险的修正，不代表已证明某部手机的下载故障由此引起或已经解决。测试 Play 时先给 Google 组选择一个可用的实际节点，重开商店，分别检查小应用与较大应用下载；如仍失败，再核对连接日志中的新域名、IPv6、账号地区和实际线路。

### 分类与上游来源

公共规则主要读取 HenryChiao 聚合后的文本，在本仓库清理、合并并生成两种格式；并非客户端直接请求每个底层项目。以下为 Henry 文档的来源说明与本模板的采用情况（2026-10-04）：

表中 BM7 = [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)，Meta = [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat)。

| 分类 | Henry 文档列出的来源 / 本模板实际采用 | 示例范围 |
|---|---|---|
| 🤖 AI | MetaCubeX、SukkaW、ConnersHua、ACL4SSR | OpenAI、Gemini、Claude、Copilot、Groq、Perplexity、xAI、Cursor |
| 💰 加密货币 | BM7、Meta、ACL4SSR | Binance、OKX、Bybit、Bitget、集合内钱包/RPC/行情 |
| 🌐 Google | BM7、Meta | Google 搜索、邮件、网盘、地图、Play、API |
| 📺 YouTube | BM7、Meta | 视频网站、视频 CDN、相关音乐服务同域请求 |
| ✈️ Telegram | 本模板直接读取 Meta 的独立 Telegram 域名与 IP，未依赖 Henry 的社交集合分类 | Telegram、t.me、Bot API、服务器 IP；Fragment 被更早的 crypto 分类接管 |
| 💬 海外社交 | BM7、Meta | X/Twitter、Facebook、Instagram、Threads、Discord、WhatsApp、LINE、Signal 等 |
| 🐙 GitHub（`gits`） | BM7、Meta | GitHub、GitLab、GitBook、npm 等；上游含 Gitee，但本模板大陆优先直连 |
| 🎬 海外流媒体（`streaming`） | 五个原集合均为 BM7、Meta | Netflix、Disney+、Prime Video、HBO/Max、Twitch |
| 🎵 TikTok | BM7、Meta、jmdugan/blocklists | TikTok 及相关主机；这里只使用域名分类，不执行广告拦截 |
| 🎧 Spotify | BM7、Meta | Spotify 音乐、播客与专用 CDN |
| 🍎 Apple 分组（`apple-proxy`） | BM7、Elysian-Realme/FuGfConfig | Apple Developer、TestFlight、部分 Apple 海外服务 |
| 大陆域名直连（`domestic`） | cn：felixonmars/dnsmasq-china-list；apple-cn：felixonmars、SukkaW；microsoft-cn：Meta；games-cn：BM7、Meta | 大陆网站、Apple/Microsoft 大陆子集、收录的游戏/下载直连域名 |
| 普通 Microsoft/Apple 直连（`vendor-direct`） | microsoft、apple：BM7、Meta | 普通微软/苹果域名；专门分类先匹配 |
| 大陆 IP 直连（`cn-ip`） | NobyDa/geoip，经 Henry `cncidr` 导出为 `ipcidr/cn.list` | 未被更早规则分类的大陆目的 IP |
| FCM IP → Google | BM7、Meta，经 Henry `googlefcm` 集合导出 | 精确推送 IP 补充；FCM 域名由 Google 集合覆盖 |
| 🧩 自定义1、🔖 自定义2 | 本仓库个人维护，非 Henry 来源 | 预测市场专用规则、个人网站例外；自用域名清单不在本文展示 |
| 🎯 节点选择、⚡ 自动选择、🧭 兜底 | 模板策略逻辑，无独立上游规则集合 | 出口选择、测速、未分类流量 |

上游“示例范围”不等于所有请求最终归该组；本模板会清理共享规则并按前述优先级决定归属。具体下载 URL、快照校验值见 [source-manifest.json](source-manifest.json)。大陆 IP 的导出对应关系也已核对 Henry 的 [构建脚本](https://github.com/HenryChiao/MIHOMO_YAMLS/blob/main/.github/workflows/Merge_ruleset.yml)。

## 导入与使用

### 导入与升级

| 模板 | 用途 | 原始文件 |
|---|---|---|
| [DailyClash_v3.yaml](templates/DailyClash_v3.yaml) | FlClash / Clash Verge Rev；公共规则用 Mihomo MRS | [导入地址](https://raw.githubusercontent.com/dozeeexx/miaomiaowu-templates/main/templates/DailyClash_v3.yaml) |
| [Dailyxhj_v3.yaml](templates/Dailyxhj_v3.yaml) | 小火箭配置订阅用 Clash YAML；公共规则用 classical 文本 | [导入地址](https://raw.githubusercontent.com/dozeeexx/miaomiaowu-templates/main/templates/Dailyxhj_v3.yaml) |

1. 在妙妙屋 V3 中导入或上传对应模板，选择节点并生成订阅。桌面使用 DailyClash；小火箭使用 Dailyxhj，在妙妙屋订阅页面复制 **Shadowrocket** 专用链接，核对类型是 `t=clash-to-shadowrocket`。
2. 客户端更新订阅后，检查分组和规则是否完整。纯节点订阅不包含本仓库的分流配置。
3. 各服务选择组默认跟随“🎯 节点选择”；按需给 🤖 AI、💰 加密货币、🧩 自定义1 或其他组手动指定实际节点。

模板包含 `__PROXY_NODES__` 占位符，没有真实节点，不能直接作为客户端最终配置使用。系统代理、TUN、监听端口由客户端设置；模板不强制开启。

**2026-10-04 精简版更换了 provider 名称。使用更早版本的用户需要在妙妙屋同步两份新版模板，并重新生成、刷新完整订阅；只刷新规则集不能完成升级。** 后续保留模板文件名，不按日期另建多份模板。

**分组图标与名称升级**：本次所有分组增加图标，Polymarket → `🧩 自定义1`，自用网站 → `🔖 自定义2`。需要在妙妙屋同步两份模板、重新生成订阅，并在客户端刷新完整配置；只刷新规则集不会更新分组。名称变化后旧的分组选择记录可能无法沿用，请重新确认所选节点。

### 小火箭：选对下发路径

妙妙屋当前源码有两条不同的路径。公开界面中的 Shadowrocket 按钮使用第一条；VPS 实际版本和手机最终响应仍需核对。

| 请求类型 | 实际输出 | Reality 节点使用建议 |
|---|---|---|
| `t=clash-to-shadowrocket` | Clash YAML；绕过原生 conf 节点转换器 | 优先使用 Dailyxhj；在小火箭**配置**页右上角 `+` 添加订阅链接，再更新并使用配置 |
| `t=shadowrocket` | `[General]`、`[Proxy]` 等原生完整配置 | proxyparser v0.2.9 丢失 Reality 公钥与 short-id，当前不要用于 Reality 节点 |
| `t=auto` | 按请求 User-Agent 选择类型 | Shadowrocket UA 在当前源码中选到 `shadowrocket`；请明确使用第一条类型 |
| `t=uri` | 纯节点分享链接列表 | 同版本离线测试保留 Reality 参数；备用节点导入，不带本仓库分组/规则 |

小火箭[支持导入含节点的 Clash YAML](https://github.com/LOWERTOP/Shadowrocket#配置文件)。使用兼容版可以保留原有两份模板，无需先修改 VPS 转换器。不要将 DailyClash 的 MRS 版拿来替代：妙妙屋该路径会将 MRS 地址后缀改成 `.yaml`，而本仓库公共产物是 MRS 与 classical 文本，没有对应的 `.yaml` 规则文件。

2026-10-04 固定版本离线复现：12 个虚构 VLESS Reality 节点在 V3 展开后均保留参数；原生完整配置的公钥、short-id 均保留 0/12；URI 输出的 UUID、服务器、端口、SNI、指纹、flow、公钥、short-id 均通过 12/12 对比。较新 v0.3.0 的同一原生输出函数也未发现 Reality 参数处理，因此不能仅凭升级版本号认定修好。这里没有 iOS 实机导入或握手验证。

部署时应检查**手机实际请求类型与响应**，不能只检查服务器上生成的 YAML 文件：响应需是 YAML、Reality 字段完整、16 个分组及 18 个规则集有效，再在 iOS 测连接与分组切换。若已使用第一条且字段完整，原生转换器的缺陷不代表当前订阅受影响。小火箭解析 DNS、规则集刷新等行为仍以客户端为准。

路径依据：[妙妙屋请求分支](https://github.com/iluobei/miaomiaowu/blob/c56d147af351ed1f0006073f08999764b9d66075/internal/handler/subscription.go#L795)、[界面链接类型](https://github.com/iluobei/miaomiaowu/blob/c56d147af351ed1f0006073f08999764b9d66075/miaomiaowu/src/routes/subscription.index.tsx#L102)、[有缺陷的 v0.2.9 转换器](https://github.com/MMWOrg/mmwX-plugins/blob/ab5e17ea22a2b430621a6b0c1da5cd8ed6a25871/proxyparser/substore/shadowrocket_template.go)。升级服务后重新核对，勿使用旧结论代替响应检查。

### FCM 跟随 Google

Google 集合覆盖 `mtalk.google.com`、安装注册等 FCM 域名；另保留 26 个精确 `/32` 推送 IP，也指向 Google。不需要额外分组。

切换 Google 影响经过代理的新 FCM 连接；已有推送长连接可能需要重连。如果删除专用 IP 集合，无域名信息的推送 IP 连接可能落入兜底，不能保证跟随 Google。推送还取决于安卓 Google Play 服务、应用支持、后台运行及是否被代理接管。iOS 使用 APNs。

### 安卓与苹果通知验收

通知到达与打开应用后加载内容是两条不同链路；QQ 通知正常不能证明 Gmail 的推送链路也正常。

| 手机 / 应用 | 常见通知链路 | 本模板对应策略 |
|---|---|---|
| 安卓 QQ 等国内应用 | 厂商推送（小米/华为/OPPO 等）、应用自身连接等；随手机与应用版本变化 | 已收录的国内域名/IP 直连；不是全部使用 FCM |
| 安卓 Gmail（有正常 Google Play 服务） | 通常依赖 Google Play 服务的 FCM | 已收录的 FCM 域名/IP → Google；Gmail 内容请求也归 Google |
| iOS QQ、Gmail 等普通远程通知 | 通常由系统 APNs 接收，应用服务端可能经 FCM 再转 APNs | `push.apple.com` 及 courier 子域命中 DIRECT；打开 Gmail 后的内容请求仍按 Google 分流 |

安卓 FCM 长连接通常不会使用系统 HTTP 代理。手机上用 FlClash 的 VPN 接管时，需要把 Google Play 服务的流量纳入；不要在分应用代理中排除它。如果客户端允许 VPN 被绕过，FCM 可能走基础网络，在大陆会因此影响连接。26 个固定 IP 只是补充，并不覆盖 Google 所有动态地址；优先依靠域名及正确的 VPN 接管，不堆整段 Google IP。官方说明见 [FCM 网络配置](https://firebase.google.com/docs/cloud-messaging/network-configuration)。

小火箭原生 conf 转换器输出 `bypass-system = true`；Clash YAML 导入后的系统绕过设置需在客户端核对。iOS 系统推送可能走系统通道，并非每次都出现在小火箭连接日志。只有带域名、且进入规则引擎的 APNs 请求才能据此确认 DIRECT，不能声称所有 APNs 纯 IP 连接都被本模板强制直连。没有添加 Apple 全 IP 直连或端口例外；正常网络下先实测，遇到问题再查看实际连接。官方说明见 [Apple 推送网络要求](https://support.apple.com/en-us/102266)。

最简单的真机测试：

1. 开启代理，确认通知权限、Gmail 同步和 Google Play 服务正常；允许代理应用保持后台运行。
2. 将 QQ/Gmail 放到后台并锁屏 5–10 分钟，不强行停止应用。用另一账号或请熟人发一条 QQ 消息，再从另一邮箱发一封带时间标记的邮件。
3. 检查锁屏时是否收到两类通知，再点击 Gmail 通知确认正文能加载。邮件送达或同步可能延迟，不能用一次短延迟直接判断模板失败。
4. 在 Wi-Fi、移动数据下各试一次，再锁屏 20–30 分钟复测。iOS 同样测试 QQ 与 Gmail，并检查专注模式、通知摘要是否延后通知。

若安卓 QQ 正常而 Gmail 只有打开后才更新，先检查 FCM 接管、Google 节点、Play 服务、同步和省电限制。若 iOS 所有应用都不推送，先对比关闭小火箭的情况，并检查 APNs 网络与系统通知设置。模板自查通过不等于完成上述真机验证。

## 长期维护

### 个人规则

两份个人集合提供固定维护入口，新增网站时通常无需增加分组。自用网站清单不在公开 README 中展示。

| 文件 | 用途 | 分组 |
|---|---|---|
| `rules/polymarket.list` | 预测市场主站、API、WebSocket 等专用域名 | 🧩 自定义1 |
| `rules/personal-sites.list` | 个人常用网站、小众服务及直连规则的例外 | 🔖 自定义2 |

在 GitHub 编辑对应文件，每行写一条规则，**不附分组名称**。下面使用保留的示例域名，不代表实际清单：

```text
DOMAIN,api.example.invalid
DOMAIN-SUFFIX,example.invalid
```

- `DOMAIN` 只匹配该主机；`DOMAIN-SUFFIX` 匹配根域及全部子域。
- 注释以 `#` 开头。当前个人集合只接受这两种域名规则。
- 两个集合均优先于大陆直连，自定义1 的 Polymarket 规则优先于加密货币；精确主机例外不会扩大到整个根域。
- 新增重要网站时，可在 `checks.json` 加入主站/API 的预期分组，保护后续更新。
- 共享 CDN、云平台或钱包供应商仅在必要时添加明确的专用主机，避免扩大匹配范围。

公共更新脚本保留两个个人文件和两份模板。提交后等待校验通过，再刷新客户端对应规则集。Polymarket 的第三方钱包、RPC、验证码按各自规则分流，初期可将 🧩 自定义1 与 💰 加密货币选到同一适用节点。

隐私范围：本文不展示自用域名，但公共仓库里的个人规则文件、检查记录与历史提交仍可查看。需要保密的域名应维护在本地覆写或受控规则源，避免提交到公共仓库。

### 自动更新

| 内容 | 更新方式 | 生效条件 |
|---|---|---|
| 公共规则产物 | Actions 每日 UTC+8 08:30 拉取上游、清理、合并、编译并检查；也可手动运行 | 成功才提交；桌面客户端每 24 小时检查或手动刷新 |
| 两份个人规则 | 自己编辑并提交 GitHub | 桌面客户端每小时检查或手动刷新；下载需成功 |
| 模板主体、分组、规则顺序、DNS | 自己修改两份模板 | 妙妙屋同步模板、重新生成订阅，客户端刷新完整配置 |

客户端必须运行且能下载；GitHub 排队、Raw 缓存可能延迟。公共仓库长期无活动时 GitHub 可能停用定时工作流，维护时检查 [Actions](https://github.com/dozeeexx/miaomiaowu-templates/actions/workflows/rules.yml) 是否启用、最近一次刷新是否成功。

小火箭远程规则刷新由客户端及实际导入结果控制，不应假定直接继承 Mihomo 的 `interval`。仓库更新不代表 iOS 已拉取，需要检查客户端设置。

#### 防止自动更新改变已知分流

更新在临时目录生成全部公共产物，先通过以下检查，再覆盖仓库文件：

- 85 个重要域名的受保护分类（含 Play、FCM、APNs 和 QQ 的样例）。
- 当前 5,599 个根域、代表子域及个人/内联样例的分类回归。
- 新出现的跨代理分组交集类型。
- 两份模板分组与路由一致、兜底与 FCM 策略正确、Play DNS 跟随 Google、个人 DNS 优先级，以及 Mihomo 配置检查。

下载、编译或上述检查失败时，停止公共规则发布，保留上次版本。分类记录见 [routing-audit.json](routing-audit.json)。它是有限样例检查，无法保证所有未来域名、通配符、IP 或第三方依赖永不产生新交集；已知优先级仍会决定首个命中。

### 修改入口与维护操作

| 想修改什么 | 修改文件 | 注意事项 |
|---|---|---|
| Polymarket 或自用网站 | `rules/polymarket.list`、`rules/personal-sites.list` | 使用精确域名或必要的后缀；重要样例加到 `checks.json` |
| 公共来源中的过宽规则/补充主机 | `policy.json` 的 `remove_by_set` / `add_by_set` | 使用**合并前来源名**，如 `youtube`、`apple`；域名源格式中 `+.example.com` 表示后缀，`api.example.com` 表示精确主机 |
| 共享基础设施后缀过滤 | `policy.json` 的 `shared_suffixes` | 会影响全部域名源；只在确认确属共享时改 |
| 同策略集合合并 | `policy.json` 的 `merged_sets` | 同时同步两份模板的 provider、路由和有关 DNS 引用；不要跨优先级合并 |
| 上游地址 | `source-manifest.json` | 保持已有 `domain/…list`、`ipcidr/…list` 的标识和纯文本格式；bytes/sha256 由刷新脚本更新 |
| 分组、路由、DNS | `templates/` 下两份 YAML | 分组与 rules 块同步；保留当前引号与结构供检查脚本读取。两版 provider 格式、DNS 不完全相同 |
| 重要域名的预期分类 | `checks.json` | 只有明确想改变该域名策略时才改预期；新增样例也放这里 |
| 已核对的分类变化 | 运行下面的维护命令或工作流 | 由脚本生成 `routing-audit.json`，不要随意手改基线 |

`rules/mihomo/`、`rules/compat/`、`sanitization.json` 是生成文件。通常修改策略或来源后重新生成，不直接补丁产物，否则下次刷新会覆盖。仓库只有两个维护脚本，不依赖 Python 第三方库。

#### 更新失败怎么处理

1. 打开失败的 Actions 日志，找到具体来源、域名或交集。
2. 下载/编译失败：检查来源地址和网络，修复后手动运行，保持 `accept_routing_changes` 未勾选。
3. `Protected routes changed`：检查宽后缀、优先级和清理策略。先恢复正确分类；确实有意更改时，修改相应预期并核对两份模板。
4. `Known classifications changed` / `New cross-group overlaps`：核对旧/新分组。优先收窄错误规则或调整已有优先级；确实接受该变化时，手动运行工作流并勾选 `accept_routing_changes`，生成新基线。

接受开关只允许已核对的分类基线变化，**不会跳过受保护域名、两份模板一致性或内核配置检查**。日常定时刷新始终不启用该开关。

#### 本地维护命令

安装 Python 3.10+，下载官方 Mihomo v1.19.32（与工作流一致）。在仓库目录中执行，下面以 PowerShell 为例：

```powershell
$env:MIHOMO_BINARY = 'D:/tools/mihomo/mihomo.exe'  # 换成自己的实际路径
python scripts/check_rules.py                   # 校验当前文件
python scripts/refresh_rules.py                 # 联网刷新，校验后生成公共文件
git diff --stat
```

有意修改分组/顺序、且已核对分类变化时：

```powershell
python scripts/check_rules.py --accept-routing-changes  # 为当前产物生成已审核基线
python scripts/refresh_rules.py --accept-routing-changes # 接受已审核的上游变化并生成
```

按实际维护情形选择命令，不需要每次都运行两条。提交前查看变更，确认个人规则与模板没有被公共刷新改写。新增 provider/更换类型还需要同步两个模板；检查脚本不负责自动设计新分流。

#### 回滚

保留每次变更的 Git 提交。错误时可 Revert 对应提交，或将涉及的模板、策略和产物一起恢复到已验证的版本；先校验再提交。怀疑上游持续错误时，暂时停用定时工作流，修复后恢复。

仅规则产物变化：刷新客户端对应规则集。模板或 provider 名称变化：妙妙屋同步模板、重建订阅并刷新完整配置。不要只回滚产物而保留引用它的新模板。

## 验证与使用边界

### 当前验证记录

2026-10-04，Mihomo v1.19.32：

- 两份展开配置通过；各 16 组、37 条顶层规则、18 个 provider，当前各加载 132,659 条规则。
- 85 个受保护域名、5,599 个分类审计样例通过；Play 精确例外修正旧行为，其他已有样例分类未变。
- 两份配置各通过 157 次本地路由/节点切换验证、28 次服务分组跟随全局节点切换验证和 30 次 DNS/Fake-IP 验证，含图标名称、Play 域族、国内字体、AI、YouTube 的正反例。
- 实际刷新脚本验证了 32 份公共产物一致，并保留模板、个人文件和模拟的未来个人新增内容。
- 模拟新 Crypto/Google 交集：普通更新被拦截且原文件保留；审核开关允许该变化。模拟大陆源抢走 ChatGPT：即使开关启用仍被保护检查拦截。

本地验证使用 SOCKS/DNS 模拟服务，没有修改系统代理/TUN。尚未进行真实节点速度、远程 DoH、加速器兼容、客户端覆写或 iOS 实机验证。规则条数与审计样例数可能随成功的后续更新变化。

### DNS 与客户端边界

桌面主模板让大陆集合返回真实 IP，使用国内 DoH；DIRECT 出站使用国内 DNS；节点域名独立解析。普通海外 DNS 经节点选择，AI、加密货币、自定义1、自定义2 的 DNS 使用对应策略；个人集合 DNS 优先于大陆集合。Play 的精确主机和下载域族另用 Google DNS 策略，`services.googleapis.cn` 即使命中大陆 Fake-IP 排除也使用 Google 解析。已验证对应本地 DNS 策略优先级，远程 DoH 的可达性仍需实测。

系统代理不会接管所有 DNS 或应用流量。客户端覆写、TUN 设置、加速器可能改变行为；规则只能管理经过内核的连接。未知大陆域名可通过大陆 IP 补充直连，覆盖仍取决于上游数据及实际解析结果。

兼容版提供真正的 classical 文本；默认 DNS 不带 Mihomo 的 `#分组` 后缀。`clash-to-shadowrocket` 保留 YAML，字段在小火箭中如何解析、是否生效需检查客户端；不能把保留字段等同于支持全部 Mihomo 行为。原生 `shadowrocket` 转换器只替换 MRS URL 后缀、不翻译纯域名文本，并且不移植 Fake-IP、`nameserver-policy`、`direct-nameserver`。两条路径的 DNS 均不能套用桌面测试结论。

原生 conf 转换器还会插入 Google Rewrite/MITM 段，推荐的 YAML 路径绕过这个生成过程。导入后检查实际配置与节点；升级妙妙屋、转换器或客户端时，重新核对下发路径、Reality 参数、分组、规则加载与 DNS 行为。

### 文件索引与参考

- `templates/`：两份长期模板。
- `rules/`：两份个人文件、公共 MRS 和兼容文本。
- `scripts/refresh_rules.py`：下载、清理、合并、编译、暂存检查与发布。
- `scripts/check_rules.py`、`checks.json`、`routing-audit.json`：检查和审计基线。
- `policy.json`、`source-manifest.json`、`sanitization.json`：策略、来源快照、清理记录。
- `.github/workflows/rules.yml`：固定编译器版本、定时更新、手动更新和提交检查。

参考：[妙妙屋](https://github.com/iluobei/miaomiaowu) · [Henry 规则说明](https://github.com/HenryChiao/MIHOMO_YAMLS/blob/main/THEDOC/RULESET_README.md) · [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat) · [Mihomo](https://github.com/MetaCubeX/mihomo)。公共来源的许可与使用声明仍适用；分流不改变服务的地区或账号政策。
