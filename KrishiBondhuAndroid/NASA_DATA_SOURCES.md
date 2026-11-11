# NASA Earth-observation data sources used by NASA KrishiBondhu

## 1. NASA POWER Daily API

Daily point requests provide broad meteorological context: air temperature, precipitation, humidity and surface solar radiation. POWER values are gridded/reanalysis-derived products; they are not in-field weather-station observations.

Endpoint: `https://power.larc.nasa.gov/api/temporal/daily/point`

## 2. NASA SMAP L4 via NASA POWER high-resolution hydrology aliases

The Android client requests `SFMC`, `RZMC`, and `PRMC` via the POWER Daily endpoint. The app displays surface and root-zone moisture values and same-month root-zone anomaly. SMAP L4 is a satellite-constrained, model-assimilated gridded product (about 9 km support), not a probe installed in the farmer's field.

## 3. NASA GPM IMERG via NASA POWER

The Android client requests daily `IMERG_PRECTOT` from the POWER Daily API and aggregates daily precipitation into monthly totals. It compares 12 latest complete months with the previous 12 complete months. The GPM values are gridded estimates (about 0.1 degree / ~10 km), not rain-gauge readings.

## 4. NASA MODIS/Terra MOD13Q1.061

The AppEEARS backend requests NDVI and an associated quality layer (preferably DetailedQA). MOD13Q1.061 is a 250 m, 16-day vegetation-index composite. Raw integer NDVI values use scale factor 0.0001. DetailedQA is decoded, not treated as a simple boolean: MODLAND QA bits 0–1 and VI usefulness bits 2–5 are checked. The current implementation accepts MODLAND good-quality and usefulness class 0 or 1; other values are excluded. NDVI is a vegetation-greenness indicator, not crop identification or a diagnosis by itself.

NASA Earthdata DOI: https://doi.org/10.5067/MODIS/MOD13Q1.061
NASA AppEEARS API: https://appeears.earthdatacloud.nasa.gov/api/

## 5. NASA ECOSTRESS L3 JET

The AppEEARS backend searches the live product catalogue and prefers `ECO_L3T_JET.003`, falling back to `.002` only if that is the available collection. It requests `ETdaily`, cloud and water masks, and uncertainty if offered by the product metadata. ETdaily is a daytime-integrated evapotranspiration estimate in mm/day, based on irregular ISS overpasses. Cloud and open-water mask values of 1 are excluded; missing values are not interpolated or interpreted as zero ET. The current backend requires at least four QA-accepted overpasses for a usable trend summary.

NASA/JPL ECOSTRESS data guide: https://ecostress.jpl.nasa.gov/data/atbds-summary-table
NASA ECOSTRESS AppEEARS guide: https://github.com/nasa/ECOSTRESS-Data-Resources/blob/main/guides/appeears_ecostress.md
NASA AppEEARS API: https://appeears.earthdatacloud.nasa.gov/api/

## Multi-sensor decision use

- GPM rainfall change and SMAP root-zone moisture anomaly supply the primary water-deficit evidence.
- MODIS NDVI trend supplies vegetation-condition context.
- ECOSTRESS ET trend is only treated as a stress contributor when rainfall/SMAP deficit and vegetation decline also co-occur. Rising ET alone is not interpreted as stress.
- NASA POWER temperature provides broad heat/climate context.
- Soil pH, NPK, organic matter, crop history, water availability and farmer priorities come from the farmer or local soil tests—not from these satellite products.

## Data limitations

The products have different spatial resolutions, temporal cadence, footprints and quality characteristics. AppEEARS point samples describe pixels around one coordinate, not an entire field polygon. MODIS NDVI varies with crop phenology, planting/harvest dates, cloud and management; it cannot identify the crop. ECOSTRESS visits are irregular, and cloud gaps are common. The scoring model is an explainable screening system, not a trained yield predictor. Validate crop calendars, cultivar, market, irrigation and disease-break constraints with local agronomists.


## 6. NASA Global Imagery Browse Services (GIBS) — visual layer

The Android Satellite tab displays NASA GIBS WMS 1.1.1 imagery using EPSG:4326 around the saved coordinate. Available layers: `MODIS_Terra_CorrectedReflectance_TrueColor`, `MODIS_Terra_NDVI_8Day`, and `MODIS_Terra_Land_Surface_Temp_Day`. The viewer supports NASA's default date or a user-selected date, plus pan and zoom controls.

GIBS imagery is a pre-generated visualization for visual exploration. Its colourized NDVI/LST images are not parsed into decision values and must not be confused with the numeric AppEEARS MODIS MOD13Q1.061 / ECOSTRESS L3 JET observations used by the app. The centre marker is the saved coordinate, not a verified field polygon.

NASA GIBS documentation: https://nasa-gibs.github.io/gibs-api-docs/
NASA GIBS WMS and time dimension: https://nasa-gibs.github.io/gibs-api-docs/access-basics/
NASA GIBS acknowledgement: imagery from NASA Global Imagery Browse Services (GIBS), part of NASA Earth Science Data and Information System (ESDIS).
