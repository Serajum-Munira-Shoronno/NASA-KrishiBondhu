# NASA KrishiBondhu FastAPI backend deployment

The app directly fetches POWER/SMAP/GPM. This backend is required for Earthdata-authenticated MODIS/ECOSTRESS AppEEARS sampling and server-side XEOI.

## Earthdata credentials

1. Create/verify an Earthdata Login account at https://urs.earthdata.nasa.gov/.
2. Check that the same account can access NASA AppEEARS at https://appeears.earthdatacloud.nasa.gov/.
3. Do not send credentials in chat, store them in the APK, or commit them to source control.

## Render Blueprint deployment

The repository root has `render.yaml`. It configures a Docker web service, health-check endpoint `/health`, and a 1 GB persistent disk at `/var/data` for AppEEARS task tracking. The configured Starter plan and persistent disk may incur a charge. Confirm current provider pricing before creating the service. A different HTTPS host is acceptable if it supports FastAPI, private environment variables and persistent storage (or a managed database).

1. Push the complete repository to a GitHub repository you control. Keep `render.yaml` at the repository root and `backend/` as a subfolder.
2. In Render choose **New + → Blueprint**, then connect the repository.
3. Review service name `krishibondhu-earth-observation-api`, Docker root directory `backend`, disk mount `/var/data`, and environment variable `NEXUS_DB_PATH=/var/data/krishibondhu_tasks.sqlite3`.
4. In the Render service dashboard set private environment variables:
   - `NASA_EARTHDATA_USERNAME`
   - `NASA_EARTHDATA_PASSWORD`
   - `ANTHROPIC_API_KEY`
5. Deploy and wait for the service to become healthy.
6. Open `https://YOUR-SERVICE.onrender.com/health`. `appeearsConfigured: true` only means both environment fields are present.
7. Open `https://YOUR-SERVICE.onrender.com/api/nasa/appeears/verify`. Only `status: verified` confirms Earthdata authentication and discovery of the configured MODIS/ECOSTRESS products/layers. This does not yet prove a farm data sample has completed.

## Configure Android

1. Build/install the updated `KrishiBondhuAndroid` app.
2. Open **Settings (⚙)**.
3. Enter the deployed HTTPS base URL under **Team backend HTTPS URL (setup only)**, with no trailing slash.
4. Save the URL.
5. NASA tab → `Fetch POWER, SMAP & GPM`.
6. NASA tab → `Fetch MODIS + ECOSTRESS`. AppEEARS sampling may take several minutes; keep the app open while it polls.
7. Confirm `status: live`, non-zero accepted counts, and QA layers in the NASA tab.
8. Rotation tab → `Generate explainable AI rotation plan`.

Do not ask farmers to enter Earthdata credentials. Before distributing a public farmer APK, preconfigure the team's backend URL in a release build and hide the development-only backend URL field.

## Local backend for API development

On Windows, copy `.env.example` to `.env` in `backend/`, edit that local file with the Earthdata Login values, then run `run_backend_windows.bat`. This starts at `http://127.0.0.1:8000` for local API testing. The Android native bridge intentionally requires an HTTPS backend URL; use a deployed HTTPS endpoint for phone/AppEEARS integration rather than exposing an unauthenticated local server.

## Endpoints

- `GET /health`
- `GET /api/nasa/appeears/verify`
- `POST /api/nasa/appeears/point`
- `GET /api/nasa/appeears/point/{task_id}`
- `POST /api/decision/rotation`
- Swagger: `/docs`

## AppEEARS processing details

- Earthdata Login produces an AppEEARS Bearer token on the backend.
- The backend paginates the AppEEARS product catalogue and reads live per-product layer metadata.
- It prefers MODIS `MOD13Q1.061` NDVI and DetailedQA/available quality layer.
- It prefers ECOSTRESS `ECO_L3T_JET.003`, or `.002` only when that is the available catalogue product, and requests ETdaily/cloud/water/uncertainty layers when present.
- The point-sample task is submitted and polled; CSV bundle results are downloaded after task completion.
- MODIS NDVI scaling and DetailedQA bit fields are processed. ECOSTRESS cloud/water flagged pixels are excluded.
- Advanced result status is `live` only with at least 8 QA-accepted MODIS observations and 4 QA-accepted ECOSTRESS overpasses plus all required quality fields. Otherwise it is `partial` and XEOI is blocked.

## Security and operational notes

This is a competition MVP. The MVP includes a basic in-memory per-IP AI request limit. Before public production, add distributed rate limiting, abuse prevention, user authentication/authorization, monitoring and a secrets-rotation procedure. The AppEEARS credentials are server-side, but the team backend endpoints are otherwise a public prototype. Persistent disk is used to keep task metadata during processing. Without persistence, a backend restart can lose the association between an AppEEARS task and the phone polling it.
