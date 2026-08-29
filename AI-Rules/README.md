# AI-Rules

> 本文件由 GitHub Actions 自动生成，订阅链接随仓库/分支自动适配。

每日自动拉取上游源，去重、归类、累积合并（上游删除不影响本库）。

## 客户端一

| 类型 | 链接 |
| --- | --- |
| 加速链接（推荐） | `https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Ai.yaml` |
| 直连备用 | `https://raw.githubusercontent.com/Mircc/sgmodule/main/AI-Rules/output/Ai.yaml` |

## 客户端二

| 类型 | 链接 |
| --- | --- |
| 加速链接（推荐） | `https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Ai.list` |
| 直连备用 | `https://raw.githubusercontent.com/Mircc/sgmodule/main/AI-Rules/output/Ai.list` |

## 客户端三

规则不写策略位，订阅时请用 `force-policy` 参数自由指定你自己的策略组。

| 类型 | 链接 |
| --- | --- |
| 加速链接（推荐） | `https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Ai.qx.list, tag=Ai, force-policy=你的策略组, enabled=true` |
| 直连备用 | `https://raw.githubusercontent.com/Mircc/sgmodule/main/AI-Rules/output/Ai.qx.list, tag=Ai, force-policy=你的策略组, enabled=true` |

## 缓存说明

- jsDelivr 分支缓存约 12 小时，急更新访问 `https://purge.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Ai.yaml` 手动刷新（每个文件各刷一次）
- 个别地区 `cdn.jsdelivr.net` 不可达时，可把域名换为 `testingcf.jsdelivr.net` / `fastly.jsdelivr.net`，路径不变

## 说明

- 上游源清单见 `sources.txt`，增删上游改这一个文件即可
- 累积模式：只去重、只新增，上游删除/清空不会导致本库规则缺失
- 专注 AI 规则：PayPal 家族（含钓鱼变体/马甲）、stripe / lemonsqueezy / paddle 等支付类一律排除
- 当前基线：14 个上游源，保留 371 条规则，三端一致
