package com.nexusfarm.mobile;

import android.app.Activity;
import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.speech.RecognizerIntent;
import android.speech.tts.TextToSpeech;
import android.widget.Toast;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.view.Window;
import android.view.WindowManager;
import android.graphics.Color;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.time.YearMonth;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MainActivity extends Activity {
    private WebView webView;
    private TextToSpeech textToSpeech;
    private String pendingVoiceCallback = "";
    private String pendingVoiceLanguage = "bn-BD";
    private static final int VOICE_REQUEST_CODE = 721;
    private static final int AUDIO_PERMISSION_REQUEST_CODE = 722;
    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        applyBars(true); // dark space-blue bars while the launch splash plays
        webView = new WebView(this);
        webView.setBackgroundColor(Color.rgb(8, 21, 48));
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.getSettings().setDatabaseEnabled(true);
        webView.getSettings().setAllowFileAccess(true);
        webView.getSettings().setAllowContentAccess(false);
        webView.setWebChromeClient(new WebChromeClient());
        webView.setWebViewClient(new WebViewClient());
        webView.addJavascriptInterface(new AndroidBridge(), "NexusNative");
        textToSpeech = new TextToSpeech(this, status -> {
            if (status == TextToSpeech.SUCCESS && textToSpeech != null) {
                textToSpeech.setLanguage(new Locale("bn", "BD"));
            }
        });
        setContentView(webView);
        webView.loadUrl("file:///android_asset/index.html");
        webView.postDelayed(() -> applyBars(false), 3500); // safety: always return to light bars
    }

    private void applyBars(boolean dark) {
        Window w = getWindow();
        int c = dark ? Color.rgb(8, 21, 48) : Color.WHITE;
        w.setStatusBarColor(c);
        w.setNavigationBarColor(c);
        w.getDecorView().setSystemUiVisibility(dark ? 0 :
                (android.view.View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR | android.view.View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR));
    }

    @Override public void onBackPressed() {
        webView.evaluateJavascript("(window.nexusBack ? window.nexusBack() : false)", value -> { if (!"true".equals(value)) finish(); });
    }

    @Override protected void onDestroy() {
        executor.shutdownNow();
        if (textToSpeech != null) { textToSpeech.stop(); textToSpeech.shutdown(); }
        if (webView != null) webView.destroy();
        super.onDestroy();
    }

    private class AndroidBridge {
        @JavascriptInterface public void fetchNasa(String requestJson) {
            String callback = "nasaCallback";
            final double lat, lon;
            try {
                JSONObject req = new JSONObject(requestJson);
                callback = req.optString("callbackId", "nasaCallback");
                lat = req.getDouble("latitude");
                lon = req.getDouble("longitude");
                if (lat < -60 || lat > 85 || lon < -180 || lon > 180) throw new IllegalArgumentException("Please enter valid farm coordinates.");
            } catch (Exception e) {
                sendResult(callback, errorJson("Invalid farm coordinates: " + e.getMessage()).toString());
                return;
            }
            final String callbackId = callback;
            executor.execute(() -> {
                String result;
                try { result = fetchNasaPower(lat, lon).toString(); }
                catch (Exception e) { result = errorJson(e.getMessage()).toString(); }
                sendResult(callbackId, result);
            });
        }
        @JavascriptInterface public void verifyBackend(String requestJson) {
            String callback = "backendVerify";
            try { callback = new JSONObject(requestJson).optString("callbackId", callback); }
            catch (Exception ignored) {}
            final String callbackId = callback;
            executor.execute(() -> {
                try {
                    JSONObject req = new JSONObject(requestJson);
                    String base = validateBackendUrl(req.optString("backendUrl", ""));
                    JSONObject response = requestJson("GET", base + "/api/nasa/appeears/verify", null);
                    sendBridgeResult("onBackendVerifyResult", callbackId, response.toString());
                } catch (Exception e) {
                    sendBridgeResult("onBackendVerifyResult", callbackId, errorJson(e.getMessage()).toString());
                }
            });
        }

        @JavascriptInterface public void submitAncillary(String requestJson) {
            String callback = "ancillarySubmit";
            try { callback = new JSONObject(requestJson).optString("callbackId", callback); }
            catch (Exception ignored) {}
            final String callbackId = callback;
            executor.execute(() -> {
                try {
                    JSONObject req = new JSONObject(requestJson);
                    String base = validateBackendUrl(req.optString("backendUrl", ""));
                    JSONObject payload = new JSONObject();
                    payload.put("latitude", req.getDouble("latitude"));
                    payload.put("longitude", req.getDouble("longitude"));
                    payload.put("months", req.optInt("months", 24));
                    JSONObject response = postJson(base + "/api/nasa/appeears/point", payload);
                    sendBridgeResult("onAncillarySubmitResult", callbackId, response.toString());
                } catch (Exception e) {
                    sendBridgeResult("onAncillarySubmitResult", callbackId, errorJson(e.getMessage()).toString());
                }
            });
        }

        @JavascriptInterface public void checkAncillary(String requestJson) {
            String callback = "ancillaryStatus";
            try { callback = new JSONObject(requestJson).optString("callbackId", callback); }
            catch (Exception ignored) {}
            final String callbackId = callback;
            executor.execute(() -> {
                try {
                    JSONObject req = new JSONObject(requestJson);
                    String base = validateBackendUrl(req.optString("backendUrl", ""));
                    String taskId = req.getString("taskId");
                    JSONObject response = requestJson("GET", base + "/api/nasa/appeears/point/" + enc(taskId), null);
                    sendBridgeResult("onAncillaryResult", callbackId, response.toString());
                } catch (Exception e) {
                    sendBridgeResult("onAncillaryResult", callbackId, errorJson(e.getMessage()).toString());
                }
            });
        }

        @JavascriptInterface public void runAiDecision(String requestJson) {
            String callback = "aiDecision";
            try { callback = new JSONObject(requestJson).optString("callbackId", callback); }
            catch (Exception ignored) {}
            final String callbackId = callback;
            executor.execute(() -> {
                try {
                    JSONObject req = new JSONObject(requestJson);
                    String base = validateBackendUrl(req.optString("backendUrl", ""));
                    JSONObject payload = new JSONObject();
                    payload.put("farm", req.getJSONObject("farm"));
                    payload.put("nasa", req.getJSONObject("nasa"));
                    payload.put("ancillary", req.getJSONObject("ancillary"));
                    payload.put("lang", req.optString("lang", "bn"));
                    JSONObject response = postJson(base + "/api/decision/rotation", payload);
                    sendBridgeResult("onAiDecisionResult", callbackId, response.toString());
                } catch (Exception e) {
                    sendBridgeResult("onAiDecisionResult", callbackId, errorJson(e.getMessage()).toString());
                }
            });
        }

        @JavascriptInterface public void startVoiceInput(String requestJson) {
            String callback = "voiceInput";
            String language = "bn-BD";
            try {
                JSONObject req = new JSONObject(requestJson);
                callback = req.optString("callbackId", callback);
                language = req.optString("language", language);
            } catch (Exception ignored) {}
            final String callbackId = callback;
            final String locale = language;
            runOnUiThread(() -> launchVoiceRecognition(callbackId, locale));
        }

        @JavascriptInterface public void speakText(String requestJson) {
            String speech = "";
            String language = "bn-BD";
            try {
                JSONObject req = new JSONObject(requestJson);
                speech = req.optString("text", "");
                language = req.optString("language", language);
            } catch (Exception ignored) {}
            final String text = speech;
            final String locale = language;
            runOnUiThread(() -> speakOutLoud(text, locale));
        }

        @JavascriptInterface public void splashDone() { runOnUiThread(() -> applyBars(false)); }

        @JavascriptInterface public String getPlatform() { return "android-native"; }
    }

    private void launchVoiceRecognition(String callbackId, String language) {
        pendingVoiceCallback = callbackId;
        pendingVoiceLanguage = language;
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO}, AUDIO_PERMISSION_REQUEST_CODE);
            return;
        }
        startVoiceActivity();
    }

    private void startVoiceActivity() {
        try {
            Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, pendingVoiceLanguage);
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, pendingVoiceLanguage);
            intent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1);
            intent.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, false);
            intent.putExtra(RecognizerIntent.EXTRA_PROMPT, pendingVoiceLanguage.startsWith("bn") ? "আপনার প্রশ্নটি বলুন" : "Speak your question");
            startActivityForResult(intent, VOICE_REQUEST_CODE);
        } catch (Exception e) {
            sendVoiceError("এই ফোনে speech recognition চালু করা যাচ্ছে না। Google speech service ইনস্টল/আপডেট করুন।");
        }
    }

    private void sendVoiceError(String message) {
        JSONObject payload = new JSONObject();
        try { payload.put("error", message); } catch (Exception ignored) {}
        sendBridgeResult("onVoiceResult", pendingVoiceCallback, payload.toString());
    }

    private void speakOutLoud(String text, String language) {
        if (textToSpeech == null || text == null || text.trim().isEmpty()) return;
        Locale target = language != null && language.toLowerCase().startsWith("bn")
                ? new Locale("bn", "BD") : Locale.US;
        int availability = textToSpeech.isLanguageAvailable(target);
        if (availability == TextToSpeech.LANG_NOT_SUPPORTED || availability == TextToSpeech.LANG_MISSING_DATA) {
            if (target.getLanguage().equals("bn")) target = new Locale("bn");
            availability = textToSpeech.isLanguageAvailable(target);
        }
        if (availability == TextToSpeech.LANG_NOT_SUPPORTED || availability == TextToSpeech.LANG_MISSING_DATA) {
            Toast.makeText(this, "বাংলা voice phone-এর Text-to-Speech settings থেকে install করুন।", Toast.LENGTH_LONG).show();
            return;
        }
        textToSpeech.setLanguage(target);
        textToSpeech.speak(text, TextToSpeech.QUEUE_FLUSH, null, "krishibondhu-answer");
    }

    @Override public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == AUDIO_PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                startVoiceActivity();
            } else {
                sendVoiceError("মাইক্রোফোন ব্যবহারের অনুমতি না দিলে কথা বলে প্রশ্ন করা যাবে না।");
            }
        }
    }

    @Override protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode != VOICE_REQUEST_CODE) return;
        if (resultCode == RESULT_OK && data != null) {
            ArrayList<String> matches = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
            if (matches != null && !matches.isEmpty()) {
                JSONObject payload = new JSONObject();
                try { payload.put("text", matches.get(0)); } catch (Exception ignored) {}
                sendBridgeResult("onVoiceResult", pendingVoiceCallback, payload.toString());
                return;
            }
        }
        sendVoiceError("কথা বোঝা যায়নি। আবার চেষ্টা করুন।");
    }

    private String validateBackendUrl(String raw) throws Exception {
        String base = raw == null ? "" : raw.trim().replaceAll("/+$", "");
        if (!base.startsWith("https://")) {
            throw new Exception("Enter the team's deployed HTTPS backend URL in My Farm settings. Earthdata credentials must stay on the backend, never in the APK.");
        }
        return base;
    }

    private JSONObject postJson(String url, JSONObject body) throws Exception {
        return requestJson("POST", url, body);
    }

    private JSONObject requestJson(String method, String urlString, JSONObject body) throws Exception {
        HttpURLConnection c = null;
        try {
            c = (HttpURLConnection) new URL(urlString).openConnection();
            c.setRequestMethod(method);
            c.setConnectTimeout(30000);
            c.setReadTimeout(120000);
            c.setRequestProperty("Accept", "application/json");
            c.setRequestProperty("User-Agent", "NASA-KrishiBondhu/2.0");
            if (body != null) {
                c.setDoOutput(true);
                c.setRequestProperty("Content-Type", "application/json; charset=utf-8");
                byte[] data = body.toString().getBytes(StandardCharsets.UTF_8);
                c.getOutputStream().write(data);
                c.getOutputStream().close();
            }
            int code = c.getResponseCode();
            BufferedReader r = new BufferedReader(new InputStreamReader(code >= 200 && code < 300 ? c.getInputStream() : c.getErrorStream(), StandardCharsets.UTF_8));
            StringBuilder b = new StringBuilder(); String line;
            while ((line = r.readLine()) != null) b.append(line);
            r.close();
            JSONObject response;
            try { response = new JSONObject(b.toString()); }
            catch (Exception parseError) { throw new Exception("Backend returned non-JSON response (HTTP " + code + "). Check backend URL and deployment logs."); }
            if (code < 200 || code >= 300) {
                Object detail = response.opt("detail");
                throw new Exception("Backend HTTP " + code + ": " + (detail == null ? response.toString() : detail.toString()));
            }
            return response;
        } finally { if (c != null) c.disconnect(); }
    }

    private void sendBridgeResult(String callbackName, String callbackId, String json) {
        runOnUiThread(() -> {
            if (webView != null) {
                String safeId = JSONObject.quote(callbackId);
                String safeJson = JSONObject.quote(json);
                String safeName = JSONObject.quote(callbackName);
                webView.evaluateJavascript("window[" + safeName + "] && window[" + safeName + "](" + safeId + ", " + safeJson + ")", null);
            }
        });
    }

    private void sendResult(String callbackId, String json) {
        sendBridgeResult("onNasaResult", callbackId, json);
    }

    private JSONObject errorJson(String message) {
        JSONObject o = new JSONObject();
        try { o.put("status", "error"); o.put("message", message == null ? "Unknown error" : message); }
        catch (Exception ignored) {}
        return o;
    }

    private JSONObject fetchNasaPower(double lat, double lon) throws Exception {
        // POWER meteorology and SMAP can be requested through the Daily API.
        // The public POWER user-community values are AG, SB and RE; HY is a
        // hydrology parameter grouping in the documentation, but is rejected
        // as a request community by the current public API (HTTP 422).
        LocalDate today = LocalDate.now();
        LocalDate end = today.minusDays(4); // allow the daily POWER feed to complete
        LocalDate start = end.minusDays(1825);
        String from = start.format(DateTimeFormatter.BASIC_ISO_DATE);
        String to = end.format(DateTimeFormatter.BASIC_ISO_DATE);
        String common = "&longitude=" + lon + "&latitude=" + lat + "&format=JSON&time-standard=UTC";

        String metUrl = "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=" + enc("T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN") +
                "&community=AG" + common + "&start=" + from + "&end=" + to;

        // SFMC/RZMC/PRMC are the POWER parameter aliases for SMAP L4
        // surface, root-zone and profile volumetric soil moisture.
        String smapUrl = "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=" + enc("SFMC,RZMC,PRMC") +
                "&community=AG" + common + "&start=" + from + "&end=" + to;

        // POWER serves IMERG_PRECTOT as daily UTC precipitation. Use a
        // conservative ~4-month cutoff to compare finalized IMERG months;
        // aggregate the daily mm values into 24 complete monthly totals below.
        LocalDate gpmEnd = today.minusMonths(4).withDayOfMonth(1).minusDays(1);
        YearMonth gpmEndMonth = YearMonth.from(gpmEnd);
        YearMonth gpmStartMonth = gpmEndMonth.minusMonths(23);
        LocalDate gpmStart = gpmStartMonth.atDay(1);
        String gpmFrom = gpmStart.format(DateTimeFormatter.BASIC_ISO_DATE);
        String gpmTo = gpmEnd.format(DateTimeFormatter.BASIC_ISO_DATE);
        String imergUrl = "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=" + enc("IMERG_PRECTOT") +
                "&community=AG" + common + "&start=" + gpmFrom + "&end=" + gpmTo;

        JSONObject met = getJson(metUrl, "NASA POWER meteorology");
        JSONObject smap = getJson(smapUrl, "NASA SMAP L4 soil moisture");
        JSONObject gpm = getJson(imergUrl, "NASA GPM IMERG daily precipitation");

        JSONObject metParams = findObject(met, "parameter");
        JSONObject smapParams = findObject(smap, "parameter");
        JSONObject gpmParams = findObject(gpm, "parameter");
        JSONObject t2m = findObject(metParams, "T2M");
        JSONObject tmax = findObject(metParams, "T2M_MAX");
        JSONObject rainDaily = findObject(metParams, "PRECTOTCORR");
        JSONObject sfmc = findObject(smapParams, "SFMC");
        JSONObject rzmc = findObject(smapParams, "RZMC");
        JSONObject prmc = findObject(smapParams, "PRMC");
        JSONObject imerg = findObject(gpmParams, "IMERG_PRECTOT");

        if (t2m == null || tmax == null || sfmc == null || rzmc == null || imerg == null ||
                t2m.length() == 0 || sfmc.length() == 0 || rzmc.length() == 0 || imerg.length() == 0) {
            throw new Exception("NASA POWER did not return all required observations (POWER, SMAP L4, GPM IMERG). " +
                    "No sample or synthetic fallback is used. Check the farm coordinates and NASA data availability, then retry.");
        }

        Double tempMean = mean(t2m);
        Double maxMean = mean(tmax);
        Double humidityMean = mean(findObject(metParams, "RH2M"));
        Double solarMean = mean(findObject(metParams, "ALLSKY_SFC_SW_DWN"));

        String latestSmapKey = latestKey(rzmc);
        double latestRz = rzmc.getDouble(latestSmapKey);
        double latestSf = sfmc.optDouble(latestSmapKey, Double.NaN);
        double latestPr = prmc == null ? Double.NaN : prmc.optDouble(latestSmapKey, Double.NaN);
        int month = Integer.parseInt(latestSmapKey.substring(4, 6));
        List<Double> sameMonth = new ArrayList<>();
        Iterator<String> sit = rzmc.keys();
        while (sit.hasNext()) {
            String k = sit.next();
            if (k.length() == 8 && Integer.parseInt(k.substring(4, 6)) == month) {
                double v = rzmc.optDouble(k, Double.NaN);
                if (!Double.isNaN(v) && v > -900) sameMonth.add(v);
            }
        }
        Double rzBase = avg(sameMonth);
        Double rzAnom = rzBase == null || Math.abs(rzBase) < 0.00001 ? null : ((latestRz - rzBase) / Math.abs(rzBase)) * 100.0;

        List<Double> monthlyImergTotals = completeMonthlyTotals(imerg, gpmStart, gpmEnd);
        Double recent12 = null, prior12 = null, rainChange = null;
        if (monthlyImergTotals.size() == 24) {
            recent12 = sum(monthlyImergTotals.subList(12, 24));
            prior12 = sum(monthlyImergTotals.subList(0, 12));
            rainChange = ((recent12 - prior12) / Math.max(prior12, 1.0)) * 100.0;
        } else {
            throw new Exception("NASA GPM IMERG returned insufficient complete daily coverage for the 24-month comparison. No fallback is used.");
        }

        Double rain30 = sumLatest(rainDaily, 30);
        int hotDays = countAtOrAbove(tmax, 35.0);
        JSONObject tminObj = findObject(metParams, "T2M_MIN");
        Integer frostDays = (tminObj == null || tminObj.length() == 0) ? null : Integer.valueOf(countFrostDays(tminObj));

        JSONObject out = new JSONObject();
        out.put("status", "live");
        out.put("retrievedAt", java.time.Instant.now().toString());
        out.put("periodStart", start.toString());
        out.put("periodEnd", end.toString());
        out.put("gpmPeriodStart", gpmStart.toString());
        out.put("gpmPeriodEnd", gpmEnd.toString());
        out.put("latitude", lat);
        out.put("longitude", lon);
        out.put("sources", new JSONArray()
                .put("NASA POWER Agroclimatology daily meteorology")
                .put("NASA SMAP L4 via POWER SFMC/RZMC/PRMC high-resolution soil-moisture aliases")
                .put("NASA GPM IMERG daily precipitation via POWER IMERG_PRECTOT"));
        out.put("temperatureMeanC", nullable(tempMean));
        out.put("temperatureMaxMeanC", nullable(maxMean));
        out.put("humidityMeanPct", nullable(humidityMean));
        out.put("solarMeanMJm2Day", nullable(solarMean));
        out.put("rainfallRecent30dMm", nullable(rain30));
        out.put("rainfallRecent12mMm", nullable(recent12));
        out.put("rainfallPrevious12mMm", nullable(prior12));
        out.put("rainfallChangePct", nullable(rainChange));
        out.put("smapLatestDate", latestSmapKey);
        out.put("smapSurfaceMoistureM3m3", nullable(latestSf));
        out.put("smapRootZoneMoistureM3m3", latestRz);
        out.put("smapProfileMoistureM3m3", nullable(latestPr));
        out.put("smapRootZoneAnomalyPct", nullable(rzAnom));
        out.put("smapSameMonthBaselineM3m3", nullable(rzBase));
        out.put("heatDays35C", hotDays);
        out.put("frostDays0C", frostDays == null ? JSONObject.NULL : frostDays);
        JSONArray gpmMonthly = new JSONArray();
        for (Double mv : monthlyImergTotals) gpmMonthly.put(Math.round(mv.doubleValue() * 10.0) / 10.0);
        out.put("gpmMonthlyMm", gpmMonthly);
        out.put("gpmFirstMonth", gpmStartMonth.toString());

        JSONObject counts = new JSONObject();
        counts.put("powerDailyT2M", t2m.length());
        counts.put("smapSurfaceDaily", sfmc.length());
        counts.put("smapRootZoneDaily", rzmc.length());
        counts.put("gpmImergDaily", imerg.length());
        counts.put("gpmCompleteMonths", monthlyImergTotals.size());
        out.put("observationCounts", counts);

        JSONObject urls = new JSONObject();
        urls.put("power", metUrl);
        urls.put("smap", smapUrl);
        urls.put("gpmImerg", imergUrl);
        out.put("requestUrls", urls);

        JSONArray quality = new JSONArray();
        quality.put("SMAP L4 is a satellite-constrained, model-assimilated product (~9 km); it is not a field moisture probe.");
        quality.put("GPM IMERG is a gridded precipitation estimate (~0.1 degree). Monthly totals are calculated by summing daily IMERG values.");
        quality.put("The GPM comparison uses the latest 24 complete months ending approximately four months before retrieval to reduce provisional-data effects.");
        quality.put("NASA POWER meteorological products can have coarser native resolution than SMAP and IMERG; do not treat mixed-resolution grids as field-scale measurements.");
        quality.put("Soil pH, NPK, organic matter, crop calendar and market constraints must come from local information.");
        quality.put("SMAP record begins in 2015; the five-year SMAP period is not a multi-decade soil-moisture climatology.");
        out.put("qualityNotes", quality);
        out.put("advancedProducts", new JSONObject()
                .put("MODIS_NDVI", "Available through the secure team AppEEARS backend; fetch separately from the NASA tab.")
                .put("ECOSTRESS_ET", "Available through the secure team AppEEARS backend; fetch separately from the NASA tab."));
        return out;
    }

    private static List<Double> completeMonthlyTotals(JSONObject dailyValues, LocalDate firstDate, LocalDate lastDate) throws Exception {
        class MonthBucket { double sum = 0.0; int count = 0; }
        Map<YearMonth, MonthBucket> buckets = new TreeMap<>();
        Iterator<String> keys = dailyValues.keys();
        while (keys.hasNext()) {
            String key = keys.next();
            if (key == null || key.length() != 8) continue;
            LocalDate date;
            try { date = LocalDate.parse(key, DateTimeFormatter.BASIC_ISO_DATE); }
            catch (Exception ignored) { continue; }
            if (date.isBefore(firstDate) || date.isAfter(lastDate)) continue;
            double value = dailyValues.optDouble(key, Double.NaN);
            if (Double.isNaN(value) || value <= -900) continue;
            YearMonth ym = YearMonth.from(date);
            MonthBucket bucket = buckets.get(ym);
            if (bucket == null) { bucket = new MonthBucket(); buckets.put(ym, bucket); }
            bucket.sum += value;
            bucket.count++;
        }

        List<Double> totals = new ArrayList<>();
        YearMonth month = YearMonth.from(firstDate);
        YearMonth finalMonth = YearMonth.from(lastDate);
        while (!month.isAfter(finalMonth)) {
            MonthBucket bucket = buckets.get(month);
            int minimumDays = (int) Math.ceil(month.lengthOfMonth() * 0.90);
            if (bucket == null || bucket.count < minimumDays) {
                throw new Exception("GPM IMERG daily coverage is incomplete for " + month +
                        " (" + (bucket == null ? 0 : bucket.count) + "/" + month.lengthOfMonth() + " days). Retry later; no fallback is used.");
            }
            totals.add(bucket.sum);
            month = month.plusMonths(1);
        }
        return totals;
    }

    private JSONObject getJson(String urlString, String label) throws Exception {
        HttpURLConnection c = null;
        try {
            c = (HttpURLConnection) new URL(urlString).openConnection();
            c.setRequestMethod("GET"); c.setConnectTimeout(30000); c.setReadTimeout(60000);
            c.setRequestProperty("Accept", "application/json"); c.setRequestProperty("User-Agent", "NASA-KrishiBondhu/1.0 (NASA Space Apps educational decision support)");
            int code = c.getResponseCode();
            BufferedReader r = new BufferedReader(new InputStreamReader(code >= 200 && code < 300 ? c.getInputStream() : c.getErrorStream(), StandardCharsets.UTF_8));
            StringBuilder b = new StringBuilder(); String line; while ((line = r.readLine()) != null) b.append(line); r.close();
            if (code < 200 || code >= 300) throw new Exception(label + " failed with HTTP " + code + ": " + b.substring(0, Math.min(400, b.length())));
            JSONObject payload = new JSONObject(b.toString());
            if (!payload.has("properties") || payload.optJSONObject("properties") == null) throw new Exception(label + " returned no properties object.");
            return payload;
        } finally { if (c != null) c.disconnect(); }
    }

    private static String enc(String s) throws Exception { return URLEncoder.encode(s, "UTF-8"); }
    private static JSONObject findObject(JSONObject root, String key) {
        if (root == null) return null;
        if (root.has(key) && root.optJSONObject(key) != null) return root.optJSONObject(key);
        Iterator<String> it = root.keys();
        while (it.hasNext()) { Object child = root.opt(it.next()); if (child instanceof JSONObject) { JSONObject f = findObject((JSONObject) child, key); if (f != null) return f; } }
        return null;
    }
    private static List<String> sortedKeys(JSONObject obj) {
        List<String> keys = new ArrayList<>(); if (obj == null) return keys;
        Iterator<String> it = obj.keys(); while (it.hasNext()) keys.add(it.next()); Collections.sort(keys); return keys;
    }
    private static String latestKey(JSONObject obj) throws Exception { List<String> k = sortedKeys(obj); if (k.isEmpty()) throw new Exception("NASA returned an empty time series."); return k.get(k.size()-1); }
    private static Double mean(JSONObject obj) {
        if (obj == null) return null; Iterator<String> it = obj.keys(); double s=0; int n=0;
        while (it.hasNext()) { double v=obj.optDouble(it.next(), Double.NaN); if (!Double.isNaN(v) && v > -900) {s+=v;n++;} }
        return n==0?null:s/n;
    }
    private static Double avg(List<Double> values) { if (values.isEmpty()) return null; double s=0; for(double v:values)s+=v; return s/values.size(); }
    private static double sum(List<Double> values) { double s=0; for(double v:values)s+=v; return s; }
    private static Double sumLatest(JSONObject obj, int n) {
        List<String> keys=sortedKeys(obj); if(keys.isEmpty())return null; int from=Math.max(0,keys.size()-n); double s=0;
        for(int i=from;i<keys.size();i++) {double v=obj.optDouble(keys.get(i),Double.NaN);if(!Double.isNaN(v)&&v>-900)s+=v;} return s;
    }
    private static int countAtOrAbove(JSONObject obj, double threshold) {
        if(obj==null)return 0; int n=0; Iterator<String> it=obj.keys(); while(it.hasNext()) {double v=obj.optDouble(it.next(),Double.NaN);if(!Double.isNaN(v)&&v>=threshold)n++;} return n;
    }
    private static int countFrostDays(JSONObject obj) {
        int n = 0; Iterator<String> it = obj.keys();
        while (it.hasNext()) { double v = obj.optDouble(it.next(), Double.NaN); if (!Double.isNaN(v) && v > -900 && v <= 0.0) n++; }
        return n;
    }
    private static Object nullable(Double v) { return v == null || v.isNaN() || v.isInfinite() ? JSONObject.NULL : v; }
}
