# Architecture and project guide

Everything a developer (or Claude Code) needs to understand and safely change Tracker. Read this before making changes.

## 1. What it is and where it runs

Tracker is a weight and nutrition tracker used daily on an iPhone. It's **one HTML file** (`tracker.html`) that runs as a **Claude artifact**: a page hosted by claude.ai, shown inside Claude's viewer (in the Claude iPhone app, or in Safari through a home screen shortcut).

Things that follow from running as a claude.ai artifact:

- **Content-security policy:** scripts may only load from cdnjs.cloudflare.com, cdn.jsdelivr.net/npm, cdn.tailwindcss.com, and code.jquery.com; stylesheets only from fonts.googleapis.com. No other network requests are allowed: no fetching other sites, no remote images. Everything else must be inline or stored as an artifact asset.
- **Artifact assets:** large files are uploaded to the artifact and served same-origin at `/_blob/<32-hex-id>`. The three assets (label-reader engine, its English data, the USDA database) are loaded with `<script src>` only when needed. Each install gets its own ids, which is why the repository's `tracker.html` has placeholders (`/_blob/REPLACE_WITH_...`) that installs fill in.
- **Runtime capabilities**, declared when the artifact is published and requested in the page with `await window.claude.use(name)`:
  - `db`: a small document database per artifact. The app uses `db.doc(path)` and `db.collection(name).doc(id)` with `.set(data)`, `.delete()`, and `.onSnapshot(next, error)`. Its access rule: anyone who can open the artifact can read; only the owner can write.
  - `sample`: asks Claude. The app uses `sample.limits()` (to see whether images are supported) and `sample.json(prompt, { images, modelTier: "default" })`. Errors carry a `code` (for example `not_granted`, `rate_limited`, `images_unavailable`, `cancelled`).
  - `assets`: allows the `/_blob/` files above.
  - `use()` resolves to `null` when a capability isn't available. **Every code path must work with `null`**, falling back to localStorage and built-in logic.
- **The viewer:** the page runs inside Claude's viewer, below Claude's own top bar. The page can't draw above that bar, can't trigger iPhone haptics (Apple restricts web pages; see "Known limits"), and `window.confirm()` is blocked, so it must never be used.

## 2. Workflow and accounts

- **This GitHub repository is the source of truth.** Changes are made here (by Claude Code, possibly signed in to a different Claude account than the owner's claude.ai account) and pushed.
- **Each person's tracker is an install:** an artifact on *their own* claude.ai account, holding their data. Nobody's tracker is edited from here directly, not even the owner's.
- **Installs update themselves from this repository.** The person tells Claude on claude.ai: "Update my tracker to the latest version from https://github.com/dariansal/tracker following SETUP-FOR-CLAUDE.md. My tracker is: <link>". Claude there reads the installed page, keeps its `/_blob/` links (re-uploading only assets the changelog says changed), inserts them into the new `tracker.html`, and republishes over the same artifact. Data, link, and home screen shortcut stay the same.
- So a change reaches the owner's phone in two steps: push a release here, then the owner asks their claude.ai Claude to update. After every release, tell the owner that's the next step.

## 3. Code map (`tracker.html`)

Search for these markers; line numbers drift.

| Part | Marker | What it does |
|---|---|---|
| Styles | `<style>` | Theme tokens on `:root` (light and dark), layout, components. Colors: `--weekly` (primary blue), `--daily` (sage). |
| Markup | `<main>` | Header (title "Tracker", tab switcher, gear), `#pane-weight`, `#pane-food`, then the settings sheet. |
| Weight module | first `<script>` | IIFE: weigh-ins, charts, weekly table, maintenance estimate, height and age profile. |
| Version | `// ===== version` | `APP_VERSION`, shown at the bottom of Settings. |
| Preferences | `// ===== preferences` | `window.appPrefs` (for example `theme`), `window.setPref()`. Saved to `settings/prefs` plus localStorage; fires a `prefs-changed` event. |
| Appearance | `// ===== appearance` | Sets `data-theme` on `<html>` from `appPrefs.theme` (`light`/`dark` force it, `system` follows the device). |
| Settings panel | `// ===== settings panel` | Gear button, bottom sheet, appearance (sun/moon) toggle. |
| Tabs | `// ===== tabs` | Weight/Food switcher with a gliding pill; remembers the last tab (localStorage `log-tab`). |
| Food module | `// ===== food` | IIFE containing everything below. |
| ↳ storage | `// ---------- storage` | Load and save days and foods; db with localStorage fallback. |
| ↳ log panel | `// ---------- adder` | Panel shown when a food is tapped: amount, unit, cooking oil, pencil rename, Add to day. |
| ↳ scanning | `// ---------- scan a nutrition label` | Label scanning pipeline (section 6). |
| ↳ new food | `// ---------- new food panel` | Panel at the top for new foods (scan, search pick, Ask Claude, or by hand). |
| ↳ render | `// ---------- render` | Totals, day heading, eaten list, and `publishCalories()` for the weight tab. |
| ↳ search | `// ---------- search` | Your foods, USDA ranking, Ask Claude. |
| ↳ hold and rename | `// ---------- press and hold`, `startTileRename` | Hold menu (Edit/Delete), double-tap rename. |
| ↳ edit | `// ---------- edit one food` | Edit panel: name, serving, unit, grams per cup and per whole, macros. |

The two modules talk through `window.appShared.kcal` (calories per day, set by the food module) and the `food-updated` event, which the weight module listens for.

## 4. Data model

Stored in the artifact `db` (see `SETUP-FOR-CLAUDE.md` for the exact document layout):

- **Weigh-ins:** `weights/<YYYY-MM-DD>` → `{ date, lb, updatedAt }`. Pounds only.
- **Food log:** `food/<YYYY-MM-DD>` → `{ date, items }`. Each item is a **snapshot**: `{ id, food, name, amount, unit, oil, kcal, p, c, f }`. Editing or deleting a food never changes past days.
- **Foods:** `settings/foods` → `{ foods: [...] }`. Every food is stored **by weight**: `per` is kcal, p, c, f **per gram**, and `units` maps each unit to grams: `g: 1`, `oz: 28.3495`, `lb: 453.592`, optional `cup`, `tbsp` (always `cup / 16`), and optional `each` (weight of one whole item). `def` is the default serving `{ amount, unit }`. `cooked: true` adds an "Olive oil (tbsp)" field when logging (1 tbsp = 13.5 g, macros from the food with id `oil`, or built-in olive oil values).
- `normalizeFood()` converts older formats (per-unit macros, units like "banana" or "scoop") into this shape on load. Keep it working.
- **Profile:** `settings/profile` → `{ heightIn, age }`. **Preferences:** `settings/prefs` → `{ theme }` (`"system"`, `"light"`, or `"dark"`).
- **Workout days:** `settings/workouts` → `{ dates: ["YYYY-MM-DD", ...] }`. Just a set of dates the owner marked as a workout day; kept separate from the food log so it never affects logged items or weigh-ins. Used for the "Workout days vs rest days" calorie comparison on the food tab.
- **localStorage keys:** `weight-log-v1`, `food-days-v1`, `food-lib-v1`, `food-workouts-v1`, `profile-v1`, `prefs-v1` (fallbacks, moved into the db when it connects), plus `log-tab`.

The user-visible units are exactly: **grams, ounces, pounds, cups, tablespoons, and whole**. The owner asked for this standard set, so don't add other units (like "serving" or "scoop"); countable things use "whole".

## 5. Features and the behavior the owner asked for

These are deliberate decisions. Keep them unless the owner asks otherwise.

**Weight tab**
- Enter a weight and save. The date then **moves forward one day**. Deleting an entry **moves the date back one day**. The page always opens on today.
- Charts are hand-drawn SVG: "Day by day" and "Weekly average" (weeks start Monday), with date labels **centered under the points**. Tap a point to see its date, weight, and calories eaten. On "Day by day", tapping a point also shows a **"See food" button** in the readout; it's a two-tap confirm (tap once, then "Tap to open ›") that opens that day on the food tab via the `open-food-day` event — never automatic. Workout days are solid dots, rest days open dots (`opts.mark`).
- Deleting (from the chart or the list) takes **two taps**: "Delete", then "Tap again to delete". No `confirm()`.
- Redraws keep your scroll position (`holdInPlace`, `scrollY` restore); the page must not jump.
- Week-by-week table: average weight, change from the previous week (neutral colors, since gaining isn't marked as bad), and average daily calories.
- Maintenance calories: over the last 28 days, the least-squares weight trend (lb/day) and the average calories on logged days. Maintenance ≈ average kcal − slope × 3500. Needs 10 weigh-ins, 10 food days, and a 14-day span; until then it shows a progress bar and an optional Mifflin-St Jeor × 1.9 estimate from height and age. The card is compact and sits just above "All weigh-ins".

**Food tab** (top to bottom)
- Day switcher and totals (kcal, protein, carbs, fat).
- **Add New Food:** search bar, big **Scan nutrition label** button (opens the rear camera directly via `capture="environment"`), and an "Or enter a food by hand" link. The new-food panel opens right there. "Scan again" appears only after a scan.
- **Foods:** a grid of food buttons (names only, with no subtext). Tap to log. **Double-tap** to rename in place (keyboard opens). **Press and hold** (480 ms) for a bottom sheet with just **Edit** and **Delete**; tap outside to close.
- The log panel (after tapping a food) has a pencil next to the name for renaming, amount and unit (switching units converts the amount), and oil for cooked foods. **Add to day** closes it instantly without moving the page.
- **Eaten Today** (or "Eaten Yesterday" / "Eaten on Sat, Sep 26") lists entries, each removed with two taps.
- Saving a new food closes the panel instantly and saves in the background, putting it back if the save fails.

**Search:** your own foods first, then the USDA database (plain raw foods rank first; processed and brand-name entries are pushed down; plurals and exact words count), then "Ask Claude about ..." for brand-name and restaurant food. Picking a result opens the new-food panel with name, serving, and macros filled in.

**Label scanning pipeline**
1. If `sample.limits().images` exists, Claude reads the photo directly.
2. Otherwise (the owner's phone), Tesseract reads the text **on the phone**: the image is scaled to 2000 px and made grayscale with more contrast. The engine loads from the asset (falling back to jsDelivr), and the English data from its asset, decompressed with `DecompressionStream`.
3. The text goes to `sample.json` to be turned into numbers. If that fails, `parseLabel()` handles common OCR errors ("g" read as "9", "O" read as "0"), picking the reading whose protein, carbs, and fat best match the printed calories.
4. The serving is converted to the standard units: countable servings like "1 scoop (46g)" become **whole**; cups and tablespoons are kept, with grams per cup worked out; everything else becomes grams. The suggested name appears as gray placeholder text, and **space accepts it**.

**Settings (gear):** the **Appearance** toggle (saved to the account) and the version number.

**Appearance** (light/dark): a single icon button in Settings — a **sun in light mode, a moon in dark mode**. It reflects the *effective* mode: `appPrefs.theme` when it's `light`/`dark`, otherwise the device's `prefers-color-scheme`. Tapping it sets `theme` to the opposite explicit value (so it stops following the device once tapped). The appearance module applies `data-theme` on `<html>`; the CSS themes (`:root`, `:root:not([data-theme="light"])` under the dark media query, and `:root[data-theme="dark"]`) do the rest, so every color is a token that flips with it. A fresh install has `theme: "system"`, so it matches the device until the first tap.

## 6. Known limits

- **Haptics:** there's no web API for vibration on iPhone. The hidden `<input switch>` trick (iOS 18) is attempted when a finger lifts after a hold, but it doesn't fire inside Claude's viewer. The owner confirmed it doesn't work. Android uses `navigator.vibrate`.
- **Photos to Claude:** on the owner's phone, `sample` has no image support, which is why the phone-side reader exists.
- **Camera permission:** if the camera shows black, that's the iOS camera permission for the app or Safari, not the page.

## 7. Bugs we've hit before (check for these)

- **Declaration order:** both modules call `render()` early, while loading. Any `let` or `const` it reaches must be declared **before** that first call, or the page breaks with "Cannot access ... before initialization". This has happened several times (`lastShared`, `tileRenaming`).
- **`hidden` overridden by CSS:** elements with `display: grid` or `flex` ignore the `hidden` attribute unless `[hidden] { display: none !important; }` is present (it is; keep it).
- **Sizing inside `<details>`:** children of `<details>` don't inherit `box-sizing` through its internals, so inputs overflowed. There's an explicit `details *, input, select, textarea, button { box-sizing: border-box; }`.
- **Replacing an element you're about to use:** `closeAdder()` calls `renderQuick()`, which rebuilds every food button. Don't hold on to a button across that (double-tap rename closes the panel without rebuilding for this reason).
- **Keyboard focus on iPhone** only works inside a real tap handler. Programmatic focus from a timer won't open the keyboard.
- **Scroll jumps:** measure before clearing content, and restore scroll after redraws.
- **Inputs under 16 px** make iOS zoom in when focused. Keep inputs at 16 px or larger.
- **Blocked `confirm()` and `alert()`:** use two-tap buttons instead.

## 8. Testing

- `python3 tools/dev_server.py` → http://localhost:8000 serves `tracker.html` with the assets hooked up. Add **`?mock=1`** to inject `tools/mock-claude.js` (a localStorage-backed stand-in for `db`, and a `sample` with no images that always fails, like being offline), so the database code paths run.
- Test at iPhone size (393 × 852). Playwright with `devices['iPhone 13']` works well, including touch events for holds and double-taps.
- Before any release, check: the page loads with no console errors, in both light and dark mode; logging, editing, deleting, and renaming work; a scan fills the form; search returns results; and reloading keeps your data (with `?mock=1`).
- What can't be tested locally: the real claude.ai database and access rules, real Claude calls, and the content-security policy. After a release, the owner updates their install and checks those on the phone.

## 9. Releasing

See "Making a release" in `CLAUDE.md`: bump `APP_VERSION`, update `CHANGELOG.md` (including which assets changed), run the placeholder checks, commit, tag `vX.Y.Z`, and push. Then tell the owner to update their install from claude.ai.
