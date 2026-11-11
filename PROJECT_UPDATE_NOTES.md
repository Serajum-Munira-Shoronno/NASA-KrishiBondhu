# NASA KrishiBondhu — Final release notes (2026.11)

## Final implementation
- Farmer-first Bangla UI, custom illustrated tabs/tiles, micro-animations, press feedback, larger touch areas and reduced-motion support.
- Android `versionCode=3`, `versionName=1.2.0`; application ID remains `com.nexusfarm.mobile` for compatible updates where the signing key is identical.
- Added 14 Bangladesh crop/season reference entries, month filtering, regional coastal crop guard, crop family/history, soil texture/pH/drainage/salinity, nutrient demand, roots and relative water-need screening.
- All five soil inputs have unit labels and broad plausibility guards; invalid values are excluded from scoring and returned as warnings. The thresholds remain screening-only and method-dependent.
- XEOI candidate ranking now uses NASA rainfall + SMAP and only combines ECOSTRESS ET decline when MODIS greenness and water-deficit evidence also co-occur. ET alone is not called drought.
- The crop candidate list and pathway crop are validated by backend before Claude explanation; the LLM cannot invent an unlisted crop or sowing month.
- The BARC district/upazila crop suitability page is linked for manual verification; it is not integrated as a live score API.
- Added crop calendar, lab unit and validation instructions plus refreshed video storyboards.

## Verification completed in this environment
- `pytest -q`: 15 backend tests passed.
- Python syntax compilation: passed.
- Front-end JavaScript syntax (`node --check`): passed.
- Backend Python syntax compilation (`main.py`, `crop_intelligence.py`): passed.
- API smoke checks: `/health` and `/api/crops/catalog` returned HTTP 200; the catalogue returned 14 crop/season entries.
- Android APK: not compiled in this environment. The Gradle wrapper could not download Gradle 8.11.1 because `services.gradle.org` DNS/network resolution failed. Build on a connected computer with Android SDK 35 and JDK 17.
- Live NASA Earthdata/AppEEARS and Claude requests: require the team's private credentials and deployed HTTPS backend; these are not claimed as live-tested.

## Required Render private environment variables
- `NASA_EARTHDATA_USERNAME`
- `NASA_EARTHDATA_PASSWORD`
- `ANTHROPIC_API_KEY`
- `CHAT_MODEL=claude-sonnet-5-5`

Never store the credentials in Android source, APK, GitHub, or any client-side setting.
