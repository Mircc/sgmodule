# AdBlock-CN · 国内 App 去广告规则集

> 本目录（`AD-Rules/`）由 GitHub Actions **每 3 天（≈72 小时）自动重建**。
> 上游出现大幅删规则或链接失效时会自动停止更新并保留现有产物，绝不会把坏结果推上来。
> 详见[上游异常保护](#六上游异常保护上游出事时不删本地)。

---

## 开篇：这是什么，以及我不是谁

### 先说清楚：我不是创造者，只是搬运工

**本项目不生产任何一条去广告规则。**

这里所有的规则都来自社区里那些长期维护、默默更新的开源项目。我做的事情只有一件——
把散落在各个仓库里的规则**搬过来、洗干净、摞整齐**，再原样交还给你。
规则的真正价值，属于下面[鸣谢](#十三鸣谢)里每一位作者。

### 为什么要做这件事

因为现在的去广告规则有三个很实际的痛点：

1. **多，而且散** —— 想要比较完整的覆盖，你得同时订阅四五个源，它们各自更新、各自为政。
2. **重复严重** —— 几个大源之间互相引用，同一个广告域名在不同的规则中被重复收录。
   手机上每一条规则都要占用匹配开销，重复就是白白耗电。
3. **水土不服** —— 通用规则库为了"全球通用"塞进了几十万条境外域名，
   而国内用户一辈子也不会访问其中的绝大多数。这些规则躺在手机里，
   只是让 Surge 每次请求都多匹配几万次。

### 目标：为手机移动端而生的精简规则集

借助 AI 对全量规则做交叉分析后，产出一个满足下面这些目标的规则集：

| 目标 | 做法 |
| --- | --- |
| **精简** | 多源合并后跨源去重 + 父子域收敛，杜绝同一条规则被重复匹配 |
| **无冗余** | 父域已收录时自动剔除冗余子域；`DOMAIN-SET` 一条引用替代上万条内联 |
| **省电、性能好** | 剔除 90% 与国内用户无关的境外域名，规则总量从 31 万降到 2.3 万，匹配开销大幅下降 |
| **覆盖主流 App** | 保留全部人工精选的国内 App 规则，并用知名度榜单捞回主流国际 App 的广告域 |
| **不牺牲功能** | 严格区分 MITM：主体规则无需解密即可生效，需要解密的单独标注 |

### 声明

- 本项目仅为**规则整合与格式转换**，不对上游规则的拦截效果作任何担保。
- 各上游规则的版权与许可归各自作者所有，使用时请遵循其原始许可。
- 若你是上游规则作者，且不希望自己的规则出现在这里，请及时联系，我会立刻移除。
- 拦截效果因 App 版本、地区、网络环境而异，遇到问题请先查[误杀处理](#十二误杀处理)。

---

## 一、订阅地址

把下面的 `Mircc/sgmodule` 换成你自己的仓库路径（默认分支若为 `master` 请一并替换 `main`）。

| 文件 | 用途 | 地址 |
| --- | --- | --- |
| `AdBlock-CN.sgmodule` | **主模块（推荐）**，主规则无需 MITM，域名集走远程引用 | `https://raw.githubusercontent.com/Mircc/sgmodule/main/AD-Rules/AdBlock-CN.sgmodule` |
| `AdBlock-CN-Standalone.sgmodule` | 完全内联版，不依赖远程域名集，离线可用 | `https://raw.githubusercontent.com/Mircc/sgmodule/main/AD-Rules/AdBlock-CN-Standalone.sgmodule` |
| `AdBlock-CN-Advanced.sgmodule` | 进阶版：`[Script]` / `[URL Rewrite]` / `[Body Rewrite]` / `[Map Local]` 段，**全部需要 MITM** | `https://raw.githubusercontent.com/Mircc/sgmodule/main/AD-Rules/AdBlock-CN-Advanced.sgmodule` |
| `adblock-cn-domains.txt` | 合并去重后的域名集（供 `DOMAIN-SET` 引用，也可单独订阅） | `https://raw.githubusercontent.com/Mircc/sgmodule/main/AD-Rules/adblock-cn-domains.txt` |
| `c_agent.mrs` | **手机端推荐**：Mihomo 系内核的二进制规则集，加载最快、内存占用最低 | `https://raw.githubusercontent.com/Mircc/sgmodule/main/AD-Rules/c_agent.mrs` |
| `c_agent-domain.list` | `c_agent.mrs` 的文本版，供不支持二进制规则集的客户端兜底 | `https://raw.githubusercontent.com/Mircc/sgmodule/main/AD-Rules/c_agent-domain.list` |
| `c_agent-rules.yaml` | `behavior: classical` 规则集，承载域名集装不下的类型（IP 段 / 复合规则等） | `https://raw.githubusercontent.com/Mircc/sgmodule/main/AD-Rules/c_agent-rules.yaml` |

### 国内加速（jsDelivr）

`raw.githubusercontent.com` 在国内经常访问不畅，可改用 jsDelivr 加速地址——
把 `https://raw.githubusercontent.com/Mircc/sgmodule/main/AD-Rules/`
换成 `https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AD-Rules/` 即可，文件完全相同：

| 文件 | jsDelivr 加速地址 |
| --- | --- |
| `AdBlock-CN.sgmodule` | `https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AD-Rules/AdBlock-CN.sgmodule` |
| `AdBlock-CN-Standalone.sgmodule` | `https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AD-Rules/AdBlock-CN-Standalone.sgmodule` |
| `AdBlock-CN-Advanced.sgmodule` | `https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AD-Rules/AdBlock-CN-Advanced.sgmodule` |
| `adblock-cn-domains.txt` | `https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AD-Rules/adblock-cn-domains.txt` |
| `c_agent.mrs` | `https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AD-Rules/c_agent.mrs` |
| `c_agent-domain.list` | `https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AD-Rules/c_agent-domain.list` |
| `c_agent-rules.yaml` | `https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AD-Rules/c_agent-rules.yaml` |

Surge 中单独订阅域名集（加速版）：

```
[Rule]
DOMAIN-SET,https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AD-Rules/adblock-cn-domains.txt,REJECT
```

**两点说明**：

- jsDelivr 有约 **12–24 小时缓存**，规则又是 72 小时才更新一次，所以缓存延迟基本感知不到。
- jsDelivr 偶尔也有波动，两个地址随时可以互换，订阅内容完全一致。

Surge 中单独订阅域名集（直连版）：

```
[Rule]
DOMAIN-SET,https://raw.githubusercontent.com/Mircc/sgmodule/main/AD-Rules/adblock-cn-domains.txt,REJECT
```

### 手机端：c_agent 规则集（Mihomo 系内核）

上面三个 `c_agent.*` 是给 **Mihomo 系内核**准备的 `rule-provider` 规则集。
要在手机上获得最好的加载速度与最低的内存占用，推荐按下面的方式引用：

```yaml
rule-providers:
  c-agent-domain:
    type: http
    behavior: domain
    format: mrs              # 二进制规则集，免解析，启动最快、内存最省
    url: "https://raw.githubusercontent.com/Mircc/sgmodule/main/AD-Rules/c_agent.mrs"
    path: ./ruleset/c_agent.mrs
    interval: 86400

  c-agent-rules:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/Mircc/sgmodule/main/AD-Rules/c_agent-rules.yaml"
    path: ./ruleset/c_agent-rules.yaml
    interval: 86400

rules:
  - RULE-SET,c-agent-domain,REJECT
  - RULE-SET,c-agent-rules,REJECT
```

> 若 `raw.githubusercontent.com` 访问不畅，把上面 `url:` 换成
> [jsDelivr 加速地址](#国内加速jsdelivr) 即可，内容完全一致。

**为什么推荐 `c_agent.mrs`**：它是二进制规则集，客户端加载时**跳过文本解析**，
对两万多条这种量级的列表，启动速度与内存占用的改善非常明显——这正是手机端最需要的。

**不支持二进制规则集怎么办**：把 `format: mrs` 换成 `format: text`，
`url` 换成 `c_agent-domain.list` 即可，拦截范围完全一致，只是加载略慢：

```yaml
  c-agent-domain:
    type: http
    behavior: domain
    format: text
    url: "https://raw.githubusercontent.com/Mircc/sgmodule/main/AD-Rules/c_agent-domain.list"
    path: ./ruleset/c_agent-domain.list
    interval: 86400
```

**两份规则集为什么不重复**：

| 文件 | 内容 | 为什么不合并 |
| --- | --- | --- |
| `c_agent.mrs` | 22,832 个域名（`behavior: domain`） | 域名走后缀匹配，二进制编码后体积极小 |
| `c_agent-rules.yaml` | 85 条规则（`behavior: classical`） | 只放域名集装不下的类型：IP-CIDR / IP-CIDR6 / DOMAIN-KEYWORD |

`DOMAIN` 与 `DOMAIN-SUFFIX` 已由域名集覆盖，因此**不会**再写进 classical 规则集——
这正呼应了本项目"不存在任何冗余"的目标。

> **为什么 classical 规则集只有 85 条？**
> Mihomo 的规则集（`rule-provider`）**并不支持全部规则类型**。实测 v1.19.30：
> 有些类型写在配置 `rules:` 主段里没问题，但放进规则集 payload 会导致
> **整份规则集静默加载成 0 条规则**（不报错，极难发现）。
>
> | 状态 | 类型 |
> | --- | --- |
> | ✅ 规则集支持 | `DOMAIN` / `DOMAIN-SUFFIX` / `DOMAIN-KEYWORD` / `DOMAIN-REGEX` / `IP-CIDR` / `IP-CIDR6` / `DST-PORT` / `SRC-PORT` / `PROCESS-NAME` / `NETWORK` / `OR` / `NOT` |
> | ❌ 规则集不支持 | `AND` / `URL-REGEX` / `USER-AGENT` / `IP-ASN` / `GEOIP` / `RULE-SET` |
>
> 因此本项目的 53 条 `URL-REGEX` / `AND` / `USER-AGENT` 规则**不会**写进
> `c_agent-rules.yaml`。这些恰好都是需要 MITM 的规则，与本项目"主体规则无需解密"
> 的目标一致；Surge 用户仍可在 `AdBlock-CN.sgmodule` 里用到它们。

> 生成说明：`c_agent.mrs` 需要 [mihomo](https://github.com/MetaCubeX/mihomo) 二进制做转换，
> 由本仓库的 GitHub Actions 自动下载并生成，且**生成后会反解自检**（抽样比对条目），
> 不通过则丢弃、只保留文本版。本地构建若没有 mihomo，会自动跳过 `.mrs`，其余产物不受影响。

---

## 二、体积从 6.7 MB 降到约 1 MB，钱花在哪了

输入 6.68 MB（adblocksurge 4.44 + anti-AD 1.93 + Blockads 0.25 + AWAvenue 0.06），
输出 `AdBlock-CN-Standalone.sgmodule` 约 1.03 MB。拆解如下（以域名条目计）：

| 阶段 | 条目数 | 本阶段移除 | 说明 |
| --- | --- | --- | --- |
| 上游原始域名条目 | 315,733 | — | 两个大域名库占绝大多数 |
| 区域过滤 + 知名度恢复 | 32,603 | 284,497（**90.1%**） | **体积下降的主因是过滤，不是去重** |
| 精确去重（`set()`） | 23,846 | 8,757（2.8%） | 只删完全相同的字符串 |
| 父子域收敛 | 22,832 | 1,014（0.3%） | 只删父域已在库内的冗余子域 |

也就是说，**去重只贡献了约 3% 的体积下降，90% 来自"剔除境外不知名域名"的过滤**。
如果你觉得砍得太狠，调节方式有两个（可叠加）：

- 放宽知名度阈值：`config/fame.json` 调大 `top_n`（每 +4 万约多捞 8 千条）
- 完全关闭过滤：把某个源的 `keep_foreign` 设为 `true`

---

## 三、当前规则源

| 源 | 类型 | 说明 |
| --- | --- | --- |
| [AWAvenue Ads Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | sgmodule | 国内 App 去广告（人工精选） |
| [Blockads](https://github.com/thNylHx/Tools) | sgmodule | 常用软件去广告合集（含 App 名注释） |
| [anti-AD](https://github.com/privacy-protection-tools/anti-AD) | domainset | 通用广告域名库 |
| [AdBlock Surge](https://github.com/217heidai/adblockfilters) | domainset | 多源合并的 Surge 广告域名库 |

### 新增规则源

编辑 `config/sources.json`，复制任意一条并修改：

```json
{
  "name": "我的新规则源",
  "url": "https://raw.githubusercontent.com/xxx/yyy/main/rules.list",
  "format": "domainset",
  "keep_foreign": false,
  "enabled": true
}
```

| 字段 | 说明 |
| --- | --- |
| `format` | `sgmodule`（Surge 模块）/ `domainset`（每行一个 `.domain` 的域名集）/ `auto`（自动识别） |
| `curated` | 是否人工精选源。为 `true`（sgmodule 默认）时该源**整体视为国内**，只在有明确境外证据时才剔除 |
| `keep_foreign` | 为 `true` 时跳过区域过滤，全部保留 |
| `enabled` | 为 `false` 时停用 |

提交后 Actions 会自动重建；你也可以本地先跑一遍验证。

---

## 四、本地构建

```bash
python3 scripts/build.py              # 全量（联网抓取）
python3 scripts/build.py --no-fetch   # 用 _cache 缓存重建，方便调参
python3 scripts/build.py --raw-base https://raw.githubusercontent.com/Mircc/sgmodule/main/AD-Rules
python3 docs/audit.py                 # 去重复核六连测
```

仅依赖 Python 3 标准库，无需安装任何包。构建结果输出到 `AD-Rules/`，统计写入 `stats.json`。

---

## 五、合并处理的完整流程

整个构建就是下面九步，对应 `scripts/build.py` 的同名阶段。括号内为本次实测数据。

### 第一步：抓取与缓存

按 `config/sources.json` 逐条抓取，写入 `_cache/`（文件名由 URL 哈希而来，6 小时内复用）。
抓取失败时自动回退上一次的缓存，保证上游短暂抽风不至于让产物消失。

> 同时载入**知名度榜单**（Tranco top-1m，见[第六节](#七过滤策略)），缓存 7 天；
> 榜单拉不到时自动回退仓库内置的 `config/fame_snapshot.txt`。

### 第二步：格式识别与解析

两种形态分别解析，**注释全程跟随，不做任何丢弃**：

| 形态 | 特征 | 解析方式 |
| --- | --- | --- |
| `sgmodule` | 含 `[Rule]` / `[Script]` / `[MITM]` 等方括号段 | 逐段解析；注释挂到紧跟其后的那条规则上，随规则一起输出 |
| `domainset` | 每行一个 `.example.com`，无分段 | 归一化成后缀域名，供 `DOMAIN-SET` 引用 |

规则行用「从末尾回扫 flag」的方式解析，因此能正确处理 `AND`/`OR`/`NOT` 嵌套括号，
以及 `URL-REGEX` 值里带逗号的情况。

> 解析结果：sgmodule 规则 **1,530 条**；域名条目 **315,733 条**。

### 第三步：采集国内域名种子

两个 sgmodule 源是**人工整理的国内去广告列表**，可信度高。
把它们出现过的域名收集为「国内种子」，用来在后续判定中识别国内 App 的子域。

> 关键约束：种子必须先排除有境外信号（境外 ccTLD / 黑名单）的域名，
> 否则 `tapad.com` 会把自己种子成"国内"，让黑名单彻底失效（循环论证）。

### 第四步：区域过滤（剔除境外不知名域名）

对每个域名做归属判定，见[第六节](#七过滤策略)的九级顺序。
这一步是体积下降的主因，也是最需要谨慎的一步。

> 结果：域名条目 315,733 → **31,236**（剔除 284,497，90.1%）
> 规则 1,530 → **1,521**（仅剔除 9 条明确的境外不知名广告 SDK）

### 第五步：域名集合并与精确去重

把**所有源**的域名合并进同一个池子，再用 `set()` 去重。
顺序很重要——必须是「先全量合并，再去重」，而不是逐源去重后再拼。

> 同时把 sgmodule 里的 `DOMAIN` / `DOMAIN-SUFFIX` 规则值并入域名集。
> **`DOMAIN-KEYWORD` 不并入**——`httpdns`、`pangolin` 这类是关键词不是域名，
> 并进来会变成 `.httpdns` 这种无意义的单 label 后缀条目。

> 结果：32,603 → **23,846**（移除 8,757 条完全相同的重复项）

### 第六步：父子域收敛

若**父域本身已在集合内**，则子域对 `DOMAIN-SUFFIX` 而言是冗余的，删掉子域。

铁律是**只删、绝不改写**：

- `{ad.cdf.xxx.com, cdf.xxx.com}` → 删 `ad.cdf.xxx.com`，产物里仍是 `cdf.xxx.com` 原样
- `{ad.cdf.xxx.com}`（无父域）→ 原样保留，**不会**被压缩成 `cdf.xxx.com` 或 `xxx.com`

> 结果：23,846 → **22,832**（移除 1,014 条冗余子域）

### 第七步：规则层去重

跨源按 `(类型, 值, 策略)` 去重，flag 取并集并按固定顺序规范化
（`extended-matching,pre-matching` 与 `pre-matching,extended-matching` 视为同一条）。

策略不同（REJECT vs DIRECT）的规则**视为不同条目，全部保留，绝不吞并**。

> 结果：1,521 → **1,425**（移除 96 条重复）

### 第八步：MITM 分流

只有 `URL-REGEX` / `URL-ADVANCED` / `USER-AGENT` 需要 HTTPS 解密才能匹配。
这类规则被单独放到 `[Rule]` 段**尾部**，前面插入醒目注释块，
对应主机名写进 `[MITM]` 段。详见[第九节 MITM 说明](#九mitm-说明)。

> 结果：无需 MITM **1,387 条** / 需要 MITM **38 条**

### 第九步：产出 Surge 系列产物

| 产物 | 说明 |
| --- | --- |
| `AdBlock-CN.sgmodule` | 主模块，域名集走 `DOMAIN-SET` 远程引用（推荐，体积小、自动更新） |
| `AdBlock-CN-Standalone.sgmodule` | 完全内联版，离线可用（约 1.03 MB） |
| `AdBlock-CN-Advanced.sgmodule` | 仅 MITM 进阶段（脚本 / 重写 / 本地映射），可选加载 |
| `adblock-cn-domains.txt` | 域名集，可单独订阅 |

### 第九步·补：产出 c_agent 系列（Mihomo 系内核）

把同一份数据再导出一份 `rule-provider` 规则集，供手机端使用，见
[订阅地址中的 c_agent 小节](#手机端c_agent-规则集mihomo-系内核)：

| 产物 | 说明 |
| --- | --- |
| `c_agent-domain.list` | 域名清单（`behavior: domain`），`+.example.com` 表示后缀匹配 |
| `c_agent-rules.yaml` | classical 规则集，只放域名集装不下的类型（85 条） |
| `c_agent.mrs` | 上面域名清单的**二进制**版本，需 mihomo 转换，生成后自动反解自检 |

三条转换规则（也是本步的关键约束）：

1. **只收录拦截类策略** —— `DIRECT` 等放行类不进规则集（本项目是去广告规则集）
2. **剥离 Surge 专有 flag** —— `pre-matching` / `extended-matching` / `no-resolve` 等
   Mihomo 不认识，留在规则里会污染解析
3. **无法安全表达的跳过** —— `PROTOCOL,TCP` 映射为 `NETWORK,tcp`；
   没有对应类型的（如 `PROTOCOL,QUIC`）以及引号内含逗号会被当分隔符截断的复合规则，直接丢弃

同时写入 `stats.json` 供 Actions 生成统计摘要。

---

## 六、上游异常保护（上游出事时不删本地）

上游仓库偶尔会出错：大规模删规则、改文件名导致链接 404、返回错误页……
如果没有保护，一次上游事故就会把**已经正常工作的规则集直接清空**。

本项目的处理原则很简单：**宁可不更新，也绝不覆盖坏结果。**

### 触发条件（命中任一即中止）

| 检查 | 说明 | 默认阈值 |
| --- | --- | --- |
| 源完全不可用 | 该源抓取失败且本地也没有缓存 | — |
| 源内容异常 | 单个源解析出的条目数过低（正常应在数千以上） | < 200 条 |
| 域名数绝对下限 | 防"上一版本身就是坏的"导致跌幅比较失效 | < 12,000 |
| 规则数绝对下限 | 同上 | < 1,000 |
| 域名数跌幅 | 上游大幅删规则 | > 30% |
| 规则数跌幅 | 同上 | > 30% |

阈值都在 `config/guard.json` 里可调。

### 触发后会怎样

1. **立即中止，一个文件都不写** —— 仓库里已发布的 `AD-Rules/` 保持原样，订阅完全不受影响
2. 进程以**退出码 2** 结束，GitHub Actions 据此跳过提交，并在运行摘要里给出告警
3. 打印"本次 / 上版"的数量对比，便于你判断是真事故还是正常变更

### 上游暂时抽风但缓存还在

如果只是这次没抓到（缓存里还有上一份完整数据），**不会中止** —— 会打印一条警告后正常构建。
判断依据是"数据是否完整"，而不是"是否拿到了最新数据"。

### 确认是正常大改时

手动运行工作流，勾选 `no_guard`（等价于本地 `python3 scripts/build.py --no-guard`）即可强制构建。

### 回滚

每次成功构建前会把上一版复制到 `AD-Rules.bak/`，需要时可直接取回。

---

## 七、过滤策略

区域判定顺序（`scripts/build.py` 的 `RegionClassifier`）：

1. **白名单**（`config/whitelist.txt`）→ 直接丢弃，防误杀
2. **中国国家/地区顶级域** → 保留
3. **国内厂商 / 广告 SDK 关键词**（`config/domestic_brands.txt`）→ 保留
4. **国际极其知名服务**（`config/intl_allowlist.txt`）→ 保留
5. **精选源中出现过的域名**及其子域 → 保留
6. **手工黑名单**（`config/foreign_denylist.txt`）→ 剔除（用户显式指定，优先级最高）
7. **知名度榜单**（`config/fame.json`）→ 排名前 N 视为家喻户晓，**保留**；
   但托管平台（`config/hosting_platforms.txt`，如 weebly / vercel / free.fr）不据此恢复
8. **境外 ccTLD**（`config/foreign_cctlds.txt`）→ 剔除
9. 其余：人工精选源保留，域名集剔除

> **设计原则一：剔除国外域名需要正面证据。**
> 国内 App 的广告域名大量使用 `.com` 等通用后缀且品牌名五花八门，
> 早期版本用"猜"的策略会误杀 `orbit.jd.com`、`ggx01.miguvideo.com`、`ad-cdn.qingting.fm` 这类域名，
> 因此改为只在命中境外 ccTLD / 明确黑名单时才剔除。
>
> **设计原则二：「是否知名」必须用客观数据判定，不能靠手写词表。**
> 手写白名单永远写不全 —— 早期版本因此丢掉了 `ad.qq.com`、`adnet.qq.com`、`adping.qq.com`
> （QQ，共 372 条）、`ad.163.com`（网易，66 条）、`ads-api.duolingo.com`（多邻国）等真正该拦的域名。
> 现在引入域名流行度排名作为客观信号，见下节。

### 知名度榜单（`config/fame.json`）

| 项 | 值 |
| --- | --- |
| 数据源 | [Tranco top-1m](https://tranco-list.eu)（`rank,domain` CSV zip，约 9 MB） |
| 默认阈值 | `top_n = 10000` |
| 缓存 | `_cache/fame_top.csv`，7 天 |
| 离线兜底 | `config/fame_snapshot.txt`（仓库内置 top10k 快照，125 KB），榜单拉不到时自动回退 |
| 参考排名 | QQ #89、163 #401、Duolingo #482、AmEx #2123、Nespresso #4918 |

阈值实测（被剔除条目 → 捞回数）：top10k 捞回 10,440；top50k 捞回 23,605，
但会开始混入 `free.fr`、`weebly.com`、`000webhost` 这类托管平台的海量垃圾子域。
因此默认取 **10000**，并用 `hosting_platforms.txt` 额外挡掉托管平台与纯 CDN 基础设施
（其子域归属任意第三方，不属于任何一个 App）。

关闭榜单：`config/fame.json` 里 `"enabled": false`（域名集会回落到约 1.4 万条）。

### 关键词匹配规则

只匹配**非 TLD** 的 label（否则 `.live` / `.link` 会命中 `live` 等关键词）：

- 精确匹配：不限长度
- 前缀模糊：token ≥ 5 字符（`douyin` → `douyinpic`）
- 后缀模糊：token ≥ 6 字符（避免 `floresina` 命中 `sina`、`drtuber` 命中 `uber`）

### 已知的 2 条源间策略冲突

`ad.12306.cn`、`nex.163.com`：AWAvenue 标 `REJECT`，Blockads 标 `DIRECT`。
两条规则都保留，AWAvenue 在产物中排前，**Surge 自上而下取首个匹配，因此 `REJECT` 生效**。

- 想"拦截优先"：保持现状
- 想"稳妥不拦截"：把这些域名加进 `config/whitelist.txt`，或调整 `sources.json` 顺序

---

## 八、去重策略（只删，绝不改写）

- **顺序**：永远先把所有源合并进一个池子，再去重（不是逐源去重后再拼）
- **规则层**：按 `(类型, 值, 策略)` 去重，flag 取并集并规范化顺序；
  策略不同（REJECT vs DIRECT）的规则视为不同条目，都保留，绝不吞并
- **域名层**：先精确去重 `set()`，再做**父子域收敛**——
  只有当**父域本身已在集合内**时才删掉冗余子域，子域绝不会被"压缩"成父域或祖父域

> 收敛的安全性建立在"知名 App 主域名不进库"之上。
> 每次改过去重逻辑，请跑一遍[第十一节](#十一去重复核九项测)的九项测。

---

## 九、MITM 说明

**主模块的主体规则无需开启 MITM**（`DOMAIN` / `DOMAIN-SUFFIX` / `IP-CIDR` 等基于 SNI 与连接信息即可匹配）。

只有 `URL-REGEX` / `USER-AGENT` 这类需要读取加密内容的规则被单独放到 **`[Rule]` 段尾部**，
并带有醒目注释块说明「以下规则需要开启 MITM（HTTPS 解密）方可生效」，对应的主机名列在 `[MITM]` 段中。

> 风险提示：MITM 会解密对应域名流量，网银、支付、政务类 App 不建议开启。
> 不需要 MITM 的用户可直接删除文件中尾部那一段与 `[MITM]` 段，主体功能不受影响。

### 关于进阶模块的外链脚本（请先读）

`AdBlock-CN-Advanced.sgmodule` 的 `[Script]` 段通过 `script-path=` 引用**第三方外链脚本**
（主要来自 KeLee 的 kelee.one），它们能去掉 App 内的广告卡片与开屏位，是纯域名拦截做不到的。

需要知悉两点：

1. **依赖外部站点可用性** —— 这些脚本不在本仓库内，由原作者托管。
   构建时实测 kelee.one 对自动化请求返回 403（可能是 WAF 拦截，也可能确已下线），
   具体是否可用请以你自己的网络环境为准。**若脚本拉不到，相关 App 的去广告会失效，但不会影响其他规则。**
2. **MITM 范围更大** —— 进阶模块会解密更多域名，请自行权衡。

不确定的话，**只加载 `AdBlock-CN.sgmodule` 即可**，主体规则完全自包含、不依赖任何外链脚本。

---

## 十、目录结构

整个项目自成一个目录（与仓库里既有的 `AI-Rules/` 保持一样的组织方式）：

```
AD-Rules/
├── README.md                   # 本文档
├── stats.json                  # 构建统计（异常保护据此与上一版比对）
│
├── AdBlock-CN.sgmodule         # Surge 主模块（推荐）
├── AdBlock-CN-Standalone.sgmodule   # Surge 内联版（离线可用）
├── AdBlock-CN-Advanced.sgmodule     # Surge 进阶段（需 MITM）
├── adblock-cn-domains.txt      # 域名集（可单独订阅）
├── c_agent.mrs                 # 二进制规则集（手机端推荐）
├── c_agent-domain.list         # 域名清单文本版
├── c_agent-rules.yaml          # classical 规则集
│
├── config/
│   ├── sources.json           # 规则源清单（新增源改这里）
│   ├── repo.json              # raw 地址前缀（Actions 会自动覆盖）
│   ├── guard.json             # 上游异常保护阈值
│   ├── fame.json              # 知名度榜单开关与阈值
│   ├── fame_snapshot.txt      # 榜单离线快照（top10k，125 KB）
│   ├── domestic_brands.txt    # 国内厂商 / 广告 SDK 关键词
│   ├── intl_allowlist.txt     # 国际极其知名服务白名单
│   ├── hosting_platforms.txt  # 托管平台（不因知名度恢复）
│   ├── foreign_cctlds.txt     # 境外国家顶级域
│   ├── foreign_denylist.txt   # 境外不知名厂商黑名单
│   ├── public_suffixes.txt    # 二级公共后缀（正确求可注册域）
│   ├── china_tlds.txt         # 中国国家/地区顶级域
│   └── whitelist.txt          # 安全白名单（防误杀）
├── scripts/build.py           # 构建脚本（仅标准库）
├── docs/audit.py              # 去重复核九项测
├── _cache/                    # 抓取缓存（不入库）
└── .bak/                      # 上一版备份（不入库，用于回滚）
```

定时构建的工作流在仓库根目录：`.github/workflows/build-ad-rules.yml`。

---

## 十一、去重复核九项测

改过去重逻辑后必跑，任一 FAIL 会以退出码 1 结束（已接入 Actions，FAIL 则不提交）：

```bash
python3 docs/audit.py
```

1. **规模**：合并后(未去重) → 精确去重 → 父子收敛，三级数字对得上，且输出文件与复算一致
2. **改写检测**：输出域名 100% 能在上游源里找到（证明只删不改）
3. **收敛合法性**：每个被删子域都能在库里找到真实父域（无孤儿删除）
4. **知名主域误杀**：`apple.com`/`qq.com`/`baidu.com`/`jd.com` 等一个都不在产物里
5. **裸后缀**：`grep -cE '^\.[a-z0-9_-]+$' AD-Rules/adblock-cn-domains.txt` 为 0
6. **冲突不吞并**：同 `(类型,值)` 但策略不同的规则必须都保留
7. **c_agent 域名清单**：条数与域名集一致，且全部是 `+.` 后缀写法
8. **c_agent 规则集**：不含 `pre-matching` / `extended-matching` / `no-resolve` / `PROTOCOL,` 残留
9. **c_agent 规则集不含 Mihomo 不支持的类型**（`AND` / `URL-REGEX` / `USER-AGENT` 等会让整份静默失效）

---

## 十二、误杀处理

发现某个域名被误拦，把它的后缀加进 `config/whitelist.txt`：

- `example.com` → 仅精确匹配 `example.com`
- `.example.com` → 匹配 `example.com` 及其全部子域

然后重新构建即可。

---

## 十三、鸣谢

**没有下面这些项目和他们日复一日的维护，就没有今天干净清爽的互联网。**

本仓库不生产任何一条规则，所有价值都属于这些作者。他们中的大多数是在没有任何回报的情况下，
长期盯着成千上万个域名的变化、追着 App 版本更新规则。
你手机上每一次"广告没了"的清爽，背后都是这些人的时间和耐心。

在此，向每一位致以最诚挚的谢意。

### 直接整合的上游规则源

| 项目 | 作者 | 说明 |
| --- | --- | --- |
| [AWAvenue Ads Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [@TG-Twilight](https://github.com/TG-Twilight)（主页 [awavenue.top](https://awavenue.top)） | 国内 App 去广告规则的集大成者，人工逐条甄别，是本项目主规则的主要来源 |
| [Blockads 软件去广告合集](https://github.com/thNylHx/Tools) | RuCu6、[@Keywos](https://github.com/Keywos)、fmz200、可莉🅥、QingRex（仓库由 [@thNylHx](https://github.com/thNylHx) 维护） | 常用国产软件的 App 级去广告合集，附带的 App 名注释极大地方便了规则核对 |
| [anti-AD](https://github.com/privacy-protection-tools/anti-AD) | [@privacy-protection-tools](https://github.com/privacy-protection-tools) | 长期稳定维护的通用广告域名库，覆盖面极广 |
| [adblockfilters（AdBlock Surge）](https://github.com/217heidai/adblockfilters) | [@217heidai](https://github.com/217heidai) | 每 8 小时自动重建的多源合并 Surge 规则，工程化程度令人钦佩 |

#### 上游维护状态（每次构建自动更新）

下面这段由 `scripts/build.py` 在每次构建时自动生成，
让你打开文档就能掌握每个上游有多久没更新了：

<!-- UPSTREAM_STATUS:START -->
<!-- 本段由 scripts/build.py 自动生成，请勿手动修改 -->
<!-- 本次构建时间：2026-09-04 08:02:54 -->

| 源 | 上游最新更新时间 | 距今 | 本次条目数 | 说明 |
| --- | --- | --- | --- | --- |
| AWAvenue Ads Rule | 2026-08-20 11:45:33 | 14 天 | 887 | 国内 App 去广告规则的集大成者，人工逐条甄别，是本项目主规则的主要来源 |
| Blockads 软件去广告合集 | 2026-08-29 15:49:38 | 5 天 | 643 | 常用国产软件的 App 级去广告合集，附带的 App 名注释极大地方便了规则核对 |
| anti-AD | 2026-09-02 05:10:40 | 2 天 | 100,977 | 长期稳定维护的通用广告域名库，覆盖面极广 |
| AdBlock Surge (217heidai) | 2026-09-04 11:54:49 | 0 天 | 214,217 | 每 8 小时自动重建的多源合并 Surge 规则，工程化程度令人钦佩 |

> 时间为上游内容里自报的更新时间（非本项目抓取时间），可据此判断上游是否还在维护。
> 距今超过 180 天会标注 ⚠️。
<!-- UPSTREAM_STATUS:END -->

### 去广告脚本作者

`AdBlock-CN-Advanced.sgmodule` 中的 `[Script]` 段直接引用了以下作者的去广告脚本，
它们能去掉 App 内部的广告卡片和开屏位，是纯域名拦截做不到的部分：

- **KeLee**（[kelee.one](https://kelee.one)）—— 12306、阿里云盘、百度贴吧、百度网页等大量 App 的 JS 去广告脚本
- **[@Keywos](https://github.com/Keywos/rule)** —— 爱思助手等 App 的去广告脚本

### 上游再上游（经 anti-AD 与 adblockfilters 间接引入）

这些项目没有直接进入本仓库，但它们的成果通过上述源汇入，同样值得感谢：

- **AdGuard 团队** —— AdGuard Base / Chinese / Mobile Ads / DNS filters
- **EasyList / EasyList China / EasyPrivacy 社区** —— 广告过滤规则的基石
- **CJX** —— CJX's Annoyance List
- **OISD**（[oisd.nl](https://oisd.nl)）—— OISD Basic
- **StevenBlack** —— StevenBlack hosts
- **DNS-Blocklists** —— DNS-Blocklists PRO mini
- **AdRules DNS List**、**xinggsf**、**jiekouAD**、**Pollock** —— 各自的长期维护

### 数据与工具支持

- **Tranco List**（[tranco-list.eu](https://tranco-list.eu)）—— 提供域名流行度排名。
  本项目用它客观判定「该服务是否家喻户晓」，替代了永远写不全的手工白名单。
- **Mihomo**（[github.com/MetaCubeX/mihomo](https://github.com/MetaCubeX/mihomo)）——
  提供 `convert-ruleset` 转换能力，`c_agent.mrs` 二进制规则集由它生成，
  让手机端得以跳过文本解析、显著降低内存占用与启动耗时。
- **DustinWin/ruleset_geodata** —— 其公开的 Actions 工作流是本项目
  `mihomo convert-ruleset` 调用方式与域名清单语法（`+.` 表示后缀匹配）的重要参考。

### 最后

如果你觉得这套整合规则有用，**请去给上面这些上游项目点一个 Star**。
我做的只是搬运和整理，真正让互联网变得干净的是他们。

---

## 十四、许可与转载

- 本项目**仅为规则整合与格式转换**，不主张对上游规则内容的任何权利。
- 各上游规则的版权与许可归各自作者所有，转载请遵循其原始许可要求。
- 上游作者若不希望自己的规则被收录，请联系移除，我会第一时间处理。
