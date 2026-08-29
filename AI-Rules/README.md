# AI-Rules

> 本文件由 GitHub Actions 自动生成, 订阅链接随仓库/分支自动适配.

每日自动拉取上游源, 去重、归类、累积合并 (上游删除不影响本库).

## 客户端一

| 类型 | 链接 |
| --- | --- |
| 加速链接 (推荐) | https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Cl_Ai.yaml |
| 直连备用 | https://raw.githubusercontent.com/Mircc/sgmodule/main/AI-Rules/output/Cl_Ai.yaml |
| mrs 域名 (省电) | https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Cl_Ai_domain.mrs |
| mrs IP (省电) | https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Cl_Ai_ipcidr.mrs |

mrs 为二进制规则集 (Clash Meta/mihomo 内核), 手机端更省电, 需配合 `behavior: domain` / `behavior: ipcidr` 两个 rule-provider 使用:

```yaml
rule-providers:
  ai-domain:
    type: http
    behavior: domain
    format: mrs
    url: https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Cl_Ai_domain.mrs
    interval: 86400
  ai-ip:
    type: http
    behavior: ipcidr
    format: mrs
    url: https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Cl_Ai_ipcidr.mrs
    interval: 86400
rules:
  - RULE-SET,ai-domain,AI
  - RULE-SET,ai-ip,AI,no-resolve
```

mrs 不含 KEYWORD/REGEX/IP-ASN 类规则 (占比极小), 全量覆盖请用 Cl_Ai.yaml.

## 客户端二

| 类型 | 链接 |
| --- | --- |
| 加速域名集 (推荐, 高性能) | https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Sg_Ai.domainset |
| 直连域名集 | https://raw.githubusercontent.com/Mircc/sgmodule/main/AI-Rules/output/Sg_Ai.domainset |
| 加速补充集 (RULE-SET) | https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Sg_Ai.list |
| 直连补充集 (RULE-SET) | https://raw.githubusercontent.com/Mircc/sgmodule/main/AI-Rules/output/Sg_Ai.list |

域名集 (DOMAIN-SET) 走专用索引, 匹配性能远优于 classical 规则集; 域名规则全部在其中,
补充集仅含 KEYWORD/REGEX/IP 类规则, 两条各写一行配合使用:

```ini
[Rule]
DOMAIN-SET,https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Sg_Ai.domainset,你的策略组
RULE-SET,https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Sg_Ai.list,你的策略组
```

## 客户端三

| 类型 | 链接 |
| --- | --- |
| 加速链接 (推荐) | https://cdn.jsdelivr.net/gh/Mircc/sgmodule@main/AI-Rules/output/Ai_qx.list, tag=Ai, force-policy=你的策略组, enabled=true |
| 直连备用 | https://raw.githubusercontent.com/Mircc/sgmodule/main/AI-Rules/output/Ai_qx.list, tag=Ai, force-policy=你的策略组, enabled=true |

客户端三订阅时请用 force-policy 参数自由指定策略组 (规则不写策略位, 不预设任何策略).

## 缓存说明

- jsDelivr 分支缓存约 12 小时, 急更新访问 https://purge.jsdelivr.net 刷新
- 个别地区可换 testingcf.jsdelivr.net / fastly.jsdelivr.net 同源镜像, 路径不变
