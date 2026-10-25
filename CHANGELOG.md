# v0.1.3

- Add clickable zone quest reports with counted IDs/names, copyable text and a native ATT zone window. Add `/atdart quests` and `/atdart quest ID`.
- Add optional `/atdart debug on|off` capture of excluded/duplicate visited entries, direct and recursive filters, character quest completion, flags and ATT paths/version/profile. Bound stored diagnostic work and report truncation.
- Preserve counting policy, retained/offline snapshots, ATT filters and collection state. Add a simulated 18-versus-3 parent-filter diagnostic case and native-window/read-only/UI-reuse checks. Real Fia-client validation remains pending.

# v0.1.2

- Exclude Dawn of the Infinite (Encounter Journal instance 1209) from ATDART selection only. Preserve its normal dungeon ranking and captured completion data.
- Replace previously saved Dawn targets on display, including offline snapshots, without rerolling other saved targets or requiring a new capture.
- Verify new captures, saved targets, localized names, stable replacement and Dawn-only snapshots under Lua 5.1. Preserve the 0.1.1 completion-count repair.

# v0.1.1

- Package the complete installable addon for CurseForge with the FiammaCollector root folder, runtime code, license and guide; exclude development and repository files.
- Fix incorrect instance totals caused by choosing the largest missing count across every ATT reference to an instance. Read the outer instance entry from the main Dungeons & Raids category instead; ignore alternate, nested and dynamic reference groups.
- Omit ambiguous canonical counts and preserve prior captures when the main category is unavailable. Require Refresh for old instance snapshots without deleting their data or quest history.
- Reproduce the Firelands mismatch: original code selects 10/193 (5.18%) instead of the canonical 294/303 (97.03%, 9 missing). Add native-label, traversal-order, read-only and snapshot-upgrade checks. Actual Fia client verification remains required.

# v0.1.0

- Standalone ATT collector companion made for Fiamma.
- Compact dark interface with white labels, yellow numbers, and dark purple controls.
- ATDART target, legacy dungeon/raid rankings, unfinished zone quests, per-section expansion filters, and retained per-character snapshots.
- Collapsible lists, shared scrolling, content-fitting height, saved position/size, minimap access, and /fiamma /atdart commands.
- Native UI and adapter regression tests; real Retail client verification still needed.

