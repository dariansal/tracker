# Changelog

Each entry says what changed, whether any file in `assets/` changed, and whether a new capability is needed. Updates use this to decide what to re-upload.

## 1.2.0 (2026-09-28)

- Food tab: a **Workout day** toggle under the day's totals. Tap it to mark that the day included a workout; tap again to clear it.
- New **Workout days vs rest days** card (shows once you have at least one workout day and one rest day with food logged): average calories eaten on workout days vs rest days, and the difference between them.
- Workout marks are stored per day in a new `settings/workouts` document (with a `food-workouts-v1` localStorage fallback), so they sync and never touch your food log or weigh-ins.

Assets changed: none.
New capabilities: none.

## 1.1.2 (2026-09-28)

- Protein goal bar redesigned to show the range **on the bar itself** instead of spelling it out in text. Two goalpost ticks mark the low and high ends of the range (labelled underneath, e.g. `151` and `185`), with a faint band between them. Your protein fills across the bar and turns green with a check once it reaches the range.

Assets changed: none.
New capabilities: none.

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
