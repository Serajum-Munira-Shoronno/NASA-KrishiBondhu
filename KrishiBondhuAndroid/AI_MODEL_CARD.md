# NASA KrishiBondhu XEOI model card

## Intended use

Support a farmer and local agriculture officer in comparing crop-rotation pathways for a selected Bangladesh field. This is a screening and decision-support prototype, not an automated planting prescription.

## Components

- **XEOI decision engine:** deterministic, explainable multi-criteria evidence-fusion and crop-candidate ranking.
- **Bangladesh crop-intelligence catalogue:** 14 crop/season entries with sowing/planting months, crop family, typical duration where available, relative water need, soil texture/pH screen, drainage, root form, nutrient demand, rotation-break flag and official reference links.
- **Claude Sonnet 5.5:** server-side language component used to explain candidate pathways in plain Bangla/English. It does not manufacture missing NASA data, add crops outside the catalogue or change numeric XEOI scores.

## Inputs

- Farmer: current crop, crop history, field location/coordinates, selected planning month, soil texture, pH, organic matter, total N %, available P mg/kg, exchangeable K cmol(+)/kg, water availability, drainage, salinity and goal/priority.
- NASA POWER: daily temperature and meteorological context.
- NASA SMAP L4 via NASA POWER: surface/root-zone moisture values and same-month root-zone anomaly.
- NASA GPM IMERG via NASA POWER: daily precipitation aggregated into complete monthly totals for recent 12-month versus prior 12-month comparison.
- NASA MODIS/Terra MOD13Q1.061: QA-screened 250 m, 16-day NDVI composites plus an associated quality layer.
- NASA ECOSTRESS L3 JET: QA-screened ETdaily with cloud and open-water masks; overpass timing is irregular.

## Decision method

1. Filter crop candidates to the selected planting month and region conditions. The database is a national reference screen, not live BARC upazila zoning.
2. Score crop candidates using crop family/history, soil texture, pH screen, drainage, salinity, nutrient-demand class, farmer water access and stated goal.
3. Soil inputs are read only when plausibly within the units labelled in the app. Very implausible values are excluded and returned as warnings. Critical levels are method-specific and must be checked against the lab/SRDI/BARC reference ranges.
4. Water-deficit screening combines recent rainfall deficit and SMAP root-zone anomaly. MODIS greenness decline contributes context. ECOSTRESS ET decline is counted only when MODIS greenness also declines and rainfall/SMAP indicate water deficit; ET change by itself is not drought diagnosis.
5. NASA POWER temperature contributes broad heat context.
6. Produce an existing-practice baseline and two actionable pathways: soil-health/legume and water-smart. Each actionable crop comes from the filtered catalogue. Farmer priority changes the weights.
7. Claude receives the measured evidence, scores and verified crop candidate list and returns short explanations, next steps and cautions. Backend validates the pathway and locks the crop/sequence to the selected catalogue candidate.

## Score meaning

All 0–100 values are relative screening/alignment scores within this prototype. They are not calibrated suitability probabilities, yield forecasts, profit predictions or a guarantee of crop success.

## Quality gates

- POWER, SMAP and GPM need non-zero observations.
- MODIS needs a supported quality layer and at least 8 accepted NDVI observations.
- ECOSTRESS needs cloud and water masks and at least 4 accepted ETdaily observations.
- MODIS DetailedQA is decoded as a bit field; invalid/low-quality classes are rejected.
- ECOSTRESS cloud and open-water observations are excluded. Missing values are not replaced by zero.
- Missing sources/metrics or no crop candidate in the selected month blocks the full plan; sample values are never substituted.

## Limitations

- No labelled field harvest, irrigation-cost or soil-outcome data were supplied, so this is not a supervised yield ML model.
- BARC district/upazila suitability is linked for manual verification, not queried live by the current version.
- The crop calendar is a compact national screening reference. Variety, actual sowing day, local soil series, flood/salinity exposure, disease break, input access and market must be checked locally.
- Satellite products have different pixel sizes, temporal cadences and observation support; a point sample does not represent every part of a small field.
- NDVI is greenness context, not crop identification or disease diagnosis; ECOSTRESS ET is an irregular overpass estimate, not a field sensor.
- Thresholds for soil-test flags depend on extraction methods and soil groups. No fertilizer or pesticide doses are provided.

## Validation needed

Before claiming predictive performance, collect multiple seasons of georeferenced crop/variety, sowing/harvest date, yield, irrigation, input, price, soil-lab and management data. Compare recommendations with independent BARC/DAE agronomist review and measured outcomes by agroecological zone. Report missing-data rates and failure modes.
