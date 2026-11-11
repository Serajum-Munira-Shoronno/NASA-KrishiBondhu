# NASA KrishiBondhu — Final release চালানোর নির্দেশনা

এই release-এ Android app, secure NASA/Claude backend, Bangladesh crop-intelligence database এবং XEOI crop-rotation engine আছে। নিচের ধাপগুলো একবার ঠিকভাবে করলে একই build থেকে ফোনে demo করা যাবে।

## ১. Android app ফোনে চালান

1. `NASA_KrishiBondhu_Final_Release.zip` Extract করুন।
2. Android Studio → Open → `NASA_KrishiBondhu/KrishiBondhuAndroid` folder নির্বাচন করুন (যে folder-এর ভেতরে `settings.gradle.kts` আছে)।
3. JDK 17, Android SDK 35 এবং Gradle Sync সম্পন্ন করুন। প্রথমবার internet লাগবে।
4. ফোনে Developer options → USB debugging চালু করুন। USB লাগিয়ে ফোনে debugging permission Allow করুন।
5. Android Studio থেকে ফোন নির্বাচন করে সবুজ ▶ Run চাপুন।
6. APK তৈরির জন্য Build → Build Bundle(s) / APK(s) → Build APK(s)। APK থাকবে `KrishiBondhuAndroid/app/build/outputs/apk/debug/app-debug.apk`-এ।

পুরোনো prototype আগে uninstall করবেন না। Android application ID একই রাখা হয়েছে (`com.nexusfarm.mobile`), তাই একই PC-এর debug signing key হলে update install হতে পারে। Signing conflict হলে আগে phone-local farm data backup নিন।

## ২. Backend ও credentials configure করুন

ফোনে App-এর ⚙ Settings → Team server URL-এ Render-এর HTTPS base URL দিতে হবে। কিন্তু তার আগে `backend/` deploy করতে হবে।

1. সম্পূর্ণ Extracted project GitHub repository-তে upload করুন; root-এ `render.yaml`, `backend/`, `KrishiBondhuAndroid/` রাখুন।
2. Render → New → Blueprint → repository connect করুন। `krishibondhu-earth-observation-api` service review করে deploy করুন।
3. Render-এর private Environment-এ দিন:
   - `NASA_EARTHDATA_USERNAME`
   - `NASA_EARTHDATA_PASSWORD`
   - `ANTHROPIC_API_KEY`
   - `CHAT_MODEL=claude-sonnet-5-5`
4. Render plan ও persistent disk-এর বর্তমান charge দেখে deploy confirm করুন। NASA/Anthropic key কখনো APK, GitHub বা chat-এ দেবেন না।
5. Browser-এ `https://YOUR-SERVICE.onrender.com/health` খুলুন। `appeearsConfigured: true` ও `aiConfigured: true` credential presence বোঝায়—live sample সফল হয়েছে, তা নয়।
6. App → ⚙ Settings-এ শুধু base URL দিন, যেমন `https://your-service.onrender.com`। `/health` যোগ করবেন না। Verify server চাপুন।

## ৩. Farmer profile দিন

- জমির নাম, গ্রাম/উপজেলা/জেলা এবং latitude/longitude দিন। area picker-এর স্থানাঙ্ক আনুমানিক; সম্ভব হলে field GPS coordinate ব্যবহার করুন।
- বর্তমান ফসল, আগের ফসলের ইতিহাস, কোন মাসে বপন/রোপণ করবেন, soil texture, পানি, drainage, salinity ও farmer priority নির্বাচন করুন।
- soil lab value জানা না থাকলে ফাঁকা রাখুন। Fixed units:
  - pH: unitless
  - Organic matter: %
  - Total nitrogen: %
  - Available phosphorus: mg/kg
  - Exchangeable potassium: cmol(+)/kg
- রিপোর্টে একক ভিন্ন হলে সরাসরি সংখ্যা বসাবেন না; আগে lab/extension officer-এর কাছ থেকে conversion নিশ্চিত করুন।

## ৪. NASA data ও crop advice আনুন

1. Satellite tab → NASA POWER + SMAP + GPM fetch করুন।
2. একই tab-এ MODIS + ECOSTRESS AppEEARS sample request দিন। App task status poll করবে; কয়েক মিনিট সময় লাগতে পারে। App বন্ধ করবেন না।
3. MODIS-এ অন্তত ৮টি QA-accepted NDVI observation এবং ECOSTRESS-এ অন্তত ৪টি cloud/water mask দিয়ে গৃহীত ET observation লাগবে। না হলে partial status থাকবে।
4. Advice tab → Generate advice চাপুন। POWER, SMAP, GPM, MODIS, ECOSTRESS-এর valid observations/metrics, অন্তত একটি crop candidate এবং Claude key না থাকলে পূর্ণ plan blocked থাকবে। এই gate নকল NASA সংখ্যা ঠেকানোর জন্য।
5. Candidate card-এ crop family, water need, root type, planting month, duration, fit score, caution ও source link দেখুন। তিনটি pathway তুলনা করুন; final planting decision-এর আগে BARC/স্থানীয় কৃষি কর্মকর্তার সঙ্গে মিলিয়ে নিন।

## ৫. Final release-এ যুক্ত সিদ্ধান্ত-সহায়ক উন্নতি

- ১৪টি Bangladesh crop/season entry: Aman/Boro/Aus rice, lentil, mustard, wheat, Rabi/Kharif maize, Kharif-1/Kharif-2/coastal-Rabi mung, Rabi/Kharif-2 soybean, potato।
- কেবল selected month-এর জন্য candidate; উপকূলীয় Rabi mung দেশের অন্য অঞ্চলে দেখানো হয় না।
- Soil texture, pH, drainage, salinity, organic matter, total N, available P, exchangeable K, irrigation availability, crop history/family, farmer goal এবং NASA water/vegetation evidence candidate ranking-এ ব্যবহৃত হয়।
- অস্বাভাবিক soil number/unit scoring থেকে বাদ দিয়ে warning দেখানো হয়। Thresholdগুলো lab recommendation নয়—screening only।
- XEOI তিনটি বিকল্প দেয়: current-practice baseline, soil-health/legume pathway এবং water-smart pathway। AI শুধু catalogue-এ থাকা crop ব্যাখ্যা করতে পারে; নতুন crop বা sowing date বানাতে পারে না।
- Tabs ও home tiles-এ আলাদা illustration, soft motion ও বড় touch area আছে; ফোনে reduced-motion setting থাকলে animation কমে।
- AI chat-এ Bangla/English speech input এবং reply read-aloud Android voice service-এর ওপর নির্ভর করে।

## ৬. Demo-র আগে যা সত্যি করে পরীক্ষা করবেন

- Browser-এ `/api/nasa/appeears/verify` status verified কি না।
- নিজের test coordinate-এ POWER/SMAP/GPM ফিরছে কি না।
- AppEEARS task `live` হয়েছে কি না; product IDs, date range, MODIS/ECOSTRESS accepted count ও QA mask আছে কি না।
- AI decision response-এ crop candidate এবং strategy sequence বাস্তব input অনুযায়ী বদলাচ্ছে কি না।
- Bengali microphone permission ও TTS ফোনে কাজ করছে কি না।
- ভিডিওতে account/email/API secret লুকিয়ে রাখুন। NASA result live না হলে live বলে দেখাবেন না।

## ৭. গুরুত্বপূর্ণ সীমাবদ্ধতা

- BARC Crop Suitability portal-এ district/upazila, season ও crop বেছে manual verification করতে হবে; current version BARC-এর live upazila suitability score নিজে fetch করে না।
- Crop calendar একটি compact national reference screen; actual variety, sowing day, waterlogging/flood/salinity, pest/disease break, seed, market এবং local soil series কৃষি কর্মকর্তার সঙ্গে মিলিয়ে নিতে হবে।
- NASA satellite grids পুরো field-এর একক measurement নয়। MODIS NDVI crop শনাক্ত করে না; ECOSTRESS ET irregular overpass estimate।
- Scores relative screening indicator; yield/profit/crop-success probability নয়। এটি harvest labels-এ trained ML model নয়, explainable evidence-fusion/rule-based engine।
- Soil-test thresholds extraction method ও soil group অনুযায়ী বদলায়। Fertilizer dose দেয় না।

## ৮. Tests ও আরও তথ্য

Backend folder-এ:

```powershell
py -m pip install -r requirements.txt
py -m pip install pytest
py -m pytest -q tests
```

Detailed method/assumptions: `FINAL_RELEASE_BN.md` এবং `KrishiBondhuAndroid/AI_MODEL_CARD.md`। ৪ মিনিট ও ৩০ সেকেন্ডের recording storyboard: `VIDEO_SCRIPT_240S_BN.md`, `VIDEO_SCRIPT_30S_BN.md`। এগুলো script; finished video নয়।
