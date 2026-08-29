# AIGC / AI 规则集

> 本文件由 GitHub Actions 自动生成，订阅链接随仓库/分支自动适配。

每日自动拉取上游源，去重、归类、累积合并（上游删除不影响本库）。

## 订阅地址（jsDelivr 加速，推荐）

| 客户端 | 订阅 URL |
| --- | --- |
| Clash rule-provider | `https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Ai.yaml` |
| Surge RULE-SET | `https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Ai.list` |
| QuantumultX filter_remote | `https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Ai.qx.list, tag=Ai, force-policy=你的策略组, enabled=true` |

## 备用直连（raw.githubusercontent）

| 客户端 | 订阅 URL |
| --- | --- |
| Clash rule-provider | `https://raw.githubusercontent.com/Mircc/sgmodule/main/AI-Rules/output/Ai.yaml` |
| Surge RULE-SET | `https://raw.githubusercontent.com/Mircc/sgmodule/main/AI-Rules/output/Ai.list` |
| QuantumultX filter_remote | `https://raw.githubusercontent.com/Mircc/sgmodule/main/AI-Rules/output/Ai.qx.list, tag=Ai, force-policy=你的策略组, enabled=true` |

## 缓存说明

- jsDelivr 分支缓存约 12 小时，急更新访问 `https://purge.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Ai.yaml` 手动刷新（每个文件各刷一次）
- 个别地区 `cdn.jsdelivr.net` 不可达时，换 `testingcf.jsdelivr.net` / `fastly.jsdelivr.net` 同源镜像域名

## 说明

- 上游源清单见 `sources.txt`，增删上游改这一个文件即可
- 累积模式：只去重、只新增，上游删除/清空不会导致本库规则缺失
- 专注 AI 规则：PayPal 家族（含钓鱼变体/马甲）、stripe / lemonsqueezy / paddle 等支付类一律排除
- 当前基线：14 个上游源，保留 371 条规则，三端一致
