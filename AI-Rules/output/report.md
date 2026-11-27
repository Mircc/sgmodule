# AIGC 规则合并报告 - 2026-11-27

- 保留规则: **571** 条
- 去重删除: **128** 条
- 输出: `Cl_Ai.yaml` (Clash) / `Sg_Ai.domainset` (Surge DOMAIN-SET 高性能域名集, 545 条) + `Sg_Ai.list` (Surge RULE-SET classical 补充, 26 条) / `Ai_qx.list` (QuantumultX 原生, 其中跳过 1 条 QX 不支持的规则类型)
- mrs: `Cl_Ai_domain.mrs` (545 条域名规则) + `Cl_Ai_ipcidr.mrs` (7 条 IP 规则); 另有 19 条 (DOMAIN-KEYWORD/REGEX/IP-ASN/GEOIP) mrs 不支持, 仅在 yaml/list 中生效
- sing-box: `Sb_Ai.srs` (567 条规则, 二进制格式, 已生成) + `Sb_Ai.json` (JSON 源码格式); 另有 4 条 (IP-ASN/GEOIP) sing-box 规则集不支持, 仅在 yaml/list 中生效

## 来源文件统计

| 来源 | 贡献规则数 |
| --- | --- |
| Cl_Ai.yaml | 570 |
| Sg_Ai.domainset | 1 |

## 去重明细

| 被删除规则 | 原因 |
| --- | --- |
| DOMAIN,ai.developer.meta.com | 被 DOMAIN-SUFFIX,meta.com 覆盖 |
| DOMAIN,ai.meta.com | 被 DOMAIN-SUFFIX,meta.com 覆盖 |
| DOMAIN,aicode.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,aida.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,aidemos.meta.com | 被 DOMAIN-SUFFIX,meta.com 覆盖 |
| DOMAIN,aisandbox-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,aistudio.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,alkalicore-pa.clients6.google.com | 被 DOMAIN-SUFFIX,clients6.google.com 覆盖 |
| DOMAIN,alkalimakersuite-pa.clients6.google.com | 被 DOMAIN-SUFFIX,clients6.google.com 覆盖 |
| DOMAIN,anthropic.auth0.com | 被 DOMAIN-SUFFIX,auth0.com 覆盖 |
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
| DOMAIN,bridge.claudeusercontent.com | 被 DOMAIN-SUFFIX,claudeusercontent.com 覆盖 |
| DOMAIN,chat.openai.com.cdn.cloudflare.net | 被 DOMAIN-SUFFIX,openai.com.cdn.cloudflare.net 覆盖 |
| DOMAIN,client-telemetry.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,cloud.zed.dev | 被 DOMAIN-SUFFIX,zed.dev 覆盖 |
| DOMAIN,cloudaicompanion.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,cloudcode-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,codewhisperer.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,cognito-identity.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,console.groq.com | 被 DOMAIN-SUFFIX,groq.com 覆盖 |
| DOMAIN,content-firebaseappcheck.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,daily-cloudcode-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,daily-cloudcode-pa.sandbox.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,desktop-release.codewhisperer.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,developer.meta.com | 被 DOMAIN-SUFFIX,meta.com 覆盖 |
| DOMAIN,firebaseappcheck.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,gateway.ai.cloudflare.com | 被 DOMAIN-SUFFIX,ai.cloudflare.com 覆盖 |
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
| DOMAIN,llama.developer.meta.com | 被 DOMAIN-SUFFIX,meta.com 覆盖 |
| DOMAIN,makersuite.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,notebooklm-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,notebooklm.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,notebooklm.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,o1158394.ingest.us.sentry.io | 被 DOMAIN-SUFFIX,sentry.io 覆盖 |
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
| DOMAIN,specs.q.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,q.us-east-1.amazonaws.com 覆盖 |
| DOMAIN,static.cloudflareinsights.com | 被 DOMAIN-SUFFIX,cloudflareinsights.com 覆盖 |
| DOMAIN,storage.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,telemetry.aws-language-servers.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,waa-pa.clients6.google.com | 被 DOMAIN-SUFFIX,clients6.google.com 覆盖 |
| DOMAIN,webchannel-alkalimakersuite-pa.clients6.google.com | 被 DOMAIN-SUFFIX,clients6.google.com 覆盖 |
| DOMAIN-SUFFIX,ai.cloudflare.com | 被 DOMAIN-SUFFIX,cloudflare.com 覆盖 |
| DOMAIN-SUFFIX,aicode.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,aida.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,aiplatform.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,aisandbox-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,aistudio.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,alkalimakersuite-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,antigravity.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
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
| DOMAIN-SUFFIX,firefly.adobe.io | 被 DOMAIN-SUFFIX,adobe.io 覆盖 |
| DOMAIN-SUFFIX,flow.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,gateway.ai.cloudflare.com | 被 DOMAIN-SUFFIX,ai.cloudflare.com 覆盖 |
| DOMAIN-SUFFIX,geller-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,gemini.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,generativelanguage.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,hermes-agent.nousresearch.com | 被 DOMAIN-SUFFIX,nousresearch.com 覆盖 |
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
| DOMAIN-SUFFIX,q.eu-central-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN-SUFFIX,q.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN-SUFFIX,robinfrontend-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,sso.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN-SUFFIX,turn.livekit.cloud | 被 DOMAIN-SUFFIX,livekit.cloud 覆盖 |
| DOMAIN-SUFFIX,windsurf-telemetry.codeium.com | 被 DOMAIN-SUFFIX,codeium.com 覆盖 |

## 未能自动归类 (Others)

以下规则需人工归入厂商类别:
- DOMAIN,ai-gateway.vercel.sh
- DOMAIN,cdn.growthbook.io
- DOMAIN,connect.facebook.net
- DOMAIN,cookieEl.style.display
- DOMAIN,cookieel.style.display
- DOMAIN,firefly.adobe.com
- DOMAIN,meta-ohttp-config-prod.fastly-edge.com
- DOMAIN,meta-ohttp-relay-prod.fastly-edge.com
- DOMAIN,production.museai.com
- DOMAIN,q-developer-integration.us-east-1.api.aws
- DOMAIN,us-central1-xi-labs.cloudfunctions.net
- DOMAIN-SUFFIX,abacus.ai
- DOMAIN-SUFFIX,abtestvm-sg.bytedance.com
- DOMAIN-SUFFIX,adobe.io
- DOMAIN-SUFFIX,ampworkers.com
- DOMAIN-SUFFIX,ant.dev
- DOMAIN-SUFFIX,antspace.dev
- DOMAIN-SUFFIX,apple-relay.fastly-edge.com
- DOMAIN-SUFFIX,artificialanalysis.ai
- DOMAIN-SUFFIX,atlassian.com
- DOMAIN-SUFFIX,atmeta.com
- DOMAIN-SUFFIX,aws.dev
- DOMAIN-SUFFIX,awsapps.com
- DOMAIN-SUFFIX,awsstatic.com
- DOMAIN-SUFFIX,awswaf.com
- DOMAIN-SUFFIX,base44.app
- DOMAIN-SUFFIX,base44.com
- DOMAIN-SUFFIX,blackbox.ai
- DOMAIN-SUFFIX,byteoversea.com
- DOMAIN-SUFFIX,chatbotclaude.com
- DOMAIN-SUFFIX,claicode.com
- DOMAIN-SUFFIX,cody.dev
- DOMAIN-SUFFIX,commandcode.ai
- DOMAIN-SUFFIX,composio.dev
- DOMAIN-SUFFIX,console.aws.a2z.com
- DOMAIN-SUFFIX,cue.im
- DOMAIN-SUFFIX,deepl.com
- DOMAIN-SUFFIX,deeplusercontent.com
- DOMAIN-SUFFIX,eigent.ai
- DOMAIN-SUFFIX,facebook.com
- DOMAIN-SUFFIX,fbcdn.net
- DOMAIN-SUFFIX,firefly.adobe.com
- DOMAIN-SUFFIX,freepik.com
- DOMAIN-SUFFIX,gemma.ai
- DOMAIN-SUFFIX,genspark.ai
- DOMAIN-SUFFIX,gspe1-ssl.ls.apple.com
- DOMAIN-SUFFIX,interaction.co
- DOMAIN-SUFFIX,interface.feedback
- DOMAIN-SUFFIX,jina.ai
- DOMAIN-SUFFIX,komo.ai
- DOMAIN-SUFFIX,lcicat.org
- DOMAIN-SUFFIX,lcicollections.org
- DOMAIN-SUFFIX,lepton.ai
- DOMAIN-SUFFIX,lf3-static.bytednsdoc.com
- DOMAIN-SUFFIX,linear.app
- DOMAIN-SUFFIX,link.com
- DOMAIN-SUFFIX,llamameta.net
- DOMAIN-SUFFIX,lmarena.ai
- DOMAIN-SUFFIX,mcpservertest.online
- DOMAIN-SUFFIX,metaaiusercontent.com
- DOMAIN-SUFFIX,metaaivm.com
- DOMAIN-SUFFIX,mindstudio.ai
- DOMAIN-SUFFIX,modelcontextprotocol.com
- DOMAIN-SUFFIX,modelcontextprotocol.io
- DOMAIN-SUFFIX,modelcontextprotocol.net
- DOMAIN-SUFFIX,modelcontextprotocol.org
- DOMAIN-SUFFIX,muse.ai
- DOMAIN-SUFFIX,muthos.com
- DOMAIN-SUFFIX,myclaw.ai
- DOMAIN-SUFFIX,notebook.google
- DOMAIN-SUFFIX,novita.ai
- DOMAIN-SUFFIX,poke.com
- DOMAIN-SUFFIX,prelude.dev
- DOMAIN-SUFFIX,px-cloud.net
- DOMAIN-SUFFIX,repl.co
- DOMAIN-SUFFIX,repl.it
- DOMAIN-SUFFIX,runway.com
- DOMAIN-SUFFIX,sf16-short-sg.bytedapm.com
- DOMAIN-SUFFIX,sillylittleguy.org
- DOMAIN-SUFFIX,simular.ai
- DOMAIN-SUFFIX,slack.com
- DOMAIN-SUFFIX,slashy.com
- DOMAIN-SUFFIX,starling.zijieapi.com
- DOMAIN-SUFFIX,stytch.com
- DOMAIN-SUFFIX,syntx.ai
- DOMAIN-SUFFIX,thinkingmachines.ai
- DOMAIN-SUFFIX,tron-sg.bytelemon.com
- DOMAIN-SUFFIX,typesafe.ai
- DOMAIN-SUFFIX,vellum.ai
- DOMAIN-SUFFIX,withpersona.com
- IP-ASN,401518
- IP-CIDR,129.146.3.78/32
- IP-CIDR,199.47.142.0/23
- IP-CIDR6,2604:f20::/32

## 已排除的非 AI 规则 (支付类黑名单)

共 33 条命中排除黑名单(PayPal 家族/通用支付 SaaS), 未纳入输出:

- DOMAIN-SUFFIX,stripe.com  <- 00_Ai.yaml
- DOMAIN,7h15.ru1353t.1s.m4d3.by.5ukk4w.skk.moe  <- 02_AIGC.yaml
- DOMAIN-SUFFIX,crixet.com  <- 03_AIGC.list
- DOMAIN-SUFFIX,pool.ntp.org  <- 03_AIGC.list
- IP-ASN,14061  <- 03_AIGC.list
- DOMAIN-SUFFIX,braintree-api.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,braintreegateway.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,braintreepayments.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,chargebee.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,checkout.com  <- 05_OverseasAI.list
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
- DOMAIN-SUFFIX,oystermercury.top  <- 14_AI_Rules.lsr
