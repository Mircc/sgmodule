::---------Theme store and Software Market-----------
::adb shell pm uninstall --user 0 com.heytap.themestore
::adb shell pm uninstall --user 0 com.heytap.market
::adb shell pm suspend com.heytap.themestore
::adb shell pm suspend com.heytap.market

::---------Recommend uninstalling-------------
adb shell pm uninstall --user 0 com.oplus.crashbox
adb shell pm uninstall --user 0 com.oplus.onetrace
adb shell pm uninstall --user 0 com.oplus.qualityprotect
adb shell pm uninstall --user 0 com.debug.loggerui
adb shell pm uninstall --user 0 com.oppo.instant.local.service
adb shell pm uninstall --user 0 com.daemon.shelper
adb shell pm uninstall --user 0 com.oplus.statistics.rom
adb shell pm uninstall --user 0 com.oplus.metis
adb shell pm uninstall --user 0 com.oplus.stdsp
adb shell pm uninstall --user 0 com.oplus.wifibackuprestore
adb shell pm uninstall --user 0 com.oplus.postmanservice
adb shell pm uninstall --user 0 com.oplus.cosa
adb shell pm uninstall --user 0 com.oplus.lfeh
adb shell pm uninstall --user 0 com.oplus.thirdkit
adb shell pm uninstall --user 0 com.oplus.obrain
adb shell pm uninstall --user 0 com.oplus.ovoicemanager
adb shell pm uninstall --user 0 com.coloros.activation
adb shell pm uninstall --user 0 com.coloros.findmyphone
adb shell pm uninstall --user 0 com.coloros.findphone.client2
adb shell pm uninstall --user 0 com.coloros.healthcheck
adb shell pm uninstall --user 0 com.coloros.phonemanager
adb shell pm uninstall --user 0 com.coloros.remoteguardservice
adb shell pm uninstall --user 0 com.coloros.securityguard
adb shell pm uninstall --user 0 com.coloros.sharescreen
adb shell pm uninstall --user 0 com.finshell.wallet
adb shell pm uninstall --user 0 com.heytap.cloud
adb shell pm uninstall --user 0 com.heytap.htms
adb shell pm uninstall --user 0 com.heytap.usercenter
adb shell pm uninstall --user 0 com.oplus.appdetail
adb shell pm uninstall --user 0 com.oplus.apprecover
adb shell pm uninstall --user 0 com.oplus.atlas
adb shell pm uninstall --user 0 com.oplus.logkit
adb shell pm uninstall --user 0 com.oplus.olc
adb shell pm uninstall --user 0 com.oplus.pay
adb shell pm uninstall --user 0 com.oplus.safecenter
adb shell pm uninstall --user 0 com.oplus.subsys
adb shell pm uninstall --user 0 com.opos.ads
adb shell pm uninstall com.coloros.personalassistant
adb shell pm disable-user com.android.nfc
adb shell am force-stop com.android.nfc

::---------Optional uninstalling-------------
adb shell pm uninstall --user 0 com.coloros.scenemode
adb shell pm uninstall --user 0 com.coloros.calendar
adb shell pm uninstall --user 0 com.coloros.filemanager
adb shell pm uninstall --user 0 com.coloros.operationManual
adb shell pm uninstall --user 0 com.coloros.assistantscreen
adb shell pm uninstall --user 0 com.coloros.childrenspace
adb shell pm uninstall --user 0 com.coloros.colordirectservice
adb shell pm uninstall --user 0 com.coloros.digitalwellbeing
adb shell pm uninstall --user 0 com.coloros.directui
adb shell pm uninstall --user 0 com.coloros.floatassistant
adb shell pm uninstall --user 0 com.coloros.focusmode
adb shell pm uninstall --user 0 com.coloros.ocrscanner
adb shell pm uninstall --user 0 com.coloros.ocrservice
adb shell pm uninstall --user 0 com.coloros.securepay
adb shell pm uninstall --user 0 com.coloros.smartdrive
adb shell pm uninstall --user 0 com.coloros.smartsidebar
adb shell pm uninstall --user 0 com.coloros.systemclone
adb shell pm uninstall --user 0 com.heytap.accessory
adb shell pm uninstall --user 0 com.heytap.browser
adb shell pm uninstall --user 0 com.heytap.music
adb shell pm uninstall --user 0 com.heytap.pictorial
adb shell pm uninstall --user 0 com.heytap.quicksearchbox
adb shell pm uninstall --user 0 com.heytap.speechassist
adb shell pm uninstall --user 0 com.heytap.yoli
adb shell pm uninstall --user 0 com.oplus.encryption
adb shell pm uninstall --user 0 com.oplus.gesture
adb shell pm uninstall --user 0 com.realme.wellbeing
adb shell pm uninstall --user 0 com.tencent.soter.soterserver

::-----------Optional uninstalling-------------
::adb shell pm uninstall --user 0 com.heytap.openid
::adb shell pm uninstall --user 0 com.coloros.sceneservice
::adb shell pm uninstall --user 0 com.nearme.instant.platform
::adb shell pm uninstall --user 0 com.oplus.healthservice
::adb shell pm uninstall --user 0 com.oplus.multiapp
::adb shell pm uninstall --user 0 com.oplus.ota
::adb shell pm uninstall --user 0 com.oplus.sos
::adb shell pm uninstall --user 0 com.coloros.translate.engine
::adb shell pm uninstall --user 0 com.coloros.accessibilityassistant

::-----------Recover some app-------------
adb shell pm install-existing com.heytap.colorfulengine
adb shell pm install-existing com.coloros.smartlock
adb shell pm install-existing com.oplus.nhs
adb shell pm install-existing com.oplus.powermonitor
adb shell pm install-existing com.oplus.customize.coreapp
adb shell pm install-existing com.oplus.uiengine
adb shell pm install-existing com.coloros.ocs.opencapabilityservice
adb shell pm install-existing com.oplus.exserviceui
adb shell pm install-existing com.amap.android.location
adb shell pm install-existing com.oplus.romupdate


pause