# NASA KrishiBondhu — Mentor Demo Guide

## 5-minute demonstration

1. Open the Android app and choose a farm point (latitude/longitude).
2. Fetch live NASA POWER, SMAP L4 and GPM IMERG data directly from the phone.
3. Show retrieval time, requested period, observation counts and units.
4. Verify the team's HTTPS backend and Earthdata/AppEEARS credentials.
5. Submit the MODIS + ECOSTRESS point sample. Keep the app open while AppEEARS processes the task.
6. Show MODIS MOD13Q1.061 NDVI, its QA-accepted sample count, ECOSTRESS ECO_L3T_JET ETdaily, cloud/water QA acceptance and observation dates.
7. After all five NASA streams pass QA and the Claude backend key is active, generate the three XEOI rotation pathways plus Claude's farmer-readable crop recommendation.
8. Explain the source evidence, scoring components, missing data, benefits, risks and local validation needs.

## What to claim

- NASA POWER supplies meteorological context.
- SMAP L4 and GPM IMERG are requested through NASA POWER's high-resolution parameter pathway.
- MODIS MOD13Q1.061 and ECOSTRESS L3 JET are sampled through NASA AppEEARS with Earthdata authentication on the backend.
- XEOI is an explainable multi-sensor evidence-fusion decision-intelligence model with transparent multi-criteria scoring. It is not a supervised model trained on crop-yield labels.
- Scores describe relative screening/alignment, not probability of crop success or measured yield.
- Satellite point samples describe pixels around the coordinate, not the whole farm; the farmer should provide local soil-test data where available.

## Do not claim

- Do not call a dataset LIVE unless a real response was received and its non-zero, quality-accepted observation counts are shown.
- Do not claim MODIS/ECOSTRESS live before the AppEEARS task returns `status: live`.
- Do not claim the app predicts yield, guarantees profit, diagnoses crop disease or replaces agronomists.
- Do not claim a competition rank or that the prototype is field-validated.

## Required backend setup

The AppEEARS backend must be deployed to an HTTPS host and configured with private `NASA_EARTHDATA_USERNAME`, `NASA_EARTHDATA_PASSWORD`, and `ANTHROPIC_API_KEY` environment variables. Set `CHAT_MODEL=claude-sonnet-5-5`. The team must verify the credentials and a farm-specific point sample before presenting those streams as live. Never put credentials in the APK or public repository.

## Update: bilingual UI, scenario slider and AI assistant
- The app brand is NASA KrishiBondhu, and the home screen uses custom illustrated action tiles designed for lower reading burden.
- The app is bilingual (Bangla/English toggle). Bangla is the default.
- Full rotation advice is blocked unless POWER, SMAP, GPM, QA-screened MODIS and QA-screened ECOSTRESS data are available. No three-source or fake-data fallback is shown.
- Claude Sonnet 5.5 generates the farmer-facing recommendation and crop sequence only when the private backend ANTHROPIC_API_KEY is configured. The XEOI multi-sensor scoring remains transparent and is not represented as a trained yield prediction model.
- The AI chat includes all five NASA indicator summaries where available. Android speech recognition provides Bangla/English voice input; TTS playback depends on the phone having Bengali voice data installed.
- The what-if slider is an illustrative scenario test (soil moisture assumed to move at half the rainfall change), not a forecast.
