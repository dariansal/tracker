# Changelog

Each entry says what changed, whether any file in `assets/` changed, and whether a new capability is needed. Updates use this to decide what to re-upload.

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
