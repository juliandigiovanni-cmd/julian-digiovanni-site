#!/usr/bin/env python3
r"""
Report what changed in cv_diGiovanni.tex since src/data/cv.ts was transcribed.

    python3 scripts/check-cv-drift.py            # report drift, exit 1 if any
    python3 scripts/check-cv-drift.py --accept   # record the current .tex as the baseline

The CV page is transcribed by hand because six sections are prose held together
with \phantom{} spacing hacks. This check is what makes that safe: it compares
the .tex against the snapshot in data/cv-source.json and names the sections that
moved, with a diff.

It deliberately does not rewrite src/data/cv.ts. Mapping this LaTeX onto
structure takes judgment; the check tells you what to look at.
"""
import sys, json, difflib, pathlib
from cv_sections import sections, TEX

ROOT = pathlib.Path(__file__).resolve().parent.parent
SNAP = ROOT / 'data/cv-source.json'

# Sections the site renders. Drift in these needs action; drift elsewhere is
# reported as informational, since those live only in the PDF.
RENDERED = {
    'Current Positions', 'Previous Positions', 'Professional Affiliations',
    'Education', 'Fellowships and Awards', 'Published Reviews and Comments',
    'Teaching', 'Professional Activities', 'Short-Term Visits', 'Other Information',
}

def main():
    # --tex lets the check be tested against a scratch copy without touching
    # the real CV.
    tex = TEX
    if '--tex' in sys.argv:
        tex = pathlib.Path(sys.argv[sys.argv.index('--tex') + 1])
    current = sections(tex)

    if '--accept' in sys.argv:
        SNAP.parent.mkdir(exist_ok=True)
        SNAP.write_text(json.dumps(current, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f'baseline recorded: {len(current)} sections -> {SNAP.relative_to(ROOT)}')
        return 0

    if not SNAP.exists():
        print(f'no baseline at {SNAP.relative_to(ROOT)}')
        print('run:  python3 scripts/check-cv-drift.py --accept')
        return 1

    old = json.loads(SNAP.read_text(encoding='utf-8'))
    changed_rendered, changed_other, added, removed = [], [], [], []

    for name, text in current.items():
        if name not in old:
            added.append(name)
        elif old[name] != text:
            (changed_rendered if name in RENDERED else changed_other).append(name)
    removed = [n for n in old if n not in current]

    print(f'source: {tex}')
    print(f'{len(current)} sections compared against {SNAP.relative_to(ROOT)}\n')

    if not (changed_rendered or changed_other or added or removed):
        print('no drift — src/data/cv.ts is in step with the .tex')
        return 0

    if changed_rendered:
        print(f'{len(changed_rendered)} RENDERED section(s) changed — update src/data/cv.ts:\n')
        for name in changed_rendered:
            print(f'--- {name}')
            for line in difflib.unified_diff(
                    old[name].split('\n'), current[name].split('\n'),
                    fromfile='snapshot', tofile='cv_diGiovanni.tex', lineterm='', n=1):
                if line.startswith(('---', '+++')): continue
                print(f'  {line}')
            print()

    if changed_other:
        print('Changed, but PDF-only so nothing to do on the site:')
        for n in changed_other: print(f'  - {n}')
        print()
    if added:   print('New sections:', ', '.join(added), '\n')
    if removed: print('Sections gone:', ', '.join(removed), '\n')

    print('When src/data/cv.ts has been brought back in step, record the new baseline:')
    print('  npm run cv:accept')
    return 1 if changed_rendered or added or removed else 0

if __name__ == '__main__':
    sys.exit(main())
