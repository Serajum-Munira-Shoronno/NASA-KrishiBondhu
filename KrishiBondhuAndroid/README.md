# NASA KrishiBondhu Android Application

A native Android shell with a locally bundled farmer-friendly UI based on the team's simple green/white card design. It does not open Chrome. The app runs on an Android phone without the developer PC once installed.

## Features

- Farmer profile stored locally on the phone (farm name, coordinates, current crop, crop history, soil test fields, irrigation availability and priorities).
- Direct live NASA POWER Daily API calls from the Android device:
  - POWER meteorology: `T2M`, `T2M_MAX`, `PRECTOTCORR`, `RH2M`, `ALLSKY_SFC_SW_DWN`.
  - SMAP L4 high-resolution hydrology aliases: `SFMC`, `RZMC`, `PRMC`.
  - GPM IMERG daily precipitation: `IMERG_PRECTOT`, aggregated to complete monthly totals.
- Secure team-backend bridge for AppEEARS:
  - MODIS/Terra MOD13Q1.061 NDVI and quality layer.
  - ECOSTRESS L3 JET ETdaily, cloud/water masks and uncertainty if exposed by the current AppEEARS product catalogue.
- XEOI backend decision engine returns three crop-rotation pathways, source-level evidence, benefits, risks, score components and limitations.
- No synthetic NASA data fallback. Missing/insufficient required observations block AI recommendations.
- Farm and results persist in Android WebView local storage.

## Important setup requirement for MODIS/ECOSTRESS and XEOI

The Android app can fetch POWER/SMAP/GPM directly. **MODIS and ECOSTRESS AppEEARS sampling and the XEOI decision endpoint require a deployed HTTPS FastAPI backend.** The team configures the backend URL under Settings (⚙). Earthdata username/password are stored only as private environment variables on the backend host and must never be placed in the APK.

Without the deployed backend and valid Earthdata credentials, MODIS/ECOSTRESS cannot be sampled and the XEOI action stays disabled. This is intentional; the app does not fabricate results.

## Build on Windows

- Android Studio stable
- Android SDK Platform 35
- Android SDK Build-Tools 35.0.0
- Android SDK Platform-Tools and Command-line Tools
- Gradle wrapper 8.11.1, AGP 8.9.1, JDK 17

Open this `KrishiBondhuAndroid` folder in Android Studio, Sync Gradle, connect phone with USB debugging, select the phone and press Run. Create APK through Build → Build Bundle(s) / APK(s) → Build APK(s).

For complete backend setup, Earthdata configuration and mentor demo flow, read `../README_BANGLA.md` and `../backend/DEPLOY_BACKEND.md`.
