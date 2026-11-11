# NASA KrishiBondhu

Open `README_BANGLA.md` for the complete Bangla setup and run guide.

Project contents:
- `KrishiBondhuAndroid/` — native Android wrapper and farmer-facing mobile UI.
- `backend/` — FastAPI backend for NASA AppEEARS MODIS/ECOSTRESS sampling and the XEOI decision engine.
- `KrishiBondhuAndroid/AI_MODEL_CARD.md` — intended use, methods, assumptions and limitations of XEOI.
- `KrishiBondhuAndroid/NASA_DATA_SOURCES.md` — NASA products, parameters, cadence and data-quality notes.
- `render.yaml` — optional Render Blueprint deployment configuration. Confirm hosting costs before deployment.

The app requires real NASA observations; it does not substitute sample data when required sources are missing. Earthdata credentials belong only in private backend environment variables, never in the Android APK.


NASA GIBS imagery is available in the Satellite tab for visual context; numeric decision values continue to come from AppEEARS.
