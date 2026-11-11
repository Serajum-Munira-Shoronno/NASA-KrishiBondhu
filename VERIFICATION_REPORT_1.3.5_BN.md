# v1.3.5 local verification

- Backend compileall: passed.
- Backend pytest: 24 passed, including a new test proving that only quality-accepted MODIS/ECOSTRESS date/value observations appear in plotted series; cloudy ECOSTRESS, MODIS reliability class 2 and MODIS fill DN are excluded.
- Android WebView JavaScript parsed with `node --check`: passed.
- Satellite view now has separate actual MODIS NDVI and ECOSTRESS ET time-series SVG charts when the backend returns dated series.
- Optional sample charts and sample advice preview are clearly watermarked; sample values do not modify global NASA state and are never passed into the decision API.
- Existing preliminary/full recommendation flow remains unchanged: preliminary uses POWER + SMAP + GPM; full XEOI requires all source and QA gates.

Not tested in this environment: live Render connectivity/deployment, live NASA AppEEARS task, Anthropic live call, Gradle APK build, and physical Android device run. The current environment could not resolve the Render host and has no Android SDK configured.
