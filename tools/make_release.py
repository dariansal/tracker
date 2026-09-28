#!/usr/bin/env python3
"""
Turn an installed copy of the tracker (with its own /_blob/ file links and personal
defaults) into the clean, shareable tracker.html for this repository.

    python3 tools/make_release.py path/to/installed.html tracker.html

It swaps the three installed file links for placeholders, clears the personal age
default, and adds the public fallback for the label-reader engine. Fails loudly if
something it expects to change isn't found, so a release is never half-made.
"""
import re, sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def sub(pattern, repl, label):
    global s
    s2, n = re.subn(pattern, repl, s, flags=re.S)
    if n == 0 and repl not in s:
        sys.exit(f"make_release: couldn't find {label}")
    s = s2

sub(r'const OCR_CORE = "/_blob/[^"]+";\s*const OCR_DATA = "/_blob/[^"]+";(\s*const OCR_CORE_CDN = "[^"]+";)?',
    'const OCR_CORE = "/_blob/REPLACE_WITH_OCR_CORE_ID";\n'
    '  const OCR_DATA = "/_blob/REPLACE_WITH_OCR_DATA_ID";\n'
    '  const OCR_CORE_CDN = "https://cdn.jsdelivr.net/npm/tesseract.js-core@5.1.1/tesseract-core-lstm.wasm.js";',
    "the label-reader file links")
sub(r'await loadScript\(OCR_CORE\)(?!\.catch)', 'await loadScript(OCR_CORE).catch(() => loadScript(OCR_CORE_CDN))',
    "the label-reader loader")
sub(r'const USDA_URL = "/_blob/[^"]+";[^\n]*', 'const USDA_URL = "/_blob/REPLACE_WITH_USDA_ID";   // SETUP: see SETUP-FOR-CLAUDE.md',
    "the food database link")
sub(r'let profile = \{ heightIn: null, age: \d+ \};', 'let profile = { heightIn: null, age: null };', "the age default")
sub(r'if \(!profile\.heightIn \|\| !latestLb\) return null;\s*const kg = latestLb \* 0\.4536, cm = profile\.heightIn \* 2\.54, age = profile\.age \|\| \d+;',
    'if (!profile.heightIn || !profile.age || !latestLb) return null;\n'
    '    const kg = latestLb * 0.4536, cm = profile.heightIn * 2.54, age = profile.age;', "the maintenance formula")

leftover = [m for m in re.findall(r'/_blob/([0-9a-f]{32})', s)]
if leftover:
    sys.exit(f"make_release: installed file links still present: {leftover}")
open(dst, "w", encoding="utf-8").write(s)
v = re.search(r'const APP_VERSION = "([^"]+)"', s)
print(f"wrote {dst} (version {v.group(1) if v else 'unknown'})")
