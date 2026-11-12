"""Bangladesh crop-calendar screening and rotation candidate ranking.

This is an explainable screening knowledge base, not a substitute for BARC's
upazila-level Crop Zoning assessment or an agronomist's field validation.
"""
from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional

BARC_SUITABILITY_URL = "https://portal.cropzoning.gov.bd/cropSuitability"
BARC_CZIS_URL = "https://czis.cropzoning.gov.bd/"

# Month numbers are Gregorian sowing/planting months, based on national AIS / BRRI
# guidance. Regional and variety-specific deviations are deliberately flagged.
CROP_DATABASE: List[Dict[str, Any]] = [
    {
        "id": "rice_aman", "crop": "Rice (Aman)", "bn": "আমন ধান", "family": "Poaceae",
        "months": [6, 7], "duration": None, "water": "high", "soils": ["Clay", "Clay loam", "Loam", "Silt"],
        "ph": [5.0, 7.5], "drainage": "moderate", "legume": False, "root": "medium",
        "nutrientDemand": "high", "rotationBreak": False,
        "notesBn": "আমন মৌসুম; জমির জলাবদ্ধতা/বন্যা-সহনশীলতা ও জাতের জীবনকাল মিলিয়ে নিন।",
        "notesEn": "Aman season; match variety duration and field flood/inundation conditions.",
        "sources": ["https://brri.gov.bd/pages/static-pages/6922dea6933eb65569e1c55f", "https://ais.gov.bd/"],
    },
    {
        "id": "rice_boro", "crop": "Rice (Boro)", "bn": "বোরো ধান", "family": "Poaceae",
        "months": [12, 1], "duration": None, "water": "high", "soils": ["Clay", "Clay loam", "Loam"],
        "ph": [5.0, 7.5], "drainage": "poor_to_moderate", "legume": False, "root": "medium",
        "nutrientDemand": "high", "rotationBreak": False,
        "notesBn": "বোরো ধানের রোপণকাল ও বীজতলার সময় স্থানীয় BRRI/কৃষি ক্যালেন্ডার মিলিয়ে নিন; সেচের পানির নিশ্চয়তা জরুরি।",
        "notesEn": "Check local BRRI/extension timing for nursery and transplanting; reliable irrigation is essential.",
        "sources": ["https://brri.gov.bd/pages/static-pages/6922dea6933eb65569e1c55f", "https://ais.gov.bd/"],
    },
    {
        "id": "rice_aus", "crop": "Rice (Aus)", "bn": "আউশ ধান", "family": "Poaceae",
        "months": [4, 5], "duration": None, "water": "medium_to_high", "soils": ["Loam", "Silt", "Clay loam"],
        "ph": [5.0, 7.5], "drainage": "moderate", "legume": False, "root": "medium",
        "nutrientDemand": "high", "rotationBreak": False,
        "notesBn": "আউশের বপন/রোপণ বৃষ্টির আগমন ও স্থানীয় পানি নিষ্কাশনের ওপর নির্ভরশীল।",
        "notesEn": "Aus timing depends on monsoon onset and local drainage.",
        "sources": ["https://brri.gov.bd/pages/static-pages/6922dea6933eb65569e1c55f", "https://ais.gov.bd/"],
    },
    {
        "id": "lentil", "crop": "Lentil", "bn": "মসুর ডাল", "family": "Fabaceae",
        "months": [10, 11], "duration": [110, 120], "water": "low", "soils": ["Loam", "Silt", "Clay loam"],
        "ph": [5.5, 7.5], "drainage": "good", "legume": True, "root": "medium",
        "nutrientDemand": "medium", "rotationBreak": True,
        "notesBn": "মসুরের সময়মতো বপন জরুরি; জলাবদ্ধতা ও দেরিতে বপন ক্ষতি করতে পারে।",
        "notesEn": "Timely sowing matters; waterlogging and delayed sowing can reduce performance.",
        "sources": ["https://ais.gov.bd/pages/ekrishi/%E0%A6%AE%E0%A6%B8%E0%A7%81%E0%A6%B0-1e2qhm-69a2cd8ae64a23d0fb624c22"],
    },
    {
        "id": "mustard", "crop": "Mustard", "bn": "সরিষা", "family": "Brassicaceae",
        "months": [10, 11], "duration": [85, 90], "water": "low_to_medium", "soils": ["Sandy", "Loam", "Clay loam"],
        "ph": [5.5, 7.5], "drainage": "good", "legume": False, "root": "taproot",
        "nutrientDemand": "medium", "rotationBreak": True,
        "notesBn": "সরিষার উপযুক্ত বপনকাল সাধারণত অক্টোবর-মধ্য নভেম্বর; জাত ও এলাকা অনুযায়ী বদলায়।",
        "notesEn": "Typical sowing is around October to mid-November; varieties and regions differ.",
        "sources": ["https://ais.gov.bd/pages/krishi-kotha/%E0%A6%B8%E0%A7%87%E0%A6%9A-%E0%A6%B8%E0%A6%BE%E0%A6%B6%E0%A7%8D%E0%A6%B0%E0%A7%9F%E0%A7%80-%E0%A6%AA%E0%A6%B0%E0%A6%BF%E0%A6%AC%E0%A7%87%E0%A6%B6%E0%A6%AC%E0%A6%BE%E0%A6%A8%E0%A7%8D%E0%A6%A7%E0%A6%AC-%E0%A6%B2%E0%A6%BE%E0%A6%AD%E0%A6%9C%E0%A6%A8%E0%A6%95-%E0%A6%AB%E0%A6%B8%E0%A6%B2-%E0%A6%AC%E0%A6%BF%E0%A6%A8%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%B8-e8b176-6922d94ddbfbfb"],
    },
    {
        "id": "wheat", "crop": "Wheat", "bn": "গম", "family": "Poaceae",
        "months": [11], "duration": None, "water": "medium", "soils": ["Loam", "Clay loam", "Silt"],
        "ph": [6.0, 8.0], "drainage": "good", "legume": False, "root": "fibrous",
        "nutrientDemand": "high", "rotationBreak": False,
        "notesBn": "গমের উপযুক্ত বপনকাল ১৫-৩০ নভেম্বর; লবণাক্ততা ও দেরিতে বপনের ঝুঁকি যাচাই করুন।",
        "notesEn": "AIS guidance gives 15–30 November as the suitable sowing period; check salinity and delay risk.",
        "sources": ["https://ais.gov.bd/pages/krishi-kotha/%E0%A6%97%E0%A6%AE%E0%A7%87%E0%A6%B0-%E0%A6%86%E0%A6%A7%E0%A7%81%E0%A6%A8%E0%A6%BF%E0%A6%95-%E0%A6%9C%E0%A6%BE%E0%A6%A4%E0%A6%B8%E0%A6%AE%E0%A7%82%E0%A6%B9-%E0%A6%93-%E0%A6%89%E0%A7%8E%E0%A6%AA%E0%A6%BE%E0%A6%A6%E0%A6%A8-%E0%A6%95%E0%A7%8C%E0%A6%B6%E0%A6%B2-a6a224-6922d944dbfbab28ce04a7c7"],
    },
    {
        "id": "maize_rabi", "crop": "Maize (Rabi)", "bn": "ভুট্টা (রবি)", "family": "Poaceae",
        "months": [10, 11], "duration": None, "water": "medium_to_high", "soils": ["Loam", "Sandy", "Clay loam"],
        "ph": [5.5, 7.5], "drainage": "good", "legume": False, "root": "deep",
        "nutrientDemand": "high", "rotationBreak": False,
        "notesBn": "রবি ভুট্টার বপনকাল অক্টোবর-নভেম্বর; পানি ও পুষ্টির চাহিদা তুলনামূলক বেশি।",
        "notesEn": "Rabi maize is commonly sown October–November and can have substantial water/nutrient needs.",
        "sources": ["https://ais.gov.bd/pages/krishi-kotha/%E0%A6%AD%E0%A7%81%E0%A6%9F%E0%A7%8D%E0%A6%9F%E0%A6%BE%E0%A6%B0-%E0%A6%86%E0%A6%A7%E0%A7%81%E0%A6%A8%E0%A6%BF%E0%A6%95-%E0%A6%9C%E0%A6%BE%E0%A6%A4-%E0%A6%93-%E0%A6%89%E0%A7%8E%E0%A6%AA%E0%A6%BE%E0%A6%A6%E0%A6%A8-%E0%A6%95%E0%A6%B2%E0%A6%BE%E0%A6%95%E0%A7%8C%E0%A6%B6%E0%A6%B2-7ae9e8-6922d95adbfbfb"],
    },
    {
        "id": "maize_kharif1", "crop": "Maize (Kharif-1)", "bn": "ভুট্টা (খরিপ-১)", "family": "Poaceae",
        "months": [2, 3], "duration": None, "water": "medium_to_high", "soils": ["Loam", "Sandy", "Clay loam"],
        "ph": [5.5, 7.5], "drainage": "good", "legume": False, "root": "deep",
        "nutrientDemand": "high", "rotationBreak": False,
        "notesBn": "খরিপ-১ ভুট্টার বপনকাল ফেব্রুয়ারি-মার্চ; অতিবৃষ্টি/জলাবদ্ধতা এড়াতে হবে।",
        "notesEn": "Kharif-1 maize is sown around February–March; avoid waterlogging and heavy-rain exposure.",
        "sources": ["https://ais.gov.bd/pages/krishi-kotha/%E0%A6%AD%E0%A7%81%E0%A6%9F%E0%A7%8D%E0%A6%9F%E0%A6%BE%E0%A6%B0-%E0%A6%86%E0%A6%A7%E0%A7%81%E0%A6%A8%E0%A6%BF%E0%A6%95-%E0%A6%9C%E0%A6%BE%E0%A6%A4-%E0%A6%93-%E0%A6%89%E0%A7%8E%E0%A6%AA%E0%A6াদন-%E0%A6%95%E0%A7%8C%E0%A6%B6%E0%A6%B2-7ae9e8-6922d95adbfbfb"],
    },
    {
        "id": "mung_kharif1", "crop": "Mung bean (Kharif-1)", "bn": "মুগ ডাল (খরিপ-১)", "family": "Fabaceae",
        "months": [2, 3], "duration": [60, 75], "water": "low", "soils": ["Sandy", "Loam", "Silt"],
        "ph": [5.5, 7.5], "drainage": "good", "legume": True, "root": "medium",
        "nutrientDemand": "low_to_medium", "rotationBreak": True,
        "notesBn": "মাঝারি উঁচু ও পানি দ্রুত নেমে যায় এমন জমি দরকার; জলাবদ্ধতা ক্ষতিকর।",
        "notesEn": "Needs a reasonably raised, well-drained field; waterlogging is harmful.",
        "sources": ["https://ais.gov.bd/pages/ekrishi/%E0%A6%AE%E0%A7%81%E0%A6%97-%E0%A6%A1%E0%A6%BE%E0%A6%B2-%E0%A6%9A%E0%A6%BE%E0%A6%B7-fsmvc2-6a1d4c0f2de6aeac14f8a9ef", "https://ais.gov.bd/pages/krishi-kotha/%E0%A6%96%E0%A6%BE%E0%A6%A6%E0%A7%8D%E0%A6%AF-%E0%A6%A8%E0%A6%BF%E0%A6%B0%E0%A6%BE%E0%A6%AA%E0%A6%A4%E0%A7%8D%E0%A6%A4%E0%A6%BE%E0%A7%9F-%E0%A6%AE%E0%A7%81%E0%A6%97%E0%A6%A1%E0%A6%BE%E0%A6%B2-%E0%A6%93-%E0%A6%9A%E0%A6%BE%E0%A6%B7%E0%A6%BE%E0%A6%ac%E0%A6%BE%E0%A6%A6-%E0%A6%AA%E0%A6%A6%E0%A7%8D%E0%A6%A7%E0%A6%A4%E0%A6%BF-c91fdb-6922d95bdbfbab28ce04bb4c"],
    },
    {
        "id": "mung_kharif2", "crop": "Mung bean (Kharif-2)", "bn": "মুগ ডাল (খরিপ-২)", "family": "Fabaceae",
        "months": [8, 9], "duration": [60, 75], "water": "low", "soils": ["Sandy", "Loam", "Silt"],
        "ph": [5.5, 7.5], "drainage": "good", "legume": True, "root": "medium",
        "nutrientDemand": "low_to_medium", "rotationBreak": True,
        "notesBn": "শ্রাবণ-ভাদ্রের বপন; অতিবৃষ্টি ও ফল পচা ঝুঁকি স্থানীয়ভাবে যাচাই করুন।",
        "notesEn": "Sown in the August–September window; check heavy-rain and pod-rot risk locally.",
        "sources": ["https://ais.gov.bd/pages/ekrishi/%E0%A6%AE%E0%A7%81%E0%A6%97-%E0%A6%A1%E0%A6%BE%E0%A6%B2-%E0%A6%9A%E0%A6%BE%E0%A6%B7-fsmvc2-6a1d4c0f2de6aeac14f8a9ef"],
    },
    {
        "id": "mung_coastal_rabi", "crop": "Mung bean (Coastal Rabi)", "bn": "মুগ ডাল (উপকূলীয় রবি)", "family": "Fabaceae",
        "months": [1, 2], "duration": [60, 75], "water": "low", "soils": ["Sandy", "Loam", "Silt"],
        "ph": [5.5, 7.5], "drainage": "good", "legume": True, "root": "medium",
        "nutrientDemand": "low_to_medium", "rotationBreak": True,
        "regionKeywords": ["barishal", "বরিশাল", "coastal", "উপকূল", "bhola", "ভোলা", "patuakhali", "পটুয়াখালী", "barguna", "বরগুনা"],
        "notesBn": "এটি উপকূলীয় অঞ্চলের জন্য বিশেষ সময়; দেশের সব এলাকায় প্রযোজ্য নয়।",
        "notesEn": "This is a regional coastal window, not a nationwide recommendation.",
        "sources": ["https://ais.gov.bd/pages/ekrishi/%E0%A6%AE%E0%A7%81%E0%A6%97-%E0%A6%A1%E0%A6%BE%E0%A6%B2-%E0%A6%9A%E0%A6%BE%E0%A6%B7-fsmvc2-6a1d4c0f2de6aeac14f8a9ef"],
    },
    {
        "id": "soybean_rabi", "crop": "Soybean (Rabi)", "bn": "সয়াবিন (রবি)", "family": "Fabaceae",
        "months": [12, 1], "duration": [90, 120], "water": "medium", "soils": ["Sandy", "Loam", "Silt"],
        "ph": [5.5, 7.5], "drainage": "good", "legume": True, "root": "deep",
        "nutrientDemand": "medium", "rotationBreak": True,
        "notesBn": "রবি সয়াবিনের উপযুক্ত সময় ডিসেম্বর-মধ্য থেকে জানুয়ারি; অঞ্চলভেদে যাচাই জরুরি।",
        "notesEn": "Rabi soybean is commonly sown mid-December through January; confirm regional fit.",
        "sources": ["https://ais.gov.bd/pages/ekrishi/%E0%A6%B8%E0%A7%9F%E0%A6%BE%E0%A6%AC%E0%A6%BF%E0%A6%A8-%E0%A6%89%E0%A7%8E%E0%A6%AA%E0%A6%BE%E0%A6%A6%E0%A6%A8-%E0%A6%AA%E0%A7%8D%E0%A6%B0%E0%A6%AF%E0%A7%81%E0%A6%95%E0%A7%8D%E0%A6%A4%E0%A6%BF-73iwcs-69ae6c499ce9b066bb46c14a"],
    },
    {
        "id": "soybean_kharif2", "crop": "Soybean (Kharif-2)", "bn": "সয়াবিন (খরিপ-২)", "family": "Fabaceae",
        "months": [7, 8], "duration": [90, 120], "water": "medium", "soils": ["Sandy", "Loam", "Silt"],
        "ph": [5.5, 7.5], "drainage": "good", "legume": True, "root": "deep",
        "nutrientDemand": "medium", "rotationBreak": True,
        "notesBn": "খরিপ-২ মৌসুমের বপনকাল; বৃষ্টির পানি বের হওয়ার ব্যবস্থা নিশ্চিত করুন।",
        "notesEn": "Kharif-2 sowing window; ensure adequate field drainage.",
        "sources": ["https://ais.gov.bd/pages/ekrishi/%E0%A6%B8%E0%A7%9F%E0%A6%BE%E0%A6%AC%E0%A6%BF%E0%A6%A8-%E0%A6%89%E0%A7%8E%E0%A6%AA%E0%A6%BE%E0%A6%A6%E0%A6%A8-%E0%A6%AA%E0%A7%8D%E0%A6%B0%E0%A6%AF%E0%A7%81%E0%A6%95%E0%A7%8D%E0%A6%A4%E0%A6%BF-73iwcs-69ae9e"],
    },
    {
        "id": "potato", "crop": "Potato", "bn": "আলু", "family": "Solanaceae",
        "months": [11, 12], "duration": None, "water": "medium", "soils": ["Sandy", "Loam", "Silt"],
        "ph": [5.0, 6.5], "drainage": "good", "legume": False, "root": "shallow",
        "nutrientDemand": "high", "rotationBreak": True,
        "notesBn": "আলু রোপণের সময় সাধারণত নভেম্বর; ডিসেম্বরের পরে দেরি হলে ফলন কমতে পারে।",
        "notesEn": "Potato planting is generally in November; late planting can lower performance.",
        "sources": ["https://ais.gov.bd/pages/krishi-kotha/%E0%A6%B0%E0%A6%AA%E0%A7%8D%E0%A6%A4%E0%A6%BE%E0%A6%A8%E0%A6%BF%E0%A6%AF%E0%A7%8B%E0%A6%97%E0%A7%8D%E0%A6%AF-%E0%A6%86%E0%A6%B2%E0%A7%81-%E0%A6%9A%E0%A6%BE%E0%A6%B7%E0%A7%87-%E0%A6%95%E0%A7%83%E0%A6%B7%E0%A6%95%E0%A6%A6%E0%A7%87%E0%A6%B0-%E0%A6%95%E0%A6%B0%E0%A6%A3%E0%A7%80%E0%A7%9F-218cc4-6922d95ddbfbfd"],
    },
]


def _num(farm: Dict[str, Any], key: str) -> Optional[float]:
    try:
        v = farm.get(key)
        if v is None or str(v).strip() == "":
            return None
        x = float(v)
        return x if x == x and abs(x) != float("inf") else None
    except (TypeError, ValueError):
        return None


def _soil_nutrient_flags(farm: Dict[str, Any]) -> Dict[str, Any]:
    """Unit-aware screening only; implausible entries are excluded from scoring."""
    raw = {
        "soilPh": _num(farm, "soilPh"),
        "organicMatterPct": _num(farm, "organicMatter"),
        "totalNitrogenPct": _num(farm, "nitrogen"),
        "availablePhosphorusMgKg": _num(farm, "phosphorus"),
        "exchangeablePotassiumCmolKg": _num(farm, "potassium"),
    }
    # Broad plausibility checks catch common unit mix-ups (for example N in kg/ha
    # entered into a percent field). They are not agronomic sufficiency ranges.
    limits = {
        "soilPh": (3.0, 10.0),
        "organicMatterPct": (0.0, 20.0),
        "totalNitrogenPct": (0.0, 2.0),
        "availablePhosphorusMgKg": (0.0, 500.0),
        "exchangeablePotassiumCmolKg": (0.0, 5.0),
    }
    valid = dict(raw)
    invalid: List[str] = []
    for key, value in raw.items():
        if value is not None and not (limits[key][0] <= value <= limits[key][1]):
            valid[key] = None
            invalid.append(key)

    flags: List[str] = []
    om, n = valid["organicMatterPct"], valid["totalNitrogenPct"]
    p, k, ph = valid["availablePhosphorusMgKg"], valid["exchangeablePotassiumCmolKg"], valid["soilPh"]
    if om is not None and om < 1.5:
        flags.append("low_organic_matter")
    if n is not None and n < 0.12:
        flags.append("low_total_nitrogen_screen")
    p_limit = 7.0 if ph is not None and ph < 5.5 else 10.0
    if p is not None and p < p_limit:
        flags.append("low_available_phosphorus_screen")
    if k is not None and k < 0.12:
        flags.append("low_exchangeable_potassium_screen")
    return {
        "flags": flags,
        "invalidFields": invalid,
        "values": raw,
        "validValues": valid,
        "interpretation": "Screening flags only. Critical values depend on soil extraction method, soil group and the lab's reference system; request a BARC/SRDI soil-test recommendation before fertilizer decisions. Implausible values are excluded from scoring; confirm units with the lab.",
    }


def recommend_crop_candidates(farm: Dict[str, Any], nasa: Dict[str, Any], ancillary: Dict[str, Any], month: Optional[int] = None) -> Dict[str, Any]:
    """Rank current sowing-window candidates for Bangladesh with transparent factor scores."""
    target_month = int(month or _num(farm, "plantingMonth") or date.today().month)
    if not 1 <= target_month <= 12:
        target_month = date.today().month
    location = str(farm.get("location") or "").lower()
    soil_type = str(farm.get("soilType") or "Unknown")
    drainage = str(farm.get("drainage") or "Unknown").lower()
    salinity = str(farm.get("salinity") or "Unknown").lower()
    water = str(farm.get("water") or "Unknown").lower()
    priority = str(farm.get("priority") or "Balanced").lower()
    current_crop = str(farm.get("currentCrop") or "").lower()
    history_text = str(farm.get("history") or "").lower()
    last_crops = [x.strip() for x in [current_crop] + history_text.split(",") if x.strip()]
    soil_flags = _soil_nutrient_flags(farm)
    valid_soil = soil_flags.get("validValues", {})
    om = valid_soil.get("organicMatterPct")
    ph = valid_soil.get("soilPh")
    nitrogen = valid_soil.get("totalNitrogenPct")
    phosphorus = valid_soil.get("availablePhosphorusMgKg")
    potassium = valid_soil.get("exchangeablePotassiumCmolKg")
    rain_change = _num(nasa, "rainfallChangePct")
    root_anomaly = _num(nasa, "smapRootZoneAnomalyPct")
    ndvi_trend = _num((ancillary or {}).get("modis", {}), "trendChangePct")
    et_trend = _num((ancillary or {}).get("ecostress", {}), "trendChangePct")
    rain_deficit = min(1.0, max(0.0, -(rain_change or 0.0)) / 50.0)
    moisture_deficit = min(1.0, max(0.0, -(root_anomaly or 0.0)) / 35.0)
    vegetation_decline = min(1.0, max(0.0, -(ndvi_trend or 0.0)) / 30.0)
    et_decline = min(1.0, max(0.0, -(et_trend or 0.0)) / 35.0)
    shared_water_signal = max(rain_deficit, moisture_deficit)
    # ECOSTRESS ET decline is counted only when vegetation also declines and a
    # water-deficit signal exists; ET change alone is never treated as drought.
    joint_et_signal = et_decline * vegetation_decline * shared_water_signal
    water_stress = min(1.0, 0.38 * rain_deficit + 0.34 * moisture_deficit
                       + 0.16 * joint_et_signal + 0.12 * vegetation_decline)

    candidates: List[Dict[str, Any]] = []
    excluded: List[Dict[str, str]] = []
    for crop in CROP_DATABASE:
        if target_month not in crop["months"]:
            continue
        region_keywords = crop.get("regionKeywords")
        if region_keywords and not any(k in location for k in region_keywords):
            excluded.append({"crop": crop["bn"], "reason": "এই বপন সময়টি নির্দিষ্ট অঞ্চলের জন্য; আপনার অবস্থান সেই অঞ্চলের সঙ্গে মেলেনি।"})
            continue

        texture_fit = 100.0 if soil_type == "Unknown" or soil_type in crop["soils"] else 58.0
        if ph is None:
            ph_fit = 72.0
        elif crop["ph"][0] <= ph <= crop["ph"][1]:
            ph_fit = 100.0
        elif crop["ph"][0] - 0.6 <= ph <= crop["ph"][1] + 0.6:
            ph_fit = 62.0
        else:
            ph_fit = 28.0

        drainage_fit = 100.0
        if drainage in {"poor", "পানি দাঁড়ায়", "poor drainage"} and crop["drainage"] == "good":
            drainage_fit = 25.0
        elif drainage in {"good", "ভালো", "well drained"} and crop["drainage"] in {"moderate", "poor_to_moderate"}:
            drainage_fit = 78.0
        elif drainage == "unknown":
            drainage_fit = 75.0

        salinity_fit = 100.0
        if salinity in {"high", "উচ্চ", "saline"}:
            # This compact database does not label a crop salt tolerant without a named variety.
            salinity_fit = 45.0
        elif salinity in {"medium", "মাঝারি", "moderate"}:
            salinity_fit = 72.0
        elif salinity == "unknown":
            salinity_fit = 72.0

        water_need = crop["water"]
        water_score = {"low": 100.0, "low_to_medium": 88.0, "medium": 72.0,
                       "medium_to_high": 54.0, "high": 35.0}[water_need]
        if water in {"limited", "rain-fed only", "সীমিত", "শুধু বৃষ্টির পানি"}:
            water_score = min(100.0, water_score + (water_stress * 12.0))
        elif water in {"abundant", "প্রচুর"}:
            water_score = min(100.0, water_score + (100.0 - water_score) * 0.18)
        else:
            water_score = water_score + water_stress * (100.0 - water_score) * 0.12

        family_repeat = 0
        for prior in last_crops:
            if (crop["family"] == "Poaceae" and any(x in prior for x in ["rice", "ধান", "wheat", "গম", "maize", "ভুট্টা"])):
                family_repeat += 1
            elif (crop["family"] == "Fabaceae" and any(x in prior for x in ["lentil", "মসুর", "mung", "মুগ", "soy", "সয়াবিন", "chickpea", "ছোলা"])):
                family_repeat += 1
            elif crop["id"].split("_")[0] in prior:
                family_repeat += 1
        rotation_fit = max(35.0, 100.0 - family_repeat * 18.0)
        crop_name_tokens = crop["crop"].lower().split(" (")[0]
        if crop_name_tokens in current_crop or crop["bn"].lower() in current_crop:
            rotation_fit = 20.0

        nutrient_penalty = 0.0
        nutrient_notes: List[str] = []
        if nitrogen is not None and nitrogen < 0.12 and crop["nutrientDemand"] == "high":
            nutrient_penalty += 12.0
            nutrient_notes.append("soil_N_low")
        if phosphorus is not None and phosphorus < (7.0 if ph is not None and ph < 5.5 else 10.0) and crop["nutrientDemand"] in {"high", "medium"}:
            nutrient_penalty += 7.0
            nutrient_notes.append("soil_P_low")
        if potassium is not None and potassium < 0.12 and crop["nutrientDemand"] == "high":
            nutrient_penalty += 6.0
            nutrient_notes.append("soil_K_low")
        nutrient_score = max(35.0, 100.0 - nutrient_penalty)
        if crop["legume"] and ("low_organic_matter" in soil_flags["flags"] or "low_total_nitrogen_screen" in soil_flags["flags"]):
            rotation_fit = min(100.0, rotation_fit + 8.0)

        soil_score = 0.42 * texture_fit + 0.28 * ph_fit + 0.18 * drainage_fit + 0.12 * salinity_fit
        if priority and ("soil" in priority or "মাটি" in priority):
            weights = {"calendar": .22, "soil": .34, "water": .12, "rotation": .20, "nutrient": .12}
        elif "water" in priority or "পানি" in priority or "climate" in priority or "জলবায়ু" in priority:
            weights = {"calendar": .22, "soil": .20, "water": .32, "rotation": .16, "nutrient": .10}
        else:
            weights = {"calendar": .22, "soil": .26, "water": .20, "rotation": .18, "nutrient": .14}
        score = (100.0 * weights["calendar"] + soil_score * weights["soil"] + water_score * weights["water"]
                 + rotation_fit * weights["rotation"] + nutrient_score * weights["nutrient"])

        is_bn = str(farm.get("lang") or "bn") == "bn"
        issues: List[str] = []
        if drainage_fit < 60:
            issues.append("জমিতে পানি দাঁড়ালে এই ফসলের ঝুঁকি আছে; স্থানীয় কৃষি কর্মকর্তার সঙ্গে মিলিয়ে নিন।" if is_bn else "Waterlogging may make this crop risky; check with local extension staff.")
        if salinity_fit < 60:
            issues.append("লবণাক্ততা বেশি হলে নির্দিষ্ট সহনশীল জাত ও BARC crop-zone যাচাই দরকার।" if is_bn else "High salinity requires a named tolerant variety and BARC crop-zone check.")
        if ph_fit < 60:
            issues.append("মাটির pH এই প্রাথমিক সীমার বাইরে; পরীক্ষাগারের ফল পুনরায় যাচাই করুন।" if is_bn else "The entered pH is outside this screening range; verify the soil-lab result.")
        if nutrient_notes:
            issues.append("মাটি পরীক্ষার এক বা একাধিক মান কম। সার ব্যবহারের আগে BARC/SRDI রিপোর্ট মিলিয়ে নিন।" if is_bn else "One or more soil-test indicators are low; use BARC/SRDI lab interpretation before fertilizer decisions.")
        if soil_flags.get("invalidFields"):
            issues.append("কিছু মাটি পরীক্ষার মান/একক অস্বাভাবিক; সেগুলো স্কোরে ধরা হয়নি।" if is_bn else "Some soil-test values/units look implausible and were excluded from scoring.")
        if crop.get("regionKeywords"):
            issues.append("এই সময়টি নির্দিষ্ট উপকূলীয় অঞ্চলের জন্য; অন্য এলাকায় প্রযোজ্য নয়।" if is_bn else "This sowing window is regional to coastal areas, not nationwide.")

        candidates.append({
            "id": crop["id"], "crop": crop["crop"], "cropBn": crop["bn"], "family": crop["family"],
            "plantingMonths": crop["months"], "durationDays": crop["duration"], "waterNeed": crop["water"],
            "rootType": crop["root"], "isLegume": crop["legume"], "relativeFitScore": round(max(0.0, min(100.0, score)), 1),
            "factorScores": {"calendar": 100.0, "soil": round(soil_score, 1), "water": round(water_score, 1),
                             "rotation": round(rotation_fit, 1), "nutrients": round(nutrient_score, 1)},
            "explanation": crop["notesBn" if str(farm.get("lang") or "bn") == "bn" else "notesEn"],
            "cautions": issues, "nutrientFlags": nutrient_notes, "sources": crop["sources"],
            "waterStressContext": round(water_stress * 100, 1),
            "rotationBreak": bool(crop.get("rotationBreak")),
        })

    candidates.sort(key=lambda x: x["relativeFitScore"], reverse=True)
    return {
        "databaseVersion": "Bangladesh-Crop-Calendar-2026.1",
        "planningMonth": target_month,
        "candidateCount": len(candidates),
        "candidates": candidates[:8],
        "excludedRegionalCandidates": excluded,
        "soilTestScreen": soil_flags,
        "waterStressContext": round(water_stress * 100, 1),
        "scoringWeights": "calendar, soil suitability, water fit (NASA rainfall + MERRA-2 soil moisture; ECOSTRESS only jointly with MODIS decline), crop-family rotation and unit-checked soil-test screening; normalized relative screening score only",
        "barcSuitability": {"status": "not_checked_live", "url": BARC_SUITABILITY_URL,
                            "note": "Select district, upazila, season and crop in BARC Crop Suitability before planting. This app's regional screening is not a BARC suitability rating."},
        "validationRequired": True,
    }
