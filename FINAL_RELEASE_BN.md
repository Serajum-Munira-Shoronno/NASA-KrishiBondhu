# NASA KrishiBondhu — Final release 2026.11

## এই release-এ কী আছে

- বাংলা-প্রথম farmer UI; পাঁচটি navigation tab-এ আলাদা illustration, চলমান micro-animation, বড় touch target, স্পষ্ট icon ও gesture feedback। Android accessibility-র `prefers-reduced-motion` পছন্দ মানা হয়।
- জমির অবস্থান/স্থানাঙ্ক, বর্তমান ফসল, ফসলের ইতিহাস, বপনের মাস, মাটির ধরন, পানি, drainage, salinity এবং ঐচ্ছিক lab values।
- NASA POWER, SMAP L4, GPM IMERG; NASA AppEEARS দিয়ে MODIS MOD13Q1.061 NDVI এবং ECOSTRESS L3 JET ETdaily—প্রয়োজনীয় QA mask/quality layer সহ।
- Claude Sonnet 5.5 server-side AI assistant; বাংলা voice input ও response read-aloud Android bridge-এর মাধ্যমে।
- বাংলাদেশি crop-calendar screening database (১৪টি crop/season entry) এবং explainable crop-family / soil / water / calendar fit ranking।
- তিনটি তুলনা: existing farm practice baseline, soil-health/legume pathway এবং water-smart pathway।
- AI-কে শুধু candidate catalogue-এ থাকা crop বেছে ব্যাখ্যা করতে দেওয়া হয়; backend candidate ও strategy ID যাচাই করে।
- N, P, K-তে explicit unit labels; অস্বাভাবিক value/unit screening-এ বাদ পড়ে এবং UI-তে warning আসে।
- BARC Crop Suitability portal-এ district/upazila/season/crop নির্বাচন করে manual local verification-এর link।

## Crop-intelligence database-এর পরিধি

ডাটাবেসে Aman/Boro/Aus rice, lentil, mustard, wheat, Rabi/Kharif maize, Kharif-1/Kharif-2/coastal-Rabi mung, Rabi/Kharif-2 soybean এবং potato-এর sowing/planting month, crop family, আনুমানিক duration (যেখানে নির্ভরযোগ্য reference পাওয়া গেছে), water-demand class, soil texture screen, pH screen, drainage, root form, nutrient demand এবং official source links আছে।

এটি জাতীয় পর্যায়ের reference calendar screening; BARC-এর live district/upazila crop suitability database নয়। BARC-এর official portal-এ কৃষক/কৃষি-পরামর্শককে জেলা, উপজেলা, মৌসুম ও ফসল মিলিয়ে শেষ যাচাই করতে হবে। Crop variety, exact planting date, local flood/salinity, disease break, irrigation, seed supply ও market আলাদাভাবে যাচাই করতে হবে।

## মাটির তথ্যের একক

- pH: unitless
- Organic matter: %
- Total nitrogen (N): %
- Available phosphorus (P): mg/kg (ppm)
- Exchangeable potassium (K): cmol(+)/kg

ল্যাব রিপোর্টে ভিন্ন একক থাকলে সরাসরি মান বসানো যাবে না; ল্যাব/কৃষি কর্মকর্তার কাছ থেকে conversion নিশ্চিত করতে হবে। Threshold-গুলো screening flag মাত্র; extraction method, soil group এবং lab reference range অনুযায়ী BARC/SRDI-এর ব্যাখ্যাই চূড়ান্ত। এই অ্যাপ কোনো fertilizer dose দেয় না।

## XEOI-এর সীমা ও সততা

- NASA POWER, SMAP, GPM, MODIS ও ECOSTRESS—পাঁচটি উৎসে non-zero usable observation, MODIS quality layer-এ অন্তত ৮টি accepted observation এবং ECOSTRESS cloud/water mask-সহ অন্তত ৪টি accepted ET observation না এলে full plan তৈরি হবে না।
- Release 1.3.2-এ প্রাথমিক পরামর্শের আলাদা mode যোগ হয়েছে: পাঁচ-source gate পূরণ না হলে কেবল real POWER + SMAP + GPM observation, farmer input এবং crop calendar দিয়ে preliminary screen তৈরি হয়। এতে MODIS/ECOSTRESS scoring-এ ব্যবহৃত হয় না; ফলাফলে 3/5 source coverage ও preliminary limitation স্পষ্ট দেখানো হয়।
- MODIS NDVI vegetation greenness দেখায়; crop identity/রোগ নির্ণয় করে না।
- ECOSTRESS ET অনিয়মিত satellite overpass estimate; প্রতিদিনের মাঠ-পরিমাপ নয়। ET একা drought প্রমাণ করে না—rainfall/SMAP water deficit ও MODIS greenness decline একসঙ্গে থাকলে তবেই যৌথ signal হিসেবে ব্যবহৃত হয়।
- Satellite pixels/grids পুরো ছোট জমির একক field measurement নয়।
- Fit score তুলনামূলক screening score; yield, profit বা crop success probability নয়।
- কোনো labelled field harvest/soil-outcome dataset দেওয়া হয়নি; XEOI trained yield ML model নয়। এটি explainable evidence-fusion ও rule-based multi-criteria engine। Claude ফলাফল ব্যাখ্যা করে; অনুপস্থিত তথ্য/ফসল/পরিমাপ বানায় না।
- BARC district/upazila suitability app-এর ভিতরে live API দিয়ে আনা হয়নি; official portal-এ manual verification আবশ্যক।
- Real-world agronomist/field validation সম্পন্ন হয়েছে—এমন দাবি করা হচ্ছে না।

## NASA / official reference

- NASA POWER: https://power.larc.nasa.gov/
- NASA AppEEARS: https://appeears.earthdatacloud.nasa.gov/
- NASA MODIS MOD13Q1.061: https://doi.org/10.5067/MODIS/MOD13Q1.061
- NASA ECOSTRESS data: https://ecostress.jpl.nasa.gov/data/atbds-summary-table
- BARC Crop Suitability: https://portal.cropzoning.gov.bd/cropSuitability
- BARC Crop Zoning Information System: https://czis.cropzoning.gov.bd/
- Bangladesh Agricultural Information Service: https://ais.gov.bd/
- Bangladesh Rice Research Institute: https://brri.gov.bd/

## Deploy/build checklist

1. Render-এ backend deploy করুন; `NASA_EARTHDATA_USERNAME`, `NASA_EARTHDATA_PASSWORD`, `ANTHROPIC_API_KEY` private environment variable-এ বসান। `CHAT_MODEL=claude-sonnet-5-5` রাখুন।
2. `/health` response-এ `appeearsConfigured` ও `aiConfigured` true দেখুন; এটি কেবল credential presence, live data check নয়।
3. Android Settings-এ HTTPS backend base URL দিন—`/health` suffix দেবেন না।
4. Verify server; এরপর POWER/SMAP/GPM fetch; তারপর MODIS/ECOSTRESS AppEEARS sampling সম্পন্ন করুন।
5. All five observations/QA pass হলে crop advice generate করুন। Crop list, month, soil screen, pathway and AI explanation-এ বাস্তব output মিলিয়ে দেখুন।
6. Android Studio-তে `KrishiBondhuAndroid` project খুলে Gradle Sync ও APK build করুন; ফোনে Bengali speech/TTS permission পরীক্ষা করুন।
7. Demo recording-এর আগে কেবল সত্যিকারের live observation-সহ নিজের test farm ব্যবহার করুন; sample field-কে NASA live data বলে দেখাবেন না।

## Tests

`backend/` ফোল্ডারে `pytest -q` চালান। Backend tests NASA product catalogue resolution, MODIS/ECOSTRESS QA parsing, five-source gating, cached evidence, Claude output validation, crop calendar filtering, coastal-only crop screening, soil-unit checks এবং crop candidate structure যাচাই করে।


## v1.3.5 video-preview note
Satellite tab can show actual dated QA-accepted MODIS/ECOSTRESS series when returned by the backend. An optional DEMO/SAMPLE chart and example-advice preview are explicitly watermarked and are not sent to or used by the advice engine. For judge-facing claims, use only live task output and an actual API-generated recommendation.
