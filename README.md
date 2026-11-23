# EnglishGo — Travel English, 44 US/UK IPA Phonemes, 100 Real-Life Video Dialogues & Live Translation Website

Official marketing, studio audio & IPA preview, privacy policy, and support website for **EnglishGo** ([AE Interactive](https://appengine.fun)).

- **Live Website:** https://englishgo.appengine.fun
- **Privacy Policy:** https://englishgo.appengine.fun/privacy
- **Support:** https://englishgo.appengine.fun/support
- **App Source Repo:** https://github.com/movemove/EnglishGo

## Features
- **5 Languages Supported:** English (`/`), Traditional Chinese (`/?lang=zh-Hant`), Simplified Chinese (`/?lang=zh-Hans`), Español (`/?lang=es`), and 日本語 (`/?lang=ja`).
- **Real In-App Studio Audio Previews:** Native American English MP3 clips bundled in EnglishGo with US IPA transcription and linked sound highlights.
- **5 Screen Previews + iPhone Duo:** Optimized WebP screenshots for iPhone 6.9" and iPhone Duo inner foldable displays across `zh-Hant`, `zh-Hans`, `es-ES`, and `ja`.
- **Transparent Free vs. $3.99 Lifetime Pricing:** No subscriptions, no ads, zero tracking (`NSPrivacyTracking = false`).
- **Cloudflare Worker Edge Bundle:** Single-file deployment serving HTML, WebP screenshots, OG card, sitemap/robots, and studio MP3 clips at the edge.

## Build & Deploy
```bash
python3 prepare_assets.py
python3 build_and_deploy.py
```
