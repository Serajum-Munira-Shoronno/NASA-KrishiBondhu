# v1.3.4 — Local verification report

## Verified locally

- Backend source compiles with `python -m compileall`.
- Backend test suite: **23 passed**.
- Decision API integration test: with NASA POWER/SMAP/GPM data and 7 accepted MODIS + 29 accepted ECOSTRESS observations, `allowPartial=true` returns a `preliminary_three_source` result; `allowPartial=false` returns HTTP 409 and keeps full mode locked.
- MODIS layer resolver test: requests NDVI + pixel reliability + DetailedQA when all catalogue layers are available.
- MODIS QA tests: marginal class-1 pixels are accepted only after DetailedQA screening; cloudy/invalid classes are rejected; fill DN `-3000` is excluded and is not converted into a valid NDVI.
- Sampling period test: 36 means 36 calendar months, including end-of-month leap-year handling.
- Android WebView JavaScript: `node --check` passed.
- Android bridge source inspection: `allowPartial` is forwarded to `/api/decision/rotation`; the ancillary request sends `months: 36`.

## Not claimed as verified

- No live AppEEARS point task was submitted from this local audit; live Earthdata credentials are not present in this build environment.
- No live Anthropic API request was made; the deployed API key and account access are private to Render. The decision API integration was exercised with a mocked guidance response, and the Claude response validation tests are mocked.
- No Android APK build/install was run because this environment has no Android SDK. JavaScript syntax was checked, but that is not a substitute for a device build/run.
- No Render deployment was performed. The updated `backend/main.py` must be pushed and deployed before the current live backend can accept the `allowPartial` workflow.
