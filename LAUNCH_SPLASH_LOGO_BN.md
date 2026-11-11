# v1.3.0 — Launch splash, animated tabs, new logo

## কী বদলেছে (শুধু এই তিনটি + একটি bug fix)
1. **২ সেকেন্ডের launch animation:** তারাভরা মহাকাশে ঘুরন্ত পৃথিবী (মহাদেশ ও মেঘ সরে যায়), কক্ষপথে ঘুরন্ত satellite, "আপনার জমি" চিহ্নে সবুজ ping, নাম ও tagline fade-in, নিচে ২ সেকেন্ডের progress bar। স্ক্রিনে ট্যাপ করলে skip হয়। Status/navigation bar splash-এর সময় গাঢ় নীল, শেষে আবার সাদা।
2. **Animated tab icons (লেখা না পড়েও চেনা যায়):** হোম = ধোঁয়া ওঠা ঘর · আমার জমি = মাঠ + লাফানো location pin · উপগ্রহ = পৃথিবীর ওপর দুলন্ত satellite + signal · কোন ফসল = বেড়ে ওঠা চারা + ঘুরন্ত সূর্য · AI সহায়ক = মাইক্রোফোনসহ কথার বুদবুদ + শব্দ-তরঙ্গ। সক্রিয় tab-এর আলাদা রং, বড় icon ও নিচে দাগ। Android-এর "reduce motion" পছন্দ মানা হয়।
3. **নতুন logo:** সূর্য + মেঘ + সারি-দেওয়া ফসলের মাঠ + কক্ষপথে satellite। Launcher icon (`ic_launcher.xml`), app header ও presentation-এর জন্য `KrishiBondhu_logo.png/.svg`।
4. **Bug fix:** `AndroidManifest.xml`-এ `TTS_SERVICE` query যোগ করা হয়েছে। এটি ছাড়া Android 11+ ফোনে বাংলা "পড়ে শোনাও" (Text-to-Speech) চালু নাও হতে পারত।

versionCode 4 / versionName 1.3.0 (পুরোনো install-এর ওপর update হবে; uninstall করবেন না)।

## বাকি সব আগের Final Release-এর মতোই আছে
Backend, XEOI, crop-intelligence database, AI chat, voice — কিছুই বদলানো হয়নি।
