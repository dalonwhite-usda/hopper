# HOPPER Model Reconstruction (from readable legacy files)

Date: 2026-05-29

## Scope and method

This document reconstructs the original 1994 HOPPER workflow using:

- Readable legacy files under original_files/HOPPER
- Current Python rewrite under ghipm

This is a practical reconstruction, not a claim of perfect one-to-one equivalence with the DOS binaries.

## Files reviewed

### Legacy documentation and outputs

- EXPLAIN.TXT
- DISCLAIM.TXT
- RESULTS.RPT
- ECON.LPO
- USERPARM.LST

### Legacy inputs and parameter tables

- FORAGE.IN
- CURRENT.WTR
- YIELD$.DAT
- SITES.DAT
- LAST.EC3
- ~TUTOR.EC3
- GENERIC.GN3

### Legacy LP deck artifacts

- WYCOW.LP, WYC_S.LP, NDCOW.LP, NE_CC.LP (representative)

### Current Python rewrite

- ghipm/data_io/*.py
- ghipm/bio/*.py
- ghipm/econ_lp/*.py
- ghipm/cli.py

## High-level model concept

HOPPER appears to be a multi-stage decision system that combines:

1. A biological forage response model (weather and forage-type response)
2. A treatment effect layer (yield and mortality differences by insecticide option)
3. A ranch economic linear program (monthly feed and grazing allocation)
4. A treatment comparison report (return delta, benefit/cost, and ecological notes)

The system evaluates "No Treatment" and multiple treatment options, solving the ranch economics for each option, then reporting incremental return and B/C ratio relative to baseline.

## Reconstructed workflow

### Stage 1: User/run configuration

Evidence:

- LAST.EC3, ~TUTOR.EC3, GENERIC.GN3 contain run/session snapshots.
- USERPARM.LST lists interface parameter keys (objective, weather, treatment date, bees, canopy, sensitive areas, life stage/hatch, etc.).

Interpretation:

- User selects a ranch/economic template and scenario conditions.
- User enters treatment timing and ecological constraints (for example, insectaries, bees, environmentally sensitive zones).

### Stage 2: Weather and forage response

Evidence:

- FORAGE.IN has warm/cool/forb thermal parameters and active-window percentages.
- CURRENT.WTR is daily weather by day-of-year.
- Python reader converts weather to monthly mean C and applies triangular temperature response.

Interpretation:

- For each forage class (warm-season grass, cool-season grass, forbs), growth weight is computed from:
  - Triangular temperature response (min, opt, max)
  - Seasonal activity factor (percent of growth window)
- Class responses are mixed (currently 0.5 warm, 0.35 cool, 0.15 forb in Python) to generate monthly production weights.
- Annual forage is distributed across months using those weights.

### Stage 3: Treatment yield effects

Evidence:

- YIELD$.DAT stores absolute forage yield by treatment (lbs/acre).
- RESULTS.RPT table shows yield, treatment cost, B/C, eggs/yd2.
- Python Treatment definitions include cost/ac, mortality %, eggs/yd2.

Interpretation:

- "No Treatment" establishes baseline yield.
- Each treatment has:
  - absolute yield target (lbs/ac)
  - treatment cost per acre
  - mortality/egg indicators used in reporting/explanation
- Monthly forage profile is scaled so annual total matches each treatment yield.

### Stage 4: Ranch economics LP

Evidence:

- WYCOW.LP and related LP files include livestock, hay, monthly forage, lease, and feed purchase variable structures.
- RESULTS.RPT and ECON.LPO show repeated optimal solves by treatment and report RETURN.
- Python LP has monthly balance constraints, hay inventory, lease caps, feed purchases, and objective maximizing return (implemented as minimizing costs).

Interpretation:

- For each month, herd forage requirement must be met by:
  - natural forage on treated acres
  - on-hand hay use
  - purchased hay
  - leased grazing (AUM converted to lbs)
- Lease use is limited by annual caps and allowed grazing months.
- Objective is economic return (legacy likely full ranch profit accounting; Python currently focuses on major feed/lease/treatment cost terms).

### Stage 5: Treatment recommendation and narrative filters

Evidence:

- EXPLAIN.TXT explains elimination/selection logic and ecological caveats.
- DISCLAIM.TXT states legal and scientific caution.
- RESULTS.RPT includes notes such as insectary buffer guidance and chemical restrictions.

Interpretation:

- Beyond pure economics, HOPPER applies rule-based treatment filtering or caution flags:
  - insectaries or beneficials present
  - managed bees
  - environmentally sensitive areas
  - chemical spray restrictions
- Final output is not only numerical rank but a constrained recommendation set plus rationale.

## Inputs needed (reconstructed)

### Core numeric files

- FORAGE.IN: forage class thermal/activity parameters
- CURRENT.WTR: daily weather records
- YIELD$.DAT: treatment yield outcomes (lbs/ac)
- SITES.DAT: weather-generation/site coefficients and station metadata

### Scenario and ranch configuration

- EC3/GN3 templates (for example LAST.EC3, ~TUTOR.EC3):
  - herd size and enterprise setup
  - treatment cost/mortality table
  - hay production and purchase options
  - lease capacities, season windows, and prices
  - treated acreage and site selection
  - survey/treatment timing and pest metrics

### Decision/rule inputs

- USERPARM.LST key family suggests switches for:
  - weather class
  - canopy condition
  - life stage and hatch status
  - target species proportion
  - beneficial insect protections and chemical restrictions

## Outputs produced (reconstructed)

### Economic comparison table by treatment

- Yield (lbs/ac)
- Total treatment cost
- Return change relative to No Treatment
- Benefit/Cost ratio
- Eggs per yd2 (ecological follow-on indicator)

### Solver/log artifacts

- LP optimization summary per treatment (optimality, pivots, objective value)

### Narrative explanation and cautions

- Why treatments were excluded or cautioned
- Environmental handling notes (buffers, bait-only contexts)
- Global disclaimer

## Mapping to current Python implementation

### Implemented in Python

- Legacy file readers for FORAGE.IN, CURRENT.WTR, YIELD$.DAT
- Monthly forage shaping from thermal response
- Treatment list and per-treatment economics loop
- Pyomo LP with feed-balance, hay inventory, lease caps, purchase variables
- Baseline-vs-treatment reporting with return delta and B/C

### Present but not yet fully integrated

- SITES.DAT parser concept exists but module currently has syntax/import issues and is not wired into the run path
- Multi-template regional LP deck replacement is simplified into one compact LP structure
- Rule/expert-system elimination logic from explanation files is only partially represented (mostly as static notes)

### Likely gaps versus original DOS system

- Full enterprise economics from larger LP decks (crop/livestock detail, labor/borrowing/auxiliary activities)
- Dynamic grasshopper population trajectory beyond one-step treatment comparison
- Rich rule base for recommendation filtering and text explanation generation
- UI/workflow behavior from original executables and help systems

## Interpretation of LP artifacts

LP files appear to be matrix-deck style formulations containing:

- Variable and constraint name dictionaries
- Index-to-coefficient blocks
- Monthly activity columns for feed/grazing flows
- Ranch enterprise activity accounting

This confirms the original system solved linear programs with treatment-specific forage perturbations, not just heuristic scoring.

## Known inaccessible or less-readable components

Not directly reconstructed from source logic:

- Executables (*.EXE)
- Binary/help/overlay assets (*.HLP, *.OVR, some proprietary formats)
- Graphics assets (*.PCX)

These likely contain UI behavior and possibly some business rules not exposed in text files.

## Practical next reconstruction targets

1. Build a robust parser/translator for LP deck files into a transparent model spec.
2. Implement rule-based treatment filtering/explanations from USERPARM keys and EXPLAIN behavior.
3. Normalize EC3/GN3 scenario files into typed Python configs (Pydantic models).
4. Expand economic objective to include full revenue/cost structure reflected by legacy decks.
5. Add golden tests that compare Python outputs against RESULTS.RPT and ECON.LPO for known scenarios.

## Bottom line

The readable legacy files support a clear architecture:

- Biophysical forage response + treatment yield effects + ranch LP economics + rule-based recommendation narrative.

Your current rewrite already captures the backbone of that architecture. The biggest missing pieces are the full legacy LP economic breadth and the explicit rule/explanation engine that mediated recommendations under ecological constraints.
