import main
from main import _decision_engine, _summarize_csv

PRODUCTS = {
    "modisProduct": "MOD13Q1.061",
    "modisNdviLayer": "250m_16_days_NDVI",
    "modisQualityLayer": "DetailedQA",
    "ecostressProduct": "ECO_L3T_JET.002",
    "ecostressEtLayer": "ETdaily",
    "ecostressUncertaintyLayer": "ETuncertainty",
    "ecostressCloudLayer": "cloud",
    "ecostressWaterLayer": "water",
}


def test_app_eears_csv_requires_and_applies_quality_layers():
    modis_csv = """Date,MOD13Q1.061_NDVI,MOD13Q1.061_DetailedQA
2024-01-01,5000,2048
2024-01-17,5500,2052
2024-02-02,6000,2056
2024-02-18,6200,2048
2024-03-05,6500,2048
2024-03-21,6600,2048
2024-04-06,6700,2048
2024-04-22,6800,2048
2024-05-08,6900,2048
2024-05-24,7000,2048
2024-06-09,7100,2048
2024-06-25,7200,2048
2024-07-11,7300,2048
"""
    eco_csv = """Date,ECO_L3T_JET.002_ETdaily,ECO_L3T_JET.002_ETuncertainty,ECO_L3T_JET.002_cloud,ECO_L3T_JET.002_water
2024-01-05,2.0,0.2,0,0
2024-02-03,2.2,0.2,0,0
2024-03-04,1.9,0.3,0,0
2024-04-02,1.7,0.3,1,0
2024-05-02,1.8,0.2,0,0
"""
    result = _summarize_csv([modis_csv, eco_csv], PRODUCTS)
    assert result["status"] == "live"
    # DetailedQA value 2056 has usefulness class 2 and is rejected.
    assert result["modis"]["observationCount"] == 12
    assert result["modis"]["qualityColumnAvailable"] is True
    # The cloudy ECOSTRESS observation is rejected.
    assert result["ecostress"]["observationCount"] == 4
    assert result["ecostress"]["cloudMaskAvailable"] is True
    assert result["ecostress"]["waterMaskAvailable"] is True


def test_modis_marginal_pixels_are_only_accepted_when_detailedqa_confirms_quality():
    modis_csv = """Date,MOD13Q1.061_NDVI,MOD13Q1.061_pixel_reliability,MOD13Q1.061_DetailedQA
2024-01-01,5000,1,2053
2024-01-17,5100,1,2053
2024-02-02,5200,1,2053
2024-02-18,5300,1,2053
2024-03-05,5400,1,2053
2024-03-21,5500,1,2053
2024-04-06,5600,1,2053
2024-04-22,5700,1,2053
2024-05-08,5800,1,2309
2024-05-24,5900,2,2053
2024-06-09,6000,3,2053
"""
    eco_csv = """Date,ECO_L3T_JET.002_ETdaily,ECO_L3T_JET.002_cloud,ECO_L3T_JET.002_water
2024-01-05,2.0,0,0
2024-02-03,2.2,0,0
2024-03-04,1.9,0,0
2024-04-02,1.7,0,0
"""
    result = _summarize_csv([modis_csv, eco_csv], PRODUCTS)
    assert result["modis"]["qualityObservationsSeen"] == 11
    assert result["modis"]["qualityObservationsAccepted"] == 8
    assert result["modis"]["marginalAcceptedWithDetailedQA"] == 8
    assert result["modis"]["marginalRejectedByDetailedQA"] == 1
    assert result["modis"]["observationCount"] == 8



def test_sensor_summaries_return_only_quality_accepted_observation_series():
    modis_csv = """Date,MOD13Q1.061_NDVI,MOD13Q1.061_pixel_reliability,MOD13Q1.061_DetailedQA
2025-01-01,5000,0,2048
2025-01-17,5500,1,2053
2025-02-02,6000,2,2048
2025-02-18,-3000,0,2048
"""
    eco_csv = """Date,ECO_L3T_JET.002_ETdaily,ECO_L3T_JET.002_cloud,ECO_L3T_JET.002_water
2025-01-05,2.0,0,0
2025-02-03,2.2,0,0
2025-03-04,1.9,1,0
"""
    result = _summarize_csv([modis_csv, eco_csv], PRODUCTS)
    # MODIS keeps only reliability=0 and DetailedQA-screened reliability=1 rows.
    assert result["modis"]["series"] == [
        {"date": "2025-01-01", "value": 0.5},
        {"date": "2025-01-17", "value": 0.55},
    ]
    # Cloud-flagged ECOSTRESS data is excluded from the visible plot.
    assert result["ecostress"]["series"] == [
        {"date": "2025-01-05", "value": 2.0},
        {"date": "2025-02-03", "value": 2.2},
    ]

def test_app_eears_csv_without_qa_is_not_live():
    modis_csv = """Date,MOD13Q1.061_NDVI
2024-01-01,5000
2024-01-17,5500
2024-02-02,6000
2024-02-18,6200
"""
    eco_csv = """Date,ECO_L3T_JET.002_ETdaily
2024-01-05,2.0
2024-02-03,2.2
2024-03-04,1.9
2024-04-02,1.7
"""
    result = _summarize_csv([modis_csv, eco_csv], PRODUCTS)
    assert result["status"] == "partial"
    assert result["modis"]["observationCount"] == 0
    assert result["ecostress"]["observationCount"] == 0


def test_xeoi_requires_all_five_live_nasa_streams():
    farm = {
        "currentCrop": "Rice",
        "history": "Rice, Wheat",
        "priority": "Save water",
        "water": "Limited",
        "soilType": "Loam",
        "organicMatter": "1.4",
        "nitrogen": "42",
    }
    nasa = {
        "status": "live",
        "temperatureMeanC": 28.5,
        "rainfallChangePct": -18.0,
        "smapRootZoneAnomalyPct": -12.0,
        "observationCounts": {"powerDailyT2M": 1500, "smapRootZoneDaily": 1500, "gpmImergDaily": 600},
    }
    ancillary = {
        "status": "live",
        "modis": {"status": "live", "observationCount": 40, "mean": 0.58, "trendChangePct": -8.0, "qualityColumnAvailable": True},
        "ecostress": {"status": "live", "observationCount": 6, "mean": 2.1, "trendChangePct": -10.0, "cloudMaskAvailable": True, "waterMaskAvailable": True},
    }
    result = _decision_engine(farm, nasa, ancillary)
    assert result["status"] == "success"
    assert result["engine"] == "KrishiBondhu Explainable Earth Observation Intelligence (XEOI)"
    assert len(result["strategies"]) == 3
    assert result["observationCounts"]["MODIS"] == 40
    assert result["observationCounts"]["ECOSTRESS"] == 6
    assert any("MODIS" in item["source"] for item in result["evidence"])
    assert any("ECOSTRESS" in item["source"] for item in result["evidence"])


def test_xeoi_blocks_missing_advanced_nasa_source():
    result = _decision_engine(
        {"currentCrop": "Rice"},
        {"status": "live", "observationCounts": {"powerDailyT2M": 10, "smapRootZoneDaily": 10, "gpmImergDaily": 10}},
        {"status": "partial", "modis": {"observationCount": 3}, "ecostress": {"observationCount": 0}},
    )
    assert result["status"] == "blocked"
    assert any("ECOSTRESS" in item for item in result["missingSources"])


def test_xeoi_blocks_live_labels_with_zero_observations():
    result = _decision_engine(
        {"currentCrop": "Rice"},
        {"status": "live", "rainfallChangePct": -5, "smapRootZoneAnomalyPct": -3, "temperatureMeanC": 27,
         "observationCounts": {"powerDailyT2M": 0, "smapRootZoneDaily": 0, "gpmImergDaily": 0}},
        {"status": "live",
         "modis": {"status": "live", "observationCount": 0, "qualityColumnAvailable": True, "trendChangePct": -2},
         "ecostress": {"status": "live", "observationCount": 0, "cloudMaskAvailable": True, "waterMaskAvailable": True, "trendChangePct": -2}},
    )
    assert result["status"] == "blocked"
    assert "NASA POWER daily observations" in result["missingSources"]
    assert any("QA-accepted MODIS" in item for item in result["missingSources"])
    assert any("QA-accepted ECOSTRESS" in item for item in result["missingSources"])


def test_app_eears_catalogue_is_paginated_and_required_layers_are_resolved(monkeypatch):
    dummy_page = [{"ProductAndVersion": f"DUMMY{i:03d}.001"} for i in range(500)]
    second_page = [
        {"ProductAndVersion": "MOD13Q1.061"},
        {"ProductAndVersion": "ECO_L3T_JET.003"},
    ]
    calls = []

    def fake_get(path, token=None, params=None):
        calls.append((path, params))
        if path == "product" and params["offset"] == 0:
            return dummy_page
        if path == "product" and params["offset"] == 500:
            return second_page
        if path == "product/MOD13Q1.061":
            return {"250m_16_days_NDVI": {}, "250m_16_days_pixel_reliability": {}, "250m_16_days_DetailedQA": {}}
        if path == "product/ECO_L3T_JET.003":
            return {"ETdaily": {}, "ETuncertainty": {}, "cloud": {}, "water": {}}
        raise AssertionError(f"Unexpected AppEEARS API path: {path}")

    monkeypatch.setattr(main, "_api_get", fake_get)
    products = main._resolve_products("test-token")
    assert products["modisProduct"] == "MOD13Q1.061"
    assert products["ecostressProduct"] == "ECO_L3T_JET.003"
    assert products["modisQualityLayer"] == "250m_16_days_pixel_reliability"
    assert products["modisDetailedQaLayer"] == "250m_16_days_DetailedQA"
    assert {x["layer"] for x in products["requestLayers"] if x["product"] == "MOD13Q1.061"} == {
        "250m_16_days_NDVI", "250m_16_days_pixel_reliability", "250m_16_days_DetailedQA"
    }
    assert products["ecostressEtLayer"] == "ETdaily"
    assert any(path == "product" and params["offset"] == 500 for path, params in calls)



def test_xeoi_allows_previously_verified_cached_nasa_data():
    farm = {"currentCrop": "Rice", "priority": "Save water", "water": "Limited"}
    nasa = {
        "status": "cached", "temperatureMeanC": 28.5, "rainfallChangePct": -18.0,
        "smapRootZoneAnomalyPct": -12.0,
        "observationCounts": {"powerDailyT2M": 100, "smapRootZoneDaily": 100, "gpmImergDaily": 100},
    }
    ancillary = {
        "status": "cached",
        "modis": {"status": "live", "observationCount": 12, "mean": 0.55, "trendChangePct": -4,
                  "qualityColumnAvailable": True},
        "ecostress": {"status": "live", "observationCount": 4, "mean": 2.0, "trendChangePct": -3,
                      "cloudMaskAvailable": True, "waterMaskAvailable": True},
    }
    result = _decision_engine(farm, nasa, ancillary)
    assert result["status"] == "success"
    assert result["observationCounts"]["MODIS"] == 12
    assert result["observationCounts"]["ECOSTRESS"] == 4


def test_claude_guidance_is_validated_and_attached(monkeypatch):
    from main import RotationRequest, _generate_ai_rotation_guidance

    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    from crop_intelligence import recommend_crop_candidates
    farm = {"name": "Test field", "currentCrop": "Rice", "location": "Tangail", "plantingMonth": "11", "soilType": "Loam", "lang": "bn"}
    catalogue = recommend_crop_candidates(farm, {}, {})["candidates"]
    chosen = catalogue[0]
    request = RotationRequest(farm=farm, nasa={"status": "live"}, ancillary={"status": "live"}, lang="bn")
    expected = {
        "heading": "আপনার জমির জন্য পরামর্শ",
        "recommendedPathwayId": "water",
        "recommendedCrop": "ভুল-ফসল",
        "sequence": ["ধান", "ভুল-ফসল"],
        "why": "পানির ঝুঁকি বিবেচনায় এই পথটি আগে যাচাই করুন।",
        "nextSteps": ["জমির পানি দেখুন", "বীজের জাত যাচাই করুন", "স্থানীয় ক্যালেন্ডার মিলিয়ে নিন"],
        "cautions": ["জমিতে পানি দাঁড়ায় কি না দেখুন", "বাজার ও বীজের প্রাপ্যতা যাচাই করুন"],
        "validationNote": "কৃষি কর্মকর্তার সঙ্গে চূড়ান্তভাবে মিলিয়ে নিন।",
    }

    class FakeResponse:
        status_code = 200
        def json(self):
            return {"content": [{"type": "text", "text": __import__("json").dumps(expected, ensure_ascii=False)}]}

    def fake_post(*args, **kwargs):
        assert kwargs["json"]["model"] == main.CHAT_MODEL
        return FakeResponse()

    monkeypatch.setattr(main.requests, "post", fake_post)
    output = _generate_ai_rotation_guidance(request, {
        "strategies": [{"id": "water", "score": 75, "sequence": ["ধান", chosen["cropBn"]], "candidateCrop": chosen}],
        "cropCandidates": catalogue, "cropCalendar": {}, "evidence": [], "indices": {}, "dataCoverageConfidence": 90
    })
    assert output["recommendedCrop"] == chosen["cropBn"]
    assert output["sequence"] == ["ধান", chosen["cropBn"]]
    assert output["model"] == main.CHAT_MODEL
    assert len(output["nextSteps"]) == 3


def test_claude_guidance_requires_private_api_key(monkeypatch):
    from fastapi import HTTPException
    from main import RotationRequest, _generate_ai_rotation_guidance

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    request = RotationRequest(farm={}, nasa={}, ancillary={})
    try:
        _generate_ai_rotation_guidance(request, {"strategies": []})
        assert False, "Expected an explicit backend configuration error"
    except HTTPException as exc:
        assert exc.status_code == 503


def test_crop_calendar_filters_candidates_by_selected_month_and_rotation_family():
    from crop_intelligence import recommend_crop_candidates

    farm = {
        "location": "Tangail, Bangladesh", "currentCrop": "Rice", "history": "Rice, Wheat",
        "plantingMonth": "11", "soilType": "Loam", "water": "Limited", "drainage": "Good",
        "salinity": "Low", "lang": "bn",
    }
    result = recommend_crop_candidates(farm, {}, {}, 11)
    assert result["candidateCount"] > 0
    assert all(11 in item["plantingMonths"] for item in result["candidates"])
    assert all(item["relativeFitScore"] <= 100 for item in result["candidates"])
    assert any(item["family"] == "Fabaceae" for item in result["candidates"])
    assert result["barcSuitability"]["status"] == "not_checked_live"


def test_coastal_rabi_mung_is_not_shown_as_nationwide():
    from crop_intelligence import recommend_crop_candidates

    common = {"currentCrop": "Rice", "plantingMonth": "1", "soilType": "Sandy", "drainage": "Good"}
    coastal = recommend_crop_candidates({**common, "location": "Bhola, Bangladesh"}, {}, {}, 1)
    inland = recommend_crop_candidates({**common, "location": "Tangail, Bangladesh"}, {}, {}, 1)
    assert any(x["id"] == "mung_coastal_rabi" for x in coastal["candidates"])
    assert not any(x["id"] == "mung_coastal_rabi" for x in inland["candidates"])
    assert any(x.get("crop") == "মুগ ডাল (উপকূলীয় রবি)" for x in inland["excludedRegionalCandidates"])


def test_all_five_soil_test_inputs_are_screened_with_explicit_units():
    from crop_intelligence import _soil_nutrient_flags

    screen = _soil_nutrient_flags({
        "soilPh": "5.0", "organicMatter": "1.0", "nitrogen": "0.08",
        "phosphorus": "5", "potassium": "0.09",
    })
    assert set(screen["flags"]) == {
        "low_organic_matter", "low_total_nitrogen_screen",
        "low_available_phosphorus_screen", "low_exchangeable_potassium_screen",
    }
    assert screen["validValues"]["soilPh"] == 5.0
    assert "extraction method" in screen["interpretation"]


def test_implausible_lab_units_are_excluded_not_rewarded():
    from crop_intelligence import _soil_nutrient_flags

    screen = _soil_nutrient_flags({"soilPh": "6.2", "organicMatter": "1.2", "nitrogen": "42",
                                   "phosphorus": "7000", "potassium": "900"})
    assert set(screen["invalidFields"]) == {
        "totalNitrogenPct", "availablePhosphorusMgKg", "exchangeablePotassiumCmolKg",
    }
    assert screen["validValues"]["totalNitrogenPct"] is None
    assert screen["validValues"]["availablePhosphorusMgKg"] is None
    assert screen["validValues"]["exchangeablePotassiumCmolKg"] is None


def test_modis_and_ecostress_affect_water_screen_only_as_a_joint_signal():
    from crop_intelligence import recommend_crop_candidates

    farm = {"location": "Tangail", "currentCrop": "Rice", "plantingMonth": "11",
            "soilType": "Loam", "water": "Limited", "drainage": "Good"}
    nasa = {"rainfallChangePct": -18, "smapRootZoneAnomalyPct": -12}
    neutral = {"modis": {"trendChangePct": 0}, "ecostress": {"trendChangePct": 0}}
    joint_decline = {"modis": {"trendChangePct": -18}, "ecostress": {"trendChangePct": -20}}
    base = recommend_crop_candidates(farm, nasa, neutral, 11)
    stressed = recommend_crop_candidates(farm, nasa, joint_decline, 11)
    assert stressed["waterStressContext"] > base["waterStressContext"]
    assert stressed["scoringWeights"] != ""


def test_candidate_catalogue_contains_crop_characteristics_and_sources():
    from crop_intelligence import CROP_DATABASE

    required = {"id", "crop", "bn", "family", "months", "duration", "water", "soils",
                "ph", "drainage", "legume", "root", "nutrientDemand", "rotationBreak", "sources"}
    assert len(CROP_DATABASE) >= 12
    assert all(required.issubset(set(row)) for row in CROP_DATABASE)
    assert all(row["sources"] and all(x.startswith("https://") for x in row["sources"]) for row in CROP_DATABASE)


def test_xeoi_allows_explicit_preliminary_three_source_result_without_faking_modis_ecostress():
    farm = {
        "name": "Demo field", "location": "Gazipur, Bangladesh", "currentCrop": "Rice",
        "history": "Rice, Wheat", "priority": "Save water", "water": "Limited",
        "soilType": "Sandy Loam", "plantingMonth": "11", "lang": "bn",
    }
    nasa = {
        "status": "live", "temperatureMeanC": 28.5, "rainfallChangePct": -18.0,
        "smapRootZoneAnomalyPct": -12.0,
        "observationCounts": {"powerDailyT2M": 1500, "smapRootZoneDaily": 1500, "gpmImergDaily": 600},
    }
    ancillary = {
        "status": "partial",
        "modis": {"status": "live", "observationCount": 3, "qualityObservationsAccepted": 3,
                  "qualityColumnAvailable": True, "mean": 0.47, "trendChangePct": None},
        "ecostress": {"status": "live", "observationCount": 30, "qualityObservationsAccepted": 30,
                      "cloudMaskAvailable": True, "waterMaskAvailable": True,
                      "mean": 1.62, "trendChangePct": -7.37},
    }
    result = _decision_engine(farm, nasa, ancillary, allow_partial=True)
    assert result["status"] == "success"
    assert result["decisionModeCode"] == "preliminary_three_source"
    assert result["sourcesUsed"] == 3
    assert result["fullFiveSourceEligible"] is False
    assert result["observationCounts"]["MODIS"] == 3
    assert result["observationCounts"]["ECOSTRESS"] == 30
    assert result["indices"]["modisMeanNdvi"] is None
    assert result["indices"]["ecostressMeanEtMmDay"] is None
    assert not any("MODIS" in item["source"] or "ECOSTRESS" in item["source"] for item in result["evidence"])
    assert "PRELIMINARY ONLY" in result["decisionNote"]
    assert len(result["strategies"]) == 3
    assert len(result["cropCandidates"]) > 0


def test_xeoi_full_five_source_remains_blocked_unless_qa_thresholds_pass():
    farm = {"location": "Gazipur, Bangladesh", "currentCrop": "Rice", "plantingMonth": "11"}
    nasa = {
        "status": "live", "temperatureMeanC": 28.5, "rainfallChangePct": -18.0,
        "smapRootZoneAnomalyPct": -12.0,
        "observationCounts": {"powerDailyT2M": 1500, "smapRootZoneDaily": 1500, "gpmImergDaily": 600},
    }
    ancillary = {
        "status": "partial",
        "modis": {"status": "live", "observationCount": 3, "qualityColumnAvailable": True, "trendChangePct": None},
        "ecostress": {"status": "live", "observationCount": 30, "cloudMaskAvailable": True, "waterMaskAvailable": True, "trendChangePct": -7.37},
    }
    result = _decision_engine(farm, nasa, ancillary, allow_partial=False)
    assert result["status"] == "blocked"
    assert "MODIS" in " ".join(result["missingSources"])



def test_rotation_request_accepts_explicit_preliminary_mode():
    from main import RotationRequest
    request = RotationRequest(farm={"currentCrop": "Rice"}, nasa={"status": "live"}, allowPartial=True)
    assert request.allowPartial is True
    assert request.ancillary == {}


def test_claude_guidance_prompt_discloses_preliminary_sources(monkeypatch):
    import json
    from main import RotationRequest, _decision_engine, _generate_ai_rotation_guidance
    from crop_intelligence import recommend_crop_candidates

    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    farm = {"location": "Gazipur, Bangladesh", "currentCrop": "Rice", "plantingMonth": "11", "soilType": "Sandy Loam", "lang": "bn"}
    nasa = {"status": "live", "temperatureMeanC": 28.5, "rainfallChangePct": -18.0, "smapRootZoneAnomalyPct": -12.0,
            "observationCounts": {"powerDailyT2M": 100, "smapRootZoneDaily": 100, "gpmImergDaily": 100}}
    ancillary = {"status": "partial", "modis": {"status": "live", "observationCount": 3, "qualityColumnAvailable": True},
                 "ecostress": {"status": "live", "observationCount": 30, "cloudMaskAvailable": True, "waterMaskAvailable": True, "trendChangePct": -7.0}}
    result = _decision_engine(farm, nasa, ancillary, allow_partial=True)
    chosen = next(x for x in result["strategies"] if x.get("candidateCrop"))
    expected = {"heading": "প্রাথমিক পরামর্শ", "recommendedPathwayId": chosen["id"],
                "recommendedCrop": chosen["candidateCrop"]["cropBn"], "sequence": chosen["sequence"],
                "why": "প্রাথমিকভাবে তিনটি NASA উৎস ও ফসল ক্যালেন্ডার ব্যবহার করা হয়েছে।",
                "nextSteps": ["স্থানীয় মৌসুম যাচাই করুন", "বীজের জাত যাচাই করুন", "জমির পানি ও নিষ্কাশন দেখুন"],
                "cautions": ["MODIS/ECOSTRESS এখনো স্কোরে ব্যবহৃত হয়নি", "স্থানীয় কৃষি কর্মকর্তার সঙ্গে মিলিয়ে নিন"],
                "validationNote": "এটি প্রাথমিক ৩-source পরামর্শ; পূর্ণ পাঁচ-source XEOI নয়। BARC ও স্থানীয় কর্মকর্তার সঙ্গে যাচাই করুন।"}
    class FakeResponse:
        status_code = 200
        def json(self):
            return {"content": [{"type": "text", "text": json.dumps(expected, ensure_ascii=False)}]}
    calls = {}
    def fake_post(*args, **kwargs):
        calls.update(kwargs)
        return FakeResponse()
    monkeypatch.setattr(main.requests, "post", fake_post)
    request = RotationRequest(farm=farm, nasa=nasa, ancillary=ancillary, lang="bn", allowPartial=True)
    output = _generate_ai_rotation_guidance(request, result)
    assert output["recommendedPathwayId"] == chosen["id"]
    assert "PRELIMINARY THREE-SOURCE" in calls["json"]["system"]


def test_modis_fill_dn_is_not_scaled_into_a_plausible_ndvi_value():
    modis_csv = """Date,MOD13Q1.061_NDVI,MOD13Q1.061_pixel_reliability,MOD13Q1.061_DetailedQA
2024-01-01,-3000,0,2048
2024-01-17,5000,0,2048
"""
    eco_csv = """Date,ECO_L3T_JET.002_ETdaily,ECO_L3T_JET.002_cloud,ECO_L3T_JET.002_water
2024-01-05,2.0,0,0
2024-02-03,2.2,0,0
2024-03-04,1.9,0,0
2024-04-02,1.7,0,0
"""
    result = _summarize_csv([modis_csv, eco_csv], PRODUCTS)
    assert result["modis"]["qualityObservationsSeen"] == 1
    assert result["modis"]["qualityObservationsAccepted"] == 1
    assert result["modis"]["mean"] == 0.5


def test_appeears_sampling_months_are_calendar_months_not_30_day_approximations():
    from datetime import date
    from main import _subtract_calendar_months

    assert _subtract_calendar_months(date(2026, 11, 2), 36) == date(2023, 11, 2)
    assert _subtract_calendar_months(date(2024, 3, 31), 1) == date(2024, 2, 29)


def test_decision_api_returns_preliminary_with_seven_modis_and_blocks_full_mode(monkeypatch):
    from fastapi.testclient import TestClient
    import main

    monkeypatch.setattr(main, "_chat_rate_ok", lambda client: True)
    monkeypatch.setattr(main, "_generate_ai_rotation_guidance", lambda request, result: {
        "heading": "প্রাথমিক পরামর্শ",
        "recommendedPathwayId": next(x["id"] for x in result["strategies"] if x.get("candidateCrop")),
        "recommendedCrop": next(x["candidateCrop"]["cropBn"] for x in result["strategies"] if x.get("candidateCrop")),
        "sequence": ["ধান", "মসুর ডাল"],
        "why": "পরীক্ষামূলক API response",
        "nextSteps": ["মৌসুম যাচাই", "জাত যাচাই", "মাটি যাচাই"],
        "cautions": ["এটি প্রাথমিক", "স্থানীয়ভাবে যাচাই করুন"],
        "validationNote": "পূর্ণাঙ্গ পাঁচ উৎসের ফল নয়।",
    })
    body = {
        "farm": {"name": "Demo Farm", "location": "Gazipur, Bangladesh", "currentCrop": "Rice",
                 "soilType": "Sandy Loam", "water": "Limited", "priority": "Save water", "plantingMonth": "11"},
        "nasa": {"status": "live", "temperatureMeanC": 28.5, "rainfallChangePct": -18,
                 "smapRootZoneAnomalyPct": -12,
                 "observationCounts": {"powerDailyT2M": 1500, "smapRootZoneDaily": 1500, "gpmImergDaily": 600}},
        "ancillary": {"status": "partial",
                      "modis": {"status": "live", "observationCount": 7, "qualityObservationsAccepted": 7,
                                "qualityObservationsSeen": 46, "qualityColumnAvailable": True, "trendChangePct": -4},
                      "ecostress": {"status": "live", "observationCount": 29, "qualityObservationsAccepted": 29,
                                    "qualityObservationsSeen": 29, "cloudMaskAvailable": True,
                                    "waterMaskAvailable": True, "trendChangePct": -7.37}},
        "lang": "bn", "allowPartial": True,
    }
    client = TestClient(main.app)
    partial = client.post("/api/decision/rotation", json=body)
    assert partial.status_code == 200, partial.text
    assert partial.json()["decisionModeCode"] == "preliminary_three_source"
    assert partial.json()["sourcesUsed"] == 3
    assert all("MODIS" not in row["source"] and "ECOSTRESS" not in row["source"] for row in partial.json()["evidence"])

    body["allowPartial"] = False
    full = client.post("/api/decision/rotation", json=body)
    assert full.status_code == 409
    assert "MODIS" in full.text
