# AIGC 规则合并报告 - 2026-08-29

- 保留规则: **438** 条
- 去重删除: **104** 条
- 输出: `Cl_Ai.yaml` (Clash) / `Sg_Ai.list` (Surge) / `Ai_qx.list` (QuantumultX 原生, 其中跳过 1 条 QX 不支持的规则类型)
- mrs: `Cl_Ai_domain.mrs` (416 条域名规则) + `Cl_Ai_ipcidr.mrs` (5 条 IP 规则); 另有 17 条 (DOMAIN-KEYWORD/REGEX/IP-ASN/GEOIP) mrs 不支持, 仅在 yaml/list 中生效

## 来源文件统计

| 来源 | 贡献规则数 |
| --- | --- |
| Cl_Ai.yaml | 438 |

## 去重明细

| 被删除规则 | 原因 |
| --- | --- |
| DOMAIN,aida.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,aisandbox-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,aistudio.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,alkalicore-pa.clients6.google.com | 被 DOMAIN-SUFFIX,clients6.google.com 覆盖 |
| DOMAIN,alkalimakersuite-pa.clients6.google.com | 被 DOMAIN-SUFFIX,clients6.google.com 覆盖 |
| DOMAIN,anthropic.auth0.com | 被 DOMAIN-SUFFIX,auth0.com 覆盖 |
| DOMAIN,antigravity-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,antigravity.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,api.apple-cloudkit.com | 被 DOMAIN-SUFFIX,apple-cloudkit.com 覆盖 |
| DOMAIN,api.cloudflare.com | 被 DOMAIN-SUFFIX,cloudflare.com 覆盖 |
| DOMAIN,api.githubcopilot.com | 被 DOMAIN-SUFFIX,githubcopilot.com 覆盖 |
| DOMAIN,api.groq.com | 被 DOMAIN-SUFFIX,groq.com 覆盖 |
| DOMAIN,api.jetbrains.ai | 被 DOMAIN-SUFFIX,jetbrains.ai 覆盖 |
| DOMAIN,api.statsig.com | 被 DOMAIN-SUFFIX,statsig.com 覆盖 |
| DOMAIN,auth.grazie.ai | 被 DOMAIN-SUFFIX,grazie.ai 覆盖 |
| DOMAIN,aws-language-servers.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,aws-toolkit-language-servers.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,bard.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,chat.openai.com.cdn.cloudflare.net | 被 DOMAIN-SUFFIX,openai.com.cdn.cloudflare.net 覆盖 |
| DOMAIN,client-telemetry.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,cloudaicompanion.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,cloudcode-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,codewhisperer.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,console.groq.com | 被 DOMAIN-SUFFIX,groq.com 覆盖 |
| DOMAIN,daily-cloudcode-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,desktop-release.codewhisperer.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,gateway.ai.cloudflare.com | 被 DOMAIN-SUFFIX,cloudflare.com 覆盖 |
| DOMAIN,gemini.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,generativelanguage.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,idetoolkits-hostedfiles.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,integrate.api.nvidia.com | 被 DOMAIN-SUFFIX,api.nvidia.com 覆盖 |
| DOMAIN,jules.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,makersuite.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,notebooklm-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,notebooklm.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN,notebooklm.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,openai-api.arkoselabs.com | 被 DOMAIN-SUFFIX,arkoselabs.com 覆盖 |
| DOMAIN,openaiapi-site.azureedge.net | 被 DOMAIN-SUFFIX,azureedge.net 覆盖 |
| DOMAIN,openaicom.imgix.net | 被 DOMAIN-SUFFIX,imgix.net 覆盖 |
| DOMAIN,ppl-ai-file-upload.s3.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,production-openaicom-storage.azureedge.net | 被 DOMAIN-SUFFIX,azureedge.net 覆盖 |
| DOMAIN,q.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,robinfrontend-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN,services.bingapis.com | 被 DOMAIN-SUFFIX,bingapis.com 覆盖 |
| DOMAIN,specs.q.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,static.cloudflareinsights.com | 被 DOMAIN-SUFFIX,cloudflareinsights.com 覆盖 |
| DOMAIN,telemetry.aws-language-servers.us-east-1.amazonaws.com | 被 DOMAIN-SUFFIX,amazonaws.com 覆盖 |
| DOMAIN,webchannel-alkalimakersuite-pa.clients6.google.com | 被 DOMAIN-SUFFIX,clients6.google.com 覆盖 |
| DOMAIN-SUFFIX,aicode.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,aida.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,aiplatform.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,aisandbox-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,aistudio.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,alkalimakersuite-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,android.chat.openai.com | 被 DOMAIN-SUFFIX,chat.openai.com 覆盖 |
| DOMAIN-SUFFIX,api.statsig.com | 被 DOMAIN-SUFFIX,statsig.com 覆盖 |
| DOMAIN-SUFFIX,apis.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,app.launchdarkly.com | 被 DOMAIN-SUFFIX,launchdarkly.com 覆盖 |
| DOMAIN-SUFFIX,auth.openai.com | 被 DOMAIN-SUFFIX,openai.com 覆盖 |
| DOMAIN-SUFFIX,auth0.openai.com | 被 DOMAIN-SUFFIX,openai.com 覆盖 |
| DOMAIN-SUFFIX,bard.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,business.gemini.google | 被 DOMAIN-SUFFIX,gemini.google 覆盖 |
| DOMAIN-SUFFIX,cdn.workos.com | 被 DOMAIN-SUFFIX,workos.com 覆盖 |
| DOMAIN-SUFFIX,challenges.cloudflare.com | 被 DOMAIN-SUFFIX,cloudflare.com 覆盖 |
| DOMAIN-SUFFIX,chat.openai.com | 被 DOMAIN-SUFFIX,openai.com 覆盖 |
| DOMAIN-SUFFIX,chatgpt.livekit.cloud | 被 DOMAIN-SUFFIX,livekit.cloud 覆盖 |
| DOMAIN-SUFFIX,client-api.arkoselabs.com | 被 DOMAIN-SUFFIX,arkoselabs.com 覆盖 |
| DOMAIN-SUFFIX,clients4.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,clients6.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,clientstream.launchdarkly.com | 被 DOMAIN-SUFFIX,launchdarkly.com 覆盖 |
| DOMAIN-SUFFIX,cloudcode-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,colab.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,colab.research.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,desktop.chat.openai.com | 被 DOMAIN-SUFFIX,chat.openai.com 覆盖 |
| DOMAIN-SUFFIX,developerprofiles.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,events.launchdarkly.com | 被 DOMAIN-SUFFIX,launchdarkly.com 覆盖 |
| DOMAIN-SUFFIX,events.statsigapi.net | 被 DOMAIN-SUFFIX,statsigapi.net 覆盖 |
| DOMAIN-SUFFIX,firebaseinstallations.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,forwarder.workos.com | 被 DOMAIN-SUFFIX,workos.com 覆盖 |
| DOMAIN-SUFFIX,gateway.ai.cloudflare.com | 被 DOMAIN-SUFFIX,cloudflare.com 覆盖 |
| DOMAIN-SUFFIX,geller-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,gemini.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,generativelanguage.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,host.livekit.cloud | 被 DOMAIN-SUFFIX,livekit.cloud 覆盖 |
| DOMAIN-SUFFIX,ios.chat.openai.com | 被 DOMAIN-SUFFIX,chat.openai.com 覆盖 |
| DOMAIN-SUFFIX,js.intercomcdn.com | 被 DOMAIN-SUFFIX,intercomcdn.com 覆盖 |
| DOMAIN-SUFFIX,jules.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,labs.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,makersuite.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,notebook.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,notebooklm.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,o207216.ingest.sentry.io | 被 DOMAIN-SUFFIX,sentry.io 覆盖 |
| DOMAIN-SUFFIX,o33249.ingest.sentry.io | 被 DOMAIN-SUFFIX,sentry.io 覆盖 |
| DOMAIN-SUFFIX,opal.google.com | 被 DOMAIN-SUFFIX,google.com 覆盖 |
| DOMAIN-SUFFIX,openaiapi-site.azureedge.net | 被 DOMAIN-SUFFIX,azureedge.net 覆盖 |
| DOMAIN-SUFFIX,openaicom.imgix.net | 被 DOMAIN-SUFFIX,imgix.net 覆盖 |
| DOMAIN-SUFFIX,proactivebackend-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,robinfrontend-pa.googleapis.com | 被 DOMAIN-SUFFIX,googleapis.com 覆盖 |
| DOMAIN-SUFFIX,setup.auth.openai.com | 被 DOMAIN-SUFFIX,auth.openai.com 覆盖 |
| DOMAIN-SUFFIX,setup.workos.com | 被 DOMAIN-SUFFIX,workos.com 覆盖 |
| DOMAIN-SUFFIX,tcr9i.chat.openai.com | 被 DOMAIN-SUFFIX,chat.openai.com 覆盖 |
| DOMAIN-SUFFIX,turn.livekit.cloud | 被 DOMAIN-SUFFIX,livekit.cloud 覆盖 |
| DOMAIN-SUFFIX,windsurf-telemetry.codeium.com | 被 DOMAIN-SUFFIX,codeium.com 覆盖 |
| DOMAIN-SUFFIX,workos.imgix.net | 被 DOMAIN-SUFFIX,imgix.net 覆盖 |

## 未能自动归类 (Others)

以下规则需人工归入厂商类别:
- IP-CIDR,129.146.3.78/32

## 已排除的非 AI 规则 (支付类黑名单)

共 270 条命中排除黑名单(PayPal 家族/通用支付 SaaS), 未纳入输出:

- DOMAIN-SUFFIX,stripe.com  <- 00_Ai.yaml
- DOMAIN,7h15.ru1353t.1s.m4d3.by.5ukk4w.skk.moe  <- 02_AIGC.yaml
- DOMAIN-SUFFIX,js.stripe.com  <- 03_AIGC.list
- DOMAIN-SUFFIX,pool.ntp.org  <- 03_AIGC.list
- DOMAIN-SUFFIX,account-paypal.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,account-paypal.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,account-paypal.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,accountpaypal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,accountpaypal.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,accountpaypal.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,anfutong.cn  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,anfutong.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,anfutong.com.cn  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,beibao.cn  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,beibao.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,beibao.com.cn  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,bill-safe.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,billmelater.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,billmelater.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,billmelater.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,bml.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,braintreegateway.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,braintreegateway.tv  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,braintreepayments.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,braintreepayments.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,braintreepayments.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,braintreepayments.tv  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,braintreepaymentsolutions.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,braintreeps.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,briantreepayments.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,briantreepayments.tv  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,buyfast-paysmart.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,card.io  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,cash2.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,cashify.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,cashify.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,chargebee.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,checkout.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,crixet.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,devtools-paypal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,experiencebillmelater.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,fastspring.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,filipino-music.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,fundpaypal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,getbraintree.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,gmoney.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,i-o-u.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,id.me  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,krakenjs.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,lemonsqueezy.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,loanbuilder.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,login-paypal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,login-paypal.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,mywaytopay.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,mywaytopay.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,pa9pal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paaypal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paddle.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paily.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paily.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paipal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,pavpal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paydiant.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paylike.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypa1.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypa1.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypaal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-activate.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-activate.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-activate.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-apac.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-apps.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-biz.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-brandcentral.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-business.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-business.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-business.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-cardcash.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-cash.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-center.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-center.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-center.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-center.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-communication.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-communications.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-communications.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-community.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-community.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-comunidad.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-corp.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-database.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-database.us  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-donations.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-dynamic.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-engineering.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-europe.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-excelinvoicing.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-exchanges.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-forward.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-galactic.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-gift.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-gifts.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-gpplus.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-here.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-hrsystem.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-innovationlab.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-integration.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-japan.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-knowledge.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-labs.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-latam.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-learning.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-login.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-login.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-login.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-login.us  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-luxury.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-mainstreet.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-marketing.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-media.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-merchantloyalty.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-mktg.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-mobilemoney.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-network.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-notice.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-notify.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-online.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-online.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-online.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-optimizer.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-pages.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-photocard.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-plaza.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-portal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-prepagata.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-prepagata.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-prepaid.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-profile.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-proserv.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-qrshopping.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-recargacelular.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-redeem.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-referral.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-retail.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-scoop.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-search.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-secure.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-secure.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-security.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-security.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-service.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-signin.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-signin.us  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-special.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-specialoffers.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-sptam.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-status.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-support.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-survey.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-survey.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-team.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal-viewpoints.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.ca  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.com.cn  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.com.hk  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.com.sg  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.hk  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.jp  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.me  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.net.cn  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.org.cn  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.so  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypal.us  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalbeacon.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalbenefits.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalbrasil.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalcommunity.cn  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalcommunity.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalcommunity.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalcommunity.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalcorp.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalcredit.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalcreditcard.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalgivingfund.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalhere.cn  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalhere.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalhere.com.cn  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalhere.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalhere.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalhere.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalhere.tv  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypali.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalinc.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalindia.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalinsuranceservices.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypall.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypallabs.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalme.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalnet.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalnet.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalnetwork.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalnetwork.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalnetwork.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalobjects.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalonline.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalonline.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalprepagata.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalprepagata.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalservice.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalshopping.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalshopping.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalsurvey.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypalx.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,paypaly.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,payppal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,payypal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,pdncommunity.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,pp-soc.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,ppaypal.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,pppds.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,pypl.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,pypl.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,pypl.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,pypl.tv  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,qpoe.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,s-xoom.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,secure-paypal.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,securepaypal.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,sheerid.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,simility.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,sslpaypal.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,swiftbank.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,swiftbank.us  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,swiftcapital.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,swiftfinancial.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,swiftfinancial.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,swiftfinancial.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,thepaypalshop.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,theshoppingexpresslane.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,venmo-touch.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,venmo.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,venmo.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,venmo.net  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,venmo.org  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,venmo.s3.amazonaws.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,webmoneyinfo.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,wiremoneytoirelandwithxoomeasierandcheaper.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,www-paypal.info  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,www-paypal.us  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,wwwxoom.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,xn--bnq297cix3a.cn  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,xoom-experience.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,xoom.com  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,xoom.io  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,xoom.net.cn  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,xoom.us  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,xoomcom.com  <- 05_OverseasAI.list
- DOMAIN-KEYWORD,paypal  <- 05_OverseasAI.list
- DOMAIN-KEYWORD,stripe  <- 05_OverseasAI.list
- IP-ASN,14061  <- 05_OverseasAI.list
- DOMAIN-SUFFIX,oystermercury.top  <- 14_AI_Rules.lsr
