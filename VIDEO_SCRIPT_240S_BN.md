# NASA KrishiBondhu — 4-minute demo video script

**Format:** 9:16 vertical phone screen recording, 1080×1920 if available. Keep taps slow enough to read. Use the actual phone and live backend response. Do not stage fake NASA values.

| Time | Screen action | Voice-over (Bangla) |
|---|---|---|
| 0:00–0:18 | App launch; show KrishiBondhu logo and illustrated home tiles | “বাংলাদেশের কৃষকের জন্য NASA-র পৃথিবী পর্যবেক্ষণ তথ্য ব্যবহার করে তৈরি NASA কৃষিবন্ধু। কম লেখা, পরিচিত ছবি আর সহজ বাংলায় জমির সিদ্ধান্ত বুঝতে সাহায্য করে।” |
| 0:18–0:42 | Tap My Farm; show district, coordinates, current crop, irrigation and priority fields | “প্রথমে কৃষক জমির অবস্থান, বর্তমান ফসল, পানির অবস্থা এবং নিজের লক্ষ্য নির্বাচন করেন। মাটির পরীক্ষার তথ্য জানা না থাকলে ফাঁকা রাখা যায়।” |
| 0:42–1:06 | Save farm; show satellite tab, POWER/SMAP/GPM retrieval button | “এরপর NASA POWER থেকে আবহাওয়া ও তাপমাত্রা, SMAP থেকে মাটির পানির অবস্থা, এবং GPM থেকে বৃষ্টির তথ্য আনা হয়। এগুলো গ্রিডভিত্তিক satellite বা model estimate—জমির হাতে ধরা মাপ নয়।” |
| 1:06–1:38 | Tap advanced NASA fetch; show task submitted/polling; then MODIS and ECOSTRESS metrics | “NASA AppEEARS দিয়ে MODIS-এর NDVI এবং ECOSTRESS-এর evapotranspiration তথ্য নেওয়া হয়। Cloud ও water quality mask দিয়ে খারাপ observation বাদ দেওয়া হয়। কম observation থাকলে অ্যাপ সেটিকে live বলে না।” |
| 1:38–2:05 | Show five source values, quality accepted counts and dates | “এখানে MODIS NDVI ও ECOSTRESS ET-এর তারিখভিত্তিক chart এবং QA accepted count দেখা যায়। কোনো উৎসে observation কম হলে পূর্ণাঙ্গ XEOI বন্ধ থাকে; তবে প্রাথমিক ৩-source পরামর্শ আলাদা করে পাওয়া যায়।” |
| 2:05–2:42 | Tap advice; generate; show month-filtered crop cards and the three pathways | “এই release-এ বাংলাদেশি reference crop calendar দিয়ে নির্বাচিত মাসের ফসল বাছাইয়ের আগে screening হয়। মাটির ধরন, pH, lab-এর NPK, drainage, salinity, আগের crop family ও পানির অবস্থা candidate rank-এ প্রভাব ফেলে। XEOI তিনটি pathway তুলনা করে; Claude Sonnet 5.5 যাচাইকৃত crop candidate-এর কারণ সহজ বাংলায় ব্যাখ্যা করে।” |
| 2:42–3:10 | Open strategy details; show NASA evidence, soil flags, crop card source and BARC portal link | “প্রতিটি pathway-এর score, সুবিধা, ঝুঁকি এবং কোন NASA evidence ব্যবহার হয়েছে তা খোলা যায়। Crop card-এ বপনের মাস, পরিবার, পানির চাহিদা ও source link আছে। BARC-এর district-upazila suitability portal-এ শেষবার মিলিয়ে নিতে হবে। Score ফলন বা লাভের নিশ্চয়তা নয়।” |
| 3:10–3:34 | Show compare and what-if slider | “কৃষক তিনটি বিকল্প পাশাপাশি তুলনা করতে পারেন এবং বৃষ্টি বা তাপমাত্রা বদলালে screening score কেমন বদলায়, তা পরীক্ষা করতে পারেন।” |
| 3:34–3:52 | Open AI helper; tap microphone; ask a short Bangla question; play spoken reply | “AI সহায়কে কৃষক বাংলায় কথা বলেও প্রশ্ন করতে পারেন। উত্তরের লেখা দেখা যায়, আবার ফোনের Bengali voice support থাকলে শুনেও নেওয়া যায়।” |
| 3:52–4:00 | Return to home; close on app name | “NASA কৃষিবন্ধু—উপগ্রহের তথ্য, কৃষকের অভিজ্ঞতা এবং ব্যাখ্যাযোগ্য AI-কে এক জায়গায় আনার চেষ্টা।” |

## Required pre-record checks
- Confirm `/health` reports both `appeearsConfigured: true` and `aiConfigured: true`.
- Confirm the farm-specific AppEEARS task is `live`, and display actual MODIS and ECOSTRESS observation counts.
- Show the selected planting month and a plausible crop-candidate card; open at least one official source link and mention BARC district/upazila manual verification.
- Enter only verified soil-lab values in the displayed units; leave unknown fields blank.
- Use the real farm coordinate and remove any account/email/API secret from the recording.
- If any source is partial or the API fails, record that honestly and do not narrate it as successful.
- Show actual microphone permission and Bengali TTS behavior on the target phone.
- Export the 4-minute cut with captions; keep spoken Bengali simple and avoid fast transitions.


## Recording integrity
Use only live charts and API-generated advice for judge-facing evidence. The app has optional DEMO/SAMPLE previews for UI layout only; keep their watermark visible and do not narrate them as live NASA data or a farm-specific recommendation.
