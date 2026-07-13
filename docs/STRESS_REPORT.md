# Stress Report

**Status:** framework initialized; no design-substantiation margins released.

## 1. Scope

Representative forward pylon-to-wingbox attachment fitting, educational use only.

## 2. Load path

See `docs/LOAD_PATH_AND_FBD.md`. A two-station statics model converts external pylon loads to forward/aft station reactions. A left/right fitting pair at the forward station reacts station force and a selected share of roll moment.

## 3. Classical methods implemented

- lug net-section stress;
- projected bearing stress;
- two-plane shear-out stress using the physical edge ligament;
- pin/fastener shear;
- rectangular-section bending stress;
- eccentric fastener-group shear distribution;
- general elastic fastener-group tension distribution;
- simultaneous shear/tension interaction;
- prying augmentation only when an explicit sourced increment/factor is supplied.

## 4. Results

Only synthetic arithmetic smoke-test results exist. They are not reportable aircraft margins.

## 5. Required before first released margin table

- source-backed representative load cases;
- frozen geometry revision;
- product-form-specific material and fastener allowables;
- safety-factor policy;
- benchmark evidence;
- extraction-rule identifiers.
