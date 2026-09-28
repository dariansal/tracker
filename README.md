# Tracker

A personal weight and nutrition tracker that runs as a Claude artifact on your iPhone. Log your weight, track calories and macros, scan nutrition labels, and see your real maintenance calories from your own results.

Everything lives in **one HTML file** (`tracker.html`). Claude installs it on your account, and your data stays private to you.

## Features

- **Weight:** daily weigh-ins, day-by-day and weekly-average charts, and a week-by-week table next to your average daily calories.
- **Maintenance calories:** after about two weeks of logging, worked out from how your weight actually moved compared with what you ate. Before then, an optional formula estimate from height and age.
- **Food:** scan a nutrition label, search the USDA database (about 8,800 foods), ask Claude about brand-name or restaurant foods, or type a food in by hand.
- **Units:** grams, ounces, pounds, cups, tablespoons, and "whole" for things like eggs or scoops.
- **Quick editing:** tap a food to log it, double-tap to rename it, and press and hold to edit or delete it.
- **Extras:** dark mode, a gliding tab switcher, and an optional glowing edge (in Settings).

## Install it

You need a Claude account on the web or in the iPhone app.

1. Download this repository: **Code → Download ZIP**, then unzip it.
2. In a new Claude chat, attach `tracker.html`, `SETUP-FOR-CLAUDE.md`, the three files in `assets/`, and `tracker-icon.png`, and send:
   > Please set up this tracker for me by following SETUP-FOR-CLAUDE.md.
3. Claude publishes your tracker and gives you a link.
4. To put it on your home screen: save `tracker-icon.png` to Photos. In the **Shortcuts** app, tap **+**, add **Open URLs** with your tracker link, tap the name at the top, choose **Add to Home Screen**, set the icon to your photo, and tap **Add**.

## Update it

When a new version is released (see `CHANGELOG.md`), open a chat in your Claude account and send:

> Update my tracker to the latest version from https://github.com/dariansal/tracker following SETUP-FOR-CLAUDE.md. My tracker is: YOUR-TRACKER-LINK

(Use your own tracker link.) Your data, link, and home screen shortcut stay the same. The version you have is shown at the bottom of **Settings** (the gear icon).

## How it's built

- One HTML file with inline CSS and JavaScript, and no build step.
- Data is stored in the artifact's own database (weigh-ins, food logs, your food list, and settings), with a browser-storage fallback.
- Label reading runs on the phone with Tesseract.js, and Claude turns the text into numbers when available.
- The food search uses a copy of USDA SR28 that's stored with your tracker.

See `ARCHITECTURE.md` for how everything works, `CLAUDE.md` for how changes and releases are made, and `SETUP-FOR-CLAUDE.md` for installing and updating.

To try it on a computer: `python3 tools/dev_server.py`, then open http://localhost:8000 (add `?mock=1` to simulate claude.ai's storage).

## Licenses

The app code is under the MIT License (`LICENSE`). Bundled components have their own licenses; see `THIRD_PARTY_NOTICES.md`.

Nutrition numbers are estimates. This app isn't medical or dietary advice.
