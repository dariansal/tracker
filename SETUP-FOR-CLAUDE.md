# Instructions for Claude

These instructions are for Claude. They cover three jobs: **installing** the tracker on the current user's account, **updating** an existing install to the latest version, and **making a release** for the repository owner.

## What's in the repository

| Path | What it is |
|---|---|
| `tracker.html` | The whole app. Contains three placeholders that must be replaced with the installed file links (see below). Its version is `APP_VERSION` in the file. |
| `assets/ocr-core.js` | Tesseract.js core 5.1.1 (`tesseract-core-lstm.wasm.js`), the label-reading engine. |
| `assets/ocr-eng-data.js` | English OCR data (`eng.traineddata`, best_int), gzipped and base64-encoded as `window.__OCR_ENG_GZ`. |
| `assets/usda-foods.js` | USDA SR28 (~8,800 foods) as `window.__USDA`, used by the food search. |
| `assets/SHA256SUMS` | Checksums of the three asset files. They change only when an asset changes. |
| `tracker-icon.png` | Optional home screen icon. |
| `tools/make_release.py` | Turns an installed copy back into the clean `tracker.html` (used for releases). |
| `CHANGELOG.md` | What changed in each version, and whether any asset changed. |

The placeholders in `tracker.html`:

- `/_blob/REPLACE_WITH_OCR_CORE_ID` → the installed link for `assets/ocr-core.js`
- `/_blob/REPLACE_WITH_OCR_DATA_ID` → the installed link for `assets/ocr-eng-data.js`
- `/_blob/REPLACE_WITH_USDA_ID` → the installed link for `assets/usda-foods.js`

## 1. Install (new user)

1. Get the files: from the user's uploads (unzip if needed), or from the repository (`https://raw.githubusercontent.com/dariansal/tracker/main/<path>`). Put them in `/mnt/user-data/outputs/tracker/`.
2. Publish `tracker.html` with the Artifact tool (`action: "publish"`), favicon ⚖️, title `Tracker`, and these capabilities:
   ```json
   {
     "assets": {},
     "db": { "rules": [ { "path": "", "read": "view", "write": "owner" } ] },
     "sample": {}
   }
   ```
   Call `action: "capabilities"` first if you need to check what this account supports. If one isn't available, leave it out; the app degrades gracefully (see "Missing capabilities").
3. Upload each of the three asset files to that artifact: one publish call each with `asset: true`, `url` set to the new artifact's link, and `file_path` set to the file.
4. Replace the three placeholders in `tracker.html` with the returned `/_blob/<id>` links.
5. Publish `tracker.html` again with `url` set to the same artifact, so it updates in place. Don't pass `capabilities`; they carry over.
6. Give the user their link, and help them add it to the home screen (Shortcuts → **Open URLs** → **Add to Home Screen**, with `tracker-icon.png` as the icon).

## 2. Update (existing install)

The user gives you the repository address and their tracker link. Their data lives in the artifact's database and isn't touched by an update.

1. **Read the installed tracker:** Artifact `action: "read"` with their tracker link. From the copied page, note:
   - its current version: the `APP_VERSION` value (installs from before version 1.0.0 don't have one; treat them as `0.9`)
   - its three installed file links: the values of `OCR_CORE`, `OCR_DATA`, and `USDA_URL`
2. **Get the latest release:** download `tracker.html`, `CHANGELOG.md`, and `assets/SHA256SUMS` from the repository's `main` branch (raw.githubusercontent.com). Read the changelog entries newer than the installed version.
3. **Assets:** if any of those entries says an asset changed, download that asset from `assets/`, upload it to the user's artifact (`asset: true`, `url` = their tracker), and use the new link for it. Otherwise, keep the installed links. To double-check an asset, save it with Artifact `read` (`path` = its id) and compare its sha256 with `SHA256SUMS`.
4. **Fill in the links:** replace the three placeholders in the new `tracker.html` with the installed (or newly uploaded) links.
5. **Publish** to the user's tracker link (`url`). If the changelog lists a new capability, pass the complete capability set (the three above plus the new one); otherwise don't pass `capabilities`.
6. Tell the user which version they're on now, and what changed, in plain words.

## 3. Releases

New versions are made in the GitHub repository (with Claude Code; see `CLAUDE.md` and `ARCHITECTURE.md` there), not on claude.ai. Everyone, including the repository owner, gets them through **2. Update** above.

If someone asks you on claude.ai to change their installed tracker directly, you can, but the change won't be in the repository and will be overwritten by the next update. Offer to save their installed page (Artifact `read`) as a file they can hand to the repository maintainer, who runs `tools/make_release.py` on it.

## Data layout

- Weigh-ins: collection `weights`, one document per day (`YYYY-MM-DD` → `{ date, lb, updatedAt }`).
- Food log: collection `food`, one document per day (`{ date, items: [...] }`). Each item keeps its own calorie and macro numbers, so editing a food later doesn't change past days.
- Food list: document `settings/foods` (`{ foods: [...] }`). Foods are stored by weight: `per` is macros **per gram**, and `units` gives grams per unit (`g`, `oz`, `lb`, plus optional `cup`, `tbsp` (cup ÷ 16), and `each` (one whole item)). The page converts older formats automatically when it loads them.
- Height and age: `settings/profile`. Preferences (such as the glowing edge): `settings/prefs`.
- If the database isn't reachable, the page uses the browser's localStorage and moves that data into the database the next time it connects.

Keep changes backward compatible with this layout, so updates never lose anyone's data. If a release must change it, have the page convert old data when it loads, as it already does for foods.

## Missing capabilities

- **No `db`:** everything works, but data stays in that phone's browser only.
- **No `sample`:** scanning still works (the phone reads the text and a built-in parser picks out the numbers). The "Ask Claude" search option is hidden.
- **No `assets`:** food search's USDA list won't load. The label reader falls back to loading its engine from cdn.jsdelivr.net, but can't load its English data, so scanning won't work. Entering foods by hand still works.
