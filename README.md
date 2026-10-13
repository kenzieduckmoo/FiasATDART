# Fia's ATDART

Custom version of the ATT tab from DuckMoo Services: Character Folio, made for Fia. Go follow her at [twitch.tv/fiamma](https://www.twitch.tv/fiamma).

The installed addon folder remains **FiammaCollector** for compatibility with v0.1.0.

**DuckMoo Services · v0.1.2 · By DuckMoo Media**

A little collector cockpit made for Fiamma: black and charcoal surfaces, dark purple controls, white text, and yellow numbers. It contains the ATT functionality from Character Folio in a separate, compact addon.

## Install

Extract **FiammaCollector** into `_retail_/Interface/AddOns/`. Enable the addon and All The Things for each character. Open with **/fiamma**, **/atdart**, or the minimap button. No Character Folio or Concentration Planner installation is required.

Open ATT and allow its main list to prepare, then click **Refresh**. On a character's first opening, the collector attempts an initial capture if ATT is ready. After that, Refresh deliberately captures a new snapshot.

## The compact window

- **ATDART % Target:** The legacy dungeon or raid with the lowest exact completion fraction. Equal minima are picked randomly once per capture. The saved target survives browsing and reloads. This is the only percentage display.
- **ATDART exclusion:** Dawn of the Infinite cannot be the ATDART target. It remains in the normal dungeon rankings and capture data. Existing saved Dawn targets are replaced automatically on display, including offline snapshots; other saved targets keep their current choice.
- **Legacy Dungeons / Legacy Raids:** Highest missing-count opportunities first. Legacy stops at Dragonflight, excluding The War Within and Midnight. Unclassified instances are omitted rather than guessed.
- **Unfinished Quests:** Zones ranked by distinct visible, collectible, uncollected quests. Capital cities are excluded. Expansion labels use ATT metadata and map ancestry.
- **Section headers:** Click the left side to collapse or expand. Use the right side to filter that section independently by expansion. All matching snapshot rows remain accessible through the shared scrollbar.
- **Hover a row:** Shows its expansion, exact missing count, and profile context. Hover the character selector for the full timestamp, active ATT profile, or loading message.
- **Character selector:** Browse retained snapshots from characters who have logged in with this addon. Refresh is available for the logged-in character.
- **Window controls:** Drag the title to move; drag the bottom-right corner to resize. Size, position, section collapse states, and expansion filters are saved. The window shrinks to its content when sections collapse, up to your preferred height.
- **Minimap:** Left-click opens/closes. Right-click refreshes the logged-in character. Drag to reposition. `/fiamma minimap` toggles visibility; `/fiamma refresh` opens and refreshes.

ATT unavailable or not ready? The window shows a message, while previously saved snapshots remain accessible. **Open ATT** works while ATT is preparing its data. The **?** control contains a compact usage tooltip.

## Reading the numbers

Counts follow the ATT profile and character/availability filters present at capture. They represent collection opportunities, not drop probabilities, guaranteed obtainable rewards, or runs required. An account-wide profile can include collectibles unavailable to a particular character. Configure ATT's filters before capture for useful character-specific results.

The collector reads ATT's prepared main tree, performs small batched scans, and never modifies ATT's data or collection flags. Instance totals come from the outer instance entries in its main Dungeons & Raids category. Alternate copies under achievements, professions, dynamic shortcuts and nested difficulty references do not override those counts. If two canonical entries conflict, that instance is omitted rather than choosing the worse-looking copy. If the main category is unavailable, the previous snapshot is retained and a loading message is shown. The Encounter Journal tier is restored after classification. Snapshot timestamps use your computer's local time. Offline snapshots are saved observations, not live queries. Refresh is deferred in combat.

**Upgrading from 0.1.0:** open ATT and let its main list finish updating, then click Refresh on each character whose snapshot you use. Older captures are retained, but their instance rankings and ATDART percentage are hidden until refreshed because they may contain incorrect reference-group totals. Quest snapshots remain available. No SavedVariables deletion is needed. Firelands at 294/303 collected is 97.03% with 9 missing; a separate 10/193 reference must not replace that main entry. ATDART may then select a different, genuinely less-complete instance.

## Source and testing

The installable ZIP includes all runtime Lua files, the TOC, license and user documentation, inside the required FiammaCollector folder. It is also the full addon package for CurseForge upload; development tests, tools, repository files and player data are excluded. Tests remain in this repository: install `requirements-dev.txt`, then run `python3 tests/run_tests.py`. Build the ZIP with `python3 tools/package.py`. These tests run Lua 5.1 with mocked Blizzard UI/APIs; actual Retail client validation is still required.

The ATT adapter is derived from DuckMoo Services: Character Folio v0.3.0. This addon has its own `FiammaCollectorDB` and can coexist with Folio and Concentration Planner. All The Things remains a separately installed addon; none of its source or database is bundled.

GNU GPL v3. Copyright 2026 DuckMoo Media. See LICENSE.

Future source updates for this addon belong in [kenzieduckmoo/FiasATDART](https://github.com/kenzieduckmoo/FiasATDART).
