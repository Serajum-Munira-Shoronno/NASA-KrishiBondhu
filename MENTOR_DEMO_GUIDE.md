# NASA KrishiBondhu — Mentor Demo Guide

## 5-minute demonstration

1. Open the Android app and choose a farm point (latitude/longitude).
2. Fetch live NASA POWER, SMAP L4 and GPM IMERG data directly from the phone.
3. Show retrieval time, requested period, observation counts and units.
4. Verify the team's HTTPS backend and Earthdata/AppEEARS credentials.
5. Submit a NEW 36-calendar-month MODIS + ECOSTRESS point sample. Keep the app open while AppEEARS processes the task.
6. Show MODIS MOD13Q1.061 NDVI chart, its QA-accepted sample count and observation dates; then show ECOSTRESS ECO_L3T_JET ETdaily chart, cloud/water QA acceptance and irregular overpass dates. Re-fetch after the v1.3.5 backend deploy to receive the dated series.
7. Open Advice. If MODIS is below 8 accepted observations, generate a clearly labelled Preliminary 3/5-source recommendation from POWER + SMAP + GPM plus the farmer profile. If all five streams pass the required QA/count gates, generate Full 5/5 XEOI instead. Both require a working Claude backend key.
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
- Preliminary advice is available from verified POWER + SMAP + GPM and farmer inputs, with an explicit 3/5-source label. Full five-source XEOI remains blocked until MODIS/ECOSTRESS QA thresholds pass. Optional sample charts/result previews are watermarked DEMO and are never used in calculations; do not present them as live evidence.
- Claude Sonnet 5.5 generates the farmer-facing recommendation and crop sequence only when the private backend ANTHROPIC_API_KEY is configured. The XEOI multi-sensor scoring remains transparent and is not represented as a trained yield prediction model.
- The AI chat includes all five NASA indicator summaries where available. Android speech recognition provides Bangla/English voice input; TTS playback depends on the phone having Bengali voice data installed.
- The what-if slider is an illustrative scenario test (soil moisture assumed to move at half the rainfall change), not a forecast.


## v1.3.5 screen-recording sequence

- Start with the Farm tab and show the real farm profile/coordinate. Hide phone notifications and do not show account credentials.
- In Satellite, fetch NASA POWER/SMAP/GPM, then submit a NEW AppEEARS sample after the v1.3.5 backend is deployed. Wait until the task returns live or partial.
- Scroll to MODIS and ECOSTRESS. Show the QA-accepted counts, dates and separate charts. A partial result is still a valid display of the accepted observations; do not call it full coverage.
- In Advice, use Preliminary 3/5 when MODIS or ECOSTRESS is below threshold. Narrate that MODIS/ECOSTRESS are displayed as context but are excluded from the preliminary score. Use Full 5/5 only after both QA gates pass.
- The “Show sample charts” / “Preview example advice result” controls exist only to preview layout. If used in a design walkthrough, keep the DEMO / SAMPLE watermark visible and explicitly call them sample UI—not NASA results or a farm-specific recommendation. Do not use these samples as proof of challenge completion.
