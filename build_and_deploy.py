#!/usr/bin/env python3
"""Build EnglishGo 5-language showcase, /privacy, and /support pages, bundle Cloudflare Worker, and deploy to https://englishgo.appengine.fun."""
from __future__ import annotations

import base64
import html as html_mod
import json
import os
import sys
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
IMG_DIR = PUBLIC_DIR / "images"
AUD_DIR = PUBLIC_DIR / "audio"

ACCOUNT_ID = "9fb3b494e6d4d659f2cf567efb94fc38"
ZONE_ID = "977b0b4fa0ab6e587b8758a04016c5e8"
SCRIPT_NAME = "englishgo-site"
HOSTNAME = "englishgo.appengine.fun"
ORIGIN = f"https://{HOSTNAME}"
APP_STORE_ID = os.environ.get("ENGLISHGO_APP_STORE_ID", "").strip()
APP_STORE_URL = f"https://apps.apple.com/app/id{APP_STORE_ID}" if APP_STORE_ID else ""

CONTENT = {
    "en": {
        "html_lang": "en",
        "title": "EnglishGo — Travel English, 44 US/UK IPA Phonemes, 100 Video Dialogues & Live Translation",
        "desc": "Master real-life travel English with 15 lessons, 44 US/UK IPA phonemes, 24 minimal pairs, 100 real-life travel video dialogues, an on-device Voice Coach, and Live Two-Way Voice Translation.",
        "keywords": "EnglishGo,travel English,IPA pronunciation,minimal pairs,voice roleplay,live voice translation,English travel dialogues,learn English,AE Interactive",
        "nav_privacy": "Privacy",
        "nav_support": "Support",
        "nav_download": "Get App",
        "hero_badge": "15 LESSONS · 44 IPA · 100 TRAVEL VIDEO DIALOGUES · LIVE TRANSLATION",
        "hero_title": "Speak Clear English <span>Before Your Flight Lands</span>",
        "hero_sub": "From 44 US/UK IPA phonemes and 24 minimal pair challenges (ship/sheep, light/right) to 100 real-life travel video dialogues, 12-scene Voice Coach roleplay, and live two-way translation—zero accounts, zero ads.",
        "status_pill": "TestFlight & App Store Ready · iPhone, iPad & iPhone Duo",
        "cta_store_sub": "Available Soon on",
        "cta_store_main": "App Store",
        "cta_audio": "▶ Hear Native Phrases",
        "cta_screens": "Explore Screens ↓",
        "sec_audio_badge": "REAL IN-APP STUDIO AUDIO · US IPA PHONETIC BREAKDOWN",
        "sec_audio_title": "Hear Everyday Travel English Clearly",
        "sec_audio_sub": "Actual studio MP3 clips bundled inside EnglishGo—paired with crisp US IPA transcription and natural travel grammar tips.",
        "btn_play": "Play",
        "btn_playing": "Playing",
        "sec_screens_badge": "LIVE APP PREVIEWS · IPHONE & IPHONE DUO",
        "sec_screens_title": "Designed for One-Handed Travel Confidence",
        "sec_screens_sub": "Clean portrait typography sized for readability at airport gates and cafés, plus native iPhone Duo foldable and iPad 13\" support.",
        "screens_labels": [
            "15-Lesson Path",
            "12-Scene Voice Tutor",
            "Live Voice Translation",
            "100 Video Dialogues",
            "44 US/UK IPA & Pairs",
            "iPhone Duo Inner Display",
        ],
        "sec_features_badge": "FIVE INTEGRATED MODULES",
        "sec_features_title": "Everything You Need in One Offline-Ready App",
        "features": [
            ("📚", "15 Guided Lessons & 18 Grammar Drills", "Progress smoothly from vowels, r-colored vowels, diphthongs, and tricky consonants (th, l/r, v/w) through café orders, dining, customs, hotels, and clinics."),
            ("🔊", "44 US/UK IPA Lab & 24 Minimal Pairs", "Switch between US and UK IPA charts with clear tongue/mouth placement guides and blind listening drills (ship/sheep, light/right, three/free)."),
            ("🎬", "100 Real-Life Travel Video Dialogues", "Five real travel stages with 200 native studio recordings, synced bilingual subtitles, IPA notation, and practical cultural highlights."),
            ("💬", "12-Scene Guided Voice Tutor & Live Interpreter", "On-device roleplay keeps helpful cue cards on screen while you speak across 3 practical rounds; instant two-way translation covers 繁中 / 简中 / ES / 日本語 ↔ English."),
            ("✍️", "160 SRS Flashcards & 320 Audio Clips", "SM-2 spaced repetition deck, 4 listening and reading test modes, plus Standard / Large / Extra Large accessibility font scaling."),
            ("🔒", "Zero Sign-In · Local Privacy Only", "No accounts, no ads, and zero third-party SDKs. Study progress stays strictly inside iOS UserDefaults on your device."),
        ],
        "sec_pricing_badge": "NO SUBSCRIPTIONS · START FREE",
        "sec_pricing_title": "Free Essentials. One-Time $3.99 Upgrade.",
        "sec_pricing_sub": "Practice 44 IPA phonemes and core travel English free—then unlock everything forever with a single App Store buyout.",
        "free_tier_title": "Free Forever",
        "free_tier_price": "$0",
        "free_tier_items": [
            "Complete 44 US/UK IPA chart & 24 minimal pair blind quizzes",
            "Full 160 SRS flashcards (320 MP3s) & 18 grammar drills",
            "Lessons 1–3 + 10 travel video dialogues (2 per category)",
            "Daily free Voice Tutor (5/day) & Live Interpreter (8/day)",
        ],
        "pro_tier_badge": "ONE-TIME BUYOUT · NO SUBSCRIPTION",
        "pro_tier_title": "EnglishGo Pro Lifetime",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "All 15 guided travel lessons (Lessons 4–15 unlocked)",
            "All 100 real-life travel videos & 200 studio recordings",
            "Unlimited 12-scene Voice Tutor roleplay practice",
            "Unlimited two-way Live Voice Interpreter (offline-ready)",
        ],
        "bottom_cta_title": "Ready for Your Next Trip Abroad?",
        "bottom_cta_sub": "Free to try on iPhone, iPad & iPhone Duo—no sign-up required.",
        "appstore_btn_label": "View TestFlight & Support",
        "privacy_title": "Privacy Policy — EnglishGo",
        "privacy_updated": "Last Updated: November 23, 2026",
        "privacy_sections": [
            ("1. Zero Account & Zero Personal Data Collection", "EnglishGo is developed by AE Interactive (AppEngine Interactive). We do not require account registration and never collect, store, sell, or transmit personal data to AE Interactive servers (App Store Connect Privacy Label: Data Not Collected / NSPrivacyTracking = false). Study progress, phoneme mastery, flashcard SRS schedules, streaks, and font sizes stay locally on your device via Apple UserDefaults (Required Reason API CA92.1)."),
            ("2. Microphone, Speech Recognition & On-Device Processing", "Microphone and speech recognition permissions are requested strictly on demand when you tap Record in Voice Tutor or Live Interpreter. Transcription, translation, and guided roleplay run via Apple's native Speech, Translation, and on-device system language frameworks so conversations never pass through AE Interactive servers."),
            ("3. No Ads, No Analytics, No Tracking", "EnglishGo bundles zero advertising networks, zero third-party telemetry SDKs, and zero cross-app tracking."),
            ("4. Contact Us", "Questions? Reach AE Interactive anytime at help@appengine.fun."),
        ],
        "support_title": "Support & Compatibility — EnglishGo",
        "support_sub": "Quick help for On-Device Voice Tutor, Offline Translation Packs, TestFlight, and App Support.",
        "support_cards": [
            ("Voice Tutor Roleplay Compatibility", "Runs cleanly via Apple's native system speech recognition & on-device language architecture across iPhone and iPad (iOS / iPadOS 17.0+, enhanced system voice & offline packs on iOS 18+ / 26+)."),
            ("Offline Courses, 44 IPA & 100 Video Dialogues", "All 15 units, 44 US/UK IPA guides, 24 minimal pair challenges, 100 real-life travel videos (200 MP3s), 160 flashcards (320 MP3s), and 18 grammar drills are bundled offline inside the app with zero login required."),
            ("Live Two-Way Translation Offline Packs", "Uses Apple's native Translation framework between Traditional Chinese, Simplified Chinese, Spanish, Japanese and English. Download language packs once in iOS Settings -> Apps -> Translate for reliable offline use while flying."),
            ("Direct Support & TestFlight", "Email AE Interactive at help@appengine.fun — we typically reply within 24 hours."),
        ],
        "footer_rights": "© 2026 AE Interactive. All rights reserved.",
        "studio_link_label": "AE Interactive Studio",
    },
    "zh-Hant": {
        "html_lang": "zh-Hant",
        "title": "EnglishGo — 旅遊英語、44 美英音標、100 個實境對話影片與雙向語音翻譯",
        "desc": "從 44 個 US/UK 音標與 24 組易混辨音、100 個旅遊實境對話影片，到 12 情境口說模擬與四語 ↔ English 雙向即時語音翻譯，免登入零追蹤。",
        "keywords": "EnglishGo,英語學習,旅遊英文,國際音標,美式發音,英式音標,易混辨音,雙向語音翻譯,英文對話練習,AE Interactive",
        "nav_privacy": "隱私權政策",
        "nav_support": "支援與常見問題",
        "nav_download": "立即體驗",
        "hero_badge": "15 堂課 · 44 US/UK 音標 · 100 個實境對話影片 · 雙向即時語音翻譯",
        "hero_title": "出國落地前，<span>先開口說出清楚自信的英語</span>",
        "hero_sub": "從 44 音標、24 組易混辨音（ship / sheep、light / right）與 100 個實境對話影片預習，銜接 12 情境店員開口模擬與現場雙向語音口譯——免註冊、零廣告、本機隱私優先。",
        "status_pill": "TestFlight 測試中 · 即將於 App Store 推出 · iPhone / iPad / iPhone Duo",
        "cta_store_sub": "即將上架 / 支援說明",
        "cta_store_main": "App Store",
        "cta_audio": "▶ 試聽錄音室發音",
        "cta_screens": "瀏覽實機畫面 ↓",
        "sec_audio_badge": "收錄真實 App 錄音室語音 · 美式 IPA 音標標註",
        "sec_audio_title": "點一下，立即試聽地道旅遊英語",
        "sec_audio_sub": "直接試聽 EnglishGo 內建 320 句單字實戰音檔之一——附上清楚美式 IPA 音標與連音解析。",
        "btn_play": "播放",
        "btn_playing": "播放中",
        "sec_screens_badge": "實機畫面精選 · IPHONE 與 IPHONE DUO 雙螢幕",
        "sec_screens_title": "單手直式大字體，機場排隊一眼看懂",
        "sec_screens_sub": "專為旅行單手操作設計，支援標準／大字／特大三段字級與 iPhone Duo 摺疊內外雙螢幕及 iPad 13 吋。",
        "screens_labels": [
            "15 堂實戰學習路徑",
            "12 情境互動口說練習",
            "現場雙向即時口譯",
            "100 個旅遊實境對話",
            "44 音標與 24 組辨音",
            "iPhone Duo 展開內螢幕",
        ],
        "sec_features_badge": "五大核心模組",
        "sec_features_title": "從音標打底到出國救急，一套就夠",
        "features": [
            ("📚", "15 堂實戰課程＋18 堂文法句型", "從短母音、長母音、捲舌 r 與咬舌 th、l/r、v/w 起步，銜接咖啡廳點餐、餐廳過敏小費、海關入住與藥局看診。"),
            ("🔊", "44 US/UK 音標實驗室＋24 組辨音", "支援美英音標雙系統切換、詳細舌位嘴型提示，以及盲聽辨音挑戰（ship / sheep、three / free、rice / lice）。"),
            ("🎬", "100 個旅遊實境對話影片（200 句錄音）", "依真實旅行時間線編排五大場景，支援雙語台詞逐句聽音、音標對照與文化小叮嚀。"),
            ("💬", "12 情境口說模擬＋雙向即時口譯", "店員主動開口發問、畫面保留參考提示陪你過關；底部最右鍵一按直達繁中／簡中／西／日 ↔ 英語即時口譯與大字卡。"),
            ("✍️", "160 張 SRS 單字卡＋320 句原生錄音", "間隔重複（SM-2）單字卡搭配 4 合一聽讀測驗，支援三段放大字體。"),
            ("🔒", "免登入註冊・100% 本機隱私", "無廣告、無第三方追蹤碼（NSPrivacyTracking = false），所有學習進度僅保存在您裝置本機 UserDefaults。"),
        ],
        "sec_pricing_badge": "無月費訂閱制 · 免費下載先體驗",
        "sec_pricing_title": "基礎永久免費 · $3.99 一次買斷解鎖",
        "sec_pricing_sub": "完整 44 音標與 160 單字卡永久免費練到會，需要全 100 支影片與無限口譯時再單次升級即可。",
        "free_tier_title": "永久免費版",
        "free_tier_price": "免費 $0",
        "free_tier_items": [
            "完整 44 US/UK 音標表 ＋ 24 組易混辨音挑戰",
            "完整 160 張單字卡（320 句發音）與 18 堂文法測驗",
            "第 1–3 課單元 ＋ 五大實境各 2 支（共 10 支）影片",
            "每日免費口說互動練習（5 次/日）與即時口譯（8 次/日）",
        ],
        "pro_tier_badge": "一次買斷 · 終身無訂閱扣款",
        "pro_tier_title": "EnglishGo Pro 終身完整版",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "永久解鎖全 15 堂實戰旅遊英語課程（含第 4–15 課）",
            "解鎖全 100 部實境旅遊對話影片與 200 句原生錄音",
            "12 大實境情境店員口說模擬不限次數練習",
            "即時雙向語音口譯無限次使用（支援離線翻譯包）",
        ],
        "bottom_cta_title": "下一趟出國自由行，帶這套就夠了",
        "bottom_cta_sub": "無需註冊帳號、打開就能練發音、預習對話與現場口譯。",
        "appstore_btn_label": "查看 TestFlight 與支援說明",
        "privacy_title": "EnglishGo 隱私權政策",
        "privacy_updated": "最後更新日期：2026 年 11 月 23 日",
        "privacy_sections": [
            ("1. 無帳號登入與不收集個人資料", "EnglishGo 由 AE Interactive（AppEngine Interactive）開發。本 App 免註冊帳號，不會收集、儲存、出售或傳輸任何個人識別資料至開發者伺服器（App Store Connect 聲明「不收集任何資料」，NSPrivacyTracking = false）。學習進度、單字複習與字級設定皆透過 Apple UserDefaults（Required Reason API CA92.1）僅保存於手機本機。"),
            ("2. 麥克風、語音辨識與本機處理", "僅在您主動按下口說練習或即時雙向口譯的麥克風按鈕時才會錄音；語音辨識、翻譯與對話引導均優先呼叫 Apple 系統原生 Speech、Translation 與裝置端語言框架執行，錄音與對話絕不上傳至開發者或廣告伺服器。"),
            ("3. 零廣告與零第三方追蹤", "本 App 不包含任何廣告聯播網、第三方分析 SDK 或跨 App 追蹤。"),
            ("4. 聯絡我們", "如有隱私權或 App 相關疑問，請來信至 help@appengine.fun。"),
        ],
        "support_title": "支援服務與常見問題 — EnglishGo",
        "support_sub": "語音辨識權限、離線翻譯包下載、TestFlight 測試與技術客服。",
        "support_cards": [
            ("互動口說練習與系統語音", "全面支援 iPhone / iPad（iOS 17.0+）；於「設定 → 輔助使用 → 語音內容 → 英文」下載強化語音後，朗讀更自然流暢。"),
            ("全部課程、44 音標與 100 支影片完全離線可用", "15 堂課程、44 個 US/UK 音標、24 組易混辨音、100 個實境對話影片（200 句錄音）、160 單字卡（320 句錄音）與 18 堂文法皆完整收錄於 App 內，搭機離線也能學。"),
            ("出發前下載離線雙向翻譯包", "「即時雙向語音口譯」使用 Apple 原生 Translation 框架；建議出發前於系統「設定 → App → 翻譯」預載英語與中文／日語／西語離線包。"),
            ("聯絡客服團隊", "若有任何建議或 TestFlight 回報，歡迎寄信至 help@appengine.fun（通常 24 小時內回覆）。"),
        ],
        "footer_rights": "© 2026 AE Interactive. 保留所有權利。",
        "studio_link_label": "AE Interactive 工作室",
    },
    "zh-Hans": {
        "html_lang": "zh-Hans",
        "title": "EnglishGo — 旅游英语、44 美英音标、100 个实景对话视频与双向语音翻译",
        "desc": "从 44 个美英音标与 24 组易混辨音、100 个旅游实景对话视频，到 12 情景口语模拟与四语 ↔ English 双向实时语音翻译，免登录零追踪。",
        "keywords": "EnglishGo,英语学习,旅游英语,国际音标,美式发音,易混辨音,双向语音翻译,英语会话练习,AE Interactive",
        "nav_privacy": "隐私政策",
        "nav_support": "支持与常见问题",
        "nav_download": "立即体验",
        "hero_badge": "15 节课 · 44 美英音标 · 100 个实景对话视频 · 双向实时语音翻译",
        "hero_title": "出国落地前，<span>先开口说出清晰自信的英语</span>",
        "hero_sub": "从 44 音标、24 组易混辨音（ship / sheep、light / right）与 100 个实景对话视频预习，衔接 12 情景店员开口模拟与现场双向语音口译——免注册、无广告、本地隐私优先。",
        "status_pill": "TestFlight 测试中 · 即将上线 App Store · iPhone / iPad / iPhone Duo",
        "cta_store_sub": "即将上线 / 支持说明",
        "cta_store_main": "App Store",
        "cta_audio": "▶ 试听录音室发音",
        "cta_screens": "查看实机截图 ↓",
        "sec_audio_badge": "内置录音室真人发音 · 美式 IPA 音标标注",
        "sec_audio_title": "点击试听地道旅游英语常用句",
        "sec_audio_sub": "直接试听 EnglishGo 应用内打包的高频词卡音频——配清晰美式 IPA 音标与实用语法小贴士。",
        "btn_play": "播放",
        "btn_playing": "播放中",
        "sec_screens_badge": "实机界面展示 · IPHONE 与 IPHONE DUO 折叠双屏",
        "sec_screens_title": "单手竖屏大字体，机场排队一眼看清",
        "sec_screens_sub": "专为出境自由行单手操作打造，支持标准／大号／特大三档字号调节，全面适配 iPhone Duo 折叠双屏与 iPad 13 英寸。",
        "screens_labels": [
            "15 节实战路线",
            "12 情景互动口语练习",
            "现场双向实时口译",
            "100 个旅游实景对话",
            "44 音标与 24 组辨音",
            "iPhone Duo 展开内屏",
        ],
        "sec_features_badge": "五大核心模块",
        "sec_features_title": "从音标打底到出国应急，一站全搞定",
        "features": [
            ("📚", "15 节实战路线 + 18 节语法特训", "从短元音、长元音、卷舌 r 与咬舌 th、l/r、v/w 起步，覆盖咖啡厅点单、餐厅小费、海关入住与药店购药。"),
            ("🔊", "44 美英音标实验室 + 24 组辨音", "支持 US / UK 音标切换、口型舌位图解与盲听辨音挑战（ship / sheep、three / free、rice / lice）。"),
            ("🎬", "100 个旅游实景对话视频（200 句音频）", "按真实出行阶段编排五大分类，支持双语字幕逐句点听、音标对照与文化提示。"),
            ("💬", "12 情景口语模拟 + 双向实时口译", "店员主动开口发问并全程保留提示卡片；底部最右栏一键直达四语 ↔ 英语双向实时口译与大字全屏展示。"),
            ("✍️", "160 张 SRS 单词卡 + 320 句原生音频", "间隔重复（SM-2）单词记忆卡配合四合一听读测验，支持三档大字号切换。"),
            ("🔒", "免账号登录 · 100% 本地隐私", "零广告、零第三方追踪代码（NSPrivacyTracking = false），学习进度仅保存于设备本地 UserDefaults。"),
        ],
        "sec_pricing_badge": "无月费订阅制 · 免费体验后按需买断",
        "sec_pricing_title": "基础永久免费 · $3.99 一次买断解锁",
        "sec_pricing_sub": "完整 44 音标与 160 词卡永久免费练，需要全 100 部实景视频与无限口译时再单次买断即可。",
        "free_tier_title": "永久免费版",
        "free_tier_price": "免费 $0",
        "free_tier_items": [
            "完整 44 美英音标表 ＋ 24 组易混辨音挑战",
            "完整 160 单词记忆卡（320 句音频）与 18 节语法",
            "第 1–3 课入门单元 ＋ 五大情景各 2 支（共 10 支）短片",
            "每日免费互动口语（5 次/天）与双向实时口译（8 次/天）",
        ],
        "pro_tier_badge": "一次买断 · 终身无订阅扣费",
        "pro_tier_title": "EnglishGo Pro 终身完整版",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "解锁全部 15 节实战旅游英语课程（第 4–15 节）",
            "解锁全部 100 部实景对话视频与 200 句原生录音",
            "12 大旅游情景店员互动口语练习不限次数",
            "双向实时语音口译无限次使用（支持离线翻译包）",
        ],
        "bottom_cta_title": "下一趟出境自由行，打开就能用",
        "bottom_cta_sub": "无需注册账号，出发前练好音标发音、实景对话与现场口译。",
        "appstore_btn_label": "查看 TestFlight 与支持说明",
        "privacy_title": "EnglishGo 隐私政策",
        "privacy_updated": "最后更新日期：2026 年 11 月 23 日",
        "privacy_sections": [
            ("1. 无需账号且不收集个人数据", "EnglishGo 由 AE Interactive（AppEngine Interactive）开发。本应用无需注册账号，不会向开发商服务器收集、存储、出售或传输任何个人身份信息（App Store Privacy 声明为“不收集数据”，NSPrivacyTracking = false）。学习进度、单词复习与字号设置仅通过系统 UserDefaults（Required Reason API CA92.1）保存在设备本地。"),
            ("2. 麦克风、语音识别与端侧处理", "仅在您主动点击口语练习或双向实时口译的麦克风按钮时才申请权限；语音识别、Apple 本地翻译与端侧对话架构均在设备本地优先运行，对话不会发送至第三方服务器。"),
            ("3. 零广告与零第三方追踪", "本应用不含任何广告 SDK、商业统计或跨应用追踪。"),
            ("4. 联系我们", "如有隐私或支持咨询，请联系 help@appengine.fun。"),
        ],
        "support_title": "技术支持与常见问题 — EnglishGo",
        "support_sub": "语音权限、离线翻译包下载、TestFlight 测试与联系客服。",
        "support_cards": [
            ("互动口语练习与系统语音", "全面兼容 iPhone 与 iPad（iOS / iPadOS 17.0+）；在系统“设置 → 辅助功能 → 朗读内容 → 英语”下载增强音色可获得更自然朗读体验。"),
            ("全部课程、44 音标与 100 部视频完全离线可用", "15 节课程、44 美英音标、24 组辨音、100 部实景对话视频（200 句音频）、160 词卡（320 句音频）与 18 节语法全部内置离线包，飞行模式也可学习。"),
            ("出行前建议预载英语离线翻译包", "“双向实时语音翻译”使用 Apple 原生 Translation 框架；可在“设置 → App → 翻译”下载“简体中文 ↔ 英语”离线包，机场或地下站台没信号照样沟通。"),
            ("联系技术支持", "如需帮助或加入测试，请致信 help@appengine.fun，AE Interactive 团队通常于 24 小时内回复。"),
        ],
        "footer_rights": "© 2026 AE Interactive. 保留所有权利。",
        "studio_link_label": "AE Interactive 工作室",
    },
    "es": {
        "html_lang": "es",
        "title": "EnglishGo — Inglés de Viaje, 44 Fonemas IPA, 100 Vídeos Reales y Traducción en Vivo",
        "desc": "Domina el inglés práctico de viaje con 15 unidades, 44 fonemas IPA EE. UU./RU, 24 pares mínimos, 100 vídeos de diálogo real, Tutor Oral en el dispositivo e Intérprete Bidireccional en Vivo.",
        "keywords": "EnglishGo,ingles viajes,fonetica ipa,pares minimos,practica voz ingles,traduccion voz ingles,dialogos viaje,AE Interactive",
        "nav_privacy": "Privacidad",
        "nav_support": "Soporte",
        "nav_download": "Ver App",
        "hero_badge": "15 LECCIONES · 44 IPA · 100 VÍDEOS DE VIAJE · TRADUCCIÓN EN VIVO",
        "hero_title": "Habla Inglés Claro <span>Antes de Aterrizar Tu Vuelo</span>",
        "hero_sub": "Desde 44 fonemas IPA y 24 pares mínimos (ship/sheep, light/right) hasta 100 vídeos de diálogo real, rol práctico en 12 escenas y traducción de voz bidireccional al instante—sin cuentas ni rastreo.",
        "status_pill": "TestFlight y Próximamente en App Store · iPhone / iPad / iPhone Duo",
        "cta_store_sub": "Próximamente en",
        "cta_store_main": "App Store",
        "cta_audio": "▶ Escuchar Frases Reales",
        "cta_screens": "Ver Capturas ↓",
        "sec_audio_badge": "AUDIO REAL DE ESTUDIO · FONÉTICA IPA",
        "sec_audio_title": "Escucha Frases Reales de Viaje en Inglés",
        "sec_audio_sub": "Clips MP3 reales incluidos dentro de EnglishGo con transcripción IPA americana clara y consejos útiles de gramática.",
        "btn_play": "Reproducir",
        "btn_playing": "Sonando",
        "sec_screens_badge": "CAPTURAS REALES · IPHONE E IPHONE DUO PLEGABLE",
        "sec_screens_title": "Diseñada para Leer Cómodo a Una Mano",
        "sec_screens_sub": "Tipografía grande ajustable y diseño vertical limpio, optimizado para iPhone, iPad 13\" y pantalla interior de iPhone Duo.",
        "screens_labels": [
            "Ruta en 15 Lecciones",
            "Tutor Oral (12 Escenas)",
            "Intérprete de Voz en Vivo",
            "100 Vídeos Reales",
            "44 IPA y Pares Mínimos",
            "Pantalla Interior iPhone Duo",
        ],
        "sec_features_badge": "CINCO MÓDULOS INTEGRADOS",
        "sec_features_title": "Todo lo Esencial en Una App Privada y Sin Registro",
        "features": [
            ("📚", "15 Lecciones Prácticas y 18 Pruebas", "Avanza desde vocales, consonantes (th, l/r, v/w) y enlaces hasta cafeterías, restaurantes, aduana, hotel y farmacia."),
            ("🔊", "Laboratorio de 44 IPA + 24 Pares Mínimos", "Alterna entre IPA de EE. UU. y Reino Unido con guía de lengua/labios y tests auditivos a ciegas."),
            ("🎬", "100 Vídeos de Diálogos Reales de Viaje", "Cinco categorías reales con 200 grabaciones nativas, subtítulos bilingües, IPA y consejos culturales."),
            ("💬", "Tutor Oral (12 Escenas) + Intérprete en Vivo", "El personal inicia el diálogo y las pistas quedan visibles al hablar; traducción instantánea Español / 繁中 / 简中 / 日本語 ↔ English."),
            ("✍️", "160 Tarjetas SRS y 320 Audios", "Repetición espaciada SM-2, 4 modos de test auditivo y lector, y letra Estándar, Grande o Extra grande."),
            ("🔒", "Sin Registro · Privacidad Total", "Sin cuentas, sin anuncios ni SDKs de rastreo. Todo tu progreso se queda únicamente en tu iPhone o iPad."),
        ],
        "sec_pricing_badge": "SIN SUSCRIPCIONES · EMPIEZA GRATIS",
        "sec_pricing_title": "Gratis para Empezar. $3.99 Pago Único.",
        "sec_pricing_sub": "Domina los 44 fonemas IPA y frases clave gratis, y desbloquea todo para siempre con una sola compra.",
        "free_tier_title": "Gratis para Siempre",
        "free_tier_price": "$0",
        "free_tier_items": [
            "Tabla completa de 44 fonemas US/UK IPA y 24 pares mínimos",
            "160 tarjetas SRS (320 audios) y 18 ejercicios de gramática",
            "Lecciones 1–3 y 10 vídeos reales (2 por categoría)",
            "Cuota diaria gratis de Tutor Oral (5/día) e Intérprete (8/día)",
        ],
        "pro_tier_badge": "PAGO ÚNICO · SIN SUSCRIPCIÓN",
        "pro_tier_title": "EnglishGo Pro De Por Vida",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "Las 15 lecciones guiadas de viaje (4–15 desbloqueadas)",
            "Los 100 vídeos de diálogo real y 200 audios nativos",
            "Práctica oral ilimitada en los 12 escenarios",
            "Intérprete de voz bidireccional sin límites (uso offline)",
        ],
        "bottom_cta_title": "¿Listo para Tu Próximo Viaje?",
        "bottom_cta_sub": "Sin crear cuenta: entrena tu oído, diálogos reales y traductor offline en una sola app.",
        "appstore_btn_label": "Ver TestFlight y Soporte",
        "privacy_title": "Política de Privacidad — EnglishGo",
        "privacy_updated": "Última actualización: 23 de noviembre de 2026",
        "privacy_sections": [
            ("1. Sin Cuenta y Sin Recopilación de Datos", "EnglishGo es desarrollada por AE Interactive (AppEngine Interactive). No solicitamos registro ni recopilamos, vendemos o enviamos datos personales (Etiqueta App Store: No se recopilan datos / NSPrivacyTracking = false). El progreso y los ajustes se guardan únicamente en local mediante UserDefaults (Required Reason API CA92.1)."),
            ("2. Micrófono, Voz y Procesamiento Local", "El micrófono y el reconocimiento de voz solo se solicitan al pulsar Grabar en el Tutor Oral o el Intérprete en Vivo. La traducción y las respuestas se ejecutan con APIs nativas de Apple sin enviar conversaciones a servidores de terceros."),
            ("3. Sin Publicidad ni Rastreo", "EnglishGo no incluye redes publicitarias, analítica externa ni rastreo entre apps."),
            ("4. Contacto", "Para cualquier consulta, escribe a help@appengine.fun."),
        ],
        "support_title": "Soporte y Compatibilidad — EnglishGo",
        "support_sub": "Requisitos de práctica de voz, paquetes sin conexión y contacto directo.",
        "support_cards": [
            ("Tutor Oral y Reconocimiento de Voz", "Compatible con iPhone y iPad (iOS / iPadOS 17.0+). Descarga voces mejoradas en Ajustes de iOS -> Accesibilidad -> Contenido leído -> Voces -> Inglés."),
            ("Acceso Completo Offline a Cursos, IPA y Vídeos", "Las 15 unidades, los 44 fonemas IPA, 24 pares mínimos, 100 vídeos reales (200 MP3), 160 tarjetas (320 MP3) y 18 ejercicios funcionan sin conexión ni cuenta."),
            ("Traducción Sin Conexión para el Viaje", "En Ajustes de iOS -> Apps -> Traducir puedes descargar el paquete Español ↔ Inglés antes de volar para usar el Intérprete sin cobertura."),
            ("Soporte Directo y TestFlight", "Escríbenos a help@appengine.fun y responderemos habitualmente en menos de 24 horas."),
        ],
        "footer_rights": "© 2026 AE Interactive. Todos los derechos reservados.",
        "studio_link_label": "Estudio AE Interactive",
    },
    "ja": {
        "html_lang": "ja",
        "title": "EnglishGo — 旅行英会話、米英44発音記号、100本の実境動画・双方向同時通訳",
        "desc": "全15課カリキュラム、米英44発音記号（IPA）＆24組の聞き分けテスト、100本の実境旅行会話動画、12場面の音声ロールプレイ、オフライン対応の双方向同時通訳を1本に。",
        "keywords": "EnglishGo,英語学習,旅行英会話,発音記号,IPA,聞き分け練習,音声翻訳,英会話ロールプレイ,AE Interactive",
        "nav_privacy": "プライバシー",
        "nav_support": "サポート",
        "nav_download": "詳細を見る",
        "hero_badge": "全15課 · 44発音記号 · 100本の実境英語動画 · 双方向同時通訳",
        "hero_title": "旅立つ前に、<span>通じる英語を自信を持って話そう</span>",
        "hero_sub": "米英44発音記号と24組の聞き分け（ship / sheep、light / right）、100本の実境英語動画での予習から、12場面ロールプレイと現地で使える双方向音声通訳まで——登録不要・広告ゼロ。",
        "status_pill": "TestFlight 実施中・App Store 公開準備中 · iPhone / iPad / iPhone Duo",
        "cta_store_sub": "近日公開 / サポート情報",
        "cta_store_main": "App Store",
        "cta_audio": "▶ ネイティブ音声を試聴",
        "cta_screens": "アプリ画面を見る ↓",
        "sec_audio_badge": "アプリ収録スタジオ音声 · アメリカ英語 IPA 表記",
        "sec_audio_title": "旅行でそのまま使える英語音声を試聴",
        "sec_audio_sub": "EnglishGo に同梱されているネイティブMP3音声の一部——アメリカ英語 IPA と実用文法メモ付き。",
        "btn_play": "再生",
        "btn_playing": "再生中",
        "sec_screens_badge": "実機スクリーンショット · IPHONE & IPHONE DUO",
        "sec_screens_title": "片手縦持ちで、空港や街角でも迷わない",
        "sec_screens_sub": "旅行中の片手操作に合わせた大きな文字サイズ（標準／大／特大）と、iPad・iPhone Duo 折りたたみ画面に対応。",
        "screens_labels": [
            "全15課の体系ロードマップ",
            "12場面の会話ロールプレイ",
            "リアルタイム双方向音声通訳",
            "100本の実境英会話動画",
            "米英44発音記号＆聞き分け",
            "iPhone Duo 展開メイン画面",
        ],
        "sec_features_badge": "5つの統合学習モジュール",
        "sec_features_title": "発音の基礎から現地対応まで、すべてオフライン対応",
        "features": [
            ("📚", "全15課カリキュラム＋18文法テスト", "母音・R母音・二重母音・子音（th / l / r / v / w）の基礎から、カフェ注文・会計・空港入国・ホテル・病院対応まで段階的に習得。"),
            ("🔊", "44発音記号（US/UK IPA）＆ 24組聞き分け", "米英IPA切替、舌の位置と口形の詳しいガイド、ネイティブ音声のブラインド聞き分けチャレンジを搭載。"),
            ("🎬", "100本の実境旅行会話動画（音声200本）", "実際の旅行シーン順に並んだ5カテゴリ×20課の動画に、日英等字幕・IPA・現地マナー解説を収録。"),
            ("💬", "12場面会話練習 ＋ 双方向リアルタイム通訳", "店員が先に話しかけてヒントカードを見ながら3ステップ会話；日本語／繁体字／簡体字／スペイン語 ⇄ English を即時音声通訳。"),
            ("✍️", "160語のSM-2単語カード＆320音声", "忘却曲線に基づく復習管理、4種類のリスニング＆読解クイズ、3段階文字サイズ調整に対応。"),
            ("🔒", "ログイン不要・100% 端末内プライバシー", "広告なし・第三者トラッキングなし（NSPrivacyTracking = false）。学習履歴はすべてお使いの端末内にのみ保存されます。"),
        ],
        "sec_pricing_badge": "月額課金なし · まずは無料で体験",
        "sec_pricing_title": "基本ずっと無料・$3.99 の買い切りアップグレード",
        "sec_pricing_sub": "44発音記号と160単語カードは無料でずっと学習可能。必要なときだけ買い切りで全コンテンツをアンロックできます。",
        "free_tier_title": "ずっと無料版",
        "free_tier_price": "無料 $0",
        "free_tier_items": [
            "米英44発音記号一覧＆24組の聞き分けテストすべて",
            "160語SRS単語カード（音声320本）＆文法テスト18種",
            "第1〜3課レッスン ＋ 各ジャンル2本（計10本）の実境動画",
            "毎日無料の会話ロールプレイ（5回/日）＆同時通訳（8回/日）",
        ],
        "pro_tier_badge": "一度きりの買い切り · 月額サブスクなし",
        "pro_tier_title": "EnglishGo Pro 買い切り版",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "全15課の旅行英会話カリキュラム（第4〜15課を解放）",
            "全100本の実境会話動画＆ネイティブ音声200本すべて",
            "12場面の店員会話ロールプレイが回数無制限",
            "双方向リアルタイム音声通訳が無制限（オフライン対応）",
        ],
        "bottom_cta_title": "次の海外旅行に、この1本を",
        "bottom_cta_sub": "アカウント登録不要。出発前から現地での会話までしっかりサポート。",
        "appstore_btn_label": "TestFlight・サポート詳細を見る",
        "privacy_title": "EnglishGo プライバシーポリシー",
        "privacy_updated": "最終更新日：2026年11月23日",
        "privacy_sections": [
            ("1. アカウント不要・個人データ非収集", "EnglishGo は AE Interactive（AppEngine Interactive）が開発しています。アカウント登録は不要で、個人データを開発者サーバーへ収集・保存・送信することは一切ありません（App Store Privacy：データ未収集 / NSPrivacyTracking = false）。進捗・単語SRS・文字サイズは Apple UserDefaults（Required Reason API CA92.1）により端末内にのみ保存されます。"),
            ("2. マイク・音声認識・端末内処理", "マイクおよび音声認識は会話練習や同時通訳の録音ボタンを押した時のみ使用します。文字起こし・翻訳・会話誘導は Apple 純正フレームワークにより端末側で処理され、開発者サーバーへ送信されません。"),
            ("3. 広告ゼロ・トラッキングゼロ", "広告SDKや外部アナリティクス、他社アプリとのトラッキングは一切含まれていません。"),
            ("4. お問い合わせ", "ご質問やプライバシーに関するお問い合わせは help@appengine.fun までご連絡ください。"),
        ],
        "support_title": "サポート・対応環境 — EnglishGo",
        "support_sub": "音声ロールプレイ対応機種、オフライン翻訳パック設定、TestFlight ご案内。",
        "support_cards": [
            ("音声ロールプレイと推奨システム音声", "iPhone・iPad（iOS / iPadOS 17.0+）に対応。「設定 → アクセシビリティ → 読み上げコンテンツ → 声 → 英語」から拡張音声をダウンロードするとより自然な発音になります。"),
            ("15課・44発音記号・100本動画は完全オフライン再生", "全15課、米英44発音記号、24組聞き分け、100本の実境会話動画（200本MP3）、160単語カード（320本MP3）、18文法練習はアプリ内にすべて同梱済みです。"),
            ("出発前のオフライン翻訳パックダウンロード", "「双方向音声通訳」は Apple 純正 Translation フレームワークを使用します。iOS「設定 → アプリ → 翻訳」で「英語 ↔ 日本語」パックを事前にダウンロードすると機内でも利用できます。"),
            ("サポート窓口・TestFlight", "ご不明点やご要望は help@appengine.fun までメールでお問い合わせください（通常24時間以内に返信）。"),
        ],
        "footer_rights": "© 2026 AE Interactive. All rights reserved.",
        "studio_link_label": "AE Interactive スタジオ",
    },
}

AUDIO_ITEMS = [
    {
        "file": "check_bill.mp3",
        "phrase": "Excuse me, could we get the check?",
        "ipa": "/ɪkˈskjuːz miː kʊd wiː ɡɛt ðə <b>tʃɛk</b>/",
        "meaning": {
            "en": "Asking politely for the restaurant bill.",
            "zh-Hant": "不好意思，請問可以結帳嗎？",
            "zh-Hans": "不好意思，请问可以结账吗？",
            "es": "Disculpe, ¿nos trae la cuenta?",
            "ja": "すみません、お会計をお願いできますか？",
        },
        "tag": {
            "en": "Dining · Check vs Bill",
            "zh-Hant": "餐廳結帳 · Check / Bill",
            "zh-Hans": "餐厅结账 · Check / Bill",
            "es": "Restaurante · La cuenta",
            "ja": "レストラン会計 · check / bill",
        },
    },
    {
        "file": "credit_card.mp3",
        "phrase": "Do you take credit cards or Apple Pay?",
        "ipa": "/duː juː teɪk <b>ˈkrɛdɪt kɑːrdz</b> ɔːr ˈæpəl peɪ/",
        "meaning": {
            "en": "Checking accepted payment methods at checkout.",
            "zh-Hant": "請問你們收信用卡或 Apple Pay 嗎？",
            "zh-Hans": "请问你们收信用卡或 Apple Pay 吗？",
            "es": "¿Aceptan tarjetas de crédito o Apple Pay?",
            "ja": "クレジットカードかApple Payは使えますか？",
        },
        "tag": {
            "en": "Café & Shop · Payment",
            "zh-Hant": "咖啡廳結帳 · 付款方式",
            "zh-Hans": "咖啡厅结账 · 付款方式",
            "es": "Cafetería · Pagos",
            "ja": "カフェ・買い物 · お支払い",
        },
    },
    {
        "file": "baggage_claim.mp3",
        "phrase": "Which way is baggage claim?",
        "ipa": "/wɪtʃ weɪ ɪz <b>ˈbæɡɪdʒ kleɪm</b>/",
        "meaning": {
            "en": "Finding the luggage carousel after landing.",
            "zh-Hant": "請問行李轉盤區往哪邊走？",
            "zh-Hans": "请问行李转盘区往哪边走？",
            "es": "¿Por dónde está el reclamo de equipaje?",
            "ja": "手荷物受取所はどちらですか？",
        },
        "tag": {
            "en": "Airport Arrival · Luggage",
            "zh-Hant": "機場入境 · 行李提領",
            "zh-Hans": "机场入境 · 行李提取",
            "es": "Aeropuerto · Equipaje",
            "ja": "空港到着 · 手荷物受取所",
        },
    },
    {
        "file": "check_in.mp3",
        "phrase": "Hi, I'd like to check in, please.",
        "ipa": "/haɪ aɪd laɪk tuː <b>tʃɛk ɪn</b> pliːz/",
        "meaning": {
            "en": "Polite arrival check-in at the hotel front desk.",
            "zh-Hant": "您好，我要辦理入住。",
            "zh-Hans": "您好，我要办理入住。",
            "es": "Hola, me gustaría hacer el check-in, por favor.",
            "ja": "こんにちは、チェックインをお願いします。",
        },
        "tag": {
            "en": "Hotel Desk · Linked Consonant",
            "zh-Hant": "飯店入住 · 連音 Check in",
            "zh-Hans": "酒店前台 · 连读 Check in",
            "es": "Hotel · Enlace Check-in",
            "ja": "ホテル受付 · リンキング表現",
        },
    },
]

CSS = """
:root {
  --bg: #070913;
  --card: rgba(20, 24, 42, 0.86);
  --card-solid: #14182a;
  --border: rgba(255, 255, 255, 0.11);
  --text: #F8FAFC;
  --muted: #94A3B8;
  --indigo: #6366F1;
  --teal: #2DD4BF;
  --coral: #FB7185;
}
* { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
html { scroll-behavior: smooth; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "PingFang TC", "PingFang SC", "Hiragino Sans", "Helvetica Neue", Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  overflow-x: hidden;
  background-image:
    radial-gradient(ellipse 80% 42% at 50% -5%, rgba(99, 102, 241, 0.24) 0%, transparent 70%),
    radial-gradient(circle at 86% 18%, rgba(45, 212, 191, 0.14) 0%, transparent 45%);
  background-repeat: no-repeat;
}
a { color: inherit; }
header { position: sticky; top: 12px; z-index: 100; padding: 0 16px; }
nav {
  max-width: 980px; margin: 0 auto; padding: 10px 16px;
  display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
  background: rgba(11, 14, 28, 0.84);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border); border-radius: 999px;
  box-shadow: 0 12px 34px rgba(0,0,0,0.45);
}
.brand { display: flex; align-items: center; gap: 10px; text-decoration: none; font-weight: 800; font-size: 17px; letter-spacing: -0.3px; }
.brand img { width: 34px; height: 34px; border-radius: 9px; border: 1px solid rgba(45, 212, 191, 0.45); }
.nav-right { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.nav-links { display: flex; gap: 14px; font-size: 13px; font-weight: 600; color: var(--muted); }
.nav-links a { text-decoration: none; transition: color .18s; }
.nav-links a:hover, .nav-links a.active { color: #fff; }
.lang-picker {
  display: flex; align-items: center; gap: 4px;
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.09);
  padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700;
}
.lang-picker a { color: var(--muted); text-decoration: none; padding: 2px 5px; border-radius: 99px; }
.lang-picker a.active { color: var(--teal); background: rgba(45,212,191,0.14); }
main { max-width: 980px; margin: 0 auto; padding: 36px 18px 64px; }
.hero { text-align: center; padding: 20px 0 36px; }
.badge {
  display: inline-block; font-size: 11px; font-weight: 800; letter-spacing: 0.7px;
  color: var(--teal); background: rgba(45,212,191,0.12);
  border: 1px solid rgba(45,212,191,0.34); padding: 6px 14px; border-radius: 999px; margin-bottom: 16px;
}
h1 { font-size: clamp(30px, 5.4vw, 54px); font-weight: 900; letter-spacing: -1.1px; line-height: 1.12; margin-bottom: 14px; text-wrap: balance; }
h1 span { background: linear-gradient(125deg, #818CF8 0%, #2DD4BF 62%, #FB7185 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { max-width: 680px; margin: 0 auto 22px; color: var(--muted); font-size: clamp(15px, 2vw, 18px); text-wrap: balance; }
.status-pill {
  display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 999px;
  background: rgba(99,102,241,0.14); border: 1px solid rgba(99,102,241,0.38);
  color: #C7D2FE; font-size: 13px; font-weight: 700; margin-bottom: 22px;
}
.hero-cta { display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }
.btn {
  display: inline-flex; align-items: center; gap: 8px; padding: 12px 22px; border-radius: 999px;
  font-size: 14px; font-weight: 700; text-decoration: none; border: 1px solid transparent; cursor: pointer;
  transition: transform .16s ease, box-shadow .16s ease, background .16s ease;
}
.btn:hover { transform: translateY(-1px); }
.btn-primary { background: linear-gradient(135deg, #6366F1, #14B8A6); color: #fff; box-shadow: 0 10px 26px rgba(99,102,241,0.32); }
.btn-ghost { background: rgba(255,255,255,0.06); border-color: var(--border); color: #E2E8F0; }
.btn-appstore {
  background: #fff; color: #090D16; border: 1px solid rgba(255,255,255,0.85);
  padding: 9px 20px; gap: 10px; box-shadow: 0 12px 30px rgba(255,255,255,0.16), 0 8px 24px rgba(99,102,241,0.28);
}
.btn-appstore svg { width: 20px; height: 24px; fill: currentColor; flex-shrink: 0; }
.btn-appstore .as-copy { display: flex; flex-direction: column; align-items: flex-start; line-height: 1.12; text-align: left; }
.btn-appstore .as-sub { font-size: 10px; font-weight: 700; opacity: 0.72; letter-spacing: 0.2px; }
.btn-appstore .as-main { font-size: 15px; font-weight: 850; letter-spacing: -0.2px; }
.nav-cta {
  display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 999px;
  background: linear-gradient(135deg, #6366F1, #14B8A6); color: #fff; text-decoration: none;
  font-size: 12.5px; font-weight: 800; box-shadow: 0 4px 14px rgba(99,102,241,0.35);
  transition: transform .16s ease, filter .16s ease;
}
.nav-cta:hover { transform: translateY(-1px); filter: brightness(1.08); }
.pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 16px; }
.price-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 22px; padding: 24px;
  display: flex; flex-direction: column; justify-content: space-between; gap: 18px;
}
.price-card.pro {
  border-color: rgba(45, 212, 191, 0.55);
  background: linear-gradient(160deg, rgba(99,102,241,0.16), rgba(20,24,42,0.94) 45%, rgba(20,184,166,0.14));
  box-shadow: 0 18px 40px rgba(0,0,0,0.42);
}
.price-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
.price-tag { font-size: 11px; font-weight: 800; color: var(--teal); letter-spacing: 0.4px; margin-bottom: 4px; }
.price-title { font-size: 20px; font-weight: 850; color: #fff; }
.price-num { font-size: 26px; font-weight: 900; color: #fff; white-space: nowrap; }
.price-list { list-style: none; display: flex; flex-direction: column; gap: 10px; }
.price-list li { display: flex; gap: 9px; font-size: 14px; color: #CBD5E1; line-height: 1.45; }
.price-list li span.chk { color: var(--teal); font-weight: 900; flex-shrink: 0; }
.price-card .btn-appstore { justify-content: center; }
.cta-banner {
  margin-top: 56px; padding: 34px 24px; border-radius: 26px; text-align: center;
  background: linear-gradient(135deg, rgba(99,102,241,0.22), rgba(20,184,166,0.18));
  border: 1px solid rgba(45,212,191,0.35);
  display: flex; flex-direction: column; align-items: center; gap: 14px;
}
.cta-banner img { width: 64px; height: 64px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.25); box-shadow: 0 10px 28px rgba(0,0,0,0.4); }
.cta-banner h2 { margin-bottom: 0; }
.cta-banner p { color: #CBD5E1; max-width: 540px; font-size: 15px; }
section { margin-top: 56px; }
.sec-head { text-align: center; margin-bottom: 24px; }
.sec-head .badge { margin-bottom: 10px; }
h2 { font-size: clamp(22px, 3.6vw, 34px); font-weight: 850; letter-spacing: -0.6px; margin-bottom: 8px; }
.sec-sub { color: var(--muted); max-width: 620px; margin: 0 auto; font-size: 15px; }
.audio-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }
.audio-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 18px; padding: 16px;
  display: flex; flex-direction: column; justify-content: space-between; gap: 12px;
  transition: border-color .2s, transform .2s;
}
.audio-card.playing { border-color: var(--teal); box-shadow: 0 0 0 1px rgba(45,212,191,0.3), 0 14px 32px rgba(0,0,0,0.4); }
.audio-tag { font-size: 11px; font-weight: 700; color: var(--teal); letter-spacing: 0.3px; }
.audio-jp { font-size: 18px; font-weight: 800; margin-top: 6px; color: #fff; }
.audio-romaji { font-size: 13px; color: #67E8F9; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; margin-top: 4px; }
.audio-romaji b { background: rgba(251, 113, 133, 0.2); color: #FDA4AF; padding: 0 4px; border-radius: 4px; }
.audio-meaning { font-size: 13px; color: var(--muted); margin-top: 4px; }
.play-btn {
  align-self: flex-start; background: rgba(99,102,241,0.2); color: #C7D2FE; border: 1px solid rgba(99,102,241,0.4);
  padding: 6px 14px; border-radius: 999px; font-size: 12.5px; font-weight: 700; cursor: pointer;
}
.audio-card.playing .play-btn { background: var(--teal); color: #042F2E; border-color: var(--teal); }
.gallery-strip {
  display: flex; gap: 16px; overflow-x: auto; padding: 8px 4px 16px; scroll-snap-type: x mandatory;
}
.shot-card {
  flex: 0 0 230px; scroll-snap-align: start; background: var(--card); border: 1px solid var(--border);
  border-radius: 20px; padding: 10px; text-align: center;
}
.shot-card.wide { flex: 0 0 330px; }
.shot-card img { width: 100%; height: auto; border-radius: 14px; display: block; }
.shot-cap { font-size: 12.5px; font-weight: 700; color: #CBD5E1; margin-top: 9px; }
.bento { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }
.bento-card { background: var(--card); border: 1px solid var(--border); border-radius: 20px; padding: 20px; }
.bento-icon { font-size: 24px; margin-bottom: 10px; }
.bento-card h3 { font-size: 17px; font-weight: 800; margin-bottom: 6px; color: #fff; }
.bento-card p { font-size: 14px; color: var(--muted); }
.doc-box { max-width: 780px; margin: 14px auto; background: var(--card); border: 1px solid var(--border); border-radius: 22px; padding: 28px; }
.doc-box h1 { font-size: clamp(24px, 4vw, 36px); text-align: left; }
.doc-item { margin-top: 22px; padding-top: 18px; border-top: 1px solid var(--border); }
.doc-item h2 { font-size: 18px; margin-bottom: 6px; color: #E2E8F0; }
.doc-item p { font-size: 14.5px; color: var(--muted); }
footer {
  max-width: 980px; margin: 36px auto 0; padding: 24px 18px 42px;
  border-top: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap;
  color: var(--muted); font-size: 13px;
}
footer a { color: #CBD5E1; text-decoration: none; }
footer a:hover { color: var(--teal); }
@media (max-width: 680px) {
  nav { border-radius: 22px; padding: 10px 14px; }
  .nav-right { gap: 8px; }
  .hero-cta .btn { width: 100%; justify-content: center; max-width: 300px; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .btn, .audio-card { transition: none; }
}
"""

SCRIPT_JS = """
const audioMap = {};
let activeKey = null;
function togglePhrase(key, src, btnEl, cardEl, playLabel, playingLabel) {
  if (activeKey && activeKey !== key && audioMap[activeKey]) {
    audioMap[activeKey].audio.pause();
    audioMap[activeKey].audio.currentTime = 0;
    audioMap[activeKey].btn.textContent = "▶ " + playLabel;
    audioMap[activeKey].card.classList.remove("playing");
  }
  let item = audioMap[key];
  if (!item) {
    const a = new Audio(src);
    item = { audio: a, btn: btnEl, card: cardEl };
    a.addEventListener("ended", () => {
      btnEl.textContent = "▶ " + playLabel;
      cardEl.classList.remove("playing");
      if (activeKey === key) activeKey = null;
    });
    audioMap[key] = item;
  }
  if (!item.audio.paused) {
    item.audio.pause();
    item.audio.currentTime = 0;
    btnEl.textContent = "▶ " + playLabel;
    cardEl.classList.remove("playing");
    activeKey = null;
  } else {
    item.audio.play();
    btnEl.textContent = "■ " + playingLabel;
    cardEl.classList.add("playing");
    activeKey = key;
  }
}
"""


def appstore_badge_svg() -> str:
    return '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'


def store_href(lang: str) -> str:
    return APP_STORE_URL if APP_STORE_URL else f"/support?lang={lang}"


def nav_html(lang: str, route: str, t: dict) -> str:
    langs = [("en", "EN"), ("zh-Hant", "繁中"), ("zh-Hans", "简中"), ("es", "ES"), ("ja", "日本語")]
    lang_links = []
    for code, label in langs:
        cls = ' class="active"' if code == lang else ""
        href = f"{route}?lang={code}"
        lang_links.append(f'<a href="{href}"{cls}>{label}</a>')
    p_cls = ' class="active"' if route == "/privacy" else ""
    s_cls = ' class="active"' if route == "/support" else ""
    q = f"?lang={lang}"
    target_attr = ' target="_blank" rel="noopener noreferrer"' if APP_STORE_URL else ""
    return f"""
<header>
  <nav aria-label="Main navigation">
    <a class="brand" href="/{q}">
      <img src="/images/icon.webp" alt="EnglishGo Icon" width="34" height="34">
      <span>EnglishGo</span>
    </a>
    <div class="nav-right">
      <div class="nav-links">
        <a href="/privacy{q}"{p_cls}>{html_mod.escape(t['nav_privacy'])}</a>
        <a href="/support{q}"{s_cls}>{html_mod.escape(t['nav_support'])}</a>
      </div>
      <div class="lang-picker" role="navigation" aria-label="Language">{''.join(lang_links)}</div>
      <a class="nav-cta" href="{store_href(lang)}"{target_attr}>{html_mod.escape(t['nav_download'])}</a>
    </div>
  </nav>
</header>"""


def footer_html(lang: str, t: dict) -> str:
    q = f"?lang={lang}"
    app_link = (
        f'<a href="{APP_STORE_URL}" target="_blank" rel="noopener noreferrer">App Store</a>'
        if APP_STORE_URL
        else '<a href="https://github.com/movemove/EnglishGo" target="_blank" rel="noopener noreferrer">GitHub</a>'
    )
    return f"""
<footer>
  <div>{html_mod.escape(t['footer_rights'])}</div>
  <div style="display:flex;gap:16px;flex-wrap:wrap;">
    <a href="/{q}">EnglishGo</a>
    {app_link}
    <a href="/privacy{q}">{html_mod.escape(t['nav_privacy'])}</a>
    <a href="/support{q}">{html_mod.escape(t['nav_support'])}</a>
    <a href="https://appengine.fun" target="_blank" rel="noopener noreferrer">{html_mod.escape(t['studio_link_label'])}</a>
    <a href="mailto:help@appengine.fun">help@appengine.fun</a>
  </div>
</footer>"""


def head_html(lang: str, t: dict, title: str, canonical_path: str) -> str:
    q = f"?lang={lang}" if lang != "en" else ""
    schema_obj = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "EnglishGo Travel English",
        "operatingSystem": "iOS 17.0+, iPadOS 17.0+",
        "applicationCategory": "EducationApplication",
        "url": ORIGIN,
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD",
        },
        "publisher": {
            "@type": "Organization",
            "name": "AE Interactive",
            "url": "https://appengine.fun",
        },
    }
    if APP_STORE_URL:
        schema_obj["downloadUrl"] = APP_STORE_URL
        schema_obj["installUrl"] = APP_STORE_URL
    schema = json.dumps(schema_obj, ensure_ascii=False)
    alternates = "".join(
        f'<link rel="alternate" hreflang="{code}" href="{ORIGIN}{canonical_path}?lang={code}">\n'
        for code in ("en", "zh-Hant", "zh-Hans", "es", "ja")
    )
    smart_banner = f'<meta name="apple-itunes-app" content="app-id={APP_STORE_ID}">\n' if APP_STORE_ID else ""
    return f"""<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_mod.escape(title)}</title>
<meta name="description" content="{html_mod.escape(t['desc'])}">
<meta name="keywords" content="{html_mod.escape(t['keywords'])}">
<meta name="theme-color" content="#070913">
{smart_banner}<link rel="canonical" href="{ORIGIN}{canonical_path}{q}">
{alternates}<link rel="alternate" hreflang="x-default" href="{ORIGIN}{canonical_path}">
<link rel="icon" type="image/png" href="/images/icon.png">
<link rel="apple-touch-icon" href="/images/icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{html_mod.escape(title)}">
<meta property="og:description" content="{html_mod.escape(t['desc'])}">
<meta property="og:url" content="{ORIGIN}{canonical_path}{q}">
<meta property="og:image" content="{ORIGIN}/images/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{ORIGIN}/images/og.png">
<script type="application/ld+json">{schema}</script>
<style>{CSS}</style>
</head>"""


def build_home(lang: str, t: dict) -> str:
    audio_cards = []
    for idx, item in enumerate(AUDIO_ITEMS):
        play_lbl = html_mod.escape(t["btn_play"])
        playing_lbl = html_mod.escape(t["btn_playing"])
        audio_cards.append(f"""
        <article class="audio-card" id="card-{idx}">
          <div>
            <div class="audio-tag">{html_mod.escape(item['tag'][lang])}</div>
            <div class="audio-jp">{html_mod.escape(item['phrase'])}</div>
            <div class="audio-romaji">{item['ipa']}</div>
            <div class="audio-meaning">{html_mod.escape(item['meaning'][lang])}</div>
          </div>
          <button type="button" class="play-btn" onclick="togglePhrase('p{idx}','/audio/{item['file']}',this,document.getElementById('card-{idx}'),'{play_lbl}','{playing_lbl}')">▶ {play_lbl}</button>
        </article>""")

    shot_lang = "zh-Hant" if lang == "en" else lang
    shot_cards = []
    for i in range(1, 6):
        lbl = html_mod.escape(t["screens_labels"][i - 1])
        shot_cards.append(f"""
        <div class="shot-card">
          <img src="/images/{shot_lang}_s0{i}.webp" alt="{lbl}" loading="lazy" width="640" height="1390">
          <div class="shot-cap">{lbl}</div>
        </div>""")
    duo_lbl = html_mod.escape(t["screens_labels"][5])
    shot_cards.append(f"""
        <div class="shot-card wide">
          <img src="/images/{shot_lang}_duo.webp" alt="{duo_lbl}" loading="lazy" width="760" height="1080">
          <div class="shot-cap">{duo_lbl}</div>
        </div>""")

    bento_cards = []
    for icon, title, body in t["features"]:
        bento_cards.append(f"""
        <article class="bento-card">
          <div class="bento-icon" aria-hidden="true">{icon}</div>
          <h3>{html_mod.escape(title)}</h3>
          <p>{html_mod.escape(body)}</p>
        </article>""")

    free_lis = "".join(f'<li><span class="chk">✓</span><span>{html_mod.escape(x)}</span></li>' for x in t["free_tier_items"])
    pro_lis = "".join(f'<li><span class="chk">✓</span><span>{html_mod.escape(x)}</span></li>' for x in t["pro_tier_items"])
    target_attr = ' target="_blank" rel="noopener noreferrer"' if APP_STORE_URL else ""
    appstore_btn = (
        f'<a class="btn btn-appstore" href="{store_href(lang)}"{target_attr}>'
        f'{appstore_badge_svg()}'
        f'<span class="as-copy"><span class="as-sub">{html_mod.escape(t["cta_store_sub"])}</span>'
        f'<span class="as-main">{html_mod.escape(t["cta_store_main"])}</span></span></a>'
    )

    return f"""{head_html(lang, t, t['title'], '/')}
<body>
{nav_html(lang, '/', t)}
<main>
  <section class="hero">
    <div class="badge">{html_mod.escape(t['hero_badge'])}</div>
    <h1>{t['hero_title']}</h1>
    <p class="hero-sub">{html_mod.escape(t['hero_sub'])}</p>
    <div class="status-pill"> {html_mod.escape(t['status_pill'])}</div>
    <div class="hero-cta">
      {appstore_btn}
      <a class="btn btn-primary" href="#audio">{html_mod.escape(t['cta_audio'])}</a>
      <a class="btn btn-ghost" href="#preview">{html_mod.escape(t['cta_screens'])}</a>
    </div>
  </section>

  <section id="audio">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_audio_badge'])}</div>
      <h2>{html_mod.escape(t['sec_audio_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['sec_audio_sub'])}</p>
    </div>
    <div class="audio-grid">{''.join(audio_cards)}</div>
  </section>

  <section id="preview">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_screens_badge'])}</div>
      <h2>{html_mod.escape(t['sec_screens_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['sec_screens_sub'])}</p>
    </div>
    <div class="gallery-strip">{''.join(shot_cards)}</div>
  </section>

  <section id="features">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_features_badge'])}</div>
      <h2>{html_mod.escape(t['sec_features_title'])}</h2>
    </div>
    <div class="bento">{''.join(bento_cards)}</div>
  </section>

  <section id="pricing">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_pricing_badge'])}</div>
      <h2>{html_mod.escape(t['sec_pricing_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['sec_pricing_sub'])}</p>
    </div>
    <div class="pricing-grid">
      <article class="price-card">
        <div>
          <div class="price-head">
            <div>
              <div class="price-tag">ENGLISHGO FREE</div>
              <div class="price-title">{html_mod.escape(t['free_tier_title'])}</div>
            </div>
            <div class="price-num">{html_mod.escape(t['free_tier_price'])}</div>
          </div>
          <ul class="price-list" style="margin-top:16px;">{free_lis}</ul>
        </div>
        <a class="btn btn-ghost" style="justify-content:center;" href="{store_href(lang)}"{target_attr}>{html_mod.escape(t['appstore_btn_label'])}</a>
      </article>
      <article class="price-card pro">
        <div>
          <div class="price-head">
            <div>
              <div class="price-tag">{html_mod.escape(t['pro_tier_badge'])}</div>
              <div class="price-title">{html_mod.escape(t['pro_tier_title'])}</div>
            </div>
            <div class="price-num">{html_mod.escape(t['pro_tier_price'])}</div>
          </div>
          <ul class="price-list" style="margin-top:16px;">{pro_lis}</ul>
        </div>
        {appstore_btn}
      </article>
    </div>
  </section>

  <section class="cta-banner">
    <img src="/images/icon.webp" alt="EnglishGo" width="64" height="64">
    <h2>{html_mod.escape(t['bottom_cta_title'])}</h2>
    <p>{html_mod.escape(t['bottom_cta_sub'])}</p>
    {appstore_btn}
  </section>
</main>
{footer_html(lang, t)}
<script>{SCRIPT_JS}</script>
</body>
</html>"""


def build_doc_page(lang: str, t: dict, route: str, heading: str, sub: str, items: list[tuple[str, str]]) -> str:
    blocks = "".join(
        f'<div class="doc-item"><h2>{html_mod.escape(h)}</h2><p>{html_mod.escape(p)}</p></div>'
        for h, p in items
    )
    return f"""{head_html(lang, t, heading + ' | EnglishGo', route)}
<body>
{nav_html(lang, route, t)}
<main>
  <article class="doc-box">
    <h1>{html_mod.escape(heading)}</h1>
    <p style="color:var(--teal);font-weight:700;font-size:14px;margin-top:8px;">{html_mod.escape(sub)}</p>
    {blocks}
  </article>
</main>
{footer_html(lang, t)}
</body>
</html>"""


def cf_request(method: str, path: str, token: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Authorization": f"Bearer {token}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(f"https://api.cloudflare.com/client/v4{path}", data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def deploy_worker(token: str, worker_js: str) -> None:
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{SCRIPT_NAME}"
    boundary = "----EnglishGoBoundary918273"
    body = [
        f"--{boundary}".encode(),
        b'Content-Disposition: form-data; name="metadata"',
        b"Content-Type: application/json",
        b"",
        json.dumps({"main_module": "index.js", "compatibility_date": "2024-03-03"}).encode(),
        f"--{boundary}".encode(),
        b'Content-Disposition: form-data; name="index.js"; filename="index.js"',
        b"Content-Type: application/javascript+module",
        b"",
        worker_js.encode("utf-8"),
        f"--{boundary}--".encode(),
        b"",
    ]
    req = urllib.request.Request(
        url,
        data=b"\r\n".join(body),
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        res = json.loads(resp.read())
        assert res.get("success"), f"Worker upload failed: {res}"
        print("WORKER_UPLOADED:", SCRIPT_NAME)


def ensure_dns_and_route(token: str) -> None:
    dns = cf_request("GET", f"/zones/{ZONE_ID}/dns_records?name={HOSTNAME}", token)
    existing = dns.get("result", [])
    if not existing:
        created = cf_request("POST", f"/zones/{ZONE_ID}/dns_records", token, {
            "type": "A",
            "name": HOSTNAME,
            "content": "192.0.2.1",
            "proxied": True,
            "ttl": 1,
        })
        assert created.get("success"), f"DNS create failed: {created}"
        print("DNS_CREATED:", HOSTNAME)
    else:
        print("DNS_EXISTS:", [(r["type"], r["name"], r["content"], r["proxied"]) for r in existing])

    routes = cf_request("GET", f"/zones/{ZONE_ID}/workers/routes", token).get("result", [])
    pattern = f"{HOSTNAME}/*"
    match = [r for r in routes if r.get("pattern") == pattern]
    if not match:
        rc = cf_request("POST", f"/zones/{ZONE_ID}/workers/routes", token, {
            "pattern": pattern,
            "script": SCRIPT_NAME,
        })
        assert rc.get("success"), f"Route create failed: {rc}"
        print("ROUTE_CREATED:", pattern, "->", SCRIPT_NAME)
    else:
        rid = match[0]["id"]
        if match[0].get("script") != SCRIPT_NAME:
            cf_request("PUT", f"/zones/{ZONE_ID}/workers/routes/{rid}", token, {
                "pattern": pattern,
                "script": SCRIPT_NAME,
            })
            print("ROUTE_UPDATED:", pattern, "->", SCRIPT_NAME)
        else:
            print("ROUTE_EXISTS:", pattern, "->", SCRIPT_NAME)


def main() -> None:
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    pages = {}
    privacy_pages = {}
    support_pages = {}
    for code, t in CONTENT.items():
        home_html = build_home(code, t)
        priv_html = build_doc_page(code, t, "/privacy", t["privacy_title"], t["privacy_updated"], t["privacy_sections"])
        supp_html = build_doc_page(code, t, "/support", t["support_title"], t["support_sub"], t["support_cards"])
        pages[code] = home_html
        privacy_pages[code] = priv_html
        support_pages[code] = supp_html
        suffix = "" if code == "en" else f"_{code}"
        (PUBLIC_DIR / f"index{suffix}.html").write_text(home_html, encoding="utf-8")
        (PUBLIC_DIR / f"privacy{suffix}.html").write_text(priv_html, encoding="utf-8")
        (PUBLIC_DIR / f"support{suffix}.html").write_text(supp_html, encoding="utf-8")

    images = {p.name: base64.b64encode(p.read_bytes()).decode("ascii") for p in sorted(IMG_DIR.glob("*"))}
    audio = {p.name: base64.b64encode(p.read_bytes()).decode("ascii") for p in sorted(AUD_DIR.glob("*.mp3"))}

    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{ORIGIN}/</loc><priority>1.0</priority></url>
  <url><loc>{ORIGIN}/?lang=zh-Hant</loc><priority>0.9</priority></url>
  <url><loc>{ORIGIN}/?lang=zh-Hans</loc><priority>0.9</priority></url>
  <url><loc>{ORIGIN}/?lang=es</loc><priority>0.9</priority></url>
  <url><loc>{ORIGIN}/?lang=ja</loc><priority>0.9</priority></url>
  <url><loc>{ORIGIN}/privacy</loc><priority>0.7</priority></url>
  <url><loc>{ORIGIN}/support</loc><priority>0.7</priority></url>
</urlset>"""
    robots_txt = f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n"

    worker_js = f"""const PAGES = {json.dumps(pages)};
const PRIVACY_PAGES = {json.dumps(privacy_pages)};
const SUPPORT_PAGES = {json.dumps(support_pages)};
const IMAGES = {json.dumps(images)};
const AUDIO = {json.dumps(audio)};
const SITEMAP = {json.dumps(sitemap_xml)};
const ROBOTS = {json.dumps(robots_txt)};

function b64ToBytes(b64) {{
  const s = atob(b64);
  const out = new Uint8Array(s.length);
  for (let i = 0; i < s.length; i++) out[i] = s.charCodeAt(i);
  return out;
}}

function resolveLang(request) {{
  const url = new URL(request.url);
  const q = url.searchParams.get("lang");
  if (q && PAGES[q]) return q;
  if (q === "zh-TW" || q === "tw" || q === "hk") return "zh-Hant";
  if (q === "zh-CN" || q === "cn" || q === "zh") return "zh-Hans";
  if (q === "jp" || q === "ja-JP") return "ja";
  const accept = (request.headers.get("accept-language") || "").toLowerCase();
  if (accept.includes("zh-tw") || accept.includes("zh-hk") || accept.includes("zh-hant")) return "zh-Hant";
  if (accept.includes("zh")) return "zh-Hans";
  if (accept.includes("es")) return "es";
  if (accept.includes("ja")) return "ja";
  return "en";
}}

export default {{
  async fetch(request) {{
    const pathname = new URL(request.url).pathname;
    if (pathname === "/sitemap.xml") {{
      return new Response(SITEMAP, {{ headers: {{ "content-type": "application/xml;charset=UTF-8", "cache-control": "public, max-age=86400" }} }});
    }}
    if (pathname === "/robots.txt") {{
      return new Response(ROBOTS, {{ headers: {{ "content-type": "text/plain;charset=UTF-8", "cache-control": "public, max-age=86400" }} }});
    }}
    if (pathname.startsWith("/images/")) {{
      const name = pathname.slice("/images/".length);
      if (IMAGES[name]) {{
        const ct = name.endsWith(".png") ? "image/png" : "image/webp";
        return new Response(b64ToBytes(IMAGES[name]), {{ headers: {{ "content-type": ct, "cache-control": "public, max-age=31536000, immutable" }} }});
      }}
      return new Response("Not Found", {{ status: 404 }});
    }}
    if (pathname.startsWith("/audio/")) {{
      const name = pathname.slice("/audio/".length);
      if (AUDIO[name]) {{
        return new Response(b64ToBytes(AUDIO[name]), {{ headers: {{ "content-type": "audio/mpeg", "accept-ranges": "bytes", "cache-control": "public, max-age=31536000, immutable" }} }});
      }}
      return new Response("Not Found", {{ status: 404 }});
    }}
    const lang = resolveLang(request);
    const htmlHeaders = {{
      "content-type": "text/html;charset=UTF-8",
      "cache-control": "public, max-age=0, must-revalidate",
      "vary": "Accept-Language"
    }};
    if (pathname === "/privacy" || pathname === "/privacy.html") {{
      return new Response(PRIVACY_PAGES[lang] || PRIVACY_PAGES.en, {{ headers: htmlHeaders }});
    }}
    if (pathname === "/support" || pathname === "/support.html") {{
      return new Response(SUPPORT_PAGES[lang] || SUPPORT_PAGES.en, {{ headers: htmlHeaders }});
    }}
    return new Response(PAGES[lang] || PAGES.en, {{ headers: htmlHeaders }});
  }}
}};
"""
    (BASE_DIR / "worker.js").write_text(worker_js, encoding="utf-8")
    print(f"BUILT_WORKER: {len(worker_js) / 1024:.1f} KB")

    if "--no-deploy" in sys.argv:
        return

    token = os.environ.get("CF_API_TOKEN", "").strip()
    if not token:
        token = Path("~/.cf_token").expanduser().read_text().strip()
    deploy_worker(token, worker_js)
    ensure_dns_and_route(token)
    print("DEPLOY_COMPLETE:", ORIGIN)


if __name__ == "__main__":
    main()
