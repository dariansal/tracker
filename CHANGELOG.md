# Changelog

Each entry says what changed, whether any file in `assets/` changed, and whether a new capability is needed. Updates use this to decide what to re-upload.

## 1.1.1 (2026-09-28)

- Protein goal is now shown as a **range** rather than a single number: 0.9 to 1.1 grams per pound of body weight (for example, `151–185 g`). The bar fills toward the low end, and the goal counts as met with a check once you reach that low end (i.e. you're in the range).

Assets changed: none.
New capabilities: none.

## 1.1.0 (2026-09-28)

- Food tab: a **daily protein goal**. A slim bar under the totals fills as you eat protein and marks the goal met with a check. The goal is 1 gram per pound of body weight, taken from the previous completed week's average weight (weeks start Monday); until there is a previous week, it uses your latest weigh-in. It stays hidden until you have logged at least one weigh-in.
- "Same as yesterday" was already present as the **Copy the day before** button under Eaten (shown when the day is empty and the day before has food); no change needed.

Assets changed: none.
New capabilities: none.

## 1.0.0 (2026-09-28)

First public release.

- Weight tab: daily weigh-ins, daily and weekly charts, week-by-week table, and maintenance calories from your own results.
- Food tab: label scanning, USDA food search, Ask Claude, and entering foods by hand. Units in grams, ounces, pounds, cups, tablespoons, and whole.
- Tap to log, double-tap to rename, press and hold to edit or delete.
- Settings panel with a glowing-edge switch, and the version number.
- Developer docs (`ARCHITECTURE.md`, `CLAUDE.md`) and local test tools (`tools/dev_server.py`, `tools/mock-claude.js`).

Assets changed: all (first release).
New capabilities: none beyond `assets`, `db`, `sample`.

Note for installs from the starter zip (before 1.0.0): the assets are identical, so an update only needs the new `tracker.html`.
