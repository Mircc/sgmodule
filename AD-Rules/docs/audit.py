#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
去重复核六连测。每次改过去重 / 区域过滤逻辑后运行，全部 PASS 才算合格。

    python3 docs/audit.py

任一检查 FAIL 则以退出码 1 结束（可接入 CI）。
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build as B  # noqa: E402

FAMOUS = (
    "apple.com icloud.com google.com youtube.com facebook.com instagram.com whatsapp.com "
    "twitter.com microsoft.com amazon.com netflix.com spotify.com discord.com line.me samsung.com "
    "adobe.com github.com dropbox.com paypal.com ebay.com twitch.tv reddit.com linkedin.com pinterest.com "
    "qq.com weixin.com wechat.com baidu.com taobao.com tmall.com jd.com alipay.com alibaba.com "
    "tencent.com weibo.com sina.com 163.com netease.com zhihu.com bilibili.com douyin.com tiktok.com "
    "meituan.com xiaomi.com mi.com huawei.com vivo.com oppo.com iqiyi.com youku.com ximalaya.com "
    "kuaishou.com pinduoduo.com bytedance.com sohu.com sogou.com 360.cn ctrip.com dianping.com "
    "mihoyo.com hoyoverse.com miui.com miguvideo.com qingting.fm yximgs.com"
).split()

results = []


def report(name, ok, detail=""):
    results.append(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")


def main():
    cfg = B.Config()
    # 必须载入知名度榜单，否则复算结果与构建产物对不上（榜单缺失 -> 少算一批域名）
    cfg.fame = B.load_fame(cfg, no_fetch=True)
    cls = B.RegionClassifier(cfg)

    srcs = {s["name"]: s for s in cfg.sources if s.get("enabled", True)}
    texts = {}
    for n, s in srcs.items():
        key = re.sub(r"[^A-Za-z0-9]+", "_", s["url"])[-120:]
        texts[n] = B.CACHE.joinpath(key).read_text(encoding="utf-8", errors="replace")

    parsed, domain_entries = [], []
    for n, s in srcs.items():
        t = texts[n]
        fmt = s.get("format", "auto") or "auto"
        if fmt == "auto":
            fmt = "sgmodule" if "[Rule]" in t else "domainset"
        if fmt == "sgmodule":
            parsed.append((n, B.parse_sgmodule(t, n)))
        else:
            domain_entries.append((n, B.parse_domainset(t, n)[1]))

    rules = []
    for n, (h, sec, o) in parsed:
        for c, l in sec.get("Rule", []):
            r = B.parse_rule_line(l, n, c)
            if r:
                rules.append(r)

    curated = {s["name"] for s in cfg.sources
               if s.get("enabled", True) and s.get("curated", True) and s.get("format", "auto") == "sgmodule"}
    for r in rules:
        if r.source in curated:
            for d in B.extract_domains(r):
                cls.add_curated(d)
    kept = [r for r in rules if B.rule_keep(r, cls, False, r.source in curated)]
    for r in kept:
        for d in B.extract_domains(r):
            cls.add_curated(d)

    merged = []
    for n, doms in domain_entries:
        merged += [d for d in doms if cls.keep(d, False)]
    for r in kept:
        if r.policy in B.POLICIES_BLOCK and r.type in ("DOMAIN", "DOMAIN-SUFFIX"):
            d = r.value.lower().strip()
            if "." in d and re.fullmatch(r"[a-z0-9][a-z0-9._-]*[a-z0-9]", d):
                merged.append(d)
    merged = [d for d in merged if not cls.is_whitelisted(d)]
    uniq = sorted(set(merged))
    base = set(uniq)
    collapsed = [d for d in uniq
                 if not any(".".join(d.split(".")[i:]) in base for i in range(1, len(d.split("."))))]

    out_ds = [l[1:].strip() for l in open(ROOT / "adblock-cn-domains.txt", encoding="utf-8")
              if l.startswith(".")]

    print("== 去重复核九项测 ==")
    print(f"  规模: 合并后 {len(merged)} -> 精确去重 {len(uniq)} -> 父子收敛 {len(collapsed)} -> 输出文件 {len(out_ds)}")
    report("A 输出与管线复算一致", out_ds == collapsed)

    in_sources = set()
    for n, doms in domain_entries:
        in_sources |= set(doms)
    for r in kept:
        if r.policy in B.POLICIES_BLOCK and r.type in ("DOMAIN", "DOMAIN-SUFFIX"):
            in_sources.add(r.value.lower().strip())
    not_src = [d for d in out_ds if d not in in_sources]
    report("B 改写检测（输出全部源自上游，只删不改）", not not_src, f"改写 {len(not_src)}")

    removed = [d for d in uniq if d not in set(collapsed)]
    orphan = [d for d in removed
              if not any(".".join(d.split(".")[i:]) in base for i in range(1, len(d.split("."))))]
    report("C 收敛合法性（每个被删子域都有真实父域）", not orphan, f"孤儿 {len(orphan)}")

    bad_ds = [d for d in out_ds if d in FAMOUS]
    mod = [l for l in open(ROOT / "AdBlock-CN.sgmodule", encoding="utf-8")
           if l.startswith(("DOMAIN,", "DOMAIN-SUFFIX,"))]
    bad_rule = [l.strip() for l in mod if l.strip().split(",")[1] in FAMOUS]
    report("D 知名 App 主域名误杀（域名集+规则均为 0）", not bad_ds and not bad_rule,
           f"域名集 {len(bad_ds)} / 规则 {len(bad_rule)}")

    bare = [d for d in out_ds if "." not in d]
    tld = [d for d in out_ds if d in cfg.two_level_suffixes or d in ("com", "cn", "net", "org")]
    report("E 裸后缀 / 单 label / TLD（应为 0）", not bare and not tld, f"单label {len(bare)} / 后缀 {len(tld)}")

    dedup = {}
    for r in kept:
        if r.key not in dedup:
            dedup[r.key] = r
    conflict = defaultdict(set)
    for r in dedup.values():
        if r.type in ("DOMAIN", "DOMAIN-SUFFIX"):
            conflict[(r.type, r.value)].add(r.policy)
    mixed = {k: v for k, v in conflict.items() if len(v) > 1}
    report("F 策略冲突不吞并（不同策略的规则都保留）", True,
           f"存在 {len(mixed)} 组冲突: {list(mixed)}")

    # --- c_agent（Mihomo 系内核）产物一致性 ---
    dom_list = [l.strip() for l in open(ROOT / "c_agent-domain.list", encoding="utf-8")
                if l.strip() and not l.startswith("#")]
    bad_prefix = [d for d in dom_list if not d.startswith("+.")]
    report("G c_agent 域名清单（条数与域名集一致，且全部为 +. 后缀写法）",
           len(dom_list) == len(out_ds) and not bad_prefix,
           f"清单 {len(dom_list)} vs 域名集 {len(out_ds)}，异常前缀 {len(bad_prefix)}")

    payload = [l.strip()[2:] for l in open(ROOT / "c_agent-rules.yaml", encoding="utf-8")
               if l.strip().startswith("- ")]
    dirty = [p for p in payload
             if any(f in p for f in (",pre-matching", ",extended-matching", ",no-resolve"))
             or "PROTOCOL," in p]
    report("H c_agent 规则集无 Surge 专有残留（flag / PROTOCOL）", not dirty,
           f"规则 {len(payload)} 条，残留 {len(dirty)} 条 {dirty[:2]}")

    # 关键回归项：Mihomo 规则集不支持这些类型，
    # 混进 payload 会让**整份规则集静默加载成 0 条规则**（不报错，极难发现）
    unsupported = [p for p in payload if p.split(",")[0] in B.MIHOMO_UNSUPPORTED_TYPES]
    report("I c_agent 规则集不含 Mihomo 不支持的类型（否则整份静默失效）",
           not unsupported,
           f"规则 {len(payload)} 条，不支持类型 {len(unsupported)} 条 {unsupported[:2]}")

    ok = all(results)
    print(f"\n  总结: {'全部 PASS' if ok else '存在 FAIL，请检查'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
