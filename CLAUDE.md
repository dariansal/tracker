# CLAUDE.md

Guidance for Claude Code working in this repository. **Read `ARCHITECTURE.md` before changing anything**: it explains how the app works, where it runs, the behavior the owner asked for, and bugs we've hit before.

## The project in one paragraph

**Tracker** is a weight and nutrition tracker the owner (GitHub **dariansal**) uses daily on an iPhone. The whole app is `tracker.html`: one file with inline CSS and JavaScript and no build step. It runs as a **Claude artifact** (a page hosted on claude.ai). Each person installs their own copy on their own claude.ai account, where it stores their data. This repository, **github.com/dariansal/tracker**, is the source of truth that installs are created and updated from.

## How changes reach people's phones

1. You make the change here, test it (see below), release it (see below), and push to GitHub.
2. Each person, including the owner, updates their install by telling Claude on **claude.ai**, on the account that owns their tracker: "Update my tracker to the latest version from https://github.com/dariansal/tracker following SETUP-FOR-CLAUDE.md. My tracker is: <their link>". Their data, link, and home screen shortcut stay the same.

This Claude Code session may be signed in to a **different Claude account** from the owner's claude.ai account, and it has no access to claude.ai artifacts anyway. Never try to publish to or edit anyone's tracker from here. After every release, remind the owner of step 2.

## Layout

- `tracker.html`: the app. It must contain exactly three placeholders: `/_blob/REPLACE_WITH_OCR_CORE_ID`, `/_blob/REPLACE_WITH_OCR_DATA_ID`, `/_blob/REPLACE_WITH_USDA_ID`.
- `assets/`: label-reading engine and English data (Tesseract.js), and the USDA food database, plus `SHA256SUMS` and the engine's license.
- `tools/dev_server.py`: run the app locally. `tools/mock-claude.js`: claude.ai runtime stand-in (`?mock=1`). `tools/make_release.py`: cleans a page file that came from an install (see below).
- `ARCHITECTURE.md`: how everything works. `SETUP-FOR-CLAUDE.md`: install and update steps for Claude on claude.ai. `CHANGELOG.md`: one entry per version.
- `README.md`, `LICENSE` (MIT), `THIRD_PARTY_NOTICES.md`.

## Rules

- **Never commit personal data or install-specific links.** `grep -cE '/_blob/[0-9a-f]{32}' tracker.html` must print 0, and `grep -c REPLACE_WITH_ tracker.html` must print 3.
- Keep it one self-contained HTML file, within claude.ai's content-security policy (scripts only from cdnjs.cloudflare.com, cdn.jsdelivr.net/npm, cdn.tailwindcss.com, code.jquery.com; no other network requests). Details in `ARCHITECTURE.md`.
- Every feature must still work when `window.claude.use()` returns `null` (fall back to localStorage and built-in logic).
- Stay backward compatible with stored data (`ARCHITECTURE.md` §4), so updates never lose anyone's data. If a stored format must change, convert old data on load, like `normalizeFood()` does.
- Keep the owner's deliberate choices (`ARCHITECTURE.md` §5) unless they ask to change them: the standard units, two-tap deletes, no `confirm()`, and so on.
- Declare any `let`/`const` that the startup `render()` touches **before** that first call (`ARCHITECTURE.md` §7).
- Mobile first: test at 393 × 852 and in dark mode.

## Testing

```sh
python3 tools/dev_server.py          # http://localhost:8000
                                     # http://localhost:8000/?mock=1  (claude.ai stand-in: db + no-image Claude)
```

Check the list in `ARCHITECTURE.md` §8. What can't be tested locally (the real claude.ai database, Claude calls, the content-security policy) gets checked on the owner's phone after they update.

## Making a release

1. Make and test the change in `tracker.html`.
2. Bump `const APP_VERSION = "x.y.z"` in `tracker.html` (patch for fixes, minor for features).
3. If an asset changed, replace it in `assets/` and regenerate the checksums: `cd assets && sha256sum *.js > SHA256SUMS`.
4. Run the two `grep` checks above.
5. Add a `CHANGELOG.md` entry: version, date, what changed in plain language, **"Assets changed: none"** (or which ones), and any new capability. Installs rely on this to know what to re-upload.
6. Commit ("Tracker x.y.z"), tag `vx.y.z`, and push the commit and the tag.
7. Tell the owner: "Version x.y.z is on GitHub. To get it, tell Claude on claude.ai: Update my tracker to the latest version from https://github.com/dariansal/tracker following SETUP-FOR-CLAUDE.md. My tracker is: <your link>".

**If a change was made directly on claude.ai instead** (someone edited their installed tracker there), bring that page file here and run `python3 tools/make_release.py <file> tracker.html`. It swaps the install's links back to placeholders and clears personal defaults. Review the diff, then release as above.

## First publish (one time)

The repository may not exist on GitHub yet. From this folder:

```sh
(cd assets && sha256sum -c SHA256SUMS)          # verify the asset files
grep -cE '/_blob/[0-9a-f]{32}' tracker.html     # must print 0
grep -c REPLACE_WITH_ tracker.html              # must print 3
git init -b main
git add -A
git commit -m "Tracker 1.0.0"
gh auth status || gh auth login                 # sign in to GitHub as dariansal if needed
gh repo create dariansal/tracker --public --source . --remote origin --push \
  --description "Weight and nutrition tracker that runs as a Claude artifact on your iPhone"
git tag v1.0.0 && git push origin v1.0.0
```

If `dariansal/tracker` already exists (for example, created on the website with a README), don't overwrite it blindly. Add it as `origin`, fetch, and look at what's there. If it only has an auto-generated README or license, merge (`git pull origin main --allow-unrelated-histories`, keeping this repository's files) and push.

Finish by opening https://github.com/dariansal/tracker and confirming `tracker.html`, `assets/` (3 `.js` files, `SHA256SUMS`, the license), and `tools/` are all there.
