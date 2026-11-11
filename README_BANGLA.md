# NASA KrishiBondhu — Android + NASA Earth Observation + AI Crop Advice

> **নতুন ফাইনাল ভার্সনের জন্য আগে `START_HERE_BANGLA.md` পড়ুন।** নিচের নির্দেশনা ব্যাকএন্ড সেটআপের জন্য এখনও প্রযোজ্য।

এই ZIP-এ Android app source project এবং MODIS/ECOSTRESS-এর জন্য secure FastAPI backend—দুটিই আছে। Farmer-facing UI নতুন করে picture-led, বড় touch target, সহজ বাংলা label ও voice prompt/read-aloud control-সহ সাজানো হয়েছে।

## আগে জেনে নিন

- Android app নিজে থেকেই NASA POWER-এর Daily API ব্যবহার করে temperature, SMAP L4 moisture aliases এবং GPM IMERG daily precipitation নেয়।
- MODIS ও ECOSTRESS data NASA AppEEARS থেকে নিতে **public HTTPS backend** দরকার। Earthdata username/password APK-তে রাখা হয় না; backend host-এর private environment variables-এ রাখতে হয়।
- Backend deploy না করা পর্যন্ত MODIS/ECOSTRESS fetch এবং XEOI AI rotation generation কাজ করবে না। শুধু Android APK install করলেই AppEEARS credentials নিরাপদে ব্যবহার করা সম্ভব নয়।
- এই ZIP থেকে APK compile করা হয়েছে বলে দাবি করা হচ্ছে না। আপনার Android Studio-তে project sync/build করতে হবে।
- XEOI হলো explainable multi-sensor evidence-fusion screening model; এর উপর Claude Sonnet 5.5 পাঁচটি NASA stream এবং farmer profile দেখে সহজ ভাষায় পরবর্তী ফসল/rotation guidance তৈরি করে। এটি field-yield label দিয়ে train করা supervised ML model নয়।

## Final release crop intelligence

`backend/crop_intelligence.py` contains a Bangladesh reference calendar with 14 crop/season entries. Candidate ranking filters by the selected planting month and uses crop family/history, soil texture, pH, drainage, salinity, unit-checked organic matter/N/P/K, irrigation access, farmer priorities and joint NASA water/vegetation signals. Three pathways include a current-practice baseline, a soil-health/legume option and a water-smart option. The selected crop is locked to an item in the verified candidate catalogue before Claude explanation is returned.

The BARC Crop Suitability portal is linked for farmer/extension-office verification by district and upazila; this version does not fetch BARC suitability results live. Soil thresholds are method-dependent screening flags only; no fertilizer dose, yield forecast or profit estimate is produced. Read `FINAL_RELEASE_BN.md` for the exact field units and limitations.

## ZIP structure

```text
KrishiBondhuAndroid/       Android Studio project (native Android + local WebView UI)
backend/                FastAPI AppEEARS integration + XEOI decision engine
render.yaml             Render Blueprint (paid persistent disk configuration)
README_BANGLA.md        এই নির্দেশনা
```

## Part A — Android app rebuild

1. এই ZIP Extract করুন।
2. Android Studio → Open → `KrishiBondhuAndroid` folder নির্বাচন করুন (যে folder-এর মধ্যে `settings.gradle.kts` আছে)।
3. Gradle Sync করুন। Project config: AGP 8.9.1, Gradle 8.11.1, compileSdk 35, Build Tools 35.0.0, Java 17।
4. USB Debugging চালু করে ফোন connect করুন।
5. Android Studio-তে নিজের ফোন নির্বাচন করে Run চাপুন। প্রথমবার microphone button চাপলে RECORD_AUDIO permission দিতে হবে। একই application ID ও একই PC-এর debug signing key হলে পুরোনো debug app update হবে; uninstall আগে করবেন না, কারণ uninstall করলে phone-local farm data মুছে যেতে পারে।
6. APK বানাতে Build → Build Bundle(s) / APK(s) → Build APK(s)।

## Part B — NASA Earthdata/AppEEARS backend

### 1) Earthdata Login

- https://urs.earthdata.nasa.gov/ এ account তৈরি/যাচাই করুন।
- https://appeears.earthdatacloud.nasa.gov/ এ একই account দিয়ে sign in করতে পারেন কি না যাচাই করুন।
- Username/password কাউকে chat-এ পাঠাবেন না এবং Android APK/GitHub-এ রাখবেন না।

### 2) Backend deploy (Render Blueprint path)

Render Blueprint একটি public HTTPS API তৈরি করবে। `render.yaml`-এ Starter web service এবং 1 GB persistent disk সেট করা আছে; এই plan/disk-এ charge হতে পারে—deploy confirm করার আগে Render-এর বর্তমান pricing দেখে নিন।

1. পুরো ZIP-এর contents নিজের GitHub repository-তে upload করুন। Root-এ `render.yaml`, `backend/` এবং `KrishiBondhuAndroid/` রাখুন।
2. Render → New → Blueprint → repository connect করুন।
3. Blueprint-এ `krishibondhu-earth-observation-api` service review করুন।
4. Render service-এর Environment-এ private secret হিসেবে `NASA_EARTHDATA_USERNAME` ও `NASA_EARTHDATA_PASSWORD` দিন।
5. Render Environment-এ `ANTHROPIC_API_KEY` হিসেবে Anthropic Console থেকে নেওয়া API key দিন। `CHAT_MODEL=claude-sonnet-5-5` রাখুন। এই key কখনো APK বা GitHub-এ রাখবেন না।
6. Deploy করুন।
7. Deploy শেষ হলে এই URL browser-এ খুলুন:
   - `https://YOUR-SERVICE.onrender.com/health`
   - `https://YOUR-SERVICE.onrender.com/api/nasa/appeears/verify`
8. `/health`-এ `appeearsConfigured: true` এবং `aiConfigured: true`—দুটিই দেখতে হবে। এগুলো credentials সেট আছে বোঝায়, data retrieval বা AI call সফল হয়েছে—এমন নয়। `/api/nasa/appeears/verify`-তে `status: verified` এলে Earthdata login এবং MODIS/ECOSTRESS product/layer discovery যাচাই হয়েছে। এটি farm-এর জন্য observation sample করা হয়েছে—এমন প্রমাণ নয়।

### 3) Android app-এ backend URL

1. Android app খুলুন → My Farm।
2. `Team backend HTTPS URL (setup only)` field-এ Render HTTPS base URL দিন—শেষে slash ছাড়া। উদাহরণ: `https://your-service.onrender.com`
3. Farm details Save করুন।
4. NASA tab-এ `Fetch POWER, SMAP & GPM` চাপুন।
5. এরপর `Fetch MODIS + ECOSTRESS` চাপুন। App AppEEARS point-sampling task জমা দেবে এবং status poll করবে। 24-month sample কয়েক মিনিট নিতে পারে। App বন্ধ করবেন না।
6. NASA tab-এ MODIS ও ECOSTRESS-এর accepted QA observation count দেখুন। অন্তত 8 MODIS এবং 4 ECOSTRESS accepted observations ও expected QA columns না থাকলে status `partial` হবে এবং AI decision ইচ্ছাকৃতভাবে blocked থাকবে।
7. পাঁচটি source live এবং Anthropic API key active হলে পরামর্শ tab → `AI দিয়ে পরামর্শ তৈরি করুন` চাপুন। Claude crop candidate, sequence, next steps ও caution দেখাবে।

### 4) Local backend (API testing only)

Windows PowerShell:

```powershell
cd backend
Copy-Item .env.example .env
notepad .env
```

`.env`-এ নিজের Earthdata username/password locally বসান। তারপর:

```powershell
.\run_backend_windows.bat
```

এই local backend `http://127.0.0.1:8000`-এ চলবে। কিন্তু Android native bridge নিরাপত্তার জন্য HTTPS backend URL গ্রহণ করে। তাই public phone demo-র জন্য deployed HTTPS endpoint ব্যবহার করুন। Local backend-কে farmers-এর জন্য public করবেন না।

## NASA product pipeline

| Source | Product / parameter | App-এ ব্যবহৃত তথ্য |
|---|---|---|
| NASA POWER | Daily T2M, T2M_MAX, PRECTOTCORR, RH2M, ALLSKY_SFC_SW_DWN | Weather/climate context |
| NASA SMAP L4 via POWER | SFMC, RZMC, PRMC aliases | Surface/root-zone/profile soil moisture |
| NASA GPM IMERG via POWER | IMERG_PRECTOT daily | Complete monthly totals and 12-month comparison |
| NASA MODIS/Terra | MOD13Q1.061 NDVI + DetailedQA/quality layer | 250 m, 16-day vegetation index trend |
| NASA ECOSTRESS | ECO_L3T_JET.003 if catalogued, otherwise .002; ETdaily + cloud/water masks + uncertainty if available | 70 m daytime ET observations at irregular ISS overpasses |

AppEEARS product list is paginated; the backend walks the product catalogue and resolves layer names from the live product metadata rather than hard-coding unverified aliases. MODIS NDVI uses the documented 0.0001 scale factor for raw integer values. DetailedQA is decoded (MODLAND QA bits 0–1 and VI usefulness bits 2–5); bad/low quality values are excluded. ECOSTRESS cloud and water masks must be present; values flagged as cloud or open water are excluded. A missing/cloudy ECOSTRESS overpass is never treated as zero ET.

## XEOI decision engine

KrishiBondhu Explainable Earth Observation Intelligence (XEOI) fuses:

- rainfall anomaly/change from GPM IMERG,
- SMAP L4 root-zone moisture anomaly,
- NASA POWER temperature context,
- MODIS QA-screened NDVI trend,
- ECOSTRESS QA-screened ETdaily trend,
- farmer crop history, soil-test entries, water availability and priorities.

It returns three pathways: existing rotation baseline, soil-improvement/legume option, and water-resilient option. Candidate crops are filtered using the selected month and Bangladesh crop reference calendar; candidates are scored using soil texture, pH, drainage, salinity, N/P/K, crop family/history, farmer water access and crop characteristics. It includes scores, source-level evidence, benefits, risks and limitations. It is an explainable screening model—not a trained yield-prediction model and not an agronomic prescription. Scores are relative prioritization indicators; they are not probabilities of crop success. The crop database is a national reference screen rather than a live BARC district/upazila rating.

## Before mentor demonstration

- Run `/api/nasa/appeears/verify` and save the result (remove any account/private details).
- On the Android phone, retrieve POWER/SMAP/GPM for the actual demo coordinates.
- Retrieve AppEEARS MODIS/ECOSTRESS and show the product IDs, date range, observation counts and QA accepted/rejected counts.
- Generate the three XEOI pathways and show evidence + risk explanations.
- State any missing data honestly. Do not label MODIS/ECOSTRESS as live unless AppEEARS returns QA-accepted observations.
- Say clearly that the decision tool supports—not replaces—farmer judgement and local agronomist validation.

## নতুন UI ও AI voice workflow

- Home screen-এর প্রতিটি কাজের tile-এ আলাদা hand-drawn SVG crop / water / chat / book / weather illustration আছে, যাতে কম পড়েও কাজ চেনা যায়।
- Brand: **NASA KrishiBondhu / নাসা কৃষিবন্ধু**। Android package ID আগেরটাই রাখা হয়েছে, যাতে debug build আগের install-এর ওপর update করা যায়।
- AI সহায়ক tab-এ microphone button চাপলে Android speech recognition Bengali (`bn-BD`) বা English (`en-US`) voice input নেবে। স্বীকৃত লেখা পাঠানোর আগে farmer edit করতে পারবেন।
- AI reply-এর নিচে `উত্তর শুনুন` button থাকবে। ফোনে Bengali Text-to-Speech voice না থাকলে Android Text-to-Speech settings থেকে Bengali voice install করতে হবে।
- `/api/chat`-এ NASA POWER/SMAP/GPM-এর পাশাপাশি QA-screened MODIS NDVI ও ECOSTRESS ET summary পাঠানো হয়।
- Rotation recommendation শুধুমাত্র five-source QA gate pass করলে তৈরি হয়। Claude Sonnet 5.5 pathway score বদলায় না; score/evidence ধরে farmer-friendly crop candidate, sequence, steps ও cautions দেয়।
- AppEEARS-এ অন্তত 8টি QA-accepted MODIS observation এবং 4টি QA-accepted ECOSTRESS observation না থাকলে পূর্ণ advice blocked থাকবে—কোনো sample/fake NASA data দিয়ে fallback হবে না।

## Video recording checklist

`VIDEO_SCRIPT_240S_BN.md`-এ 4-minute demo storyboard এবং `VIDEO_SCRIPT_30S_BN.md`-এ 30-second teaser narration দেওয়া আছে। এগুলো script/storyboard; এই ZIP থেকে কোনো screen recording বা finished video তৈরি করা হয়নি।

## Tests

From `backend/` with Python installed:

```powershell
py -m pip install -r requirements.txt
py -m pip install pytest
py -m pytest -q tests
```

These tests validate parsing, QA logic, product catalogue pagination, decision gating, three-strategy generation, crop-month filtering, coastal-region screening, soil-unit guards and the crop catalogue using test fixtures. They do **not** prove that the user's Earthdata credentials, AppEEARS access, a particular farm coordinate or the deployed host has returned live NASA observations. Those must be verified using the deployed backend and the Android phone.


Satellite ট্যাবে NASA GIBS-এর আসল উপগ্রহের ছবি দেখা যায়; সিদ্ধান্তের সংখ্যাগত মান AppEEARS থেকেই আসে।
