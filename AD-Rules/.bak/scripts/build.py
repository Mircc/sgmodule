#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AdBlock-CN Builder
==================

把多个 Surge 去广告规则源整合为一个「以净化国内 App 为主」的规则集：

  1. 抓取 config/sources.json 中启用的所有规则源
  2. 解析 sgmodule（保留 [Rule]/[Script]/[URL Rewrite]/[Body Rewrite]/[Map Local]/[MITM] 段与全部注释）
     以及 domainset（每行一个 .domain 后缀列表，用于 Surge 的 DOMAIN-SET）
  3. 归一化 + 去重（含 DOMAIN-SUFFIX 父子域自动收敛）
  4. 区域过滤：只保留国内 App / 厂商，以及国际「极其知名」服务的域名；不知名国外域名丢弃
  5. MITM 分流：URL-REGEX / USER-AGENT 等需要 HTTPS 解密的规则单独放到尾部并加注释说明
  6. 输出到 AD-Rules/

用法：
    python3 scripts/build.py                        # 全量构建
    python3 scripts/build.py --no-fetch             # 使用 _cache 里的缓存重新构建
    python3 scripts/build.py --raw-base <url>       # 覆盖 DOMAIN-SET 引用的 raw 地址
    python3 scripts/build.py --stats-only           # 只打印统计，不写文件
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from collections import OrderedDict, defaultdict
from pathlib import Path

# 目录约定（与仓库里既有的 AI-Rules 保持一致：每个规则项目自成一个目录）
#   AD-Rules/          项目根目录，产物与文档都在这里
#   AD-Rules/config/   策略配置
#   AD-Rules/scripts/  构建脚本
#   AD-Rules/docs/     复核脚本
#   AD-Rules/_cache/   抓取缓存（不入库）
#   AD-Rules/.bak/     上一版备份（不入库）
ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"
CACHE = ROOT / "_cache"
OUT = ROOT                       # 产物直接放在 AD-Rules/ 下
BACKUP = ROOT / ".bak"
README_PATH = ROOT / "README.md"

# ---------------------------------------------------------------------------
# Surge 语法常量
# ---------------------------------------------------------------------------

KNOWN_FLAGS = {
    "no-resolve",
    "pre-matching",
    "extended-matching",
    "force-remote-dns",
    "force-http3",
    "no-track",
    "h2c",
}

# flag 的规范化顺序（Surge 对顺序不敏感，统一顺序便于去重）
FLAG_ORDER = ["pre-matching", "extended-matching", "no-resolve", "force-remote-dns", "force-http3", "no-track", "h2c"]

# 必须开启 MITM（HTTPS 解密）才能匹配的规则类型
MITM_RULE_TYPES = {"URL-REGEX", "URL-ADVANCED", "USER-AGENT"}

# 需要 MITM 才能工作的模块段
MITM_SECTIONS = ["Script", "URL Rewrite", "Body Rewrite", "Map Local"]

POLICIES_BLOCK = {"REJECT", "REJECT-DROP", "REJECT-TINYGIF", "BLACKHOLE"}

DOMAIN_RULE_TYPES = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "DOMAIN-SET", "DOMAIN-REGEX"}

IP_RULE_TYPES = {"IP-CIDR", "IP-CIDR6", "IP-ASN", "GEOIP"}

# 注意：必须用非捕获分组，否则 findall 只会返回最后一个 label
DOMAIN_RE = re.compile(r"(?<![\w-])(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,24}(?![\w.-])")

# ---------------------------------------------------------------------------
# c_agent（Mihomo 系内核）产物相关常量
#
# 转换命令（已由 DustinWin/ruleset_geodata 的生产工作流验证）：
#   mihomo convert-ruleset <behavior> <input-format> <input> <output>
#   mihomo convert-ruleset domain   text domains.list out.mrs
#   mihomo convert-ruleset ipcidr   text ips.list     out.mrs
#
# 域名清单语法（behavior: domain）：
#   example.com    -> DOMAIN         精确匹配
#   +.example.com  -> DOMAIN-SUFFIX  匹配该域及其全部子域
# ---------------------------------------------------------------------------

MIHOMO_API = "https://api.github.com/repos/MetaCubeX/mihomo/releases/latest"
MIHOMO_ASSET_FMT = ("https://github.com/MetaCubeX/mihomo/releases/download/{tag}/"
                    "mihomo-{goos}-{goarch}-{tag}.gz")

# 只把「拦截类」策略写进规则集；DIRECT 等放行类不进（本项目是去广告规则集）
MIHOMO_BLOCK_POLICY = {
    "REJECT": "REJECT",
    "REJECT-DROP": "REJECT",
    "REJECT-TINYGIF": "REJECT",
    "BLACKHOLE": "REJECT",
}

# 这些类型不写进 classical 规则集：
#   DOMAIN / DOMAIN-SUFFIX 已由域名集（c_agent.mrs，behavior: domain）覆盖，再写即冗余
#   DOMAIN-SET 是 Surge 语法，Mihomo 侧对应 RULE-SET，不落在规则集文件里
CAGENT_SKIP_TYPES = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-SET"}

# Surge 专有 flag，Mihomo 不认识，必须剥离，否则会污染规则
SURGE_ONLY_FLAGS = {"pre-matching", "extended-matching", "no-resolve",
                    "force-remote-dns", "force-http3", "no-track", "h2c"}

# ---------------------------------------------------------------------------
# 重要：Mihomo 的 rule-provider（behavior: classical）**并不支持全部规则类型**。
#
# 下列类型写在配置文件的 rules: 主段里没问题，但放进规则集 payload 会导致
# 该规则集整体加载失败（实测 ruleCount 变成 0，且不报错 —— 静默失效，极难发现）。
#
# 实测（mihomo v1.19.30，逐个类型验证 ruleCount）：
#   支持  : DOMAIN / DOMAIN-SUFFIX / DOMAIN-KEYWORD / DOMAIN-REGEX / IP-CIDR /
#           IP-CIDR6 / DST-PORT / SRC-PORT / PROCESS-NAME / NETWORK / OR / NOT
#   不支持: AND / URL-REGEX / USER-AGENT / IP-ASN / GEOIP / RULE-SET
#
# 因此必须在这里过滤掉。被过滤的类型主要是需要 MITM 的规则与复合规则，
# 与本项目"主体规则无需 MITM"的目标一致。
# ---------------------------------------------------------------------------
MIHOMO_UNSUPPORTED_TYPES = {
    "AND", "URL-REGEX", "USER-AGENT", "IP-ASN", "GEOIP", "RULE-SET", "DOMAIN-SET",
}


# ---------------------------------------------------------------------------
# 配置加载
# ---------------------------------------------------------------------------

def load_lines(path: Path):
    """读取 # 注释型配置文件，返回非空、非注释行的小写集合。"""
    if not path.exists():
        return []
    out = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip().lower()
        if not s or s.startswith("#"):
            continue
        out.append(s)
    return out


class Config:
    def __init__(self):
        self.sources = json.loads((CONFIG / "sources.json").read_text(encoding="utf-8"))["sources"]
        self.domestic_brands = load_lines(CONFIG / "domestic_brands.txt")
        self.intl_allowlist = load_lines(CONFIG / "intl_allowlist.txt")
        self.china_tlds = load_lines(CONFIG / "china_tlds.txt")
        self.foreign_cctlds = set(load_lines(CONFIG / "foreign_cctlds.txt"))
        self.foreign_denylist = load_lines(CONFIG / "foreign_denylist.txt")
        self.whitelist = load_lines(CONFIG / "whitelist.txt")
        self.hosting_platforms = load_lines(CONFIG / "hosting_platforms.txt")
        repo_cfg = CONFIG / "repo.json"
        self.raw_base = ""
        if repo_cfg.exists():
            self.raw_base = json.loads(repo_cfg.read_text(encoding="utf-8")).get("raw_base", "").rstrip("/")
        # 二级公共后缀（如 com.cn / co.uk），用于求「可注册域名」
        self.two_level_suffixes = {t for t in self.china_tlds if "." in t}
        self.two_level_suffixes |= set(load_lines(CONFIG / "public_suffixes.txt"))
        self.tld_set = set(self.china_tlds)
        # 上游异常保护配置
        self.guard_cfg = {
            "enabled": True, "max_drop_ratio": 0.30, "min_domains": 12000,
            "min_rules": 1000, "require_all_sources": True,
            "min_source_entries": 200, "keep_backup": True, "exit_code": 2,
        }
        guard_cfg = CONFIG / "guard.json"
        if guard_cfg.exists():
            self.guard_cfg.update(json.loads(guard_cfg.read_text(encoding="utf-8")))
        # 知名度榜单配置
        self.fame_cfg = {"enabled": False, "url": "", "top_n": 10000, "cache_days": 7}
        fame_cfg = CONFIG / "fame.json"
        if fame_cfg.exists():
            self.fame_cfg.update(json.loads(fame_cfg.read_text(encoding="utf-8")))
        self.fame = {}          # {可注册域: 排名}
        self.fame_ranks = {}    # {域名: 排名}（含子域直查）


# ---------------------------------------------------------------------------
# 抓取
# ---------------------------------------------------------------------------

def fetch(url: str, no_fetch: bool = False, retries: int = 3,
          report: dict = None, name: str = "") -> str:
    """
    抓取上游内容。

    report[name] 记录本次抓取状态，供上游异常保护判断：
      fresh          抓到了新内容
      cache-fresh    命中 6 小时内的新鲜缓存
      cache-stale    命中过期缓存（--no-fetch 时为常态）
      cache-fallback 抓取失败，回退到缓存（上游暂时不可用，仍继续构建）
      failed         抓取失败且无缓存 —— 该源本次完全没有数据，保护会中止构建
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    key = re.sub(r"[^A-Za-z0-9]+", "_", url)[-120:]
    cache_file = CACHE / key

    def mark(st):
        if report is not None and name:
            report[name] = st

    if cache_file.exists():
        age = time.time() - cache_file.stat().st_mtime
        if no_fetch or age < 6 * 3600:
            mark("cache-fresh" if age < 6 * 3600 else "cache-stale")
            return cache_file.read_text(encoding="utf-8", errors="replace")
    if no_fetch:
        mark("cache-stale" if cache_file.exists() else "failed")
        return cache_file.read_text(encoding="utf-8", errors="replace") if cache_file.exists() else ""
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AdBlock-CN-Builder/1.0"})
            with urllib.request.urlopen(req, timeout=90) as r:
                text = r.read().decode("utf-8", errors="replace")
            cache_file.write_text(text, encoding="utf-8")
            mark("fresh")
            return text
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (i + 1))
    if cache_file.exists():
        print(f"  ! 抓取失败，回退缓存（上游暂时不可用）: {url} ({last})", file=sys.stderr)
        mark("cache-fallback")
        return cache_file.read_text(encoding="utf-8", errors="replace")
    print(f"  ! 抓取失败且无缓存: {url} ({last})", file=sys.stderr)
    mark("failed")
    return ""


# 上游内容里「自报更新时间」的常见写法。用于 README 展示上游有多久没更新。
UPSTREAM_TIME_PATTERNS = [
    # AWAvenue:  #!desc=Update time: 2026-08-20 11:45:33 UTC+8
    re.compile(r"Update time:\s*(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2}):(\d{2})"),
    # Blockads:  #!date = 2026-08-29 15:49:38
    re.compile(r"#!date\s*=\s*(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2}):(\d{2})"),
    # 217heidai: #!date=2026/08/31 12:51:19
    re.compile(r"#!date\s*=\s*(\d{4})/(\d{2})/(\d{2})[ T](\d{2}):(\d{2}):(\d{2})"),
    # anti-AD:   #VER=20260829094849
    re.compile(r"#VER=(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})"),
    # 兜底：任意 ISO 风格时间
    re.compile(r"(?<!\d)(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2}):(\d{2})"),
]


def parse_upstream_time(text: str):
    """从上游内容里解析其自报的更新时间，返回 'YYYY-MM-DD HH:MM:SS' 或 None。"""
    head = "\n".join(text.splitlines()[:40])  # 只在头部找，避免误配正文
    for pat in UPSTREAM_TIME_PATTERNS:
        m = pat.search(head)
        if not m:
            continue
        g = m.groups()
        if len(g) != 6:
            continue
        try:
            y, mo, d, h, mi, s = (int(x) for x in g)
            ts = time.mktime((y, mo, d, h, mi, s, 0, 0, -1))
        except (ValueError, OverflowError):
            continue
        # 过滤掉明显不合理的时间（早于 2015 年或晚于当前 1 天以上）
        now = time.time()
        if ts < time.mktime((2015, 1, 1, 0, 0, 0, 0, 0, -1)) or ts > now + 86400:
            continue
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts)), ts
    return None


def days_since(ts: float) -> int:
    return max(0, int((time.time() - ts) // 86400))


def check_guard(cfg: Config, new: dict, old: dict, fetch_report: dict,
                source_entries: dict):
    """
    上游异常保护。返回 (是否放行, 中止原因列表)。

    任何一条命中都中止构建，绝不把坏结果覆盖到已发布的产物上：
      1. 某个源抓取失败且无缓存（完全没数据）
      2. 某个源解析出的条目数低于下限（内容异常/链接返回了错误页）
      3. 域名数或规则数低于绝对下限（防『上一版本身就是坏的』导致跌幅比较失效）
      4. 域名数或规则数相比上一版跌幅超过阈值（上游大幅删规则）
    """
    g = cfg.guard_cfg
    if not g.get("enabled"):
        return True, []
    reasons = []

    if g.get("require_all_sources", True):
        for name, st in fetch_report.items():
            if st == "failed":
                reasons.append(f"源「{name}」抓取失败且无可用缓存（上游链接可能已失效）")

    min_entries = int(g.get("min_source_entries", 200))
    for name, n in source_entries.items():
        if n < min_entries:
            reasons.append(f"源「{name}」仅解析出 {n} 条，低于下限 {min_entries}（内容异常）")

    n_dom = new.get("domains", 0)
    n_rule = new.get("rules", 0)
    min_dom = int(g.get("min_domains", 0))
    min_rule = int(g.get("min_rules", 0))
    if n_dom < min_dom:
        reasons.append(f"域名数 {n_dom} 低于绝对下限 {min_dom}")
    if n_rule < min_rule:
        reasons.append(f"规则数 {n_rule} 低于绝对下限 {min_rule}")

    if old:
        ratio = float(g.get("max_drop_ratio", 0.30))
        o_dom = old.get("domains", 0)
        o_rule = old.get("rules", 0)
        if o_dom > 0:
            drop = (o_dom - n_dom) / o_dom
            if drop > ratio:
                reasons.append(
                    f"域名数从 {o_dom} 跌到 {n_dom}（-{drop*100:.1f}%，超过阈值 {ratio*100:.0f}%）"
                    f"，疑似上游大幅删规则")
        if o_rule > 0:
            drop = (o_rule - n_rule) / o_rule
            if drop > ratio:
                reasons.append(
                    f"规则数从 {o_rule} 跌到 {n_rule}（-{drop*100:.1f}%，超过阈值 {ratio*100:.0f}%）"
                    f"，疑似上游大幅删规则")
    return (not reasons), reasons


def load_fame(cfg: Config, no_fetch: bool = False):
    """
    载入域名知名度榜单（Tranco top-1m），返回 {域名: 排名}。

    用客观的流行度排名判断「该服务是否家喻户晓」，替代永远写不全的手工白名单。
    榜单抓取失败时返回空表，构建自动降级为纯手工词表模式，不会中断。
    """
    fcfg = cfg.fame_cfg
    if not fcfg.get("enabled"):
        return {}
    CACHE.mkdir(parents=True, exist_ok=True)
    cache = CACHE / "fame_top.csv"
    stale = True
    if cache.exists():
        age_days = (time.time() - cache.stat().st_mtime) / 86400
        stale = age_days > float(fcfg.get("cache_days", 7))
    if stale and not no_fetch:
        try:
            print(f"  - 拉取知名度榜单: {fcfg['url']}")
            req = urllib.request.Request(fcfg["url"], headers={"User-Agent": "AdBlock-CN-Builder/1.0"})
            with urllib.request.urlopen(req, timeout=180) as r:
                blob = r.read()
            import zipfile
            import io
            with zipfile.ZipFile(io.BytesIO(blob)) as z:
                name = next(n for n in z.namelist() if n.endswith(".csv"))
                text = z.read(name).decode("utf-8", errors="replace")
            cache.write_text(text, encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            print(f"  ! 榜单拉取失败，回退缓存/快照: {e}", file=sys.stderr)
    if not cache.exists():
        # 仓库内置快照兜底，保证离线或榜单下线时构建仍可完成
        snap = CONFIG / "fame_snapshot.txt"
        if snap.exists():
            print("  - 使用仓库内置知名度快照")
            ranks = {}
            idx = 0
            for line in snap.read_text(encoding="utf-8").splitlines():
                s = line.strip().lower()
                if not s or s.startswith("#"):
                    continue
                idx += 1
                if idx > int(fcfg.get("top_n", 10000)):
                    break
                ranks[s] = idx
            return ranks
        return {}
    top_n = int(fcfg.get("top_n", 10000))
    ranks = {}
    for line in cache.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.strip().split(",")
        if len(parts) != 2:
            continue
        try:
            rank = int(parts[0])
        except ValueError:
            continue
        if rank > top_n:
            break
        ranks[parts[1].strip().lower()] = rank
    print(f"  - 知名度榜单载入 {len(ranks)} 个域名（top{top_n}）")
    return ranks


# ---------------------------------------------------------------------------
# 解析
# ---------------------------------------------------------------------------

class Rule:
    __slots__ = ("type", "value", "policy", "flags", "comments", "source", "raw")

    def __init__(self, type_, value, policy, flags, comments, source, raw):
        self.type = type_
        self.value = value
        self.policy = policy
        self.flags = flags
        self.comments = comments
        self.source = source
        self.raw = raw

    @property
    def key(self):
        return (self.type, self.value, self.policy)

    def render(self) -> str:
        parts = [self.type, self.value, self.policy] + list(self.flags)
        return ",".join(parts)


def parse_rule_line(line: str, source: str, comments: list) -> Rule | None:
    """把一条 Surge 规则解析成结构化对象。兼容 AND/OR/NOT 与值里带逗号的 URL-REGEX。"""
    line = line.strip()
    if not line or line.startswith("#") or line.startswith("//"):
        return None
    tokens = line.split(",")
    if len(tokens) < 2:
        return None
    rtype = tokens[0].strip()
    # 从末尾回扫 flag，flag 之前的那个 token 即 policy
    idx = len(tokens) - 1
    flags = []
    while idx >= 1 and tokens[idx].strip() in KNOWN_FLAGS:
        flags.append(tokens[idx].strip())
        idx -= 1
    if idx < 1:
        return None
    policy = tokens[idx].strip()
    value = ",".join(tokens[1:idx]).strip()
    if not value:
        return None
    canon = [f for f in FLAG_ORDER if f in set(flags)]
    canon += sorted(set(flags) - set(canon))
    return Rule(rtype, value, policy, canon, list(comments), source, line)


def parse_sgmodule(text: str, source: str):
    """解析 sgmodule。返回 (header_lines, {section: [(comments, line)]}, order)"""
    header, section, sections, order = [], None, defaultdict(list), []
    pending = []
    for raw in text.splitlines():
        s = raw.strip()
        if s.startswith("[") and s.endswith("]"):
            name = s[1:-1].strip()
            if section is None:
                header = pending
            section = name
            if name not in sections:
                sections[name] = []
                order.append(name)
            pending = []
            continue
        if section is None:
            if s == "" and not pending:
                continue
            pending.append(raw.rstrip())
            continue
        if not s:
            continue
        if s.startswith("#") or s.startswith("//"):
            pending.append(raw.rstrip())
            continue
        sections[section].append((pending, raw.rstrip()))
        pending = []
    if section is None:
        header = pending
    else:
        for c in pending:  # 段尾残留注释不丢弃
            sections[section].append(([c], ""))
    return header, sections, order


def parse_domainset(text: str, source: str):
    """解析 DOMAIN-SET 风格列表。返回 (header_lines, [domain])"""
    header, domains = [], []
    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            continue
        if s.startswith("#") or s.startswith("//"):
            header.append(raw.rstrip())
            continue
        d = s.lstrip(".").rstrip(".").lower()
        if re.fullmatch(r"[a-z0-9][a-z0-9._-]*[a-z0-9]", d):
            domains.append(d)
    return header, domains


# ---------------------------------------------------------------------------
# 域名工具
# ---------------------------------------------------------------------------

def registrable(domain: str, two_level: set) -> str:
    labels = domain.split(".")
    if len(labels) <= 2:
        return domain
    if ".".join(labels[-2:]) in two_level and len(labels) >= 3:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def token_match(domain: str, tokens) -> bool:
    """
    品牌关键词匹配。

    * 只匹配「非 TLD」的 label —— 否则 .live / .link 这类通用后缀会误命中 live 等关键词
    * 精确匹配：任意长度均可
    * 前缀模糊：token 长度 >= 5（douyin -> douyinpic）
    * 后缀模糊：token 长度 >= 6 —— 后缀最容易误伤（sina -> floresina、uber -> drtuber）
    """
    labels = domain.lower().split(".")
    if len(labels) > 1:
        labels = labels[:-1]  # 去掉 TLD
    for tok in tokens:
        for lab in labels:
            if lab == tok:
                return True
            if len(tok) >= 5 and lab.startswith(tok):
                return True
            if len(tok) >= 6 and lab.endswith(tok):
                return True
    return False


ESCAPE_RE = re.compile(r"\\(.)")


class RegionClassifier:
    """
    判定一个域名属于「国内 / 国际知名 / 国外不知名 / 未知」。

    核心原则：**剔除国外不知名域名需要正面证据**。
    国内 App 的广告域名大量使用 .com 等通用后缀且品牌名五花八门，
    任何"猜"的策略都会误杀；因此只有命中境外 ccTLD 或明确黑名单时才判为国外。
    """

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.curated = set()          # 精选源（人工整理的国内去广告模块）反推出的域名种子
        self.curated_reg = set()      # 上述种子的可注册域

    def add_curated(self, domain: str):
        d = ESCAPE_RE.sub(r"\1", domain).lstrip(".").lower().rstrip(".")
        if not d or not re.fullmatch(r"[a-z0-9][a-z0-9._-]*[a-z0-9]", d):
            return
        # 不要把有明确境外信号的域名当种子，否则会自证为"国内"（循环论证）
        if token_match(d, self.cfg.intl_allowlist):
            pass
        elif d.split(".")[-1] in self.cfg.foreign_cctlds or token_match(d, self.cfg.foreign_denylist):
            return
        self.curated.add(d)
        self.curated_reg.add(registrable(d, self.cfg.two_level_suffixes))

    def is_whitelisted(self, domain: str) -> bool:
        """白名单：以 . 开头的条目按后缀匹配，其余为精确匹配。"""
        d = domain.lower().lstrip(".").rstrip(".")
        for w in self.cfg.whitelist:
            if w.startswith("."):
                w = w.lstrip(".").rstrip(".")
                if d == w or d.endswith("." + w):
                    return True
            else:
                if d == w:
                    return True
        return False

    def classify(self, domain: str) -> str:
        d = ESCAPE_RE.sub(r"\1", domain).lower().lstrip(".").rstrip(".")
        if not d:
            return "unknown"
        if self.is_whitelisted(d):
            return "blocked"
        labels = d.split(".")
        tld = labels[-1]
        # 1) 中国国家/地区顶级域
        if tld in self.cfg.tld_set or ".".join(labels[-2:]) in self.cfg.tld_set:
            return "cn"
        # 2) 国内厂商 / 广告 SDK 关键词
        if token_match(d, self.cfg.domestic_brands):
            return "cn"
        # 3) 国际极其知名服务
        if token_match(d, self.cfg.intl_allowlist):
            return "intl"
        # 4) 精选国内规则中出现过的域名及其子域
        if d in self.curated or registrable(d, self.cfg.two_level_suffixes) in self.curated_reg:
            return "cn"
        for c in self.curated:
            if d.endswith("." + c):
                return "cn"
        # 5) 手工黑名单（用户显式指定"这是垃圾"，优先级高于知名度）
        if token_match(d, self.cfg.foreign_denylist):
            return "foreign"
        # 6) 知名度榜单：家喻户晓的服务，其广告/统计子域应当保留
        #    但托管平台（weebly / vercel / free.fr …）的子域属于任意第三方，不算
        if self.cfg.fame and not self.is_hosting_platform(d):
            r = self.cfg.fame.get(registrable(d, self.cfg.two_level_suffixes))
            if r:
                return "famous"
        # 7) 明确的境外信号
        if tld in self.cfg.foreign_cctlds:
            return "foreign"
        return "unknown"

    def is_hosting_platform(self, domain: str) -> bool:
        """是否托管平台 / CDN 基础设施（其子域归属任意第三方，不是某个 App 自己）。"""
        d = domain.lower().lstrip(".").rstrip(".")
        for p in self.cfg.hosting_platforms:
            p = p.lstrip(".").rstrip(".")
            if d == p or d.endswith("." + p):
                return True
        return False

    def keep(self, domain: str, keep_unknown: bool = False) -> bool:
        """keep_unknown=True 用于人工精选源（默认信任）；域名集默认丢弃 unknown。"""
        c = self.classify(domain)
        if c in ("cn", "intl", "famous"):
            return True
        if c == "unknown":
            return keep_unknown
        return False


def extract_domains(rule: Rule) -> list:
    """从规则中抽取用于区域判定的域名（URL-REGEX 里的 \\. 会先被还原成 .）。"""
    t = rule.type
    v = ESCAPE_RE.sub(r"\1", rule.value).lower()
    if t in ("DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "DOMAIN-REGEX"):
        return [v.strip("^$.*?[]()+|")] if v else []
    if t == "DOMAIN-SET":
        return DOMAIN_RE.findall(v)
    # URL-REGEX / USER-AGENT / AND / OR / NOT / 复合规则：抓所有域名样式的片段
    return list(DOMAIN_RE.findall(v))


def has_chinese_comment(comments: list) -> bool:
    return any(re.search(r"[\u4e00-\u9fff]", c) for c in comments)


CJK_APP_RE = re.compile(r"[\u4e00-\u9fff]{2,}")


def rule_keep(rule: Rule, cls: RegionClassifier, keep_foreign: bool, keep_unknown: bool) -> bool:
    """
    决定一条规则是否保留。

    keep_unknown: 当规则的来源域名归属判定不出（既非国内、也非国际知名，
                  也没有境外证据）时是否保留。人工精选的国内去广告源应设为 True。
    """
    if keep_foreign:
        return True
    t = rule.type
    ds = extract_domains(rule)
    # IP / 协议 / 端口 / 进程 类规则无法归属到具体 App，多为国内 App 定制，保留
    if t in IP_RULE_TYPES or t in ("PROTOCOL", "DEST-PORT", "SRC-PORT", "IN-PORT", "SRC-IP", "DEST-IP",
                                   "PROCESS-NAME", "INBOUND-USER-AGENT", "SUB-COMMAND"):
        if ds:
            return any(cls.classify(d) != "foreign" for d in ds)
        return True
    # 带中文注释的精选规则：人工标注过国内 App，直接保留
    if has_chinese_comment(rule.comments):
        return True
    if not ds:
        # 判定不了来源，保守保留
        return True
    verdicts = [cls.classify(d) for d in ds]
    if "blocked" in verdicts and "cn" not in verdicts:
        return False
    if any(v in ("cn", "intl", "famous") for v in verdicts):
        return True
    if "foreign" in verdicts and not any(v == "unknown" for v in verdicts):
        return False
    return keep_unknown


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def build(args):
    cfg = Config()
    cls = RegionClassifier(cfg)

    raw_base = args.raw_base or cfg.raw_base or "https://raw.githubusercontent.com/USER/REPO/main/AD-Rules"

    # 上一版统计（用于上游异常保护的跌幅比较）。必须在覆盖 stats.json 之前读取。
    prev_stats = {}
    prev_file = ROOT / "stats.json"
    if prev_file.exists():
        try:
            prev_stats = json.loads(prev_file.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            prev_stats = {}

    print("== 0/6 载入知名度榜单 ==")
    cfg.fame = load_fame(cfg, no_fetch=args.no_fetch)

    print("== 1/6 抓取规则源 ==")
    texts, fetch_report = {}, {}
    for src in cfg.sources:
        if not src.get("enabled", True):
            continue
        texts[src["name"]] = fetch(src["url"], no_fetch=args.no_fetch,
                                   report=fetch_report, name=src["name"])
        st = fetch_report.get(src["name"], "?")
        label = {"fresh": "新内容", "cache-fresh": "新鲜缓存", "cache-stale": "过期缓存",
                 "cache-fallback": "抓取失败→回退缓存", "failed": "抓取失败且无缓存"}.get(st, st)
        print(f"  - {src['name']} [{label}]")

    print("== 2/6 解析 ==")
    module_rules = []          # 结构化规则（来自 sgmodule 的 [Rule]）
    advanced = OrderedDict()   # MITM 段（Script / URL Rewrite / ...）
    mitm_hosts = set()
    domain_entries = []        # 来自 domainset 的域名
    seen_headers = []
    stats = defaultdict(int)

    # 第一遍：解析 sgmodule，收集精选国内域名种子
    parsed_modules = []
    source_entries = {}      # 每个源解析出的条目数（供异常保护判断内容是否正常）
    upstream_meta = {}       # 每个源自报的更新时间（供 README 展示上游有多久没更新）
    for src in cfg.sources:
        if not src.get("enabled", True):
            continue
        text = texts.get(src["name"], "")
        if not text:
            source_entries[src["name"]] = 0
            continue
        # 解析上游自报的更新时间
        got = parse_upstream_time(text)
        upstream_meta[src["name"]] = {
            "declared_time": got[0] if got else None,
            "declared_ts": got[1] if got else None,
            "days": days_since(got[1]) if got else None,
        }
        fmt = src.get("format", "auto")
        if fmt == "auto":
            fmt = "sgmodule" if "[Rule]" in text else "domainset"
        if fmt == "sgmodule":
            header, sections, order = parse_sgmodule(text, src["name"])
            parsed_modules.append((src, header, sections, order))
            seen_headers.append((src["name"], header))
            source_entries[src["name"]] = sum(
                1 for _p, l in sections.get("Rule", []) if l.strip())
        else:
            header, domains = parse_domainset(text, src["name"])
            seen_headers.append((src["name"], header))
            domain_entries.append((src["name"], domains))
            source_entries[src["name"]] = len(domains)

    for src, header, sections, order in parsed_modules:
        for pending, line in sections.get("Rule", []):
            r = parse_rule_line(line, src["name"], pending)
            if r is None:
                continue
            module_rules.append(r)

    # 精选源（人工整理的国内去广告模块）整源视为国内种子
    curated_sources = {s["name"] for s in cfg.sources
                       if s.get("enabled", True) and s.get("curated", True)
                       and s.get("format", "auto") == "sgmodule"}
    for r in module_rules:
        if r.source in curated_sources:
            for d in extract_domains(r):
                cls.add_curated(d)
    print(f"  精选规则 {len(module_rules)} 条，反推国内域名种子 {len(cls.curated)} 个")

    print("== 3/6 区域过滤 ==")
    kept_rules, dropped_rules = [], []
    for r in module_rules:
        if rule_keep(r, cls, src_keep_foreign(r.source, cfg), keep_unknown=(r.source in curated_sources)):
            kept_rules.append(r)
        else:
            dropped_rules.append(r)
    print(f"  保留 {len(kept_rules)} 条，剔除国外不知名 {len(dropped_rules)} 条")

    # 将保留下来的规则域名也纳入种子
    for r in kept_rules:
        for d in extract_domains(r):
            cls.add_curated(d)

    print("== 4/6 域名集合并去重 ==")
    merged = []
    for name, domains in domain_entries:
        if not src_keep_foreign(name, cfg):
            before = len(domains)
            domains = [d for d in domains if cls.keep(d)]
            print(f"  - {name}: {before} -> {len(domains)}")
        merged.extend(domains)
    # 把 sgmodule 里出现的域名也并入域名集
    # 注意：只并入 DOMAIN / DOMAIN-SUFFIX。
    #   DOMAIN-KEYWORD 是关键词匹配（如 httpdns、pangolin），不是域名，
    #   并入 DOMAIN-SET 会把单 label 关键词当成后缀域名，造成误匹配。
    for r in kept_rules:
        if r.policy in POLICIES_BLOCK and r.type in ("DOMAIN", "DOMAIN-SUFFIX"):
            d = r.value.lower().strip()
            if "." in d and re.fullmatch(r"[a-z0-9][a-z0-9._-]*[a-z0-9]", d):
                merged.append(d)
    merged = [d for d in merged if not cls.is_whitelisted(d)]
    merged = sorted(set(merged))
    print(f"  合并后 {len(merged)} 个")

    # 父子域收敛：若父域已在集合内，子域是冗余的（DOMAIN-SUFFIX 语义）
    base = set(merged)
    collapsed = []
    for d in merged:
        labels = d.split(".")
        redundant = False
        for i in range(1, len(labels)):
            if ".".join(labels[i:]) in base:
                redundant = True
                break
        if not redundant:
            collapsed.append(d)
    print(f"  父子域收敛后 {len(collapsed)} 个（移除 {len(merged) - len(collapsed)} 个冗余子域）")

    print("== 5/6 规则去重 ==")
    merged_rules = OrderedDict()
    for r in kept_rules:
        k = r.key
        if k in merged_rules:
            prev = merged_rules[k]
            if set(r.flags) - set(prev.flags):
                prev.flags = [f for f in FLAG_ORDER if f in (set(prev.flags) | set(r.flags))]
            stats[f"dup:{r.source}"] += 1
            continue
        merged_rules[k] = r
    deduped = list(merged_rules.values())
    print(f"  规则去重后 {len(deduped)} 条（移除 {len(kept_rules) - len(deduped)} 条重复）")

    # 按「来源 -> 原始顺序」归组，保留注释
    by_source = defaultdict(list)
    for r in deduped:
        by_source[r.source].append(r)

    plain_rules, mitm_rules = [], []
    for r in deduped:
        (mitm_rules if r.type in MITM_RULE_TYPES else plain_rules).append(r)

    print(f"  无需 MITM: {len(plain_rules)} 条 / 需要 MITM: {len(mitm_rules)} 条")

    # MITM 主机名：优先用来源模块自带的 [MITM] 段（它已经过作者验证），
    # 只保留与本次保留下来的 MITM 规则同域的条目；再补充从规则里抽出的域名。
    mitm_hosts = set()
    rule_reg = set()
    for r in mitm_rules:
        for d in extract_domains(r):
            if cls.classify(d) in ("cn", "intl"):
                mitm_hosts.add(ESCAPE_RE.sub(r"\1", d).lower())
                rule_reg.add(registrable(ESCAPE_RE.sub(r"\1", d).lower(), cfg.two_level_suffixes))
    for src, header, sections, order in parsed_modules:
        for _pending, line in sections.get("MITM", []):
            if "=" not in line:
                continue
            for h in line.split("=", 1)[-1].split(","):
                h = h.strip()
                if not h or h == "%APPEND%":
                    continue
                h = h.replace("*", "").strip().lower()
                if not h:
                    continue
                if h in mitm_hosts or registrable(h, cfg.two_level_suffixes) in rule_reg:
                    mitm_hosts.add(h)
    mitm_hosts = sorted({h for h in mitm_hosts if h and cls.keep(h, keep_unknown=False)})

    # =====================================================================
    # 上游异常保护：在写任何文件之前先判断。
    # 上游大幅删规则 / 链接失效 / 返回异常内容时，中止构建，
    # 保留仓库里已发布的上一版产物，绝不把坏结果覆盖上去。
    # =====================================================================
    new_counters = {
        "domains": len(collapsed),
        "rules": len(deduped),
    }
    prev_counters = {
        "domains": prev_stats.get("domainset", {}).get("after_region_filter_and_dedupe", 0),
        "rules": prev_stats.get("rules", {}).get("after_dedupe", 0),
    }
    if args.no_guard:
        cfg.guard_cfg["enabled"] = False
        print("  ! 已通过 --no-guard 关闭上游异常保护")
    ok, reasons = check_guard(cfg, new_counters, prev_counters,
                              fetch_report, source_entries)
    if not ok:
        code = int(cfg.guard_cfg.get("exit_code", 2))
        print("\n" + "!" * 68)
        print("! 上游异常保护触发 —— 已中止构建，仓库内已发布的产物保持原样未被覆盖")
        print("!" * 68)
        for r in reasons:
            print(f"  - {r}")
        print(f"\n  本次: 域名 {new_counters['domains']} / 规则 {new_counters['rules']}")
        print(f"  上版: 域名 {prev_counters['domains']} / 规则 {prev_counters['rules']}")
        print("  处理建议：确认上游是否真的在删规则。若确属正常变更，"
              "可调 config/guard.json 阈值后重跑。")
        sys.exit(code)
    if any(v == "cache-fallback" for v in fetch_report.values()):
        print("  ! 部分源本次抓取失败使用了缓存，内容可能不是最新（已放行，因数据完整）")

    print("== 6/6 生成输出 ==")
    # 写入前先备份上一版，便于需要时回滚
    if cfg.guard_cfg.get("keep_backup", True) and OUT.exists():
        bak = BACKUP
        shutil.rmtree(bak, ignore_errors=True)
        try:
            # 必须排除 .bak 自身与缓存目录，否则 copytree 会把备份目录拷进备份目录
            shutil.copytree(OUT, bak, ignore=shutil.ignore_patterns(
                ".bak", "_cache", "__pycache__", "build.log"))
        except Exception:  # noqa: BLE001
            pass
    OUT.mkdir(parents=True, exist_ok=True)

    # --- 域名集文件 ---
    ds_path = OUT / "adblock-cn-domains.txt"
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with ds_path.open("w", encoding="utf-8") as f:
        f.write(f"# AdBlock-CN 合并去重域名集\n")
        f.write(f"# 生成时间: {ts}\n")
        f.write(f"# 规则源: {', '.join(s['name'] for s in cfg.sources if s.get('enabled', True))}\n")
        f.write(f"# 用途: DOMAIN-SET,{raw_base}/adblock-cn-domains.txt,REJECT\n")
        f.write(f"# 域名数量: {len(collapsed)}\n")
        f.write("#\n")
        for d in collapsed:
            f.write("." + d + "\n")

    # --- MITM 高级段（可选模块）---
    adv_lines, adv_order = [], []
    for src, header, sections, order in parsed_modules:
        for sec in MITM_SECTIONS:
            if sec in sections:
                adv_order.append((src["name"], sec))
    if adv_order:
        with (OUT / "AdBlock-CN-Advanced.sgmodule").open("w", encoding="utf-8") as f:
            write_header(f, "AdBlock-CN Advanced (需 MITM)", ts, cfg,
                         "本模块包含 [Script] / [URL Rewrite] / [Body Rewrite] / [Map Local] 段，"
                         "全部需要开启 MITM（HTTPS 解密）才能生效。不需要 MITM 的用户请不要加载本模块。")
            for sec in MITM_SECTIONS:
                blocks = [(src, sections) for src, h, sections, o in parsed_modules if sec in sections]
                if not blocks:
                    continue
                f.write(f"\n[{sec}]\n")
                for src, h, sections, o in parsed_modules:
                    if sec not in sections:
                        continue
                    f.write(f"\n# ============ 来源：{ src } ============\n")
                    for pending, line in sections[sec]:
                        for c in pending:
                            f.write(c + "\n")
                        if line:
                            f.write(line + "\n")
            f.write("\n[MITM]\n")
            f.write("hostname = %APPEND% " + ", ".join(mitm_hosts) + "\n")

    # --- 主模块（DOMAIN-SET 引用版）---
    write_module(OUT / "AdBlock-CN.sgmodule", by_source, cfg, collapsed, ts, raw_base,
                 mitm_rules, mitm_hosts, mode="domainset", cls=cls)

    # --- 主模块（完全内联版）---
    write_module(OUT / "AdBlock-CN-Standalone.sgmodule", by_source, cfg, collapsed, ts, raw_base,
                 mitm_rules, mitm_hosts, mode="standalone", cls=cls)

    # --- c_agent（Mihomo 系内核）产物 ---
    print("== 7/7 生成 c_agent 产物（Mihomo 系内核）==")
    cagent = write_cagent(collapsed, deduped, ts, raw_base,
                          mihomo_arg=args.mihomo, enabled=not args.no_mrs)

    stats["domainset"] = len(collapsed)
    stats["rules_total"] = len(deduped)
    stats["rules_plain"] = len(plain_rules)
    stats["rules_mitm"] = len(mitm_rules)
    stats["dropped_foreign"] = len(dropped_rules)

    # --- 统计报告 ---
    report = {
        "generated_at": ts,
        "sources": [{"name": s["name"], "url": s["url"]} for s in cfg.sources if s.get("enabled", True)],
        "rules": {
            "raw": len(module_rules),
            "kept_after_region_filter": len(kept_rules),
            "dropped_foreign": len(dropped_rules),
            "after_dedupe": len(deduped),
            "no_mitm_required": len(plain_rules),
            "mitm_required": len(mitm_rules),
        },
        "domainset": {
            "raw_entries": sum(len(d) for _, d in domain_entries),
            "after_region_filter_and_dedupe": len(collapsed),
        },
        "mitm_hostnames": len(mitm_hosts),
        "cagent": cagent,
        "fetch_status": fetch_report,
        "source_entries": source_entries,
        "upstream": {
            name: {"declared_time": m["declared_time"], "days_since_update": m["days"]}
            for name, m in upstream_meta.items()
        },
    }
    (ROOT / "stats.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # --- 把上游更新时间写回 README（供直接阅读时掌握上游有多久没更新）---
    inject_readme_upstream(cfg, upstream_meta, source_entries, ts)

    print("\n---- 统计 ----")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


README_START = "<!-- UPSTREAM_STATUS:START -->"
README_END = "<!-- UPSTREAM_STATUS:END -->"


def inject_readme_upstream(cfg: Config, upstream_meta: dict,
                           source_entries: dict, ts: str):
    """
    把「上游最新更新时间 + 距今天数」写回 README 的标记区块。

    时间取自上游内容里自报的时间戳（各源头部写法不同，见 UPSTREAM_TIME_PATTERNS），
    比"我们上次抓取的时间"更能反映上游真实的维护状况。
    """
    readme = README_PATH
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    if README_START not in text or README_END not in text:
        print("  ! README 中未找到上游状态标记，跳过注入")
        return

    rows = ["| 源 | 上游最新更新时间 | 距今 | 本次条目数 | 说明 |", "| --- | --- | --- | --- | --- |"]
    stale = []
    for src in cfg.sources:
        if not src.get("enabled", True):
            continue
        name = src["name"]
        meta = upstream_meta.get(name, {})
        when = meta.get("declared_time")
        days = meta.get("days")
        if when and days is not None:
            when_cell = when
            if days >= 180:
                flag = f" ⚠️ 已 {days} 天"
                stale.append(f"{name}（{days} 天）")
            elif days >= 60:
                flag = f" （{days} 天）"
            else:
                flag = ""
            days_cell = f"{days} 天{flag}"
        else:
            when_cell = "未能解析"
            days_cell = "—"
        rows.append(f"| {name} | {when_cell} | {days_cell} | "
                    f"{source_entries.get(name, 0):,} | {src.get('desc', '')} |")

    block = "\n".join([
        README_START,
        "<!-- 本段由 scripts/build.py 自动生成，请勿手动修改 -->",
        f"<!-- 本次构建时间：{ts} -->",
        "",
    ] + rows + [
        "",
        "> 时间为上游内容里自报的更新时间（非本项目抓取时间），可据此判断上游是否还在维护。",
        "> 距今超过 180 天会标注 ⚠️。",
        README_END,
    ])

    pre, rest = text.split(README_START, 1)
    _old, post = rest.split(README_END, 1)
    readme.write_text(pre + block + post, encoding="utf-8")
    print(f"  - README 上游更新时间已更新（{len(rows) - 2} 个源）")
    if stale:
        print(f"  ! 以下上游已超过 180 天未更新: {'; '.join(stale)}")


def src_keep_foreign(name: str, cfg: Config) -> bool:
    for s in cfg.sources:
        if s["name"] == name:
            return s.get("keep_foreign", False)
    return False


def write_header(f, name, ts, cfg, desc):
    f.write(f"#!name={name}\n")
    f.write(f"#!desc={desc}\n")
    f.write(f"#!category=广告拦截\n")
    f.write(f"#!author=AdBlock-CN Builder\n")
    f.write(f"#!icon=https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad.png\n")
    f.write(f"#!homepage=https://github.com/privacy-protection-tools/anti-AD\n")
    f.write(f"#!date={ts}\n")
    f.write("#\n")
    f.write(f"# 规则源：{', '.join(s['name'] for s in cfg.sources if s.get('enabled', True))}\n")
    f.write("#\n")


MITM_NOTICE = """\
# =============================================================================
#  以下规则需要开启 MITM（HTTPS 解密）方可生效
# -----------------------------------------------------------------------------
#  URL-REGEX / USER-AGENT 这类规则需要读取加密流量中的内容才能匹配，
#  因此必须在 Surge -> 首页 -> 解密 HTTPS 流量（MITM）中为本模块列出的主机名
#  开启解密，否则这些规则不会命中。
#
#  风险提示：MITM 会解密对应域名的流量，请只对可信域名开启；
#          网银、支付、政务类 App 不建议开启 MITM。
#          本模块已尽量剔除需要 MITM 的规则，默认主体规则均无需解密即可生效。
# =============================================================================
"""


def write_module(path: Path, by_source, cfg, collapsed, ts, raw_base, mitm_rules, mitm_hosts,
                 mode="domainset", cls=None):
    with path.open("w", encoding="utf-8") as f:
        desc = ("以净化国内 App 为主的 Surge 去广告规则集：多源整合 + 去重 + 剔除不知名国外 App，"
                "主规则无需 MITM" if mode == "domainset" else
                "以净化国内 App 为主的 Surge 去广告规则集（完全内联版，无需联网拉取域名集）")
        write_header(f, "AdBlock CN · 国内 App 去广告", ts, cfg, desc)
        f.write("# 生成方式：scripts/build.py（配置见 config/，新增规则源编辑 config/sources.json）\n")
        f.write(f"# 规则总数：{sum(len(v) for v in by_source.values())} 条"
                f"（其中需要 MITM 的 {len(mitm_rules)} 条）\n")
        f.write(f"# 域名集：{len(collapsed)} 个\n")
        f.write("#\n\n")

        f.write("[Rule]\n")

        # 1) 各来源的精选规则（保留原始注释，无需 MITM 的在前）
        for source, rules in by_source.items():
            plain = [r for r in rules if r.type not in MITM_RULE_TYPES]
            if not plain:
                continue
            f.write(f"\n# ============ 来源：{source} ============\n")
            for r in plain:
                for c in r.comments:
                    f.write(c + "\n")
                f.write(r.render() + "\n")

        # 2) 合并去重后的域名集
        f.write("\n# ============ 合并去重域名集（anti-AD / AdBlock Surge / 各源域名）============\n")
        if mode == "domainset":
            f.write(f"# 该域名集由本仓库定时重新生成，Surge 会随模块自动更新\n")
            f.write(f"DOMAIN-SET,{raw_base}/adblock-cn-domains.txt,REJECT\n")
        else:
            for d in collapsed:
                f.write(f"DOMAIN-SUFFIX,{d},REJECT\n")

        # 3) 需要 MITM 的规则
        if mitm_rules:
            f.write("\n" + MITM_NOTICE + "\n")
            per_source = defaultdict(list)
            for r in mitm_rules:
                per_source[r.source].append(r)
            for source, rules in per_source.items():
                f.write(f"# ---- 来源：{source} ----\n")
                for r in rules:
                    for c in r.comments:
                        f.write(c + "\n")
                    f.write(r.render() + "\n")

        # 4) MITM 主机名
        if mitm_hosts:
            f.write("\n[MITM]\n")
            f.write("# 仅上面「需要 MITM」的规则会用到；不使用这些规则可删除本段\n")
            f.write("hostname = %APPEND% " + ", ".join(mitm_hosts) + "\n")


# ---------------------------------------------------------------------------
# c_agent（Mihomo 系内核）产物生成
# ---------------------------------------------------------------------------

def to_mihomo_rule(r: Rule):
    """
    Surge 规则 -> Mihomo classical 规则（payload 不带策略，由 RULE-SET 统一指定）。

    返回 None 表示该条不该进入 classical 规则集：
      - DOMAIN / DOMAIN-SUFFIX：已由域名集（behavior: domain）覆盖，写入即冗余
      - 放行类策略（DIRECT 等）：本项目是去广告规则集，不收录
      - URL-REGEX 值内含逗号：会被当成字段分隔符，宁可跳过也不产出畸形规则
    """
    if r.type in CAGENT_SKIP_TYPES:
        return None
    if r.type in MIHOMO_UNSUPPORTED_TYPES:
        return None
    if r.policy not in MIHOMO_BLOCK_POLICY:
        return None
    value = r.value
    if r.type in ("AND", "OR", "NOT"):
        # 嵌套子规则里的 Surge 专有 flag 同样要剥掉
        value = re.sub(r",(?:%s)" % "|".join(sorted(SURGE_ONLY_FLAGS)), "", value)
        # Surge 的 PROTOCOL 在 Mihomo 里叫 NETWORK；仅 TCP/UDP 可映射，
        # QUIC 之类没有对应类型，整条丢弃以免产出无法解析的规则
        value = re.sub(r"\(PROTOCOL,TCP\)", "(NETWORK,tcp)", value)
        value = re.sub(r"\(PROTOCOL,UDP\)", "(NETWORK,udp)", value)
        if re.search(r"\(PROTOCOL,", value):
            return None
        # 引号内的值若含逗号，Mihomo 会把它当字段分隔符截断 -> 跳过
        for seg in re.findall(r'"([^"]*)"', value):
            if "," in seg:
                return None
    if r.type == "URL-REGEX" and "," in value:
        return None
    return f"{r.type},{value}"


def find_mihomo(explicit: str = "") -> str:
    """定位 mihomo 二进制：显式路径 > 环境变量 MIHOMO > PATH > _cache/mihomo。"""
    candidates = [explicit, os.environ.get("MIHOMO", ""), "mihomo", str(CACHE / "mihomo")]
    for c in candidates:
        if not c:
            continue
        if os.path.isabs(c) or os.sep in c:
            if os.path.isfile(c) and os.access(c, os.X_OK):
                return c
        else:
            found = shutil.which(c)
            if found:
                return found
    return ""


def mihomo_convert(binary: str, behavior: str, input_format: str, src, dst) -> tuple:
    """调用 mihomo convert-ruleset。返回 (是否成功, 错误说明)。"""
    try:
        proc = subprocess.run(
            [binary, "convert-ruleset", behavior, input_format, str(src), str(dst)],
            capture_output=True, text=True, timeout=300,
        )
    except Exception as e:  # noqa: BLE001
        return False, f"执行失败: {e}"
    if proc.returncode != 0:
        return False, (proc.stderr or proc.stdout or "").strip()[:300]
    p = Path(dst)
    if not p.exists() or p.stat().st_size == 0:
        return False, "未生成产物或产物为空"
    return True, ""


def _norm_domain(line: str) -> str:
    """把 rule-set 里的域名写法归一化，便于比较：+.a.com / .a.com / a.com -> a.com"""
    s = line.strip().lstrip("+").lstrip(".").lower()
    return s


def mihomo_verify(binary: str, mrs_path, expected_domains) -> tuple:
    """
    把 .mrs 反向解回文本并抽样核对。

    本地不一定能拿到 mihomo 二进制，因此加这一步自检：万一命令语义理解有误，
    能立刻发现并丢弃坏文件，而不是把坏产物提交出去。

    之所以用「抽样比对 + 数量容差」而不是严格相等：mihomo 在编码/解码时
    可能做归一化或合并，行数未必逐条对应，强行要求相等会误杀好的产物。
    """
    import random as _rnd
    tmp = Path(tempfile.mkdtemp(prefix="mrsverify-")) / "back.txt"
    try:
        ok, msg = mihomo_convert(binary, "domain", "mrs", mrs_path, tmp)
        if not ok:
            return False, f"反解失败: {msg}"
        got = {_norm_domain(l) for l in
               tmp.read_text(encoding="utf-8", errors="replace").splitlines()
               if l.strip() and not l.strip().startswith("#")}
        if not got:
            return False, "反解结果为空"
        n_exp, n_got = len(expected_domains), len(got)
        # 数量容差 ±2%（允许 mihomo 做归一化/合并）
        if abs(n_got - n_exp) > max(int(n_exp * 0.02), 10):
            return False, f"条目数偏差过大（期望 {n_exp}，实际 {n_got}）"
        # 抽样比对：随机 300 条，允许极少量缺失
        sample = expected_domains if n_exp <= 300 else _rnd.sample(expected_domains, 300)
        missing = [d for d in sample if d not in got]
        if len(missing) > max(int(len(sample) * 0.01), 1):
            return False, (f"抽样 {len(sample)} 条中有 {len(missing)} 条缺失，"
                           f"例如: {missing[:3]}")
        return True, ""
    finally:
        shutil.rmtree(tmp.parent, ignore_errors=True)


def write_cagent(collapsed, deduped, ts, raw_base, mihomo_arg="", enabled=True):
    """
    生成 c_agent 系列产物（Mihomo 系内核规则集）：

      c_agent.mrs          二进制规则集，behavior: domain —— 移动端加载最快、内存占用最低
      c_agent-domain.list  同名文本版，behavior: domain / format: text —— 不支持 mrs 时的兜底
      c_agent-rules.yaml   classical 规则集，承载域名集装不下的类型（IP-CIDR / URL-REGEX / 复合规则等）

    mihomo 二进制缺失或转换失败时，只产出文本格式，不中断构建。
    """
    stats = {}

    # ---- 1) 域名清单（behavior: domain）----
    dom_path = OUT / "c_agent-domain.list"
    with dom_path.open("w", encoding="utf-8") as f:
        f.write("# c_agent 域名清单（rule-provider behavior: domain）\n")
        f.write(f"# 生成时间: {ts}\n")
        f.write("# 语法: example.com = 精确匹配(DOMAIN) / +.example.com = 后缀匹配(DOMAIN-SUFFIX)\n")
        f.write(f"# 域名数量: {len(collapsed)}\n")
        f.write("#\n")
        for d in collapsed:
            f.write("+." + d + "\n")
    stats["domains"] = len(collapsed)

    # ---- 2) classical 规则集 ----
    emitted, skipped_comma, skipped_unsupported = [], 0, 0
    for r in deduped:
        m = to_mihomo_rule(r)
        if m is None:
            if r.type in MIHOMO_UNSUPPORTED_TYPES and r.policy in MIHOMO_BLOCK_POLICY:
                skipped_unsupported += 1
            elif r.type == "URL-REGEX" and "," in r.value:
                skipped_comma += 1
            continue
        emitted.append(m)
    emitted = sorted(set(emitted))
    stats["rules"] = len(emitted)
    stats["skipped_regex_comma"] = skipped_comma
    stats["skipped_unsupported"] = skipped_unsupported
    if skipped_unsupported:
        print(f"  - 另有 {skipped_unsupported} 条规则因 Mihomo 规则集不支持该类型而跳过"
              f"（{"、".join(sorted(MIHOMO_UNSUPPORTED_TYPES))}）")

    rules_path = OUT / "c_agent-rules.yaml"
    with rules_path.open("w", encoding="utf-8") as f:
        f.write("# c_agent 规则集（rule-provider behavior: classical）\n")
        f.write(f"# 生成时间: {ts}\n")
        f.write("# 只收录域名集装不下的类型；DOMAIN / DOMAIN-SUFFIX 由 c_agent.mrs 覆盖，此处不再重复\n")
        f.write(f"# 规则数量: {len(emitted)}\n")
        f.write("payload:\n")
        for r in emitted:
            f.write(f"  - {r}\n")

    # ---- 3) 二进制规则集（需要 mihomo）----
    mrs_path = OUT / "c_agent.mrs"
    if not enabled:
        print("  - c_agent.mrs 已按配置跳过")
        stats["mrs"] = "disabled"
        return stats

    binary = find_mihomo(mihomo_arg)
    if not binary:
        print("  - 未找到 mihomo 二进制，跳过 c_agent.mrs（文本格式产物不受影响）")
        print("    提示: 设置 MIHOMO=/path/to/mihomo 或 brew install mihomo 后再构建")
        stats["mrs"] = "no-binary"
        return stats

    ok, msg = mihomo_convert(binary, "domain", "text", dom_path, mrs_path)
    if not ok:
        print(f"  ! mihomo 转换失败，已丢弃 {mrs_path.name}: {msg}")
        mrs_path.unlink(missing_ok=True)
        stats["mrs"] = f"convert-failed: {msg}"
        return stats

    ok, msg = mihomo_verify(binary, mrs_path, collapsed)
    if not ok:
        print(f"  ! c_agent.mrs 自检未通过，已丢弃: {msg}")
        mrs_path.unlink(missing_ok=True)
        stats["mrs"] = f"verify-failed: {msg}"
        return stats

    size_kb = mrs_path.stat().st_size / 1024
    print(f"  - c_agent.mrs 生成成功并通过自检（{size_kb:.0f} KB，"
          f"较文本版压缩 {dom_path.stat().st_size / max(mrs_path.stat().st_size, 1):.1f}x）")
    stats["mrs"] = "ok"
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-fetch", action="store_true", help="使用缓存，不联网")
    ap.add_argument("--raw-base", default="", help="DOMAIN-SET 引用的 raw 地址前缀")
    ap.add_argument("--stats-only", action="store_true", help="只打印统计")
    ap.add_argument("--mihomo", default="", help="mihomo 二进制路径，用于生成 c_agent.mrs")
    ap.add_argument("--no-mrs", action="store_true", help="跳过 c_agent.mrs 生成")
    ap.add_argument("--no-guard", action="store_true",
                    help="跳过上游异常保护（仅在确认上游确实在大改时使用）")
    args = ap.parse_args()
    build(args)


if __name__ == "__main__":
    main()
