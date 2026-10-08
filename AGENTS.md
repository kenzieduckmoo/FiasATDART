# Fiamma Collector development

- Keep this standalone addon separate from DuckMooFolio and Concentration Planner. SavedVariables: FiammaCollectorDB.
- Preserve the compact dark palette, white text, and yellow numeric values. No giant cards or explanatory blocks in the main window; full context belongs in tooltips.
- Retain independent expansion filters, section collapse states, snapshots, and the ATDART target.
- ATT access is optional and read-only. Do not change ATT data, filters, or collection flags, or bundle its database.
- Unknown expansions are not legacy. The legacy cutoff remains Dragonflight unless the user requests a change.
- Use Lua 5.1; recycle native frames and avoid accumulating tooltip hooks.
- Run tests/run_tests.py and package with tools/package.py. Report native Retail validation separately from mock tests.

- Canonical repository: https://github.com/kenzieduckmoo/FiasATDART. Keep runtime folder/TOC identity FiammaCollector for compatibility.
- From the repository root, validate with python3 tests/run_tests.py and build with python3 tools/package.py. ZIPs must contain a FiammaCollector root and exclude .git and .github.
