#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AIGC Rules Merger - 合并去重归类 AIGC 分流规则
支持输入: Clash rule-provider yaml / Clash config rules / QuantumultX yaml filter /
         QuantumultX legacy list / Surge list / 混合文本 / 远程 URL 列表文件
输出: Ai.yaml (Clash) / Ai.list (Surge) / Ai.qx.list (QuantumultX 原生语法) / report.md
仅依赖 Python 标准库, 可被任何工具(Cursor/Claude/Codex)与 GitHub Actions 直接调用。
用法:
  python merge_aigc_rules.py <输入文件或目录...> -o <输出目录> [--name Ai]
      [--qx-policy no-policy] [--sources-file sources.txt]
  # 仅用远程 sources.txt 时输入路径可省略:
  python merge_aigc_rules.py --sources-file sources.txt -o output/
"""
import argparse
import datetime
import ipaddress
import os
import re
import sys
import tempfile
import urllib.request

# ---------------- 规则类型 ----------------
# (类型, 是否域名类)
DOMAIN_TYPES = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "DOMAIN-REGEX"}
IP_TYPES = {"IP-CIDR", "IP-CIDR6", "IP-ASN"}
SUPPORTED = DOMAIN_TYPES | IP_TYPES | {"GEOIP"}

# 非域名类规则类型, 一律忽略(不属于本技能的分流范围)
IGNORED_HEADS = {"user-agent", "useragent", "and", "or", "not", "final",
                 "subnet", "wi-fi", "wifi-ssid", "rule-set", "sub-rules"}

# ---------------- 非 AI 排除黑名单 (专注 AIGC 分流, 支付类等一律不收) ----------------
# PayPal 家族: paypal 及钓鱼变体 paypa1/paypaal、braintree、billmelater、card.io、
# cashify、贝宝(beibao)、安付通(anfutong)、mywaytopay 等马甲域名,
# 以及通用支付 SaaS (checkout/chargebee/fastspring/paylike/paydiant)
EXCLUDE_RE = re.compile(
    r"paypal|paypa1|paypaal|braintree|briantreepayments|billmelater|bill-safe"
    r"|bml\.info|card\.io|cash2|cashify|paysmart|mywaytopay|paydiant|paylike"
    r"|checkout\.com|chargebee|fastspring|venmo|xoom|simility"
    r"|beibao|anfutong"
    # PayPal 变体/关联: pypl(官方短域) 钓鱼拼写变体 krakenjs loanbuilder pdncommunity sheerid id.me
    r"|pypl|pa9pal|paaypal|paily|paipal|pavpal|payppal|payypal|krakenjs"
    r"|loanbuilder|pdncommunity|pp-soc|pppds|sheerid|id\.me"
    # 其他金融/垃圾域
    r"|swiftbank|swiftcapital|swiftfinancial|webmoneyinfo|gmoney"
    r"|theshoppingexpresslane|filipino-music|i-o-u|xn--"
    # 支付 SaaS(用户口径: 支付类统一放 PayPal 规则集, AI 规则专注 AI)
    r"|stripe|lemonsqueezy|paddle\.com|paddle\.net",
    re.IGNORECASE,
)

# 不明确/非 AI 的具体规则精确黑名单(上游反复带入, 永久剔除)
# 注: google.com 不在此列, 已归入 Google AI / Gemini 组
EXCLUDE_EXACT = {
    "7h15.ru1353t.1s.m4d3.by.5ukk4w.skk.moe",  # Sukka 彩蛋签名域
    "crixet.com",      # 归属不明
    "pool.ntp.org",    # NTP 时间同步, 非 AI
    "qpoe.com",        # 归属不明
    "14061",           # ASN 14061 (DigitalOcean 通用云), 非 AI 专属
}


# QX 旧版格式 -> 通用格式 映射
QX_LEGACY_MAP = {
    "host": "DOMAIN",
    "host-suffix": "DOMAIN-SUFFIX",
    "host-keyword": "DOMAIN-KEYWORD",
    "host-wildcard": "DOMAIN-WILDCARD",
    "ip-cidr": "IP-CIDR",
    "ip-cidr6": "IP-CIDR6",
    "ip-asn": "IP-ASN",
    "geoip": "GEOIP",
}

# 通用格式 -> QX 原生格式 映射 (QX filter_remote 单独输出时使用)
QX_NATIVE_MAP = {
    "DOMAIN": "HOST",
    "DOMAIN-SUFFIX": "HOST-SUFFIX",
    "DOMAIN-KEYWORD": "HOST-KEYWORD",
    "DOMAIN-WILDCARD": "HOST-WILDCARD",
    "IP-CIDR": "IP-CIDR",
    "IP-CIDR6": "IP-CIDR6",
    "IP-ASN": "IP-ASN",
    "GEOIP": "GEOIP",
}
# QX 原生 filter 不支持 DOMAIN-REGEX, 也不支持 no-resolve 参数(实测头部作者全部如此)


# ---------------- AIGC 厂商归类 (按优先级从上到下匹配) ----------------
PROVIDER_MAP = [
    ("OpenAI / ChatGPT", [
        "openai", "chatgpt", "oaistatic", "oaiusercontent", "chat.com",
        "sora.com", "livekit", "ai.com",
    ]),
    ("Anthropic / Claude", [
        "anthropic", "claude", "claudeusercontent", "grazie", "poetry-db",
        "clau.de", "prodregistryv2", "servd-anthropic-website",
    ]),
    ("Cursor / 开发 AI", ["cursor", "cursor.sh", "cursor-cdn", "cursorapi", "cursorvm", "cursor.com",
                          "codeium", "windsurf", "replit", "tabnine", "v0.dev", "v0.app", "bolt.new",
                          "ampcode", "augment", "cline", "continue.dev", "cosine", "coderabbit",
                          "cognition", "devin", "context7", "factory.ai", "grep.app", "greptile",
                          "kilo", "kilocode", "lovable", "models.dev", "opencode", "opncd",
                          "openclaw", "clawhub", "pieces.app", "qodo", "refact", "roocode",
                          "sourcery", "sourcegraph", "supermaven", "sweep.dev", "tabbyml",
                          "warp.dev", "zed"]),
    ("GitHub Copilot", ["githubcopilot", "github.githubassets.com"]),
    ("Apple Intelligence", ["apple-wit", "intelligence.apple.com", "apple-cloudkit.com",
                            "apple-livephotos.com", "madservices.apple.com", "guzzoni.apple.com",
                            "smoot.apple.com", "blackbird.apple.com"]),
    ("Dify", ["dify"]),
    ("Manus", ["manus.im", "manuscdn", "manus"]),
    ("OpenRouter", ["openrouter"]),
    ("Jasper", ["jasper"]),
    ("Notion AI", ["notion", "notion-static"]),
    ("OpenArt", ["openart"]),
    ("JetBrains AI", ["jetbrains"]),
    ("图像生成", ["recraft.ai", "ideogram.ai", "leonardo.ai", "playground.ai", "playgroundai",
                 "krea", "magnific", "photoroom", "remove.bg", "topazlabs", "artbreeder",
                 "kaiber", "higgsfield", "hedra", "viggle", "lovart"]),
    ("视频生成", ["runwayml", "lumalabs", "luma", "pika.art", "klingai", "synthesia", "heygen", "d-id",
                 "captions", "fliki", "pictory", "genmo", "invideo", "colossyan", "descript"]),
    ("LLM 平台", ["replicate", "cerebras", "together.ai", "together.xyz", "modal.com"]),
    ("写作/搜索 AI", ["you.com", "copy.ai", "writesonic", "grammarly", "quillbot", "wordtune",
                     "writer.com", "rytr", "sudowrite", "plusai", "gamma.app", "beautiful.ai",
                     "speechify"]),
    ("设计工具", ["canva.com", "figma.com"]),
    ("Google AI / Gemini", [
        "gemini", "generativelanguage", "deepmind", "generativeai",
        "bard.google", "ai.google.dev", "makersuite", "aistudio",
        "notebooklm.google", "jules.google", "labs.google", "alphafold",
        "g.ai", "antigravity", "featureassets", "ai.google",
        "google.com",  # 上游带 google.com 主体域, 经用户确认归入本组
        "googleapis.com", "googleusercontent.com", "colab.google", "colab.research.google",
        "apis.google.com", "clients4.google.com", "clients6.google.com",
        "developerprofiles.google.com", "proactivebackend-pa.googleapis.com",
        "colab", "developerprofiles",
    ]),
    ("Microsoft Copilot / Bing", [
        "copilot", "bingviz", "bing", "msn.com", "sydney.bing",
        "bingapis", "bing-shopping", "edgeservices.bing", "officeapps",
        "office.com", "microsoftapp.net", "microsofttranslator", "api.github.com",
    ]),
    ("xAI / Grok", ["x.ai", "grok"]),
    ("Perplexity", ["perplexity", "pplx"]),
    ("Poe", ["poe.com", "poecdn"]),
    ("Midjourney", ["midjourney"]),
    ("Meta AI", ["meta.ai", "llama.com", "meta.com"]),
    ("Mistral", ["mistral.ai", "chat.mistral", "lechat"]),
    ("HuggingFace", ["huggingface", "hf.co", "hf.space", "huggingface.co"]),
    ("Cohere", ["cohere", "cohereai"]),
    ("Stability", ["stability", "stablediffusion", "clipdrop", "dreamstudio", "civitai"]),
    ("ElevenLabs / 语音音乐", ["elevenlabs", "elevenreader", "murf.ai", "suno.com", "suno.ai", "udio.com",
                              "assemblyai", "cartesia", "deepgram", "lmnt", "resemble", "respeecher",
                              "play.ht", "wellsaid", "voice.ai", "otter.ai", "read.ai", "meetgeek",
                              "tldv", "fireflies", "fathom.video", "hume.ai"]),
    ("NVIDIA AI", ["nvidia"]),
    ("云厂商 AI", ["ai.azure.com", "azuredatabricks", "databricks", "bedrock", "idetoolkits",
                  "ml.cloud.ibm.com", "watsonx", "snowflakecomputing"]),
    ("推理/算力平台", ["baseten", "cerebras", "coreweave", "crusoe", "deepinfra", "fireworks",
                     "hyperbolic", "lambda", "nebius", "runpod", "sambanova", "anyscale",
                     "vast.ai", "modal", "fal.ai"]),
    ("独立模型公司", ["ai21", "aleph-alpha", "allenai", "inflection", "reka", "liquid.ai",
                    "nomic", "nousresearch", "smallcloud", "voyageai", "bfl.ai",
                    "blackforestlabs", "pi.ai"]),
    ("LLM 开发栈/向量库", ["langchain", "llamaindex", "litellm", "portkey", "helicone", "langfuse",
                         "langsmith", "arize", "braintrust", "wandb", "mintlify", "pinecone",
                         "qdrant", "weaviate", "milvus", "trychroma", "chroma", "turbopuffer"]),
    ("数据采集/搜索 API", ["apify", "brightdata", "browserbase", "browserless", "diffbot",
                          "exa", "firecrawl", "scrapingbee", "serpapi", "serper", "tavily",
                          "zenrows", "phind"]),
    ("智能体/企业 AI", ["lindy", "relay.app", "dust.tt", "sierra", "hebbia", "glean", "mem.ai",
                       "granola", "diabrowser", "bardeen"]),
    ("Groq", ["groq.com", "grokmind"]),
    ("DeepSeek", ["deepseek"]),
    ("ByteDance / 豆包", ["doubao", "coze", "volces", "volcengine", "byteintl", "lf-ai"]),
    ("Alibaba / 通义", ["tongyi", "qianwen", "dashscope", "aliyun-ai", "baichuan-ai",
                        "modelscope", "bailian", "aliyuncs.com/ai"]),
    ("Baidu / 文心", ["yiyan", "ernie", "aip.baidubce", "wenxin"]),
    ("Moonshot / Kimi", ["moonshot", "kimi", "kimi.com", "mcp.ai-cache"]),
    ("Zhipu / 智谱", ["bigmodel", "chatglm", "zhipuai", "glm.ai"]),
    ("MiniMax", ["minimax", "minimaxi", "abab"]),
    ("Tencent / 混元", ["hunyuan", "tencentcs", "hunyuan.cloud.tencent"]),
    ("Character.AI", ["character.ai", "characterai", "c.ai"]),
    ("AI 通用基础设施", [
        # 统计/实验平台
        "statsig", "featuregates", "launchdarkly", "segment.io", "segment",
        "datadoghq", "datadog",
        "sentry", "posthog", "amplitude", "mixpanel",
        "cloudflareinsights", "heap.io", "hotjar", "fullstory", "logrocket",
        "events.data.microsoft", "location.microsoft",
        # 登录/认证
        "auth0", "okta", "clerk", "onelogin", "workos",
        # 支付
        "stripe", "lemonsqueezy", "paddle", "recurly", "revenuecat",
        # 邮件
        "sendgrid",
        # CDN/风控
        "cloudflare", "challenges.cloudflare", "arkoselabs", "hcaptcha",
        "recaptcha", "turnstile", "perimeterx", "px-cdn", "imperva", "observeit",
        # 检索/推送
        "algolia", "pusher", "pubnub", "ably", "fanservices",
        "firebase", "crashlytics", "appcenter", "in.appcenter.ms",
        # 其他通用
        "intercom", "intercomcdn", "zendesk", "freshdesk", "liveperson",
        "imgix", "azureedge", "wp.com", "amazonaws", "identrust",
        "usefathom", "plausible", "cloudinary",
    ]),
]

# 已知 IP 资产归属 (网段/ASN 精确匹配; 来源: 各上游规则集与厂商官方公告)
IP_PROVIDER_MAP = {
    "160.79.104.0/21": "Anthropic / Claude",
    "2607:6bc0::/32": "Anthropic / Claude",
    "24.199.123.28/32": "OpenAI / ChatGPT",
    "64.23.132.171/32": "OpenAI / ChatGPT",
    "399358": "Anthropic / Claude",      # AS399358 Anthropic PBC
    "20473": "OpenAI / ChatGPT",         # AS20473 Vultr (OpenAI 出口)
    "13335": "AI 通用基础设施",            # AS13335 Cloudflare
}

# 基础设施类别名(用于注释分组)
INFRA_LABEL = "AI 通用基础设施"


def classify(value, rtype):
    """按域名值归类到厂商, 返回类别名; 无法归类返回 'Others'"""
    v = value.lower()
    if rtype in IP_TYPES:
        return IP_PROVIDER_MAP.get(v, "Others")  # IP 资产精确匹配, 未收录返回 Others
    if rtype == "GEOIP":
        return "Others"
    for label, kws in PROVIDER_MAP:
        for kw in kws:
            # 边界匹配: kw 需出现在域名标签边界(点或连字符)上, 避免词中误命中
            if v == kw or v.endswith("." + kw) or (
                kw in v and (("." + kw) in ("." + v) or ("-" + kw) in ("-" + v))
            ):
                return label
    # 关键词型规则用包含匹配
    for label, kws in PROVIDER_MAP:
        if rtype == "DOMAIN-KEYWORD" and any(kw in v for kw in kws):
            return label
    return "Others"


# ---------------- 解析 ----------------
def parse_rule_line(line):
    """解析一行规则 -> (rtype, value, no_resolve) 或 None"""
    s = line.strip().strip('"').strip("'")
    if not s or s.startswith("#") or s.startswith("//"):
        return None
    # 去掉行内注释
    if "#" in s and "," in s and s.index("#") > s.index(","):
        s = s[: s.index("#")].strip()
    # 去掉策略参数: DOMAIN-SUFFIX,openai.com,PROXY -> 只留前两段(域名类)
    parts = [p.strip() for p in s.split(",")]
    if not parts or not parts[0]:
        return None
    head = parts[0].strip("-").lower().replace(" ", "")
    if head in IGNORED_HEADS:
        return None

    rtype, value, no_resolve = None, None, False
    # QX 旧版格式
    if head in QX_LEGACY_MAP:
        rtype = QX_LEGACY_MAP[head]
        if len(parts) < 2:
            return None
        value = parts[1]
        rest = [p for p in parts[2:] if p and not p.startswith("PROXY")
                and p not in ("DIRECT", "REJECT", "proxy", "direct", "reject")]
        no_resolve = any(p.lower() == "no-resolve" for p in rest)
    elif head.upper() in SUPPORTED:
        rtype = head.upper()
        if len(parts) < 2:
            return None
        value = parts[1]
        rest = parts[2:]
        no_resolve = any(p.lower() == "no-resolve" for p in rest)
    else:
        # 纯域名行(裸 host)
        if re.fullmatch(r"[A-Za-z0-9_*.-]+\.[A-Za-z]{2,}", s.split()[0]):
            first = s.split()[0]
            if "*" in first:
                return ("DOMAIN-WILDCARD", first, False)
            return ("DOMAIN", first, False)
        return None

    # 清洗 value
    value = value.strip().strip('"').strip("'").lower().rstrip(".")
    if rtype in DOMAIN_TYPES or rtype == "DOMAIN-WILDCARD":
        value = value.lstrip(".") if value.startswith(".") else value
        if not re.fullmatch(r"[A-Za-z0-9_*.-]+", value.replace(":", "")):
            # DOMAIN-REGEX 允许正则字符
            if rtype != "DOMAIN-REGEX":
                return None
    if not value:
        return None
    return (rtype, value, no_resolve)


def parse_payload_yaml(text, source):
    """解析 Clash/QX 的 payload: yaml"""
    rules = []
    in_payload = False
    for raw in text.splitlines():
        line = raw.rstrip()
        ls = line.strip()
        if ls.startswith("payload:"):
            in_payload = True
            continue
        if in_payload:
            m = re.match(r"^\s*-\s+(.+)$", ls)
            if m:
                r = parse_rule_line(m.group(1))
                if r:
                    rules.append((r[0], r[1], r[2], source))
            elif not ls and not line.startswith(" "):
                pass
    return rules


def parse_rules_section(text, source):
    """解析 Clash 配置 rules: 段"""
    rules = []
    in_rules = False
    for raw in text.splitlines():
        line = raw.rstrip()
        ls = line.strip()
        if re.match(r"^rules:\s*$", ls):
            in_rules = True
            continue
        if in_rules:
            if re.match(r"^[A-Za-z-]+:\s*$", line) and not line.startswith((" ", "\t", "-")):
                in_rules = False
                continue
            m = re.match(r"^\s*-\s*(?:'([^']+)'|\"([^\"]+)\"|(.+))\s*$", ls)
            if m:
                item = m.group(1) or m.group(2) or m.group(3)
                r = parse_rule_line(item)
                if r:
                    rules.append((r[0], r[1], r[2], source))
    return rules


def parse_plain_list(text, source):
    """解析 Surge/QX/纯文本 list"""
    rules = []
    for line in text.splitlines():
        ls = line.strip()
        if not ls:
            continue
        if ls.startswith("- ") and ls.count(",") >= 1:
            ls = ls[2:]
        r = parse_rule_line(ls)
        if r:
            rules.append((r[0], r[1], r[2], source))
    return rules


def parse_file(path):
    """自动识别文件格式并解析"""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except OSError as e:
        print(f"[WARN] 无法读取 {path}: {e}", file=sys.stderr)
        return []
    rules = []
    rules += parse_payload_yaml(text, os.path.basename(path))
    rules += parse_rules_section(text, os.path.basename(path))
    if "payload:" not in text and "rules:" not in text:
        rules += parse_plain_list(text, os.path.basename(path))
    # 逐行兜底: 文件被解析出过 payload/rules 但行数对不上时补充裸行
    return rules


# ---------------- 去重 ----------------
def collect_dirs(rules):
    """聚合: 返回 dict[(rtype, value)] = 规则"""
    agg = {}
    for rtype, value, nr, src in rules:
        key = (rtype, value)
        if key in agg:
            # no-resolve 取或
            old = agg[key]
            agg[key] = (old[0], old[1], old[2] or nr, old[3])
        else:
            agg[key] = (rtype, value, nr, [src])
    return agg


def dedupe(agg):
    """
    去重(含包含关系):
      1. 精确重复已由聚合处理
      2. DOMAIN,x.com 被 DOMAIN-SUFFIX,x.com 覆盖
      3. DOMAIN,a.b.com 被 DOMAIN-SUFFIX,b.com 覆盖
      4. DOMAIN-SUFFIX,b.com 存在时 DOMAIN-SUFFIX,a.b.com 冗余
      5. IP-CIDR 被更大网段覆盖
    返回: (保留规则dict, 删除明细list)
    """
    removed = []
    suffixes = {v for (t, v) in agg if t == "DOMAIN-SUFFIX"}
    domains = {v for (t, v) in agg if t == "DOMAIN"}
    sub_domains = {v for (t, v) in agg if t == "DOMAIN-SUFFIX"}
    keep = dict(agg)

    # DOMAIN 被 DOMAIN-SUFFIX 覆盖
    for d in sorted(domains):
        parts = d.split(".")
        for i in range(len(parts) - 2):  # 最多退到 eTLD+1 由后续判断
            parent = ".".join(parts[i + 1:])
            if parent in suffixes:
                removed.append((("DOMAIN", d), f"被 DOMAIN-SUFFIX,{parent} 覆盖"))
                keep.pop(("DOMAIN", d), None)
                break
    # 子 DOMAIN-SUFFIX 被父 DOMAIN-SUFFIX 覆盖
    for sd in sorted(sub_domains):
        parts = sd.split(".")
        for i in range(1, len(parts) - 1):
            parent = ".".join(parts[i:])
            if parent in sub_domains and sd != parent:
                removed.append((("DOMAIN-SUFFIX", sd), f"被 DOMAIN-SUFFIX,{parent} 覆盖"))
                keep.pop(("DOMAIN-SUFFIX", sd), None)
                break
    # IP-CIDR 网段包含 (按 IPv4/IPv6 分组, 避免 subnet_of 跨版本 TypeError)
    nets = []
    for (t, v), rec in agg.items():
        if t in ("IP-CIDR", "IP-CIDR6"):
            try:
                nets.append((ipaddress.ip_network(v, strict=False), (t, v)))
            except ValueError:
                pass
    for i, (net_a, key_a) in enumerate(nets):
        for j, (net_b, key_b) in enumerate(nets):
            if i != j and key_a in keep and net_a.version == net_b.version \
                    and net_a != net_b and net_a.subnet_of(net_b):
                removed.append((key_a, f"被 {key_b[0]},{key_b[1]} 网段覆盖"))
                keep.pop(key_a, None)
    return keep, removed


# ---------------- 输出 ----------------
def order_key(item):
    (t, v), rec = item
    cat = classify(v, t)
    idx = next((i for i, (label, _) in enumerate(PROVIDER_MAP) if label == cat), len(PROVIDER_MAP))
    return (idx, cat, t, v)


def build_outputs(keep, removed, args):
    today = datetime.date.today().isoformat()
    outdir = args.output
    os.makedirs(outdir, exist_ok=True)
    items = sorted(keep.items(), key=order_key)

    # ---- Ai.yaml (Clash; QX 亦可经单向兼容直接订阅) ----
    yaml_lines = [
        f"# NAME: {args.name} AIGC Rules",
        f"# DESC: 合并整理的 AIGC 分流规则 (Clash rule-provider; QX 亦可直接订阅)",
        f"# UPDATED: {today}",
        f"# COUNT: {len(keep)}",
        "",
        "payload:",
    ]
    last_cat = None
    for (t, v), rec in items:
        cat = classify(v, t)
        if cat != last_cat:
            yaml_lines.append(f"  # >> {cat}")
            last_cat = cat
        nr = ",no-resolve" if rec[2] and t in IP_TYPES else ""
        yaml_lines.append(f"  - {t},{v}{nr}")
    with open(os.path.join(outdir, f"{args.name}.yaml"), "w", encoding="utf-8") as f:
        f.write("\n".join(yaml_lines) + "\n")

    # ---- Ai.list (Surge) ----
    list_lines = [
        f"# {args.name} AIGC Rules (Surge RULE-SET)",
        f"# UPDATED: {today}",
        f"# COUNT: {len(keep)}",
        "",
    ]
    last_cat = None
    for (t, v), rec in items:
        cat = classify(v, t)
        if cat != last_cat:
            list_lines.append(f"# >> {cat}")
            last_cat = cat
        nr = ",no-resolve" if rec[2] and t in IP_TYPES else ""
        list_lines.append(f"{t},{v}{nr}")
    with open(os.path.join(outdir, f"{args.name}.list"), "w", encoding="utf-8") as f:
        f.write("\n".join(list_lines) + "\n")

    # ---- Ai.qx.list (QuantumultX 原生语法) ----
    # QX 原生格式: HOST-SUFFIX,openai.com,no-policy (占位策略; 订阅时 force-policy 覆盖)
    qx_lines = [
        f"# {args.name} AIGC Rules (QuantumultX 原生 filter)",
        f"# UPDATED: {today}",
        f"# COUNT: {len(keep)} (DOMAIN-REGEX 规则 QX 不支持, 已自动跳过)",
        f"# 策略为占位符 {args.qx_policy}, 请订阅时用 force-policy=你的策略组 自由指定",
        "",
    ]
    last_cat = None
    qx_skipped = 0
    for (t, v), rec in items:
        cat = classify(v, t)
        if cat != last_cat:
            qx_lines.append(f"# >> {cat}")
            last_cat = cat
        if t not in QX_NATIVE_MAP:
            qx_skipped += 1
            continue
        qx_lines.append(f"{QX_NATIVE_MAP[t]},{v},{args.qx_policy}")
    with open(os.path.join(outdir, f"{args.name}.qx.list"), "w", encoding="utf-8") as f:
        f.write("\n".join(qx_lines) + "\n")

    # ---- report.md ----
    sources = {}
    for rec in keep.values():
        for s in rec[3]:
            sources[s] = sources.get(s, 0) + 1
    others = [(t, v) for (t, v) in keep if classify(v, t) == "Others"]
    rep = [
        f"# AIGC 规则合并报告 - {today}",
        "",
        f"- 保留规则: **{len(keep)}** 条",
        f"- 去重删除: **{len(removed)}** 条",
        f"- 输出: `{args.name}.yaml` (Clash) / `{args.name}.list` (Surge) / "
        f"`{args.name}.qx.list` (QuantumultX 原生, 其中跳过 {qx_skipped} 条 QX 不支持的规则类型)",
        "",
        "## 来源文件统计",
        "",
        "| 来源 | 贡献规则数 |",
        "| --- | --- |",
    ]
    for s, n in sorted(sources.items(), key=lambda x: -x[1]):
        rep.append(f"| {s} | {n} |")
    rep += ["", "## 去重明细", ""]
    if removed:
        rep.append("| 被删除规则 | 原因 |")
        rep.append("| --- | --- |")
        for (t, v), why in removed:
            rep.append(f"| {t},{v} | {why} |")
    else:
        rep.append("无重复。")
    rep += ["", "## 未能自动归类 (Others)", ""]
    if others:
        rep.append("以下规则需人工归入厂商类别:")
        for t, v in sorted(others):
            rep.append(f"- {t},{v}")
    else:
        rep.append("全部规则均已归类。")
    with open(os.path.join(outdir, "report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    return len(keep), len(removed), others


def fetch_sources(sources_file):
    """读取 sources.txt 中的 URL 列表并下载到临时目录, 返回下载后的文件路径列表"""
    urls = []
    with open(sources_file, "r", encoding="utf-8") as f:
        for line in f:
            ls = line.strip()
            if ls and not ls.startswith("#") and ls.lower().startswith("http"):
                urls.append(ls)
    if not urls:
        return []
    tmpdir = tempfile.mkdtemp(prefix="aigc_src_")
    files = []
    for i, url in enumerate(urls):
        name = re.sub(r"[^A-Za-z0-9._-]", "_", url.split("/")[-1] or f"src{i}") or f"src{i}"
        path = os.path.join(tmpdir, f"{i:02d}_{name}")
        ok = False
        # 先 urllib 重试 2 次
        for _ in range(2):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "aigc-rules-merger/1.0"})
                with urllib.request.urlopen(req, timeout=30) as resp, open(path, "wb") as out:
                    out.write(resp.read())
                ok = True
                break
            except Exception:
                continue
        # 失败则 curl 兜底(代理/分块传输场景更稳)
        if not ok:
            try:
                import subprocess
                r = subprocess.run(["curl", "-sL", "--max-time", "60", url],
                                   capture_output=True, timeout=90)
                if r.returncode == 0 and r.stdout:
                    with open(path, "wb") as out:
                        out.write(r.stdout)
                    ok = True
            except Exception:
                pass
        if ok:
            files.append(path)
            print(f"[INFO] 下载成功: {url}")
        else:
            print(f"[WARN] 下载失败(跳过): {url}", file=sys.stderr)
    return files


def main():
    ap = argparse.ArgumentParser(description="AIGC 分流规则合并去重归类")
    ap.add_argument("inputs", nargs="*", help="输入文件或目录(目录会递归扫描; 有 --sources-file 时可省略)")
    ap.add_argument("-o", "--output", default="./output", help="输出目录 (默认 ./output)")
    ap.add_argument("--name", default="Ai", help="输出文件名前缀 (默认 Ai)")
    ap.add_argument("--qx-policy", default="no-policy",
                    help="QuantumultX 原生输出内嵌的策略占位符 (默认 no-policy, 不预设具体策略; "
                         "语法第三字段必须存在, 订阅时用 force-policy=自定义策略组 覆盖即可自由指定)")
    ap.add_argument("--sources-file", dest="sources_file", default=None,
                    help="URL 列表文件(每行一个 http(s) 链接, # 注释), 自动下载后并入输入")
    ap.add_argument("--cumulative", action="store_true",
                    help="累积模式: 先读入输出目录已有规则作为基底再合并新源, "
                         "上游删除的规则本地继续保留, 只去重/新增(防上游恶意删除)")
    args = ap.parse_args()

    files = []
    if args.cumulative:
        # 累积模式: 上一轮输出回灌为基底输入(置于最前, 报告中来源显示为基底文件)
        base_names = [f"{args.name}.yaml", f"{args.name}.list", f"{args.name}.qx.list"]
        for bn in base_names:
            bp = os.path.join(args.output, bn)
            if os.path.isfile(bp):
                files.append(bp)
            else:
                print(f"[INFO] 累积基底不存在(首轮运行, 跳过): {bp}", file=sys.stderr)
        if files:
            print(f"[INFO] 累积模式: 已载入 {len(files)} 个基底文件(上轮输出)")
    if args.sources_file:
        if not os.path.isfile(args.sources_file):
            print(f"[ERROR] sources 文件不存在: {args.sources_file}", file=sys.stderr)
            sys.exit(1)
        files += fetch_sources(args.sources_file)
    for p in args.inputs:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                for n in names:
                    if n.lower().endswith((".yaml", ".yml", ".list", ".txt", ".conf", ".rule", ".rules")):
                        files.append(os.path.join(root, n))
        elif os.path.isfile(p):
            files.append(p)
        else:
            print(f"[WARN] 跳过不存在路径: {p}", file=sys.stderr)
    if not files:
        print("[ERROR] 没有可处理的输入文件", file=sys.stderr)
        sys.exit(1)

    rules = []
    for f in files:
        n = len(rules)
        rules += parse_file(f)
        print(f"[INFO] {f}: 解析出 {len(rules) - n} 条规则")

    if not rules:
        print("[ERROR] 未解析到任何规则", file=sys.stderr)
        sys.exit(1)

    # 排除非 AI 规则(支付类等黑名单)
    filtered, excluded = [], []
    for r in rules:
        if EXCLUDE_RE.search(r[1]) or r[1].strip().lower() in EXCLUDE_EXACT:
            excluded.append(r)
        else:
            filtered.append(r)
    if excluded:
        print(f"[INFO] 已排除 {len(excluded)} 条非 AI 规则(支付类黑名单, 详见 report.md)")

    agg = collect_dirs(filtered)
    keep, removed = dedupe(agg)
    kept, rm, others = build_outputs(keep, removed, args)
    if excluded:
        with open(os.path.join(args.output, "report.md"), "a", encoding="utf-8") as fp:
            fp.write("\n## 已排除的非 AI 规则 (支付类黑名单)\n\n")
            fp.write(f"共 {len(excluded)} 条命中排除黑名单(PayPal 家族/通用支付 SaaS), 未纳入输出:\n\n")
            seen = set()
            for rtype, value, _nr, src in excluded:
                key = (rtype, value)
                if key in seen:
                    continue
                seen.add(key)
                fp.write(f"- {rtype},{value}  <- {src}\n")
    print(f"\n[DONE] 共 {len(rules)} 条 -> 排除 {len(excluded)} 条非AI, 保留 {kept} 条, 去重 {rm} 条, 未归类 {len(others)} 条")
    print(f"[DONE] 输出目录: {os.path.abspath(args.output)}")


if __name__ == "__main__":
    main()
