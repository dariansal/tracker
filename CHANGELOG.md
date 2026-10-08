# Changelog

Each entry says what changed, whether any file in `assets/` changed, and whether a new capability is needed. Updates use this to decide what to re-upload.

## 1.10.0 (2026-10-08)

- **Workout days are now the default.** Every day counts as a workout day unless you tap the dumbbell to mark it a **rest** day — the opposite of before. Your existing data is converted automatically: days you'd already marked as workouts stay workouts, and days with food logged that you hadn't marked become rest days, so the "Workout days vs rest days" comparison and the chart dots look the same as before.
- **Your foods now sort by how often you log them** — the more you log a food, the higher it rises in the "Foods" grid. (The app starts counting from this version; ties keep their previous order.)

Assets changed: none.
New capabilities: none.

## 1.9.0 (2026-09-30)

- The **Foods** grid is condensed: a **"Filter your foods" box** above it narrows the list as you type, the tiles are smaller (about three per row), and the whole grid sits in a **capped, scrollable area** so it no longer runs on forever.
- When you tap a food to log it, the app now **scrolls the log panel into view**, so "Add to day" is right there instead of down the page.

Assets changed: none.
New capabilities: none.

## 1.8.0 (2026-09-29)

- You can now **edit the portion of something already in "Eaten Today"** — each entry has an **Edit** button next to Remove. Tap it to change the amount (and unit, or cooking oil), see the new calories/macros update live, and Save. For example, change "1 cup white rice" to "2 cups" instead of adding a second entry. The day's totals and protein bar update automatically.

Assets changed: none.
New capabilities: none.

## 1.7.2 (2026-09-29)

- "Workout days vs rest days" on the Food tab is now a **collapsible section you tap to open and close** (like "All weigh-ins" on the Weight tab), and it starts collapsed.
- Added space above it so it no longer crowds the "Eaten" card.

Assets changed: none.
New capabilities: none.

## 1.7.1 (2026-09-29)

- "Day by day" chart is cleaner: removed the description line under the heading, and tapping a point now shows **only the weight** (the date and calories are available via "See food"). The "See food" and delete buttons are unchanged.
- The **selected dot is now shown by colour, not shape** — dots keep their workout (solid) / rest (open) look at all times, and the one you tapped turns a highlight colour, so you can always tell workout from rest days even when one is selected.

Assets changed: none.
New capabilities: none.

## 1.7.0 (2026-09-28)

- The app is now **dark only** — removed the light/dark appearance setting entirely (and the sun/moon icon).
- New **Protein goal** setting: set your target range in grams of protein per pound of body weight (two inputs, "0.9 to 1.1"). Defaults to 0.9–1.1. The goal bar on the Food tab updates to whatever you set.

Assets changed: none.
New capabilities: none.

## 1.6.1 (2026-09-28)

- Refined the Appearance sun/moon into thinner, cleaner line icons (lighter stroke, tidier proportions) to match the rest of the app's icons.

Assets changed: none.
New capabilities: none.

## 1.6.0 (2026-09-28)

- Removed the glowing edge entirely.
- Settings now has an **Appearance** control: a single icon button that's a **sun in light mode and a moon in dark mode**. Tap it to switch the whole app between light and dark, and the icon flips with it. It starts by matching your device's light/dark setting until you tap it.

Assets changed: none.
New capabilities: none.

## 1.5.0 (2026-09-28)

- Opening a day's food from the weight chart no longer uses a press-and-hold (which was unreliable) and never jumps automatically. Now: **tap a point** on "Day by day", then tap the **"See food"** button that appears in the readout, then **"Tap to open ›"** to confirm — a deliberate two-tap so you're always the one choosing to switch.
- Glowing edge is now a **one-shot**: when you open the tracker, the line **races around the screen once and then fades away**, instead of reappearing every couple of minutes. Turning the switch on in Settings replays it.

Assets changed: none.
New capabilities: none.

## 1.4.0 (2026-09-28)

- The workout marker by the date is now a small **dumbbell** (not the weight-lifter person), a bit smaller and nudged slightly to the right of the date.
- On the "Day by day" weight chart, **press and hold a point to jump to that day's food** (short tap still shows the weight/calories readout with delete). The chart's help text mentions this.
- Glowing edge: **twice as fast** (a lap now takes 18 s instead of 36 s) and **50% thicker**.

Assets changed: none.
New capabilities: none.

## 1.3.0 (2026-09-28)

- The workout marker moved from the button under the totals to a small **🏋️ toggle right next to the date** on the Food tab. Tap it to mark the day (it lights up); tap again to clear. Much more minimal, and it sits with the day it belongs to.
- **Workout days are now shown on the "Day by day" weight chart**: workout days are solid dots, rest days are open (hollow) dots, with a small legend under the chart. Tapping a point also notes "· workout". This makes it easy to see how weight and calories track with your workouts. (The chart looks unchanged until you start marking workout days.)

Assets changed: none.
New capabilities: none.

## 1.2.1 (2026-09-28)

- Fix: when saving a new food (for example after a scan) with a required field missing, the error (like "Enter the calories for that serving.") now appears **inside the New food panel**, right by the Save button, instead of at the bottom of the screen where it was easy to miss. The field that needs attention is focused.

Assets changed: none.
New capabilities: none.

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
