# AIGC 规则合并报告 - 2026-10-30

- 保留规则: **526** 条
- 去重删除: **109** 条
- 输出: `Cl_Ai.yaml` (Clash) / `Sg_Ai.domainset` (Surge DOMAIN-SET 高性能域名集, 504 条) + `Sg_Ai.list` (Surge RULE-SET classical 补充, 22 条) / `Ai_qx.list` (QuantumultX 原生, 其中跳过 1 条 QX 不支持的规则类型)
- mrs: `Cl_Ai_domain.mrs` (504 条域名规则) + `Cl_Ai_ipcidr.mrs` (5 条 IP 规则); 另有 17 条 (DOMAIN-KEYWORD/REGEX/IP-ASN/GEOIP) mrs 不支持, 仅在 yaml/list 中生效
- sing-box: `Sb_Ai.srs` (523 条规则, 二进制格式, 已生成) + `Sb_Ai.json` (JSON 源码格式); 另有 3 条 (IP-ASN/GEOIP) sing-box 规则集不支持, 仅在 yaml/list 中生效

## 来源文件统计

| 来源 | 贡献规则数 |
| --- | --- |
| Cl_Ai.yaml | 525 |
| Sg_Ai.domainset | 1 |

## 去重明细

| 被删除规则 | 原因 |
| --- | --- |
| DOMAIN,aicode.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,aida.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,aisandbox-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,aistudio.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,alkalicore-pa.clients6.google.com | 被 DOMAIN-SUFFIX,clients6.google.com 覆盖 |
| DOMAIN,alkalimakersuite-pa.clients6.google.com | 被 DOMAIN-SUFFIX,clients6.google.com 覆盖 |
| DOMAIN,antigravity-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,antigravity.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,api.cloudflare.com | 被 DOMAIN-SUFFIX,cloudflare.com 覆盖 |
| DOMAIN,api.githubcopilot.com | 被 DOMAIN-SUFFIX,githubcopilot.com 覆盖 |
| DOMAIN,api.groq.com | 被 DOMAIN-SUFFIX,groq.com 覆盖 |
| DOMAIN,api.jetbrains.ai | 被 DOMAIN-SUFFIX,jetbrains.ai 覆盖 |
| DOMAIN,api.statsig.com | 被 DOMAIN-SUFFIX,statsig.com 覆盖 |
| DOMAIN,api.together.xyz | 被 DOMAIN-SUFFIX,together.xyz 覆盖 |
| DOMAIN,appsgenaiserver-pa.clients.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,appsgenaiserver-pa.clients6.google.com | 被 DOMAIN-SUFFIX,clients6.google.com 覆盖 |
| DOMAIN,appsgenaiserver-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,auth.grazie.ai | 被 DOMAIN-SUFFIX,grazie.ai 覆盖 |
| DOMAIN,auth.meta.com | 被 DOMAIN-SUFFIX,meta.com 覆盖 |
| DOMAIN,aws-language-servers.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,aws-toolkit-language-servers.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,bard.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,chat.openai.com.cdn.cloudflare.net | 被 DOMAIN-SUFFIX,openai.com.cdn.cloudflare.net 覆盖 |
| DOMAIN,client-telemetry.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,cloudaicompanion.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,cloudcode-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,codewhisperer.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,console.groq.com | 被 DOMAIN-SUFFIX,groq.com 覆盖 |
| DOMAIN,content-firebaseappcheck.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,daily-cloudcode-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,desktop-release.codewhisperer.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,firebaseappcheck.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,gateway.ai.cloudflare.com | 被 DOMAIN-SUFFIX,cloudflare.com 覆盖 |
| DOMAIN,geller-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,gemini.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,geminiweb-pa.clients.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,geminiweb-pa.clients6.google.com | 被 DOMAIN-SUFFIX,clients6.google.com 覆盖 |
| DOMAIN,generativelanguage.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,identitytoolkit.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,idetoolkits-hostedfiles.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,inference.codeium.com | 被 DOMAIN-SUFFIX,codeium.com 覆盖 |
| DOMAIN,integrate.api.nvidia.com | 被 DOMAIN-SUFFIX,api.nvidia.com 覆盖 |
| DOMAIN,jules.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,labstailwind.pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,makersuite.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,notebooklm-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,notebooklm.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,notebooklm.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,openai-api.arkoselabs.com | 被 DOMAIN-SUFFIX,arkoselabs.com 覆盖 |
| DOMAIN,openaiapi-site.azureedge.net | 被 DOMAIN-SUFFIX,azureedge.net 覆盖 |
| DOMAIN,openaicom.imgix.net | 被 DOMAIN-SUFFIX,imgix.net 覆盖 |
| DOMAIN,pay.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,ppl-ai-file-upload.s3.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,production-openaicom-storage.azureedge.net | 被 DOMAIN-SUFFIX,azureedge.net 覆盖 |
| DOMAIN,q.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,robinfrontend-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,securetoken.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,server.codeium.com | 被 DOMAIN-SUFFIX,codeium.com 覆盖 |
| DOMAIN,server.self-serve.windsurf.com | 被 DOMAIN-SUFFIX,windsurf.com 覆盖 |
| DOMAIN,services.bingapis.com | 被 DOMAIN-SUFFIX,bingapis.com 覆盖 |
| DOMAIN,specs.q.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,static.cloudflareinsights.com | 被 DOMAIN-SUFFIX,cloudflareinsights.com 覆盖 |
| DOMAIN,telemetry.aws-language-servers.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,waa-pa.clients6.google.com | 被 DOMAIN-SUFFIX,clients6.google.com 覆盖 |
| DOMAIN,webchannel-alkalimakersuite-pa.clients6.google.com | 被 DOMAIN-SUFFIX,clients6.google.com 覆盖 |
| DOMAIN-SUFFIX,aicode.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,aida.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,aiplatform.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,aisandbox-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,aistudio.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,alkalimakersuite-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,api.statsig.com | 被 DOMAIN-SUFFIX,statsig.com 覆盖 |
| DOMAIN-SUFFIX,apis.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,bard.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,bedrock.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN-SUFFIX,business.gemini.google | 被 DOMAIN-SUFFIX,gemini.google 覆盖 |
| DOMAIN-SUFFIX,challenges.cloudflare.com | 被 DOMAIN-SUFFIX,cloudflare.com 覆盖 |
| DOMAIN-SUFFIX,chatgpt.livekit.cloud | 被 DOMAIN-SUFFIX,livekit.cloud 覆盖 |
| DOMAIN-SUFFIX,client-api.arkoselabs.com | 被 DOMAIN-SUFFIX,arkoselabs.com 覆盖 |
| DOMAIN-SUFFIX,clients4.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,clients6.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,cloudcode-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,colab.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,colab.research.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,cp4.cloudflare.com | 被 DOMAIN-SUFFIX,cloudflare.com 覆盖 |
| DOMAIN-SUFFIX,developerprofiles.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,events.statsigapi.net | 被 DOMAIN-SUFFIX,statsigapi.net 覆盖 |
| DOMAIN-SUFFIX,firebaseinstallations.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,flow.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,gateway.ai.cloudflare.com | 被 DOMAIN-SUFFIX,cloudflare.com 覆盖 |
| DOMAIN-SUFFIX,geller-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,gemini.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,generativelanguage.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,host.livekit.cloud | 被 DOMAIN-SUFFIX,livekit.cloud 覆盖 |
| DOMAIN-SUFFIX,jules.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,labs.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,labstailwind.pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,makersuite.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,notebook.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,notebooklm.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,one.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,opal.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,openaiapi-site.azureedge.net | 被 DOMAIN-SUFFIX,azureedge.net 覆盖 |
| DOMAIN-SUFFIX,openaicom.imgix.net | 被 DOMAIN-SUFFIX,imgix.net 覆盖 |
| DOMAIN-SUFFIX,payments.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,proactivebackend-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,robinfrontend-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,turn.livekit.cloud | 被 DOMAIN-SUFFIX,livekit.cloud 覆盖 |
| DOMAIN-SUFFIX,windsurf-telemetry.codeium.com | 被 DOMAIN-SUFFIX,codeium.com 覆盖 |

## 未能自动归类 (Others)

以下规则需人工归入厂商类别:
- DOMAIN,ai-gateway.vercel.sh
- DOMAIN,connect.facebook.net
- DOMAIN,cookieEl.style.display
- DOMAIN,cookieel.style.display
- DOMAIN,firefly.adobe.com
- DOMAIN,meta-ohttp-config-prod.fastly-edge.com
- DOMAIN,meta-ohttp-relay-prod.fastly-edge.com
- DOMAIN,production.museai.com
- DOMAIN,us-central1-xi-labs.cloudfunctions.net
- DOMAIN-SUFFIX,abacus.ai
- DOMAIN-SUFFIX,adobe.io
- DOMAIN-SUFFIX,ant.dev
- DOMAIN-SUFFIX,antspace.dev
- DOMAIN-SUFFIX,apple-relay.fastly-edge.com
- DOMAIN-SUFFIX,artificialanalysis.ai
- DOMAIN-SUFFIX,atlassian.com
- DOMAIN-SUFFIX,atmeta.com
- DOMAIN-SUFFIX,awswaf.com
- DOMAIN-SUFFIX,base44.app
- DOMAIN-SUFFIX,base44.com
- DOMAIN-SUFFIX,blackbox.ai
- DOMAIN-SUFFIX,chatbotclaude.com
- DOMAIN-SUFFIX,claicode.com
- DOMAIN-SUFFIX,commandcode.ai
- DOMAIN-SUFFIX,composio.dev
- DOMAIN-SUFFIX,cue.im
- DOMAIN-SUFFIX,deepl.com
- DOMAIN-SUFFIX,deeplusercontent.com
- DOMAIN-SUFFIX,eigent.ai
- DOMAIN-SUFFIX,facebook.com
- DOMAIN-SUFFIX,fbcdn.net
- DOMAIN-SUFFIX,freepik.com
- DOMAIN-SUFFIX,genspark.ai
- DOMAIN-SUFFIX,gspe1-ssl.ls.apple.com
- DOMAIN-SUFFIX,interaction.co
- DOMAIN-SUFFIX,jina.ai
- DOMAIN-SUFFIX,komo.ai
- DOMAIN-SUFFIX,lepton.ai
- DOMAIN-SUFFIX,linear.app
- DOMAIN-SUFFIX,link.com
- DOMAIN-SUFFIX,llamameta.net
- DOMAIN-SUFFIX,metaaiusercontent.com
- DOMAIN-SUFFIX,metaaivm.com
- DOMAIN-SUFFIX,mindstudio.ai
- DOMAIN-SUFFIX,muse.ai
- DOMAIN-SUFFIX,myclaw.ai
- DOMAIN-SUFFIX,notebook.google
- DOMAIN-SUFFIX,novita.ai
- DOMAIN-SUFFIX,poke.com
- DOMAIN-SUFFIX,prelude.dev
- DOMAIN-SUFFIX,px-cloud.net
- DOMAIN-SUFFIX,runway.com
- DOMAIN-SUFFIX,simular.ai
- DOMAIN-SUFFIX,slack.com
- DOMAIN-SUFFIX,slashy.com
- DOMAIN-SUFFIX,stytch.com
- DOMAIN-SUFFIX,syntx.ai
- DOMAIN-SUFFIX,thinkingmachines.ai
- DOMAIN-SUFFIX,typesafe.ai
- DOMAIN-SUFFIX,vellum.ai
- DOMAIN-SUFFIX,withpersona.com
- IP-CIDR,129.146.3.78/32

## 已排除的非 AI 规则 (支付类黑名单)

共 31 条命中排除黑名单(PayPal 家族/通用支付 SaaS), 未纳入输出:

- DOMAIN-SUFFIX,stripe.com  <- 00_Ai.yaml
- DOMAIN,7h15.ru1353t.1s.m4d3.by.5ukk4w.skk.moe  <- 02_AIGC.yaml
- DOMAIN-SUFFIX,pool.ntp.org  <- 03_AIGC.list
- DOMAIN-SUFFIX,braintree-api.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,braintreegateway.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,braintreepayments.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,chargebee.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,checkout.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,crixet.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,fastspring.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,getbraintree.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,id.me  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,lemonsqueezy.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paddle.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.me  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalobjects.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,qpoe.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,sheerid.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,venmo.com  <- 05_OverseasAI.list
- DOMAIN-KEYWORD,paypal  <- 05_OverseasAI.list
- DOMAIN-KEYWORD,stripe  <- 05_OverseasAI.list
- IP-ASN,14061  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,oystermercury.top  <- 14_AI_Rules.lsr
