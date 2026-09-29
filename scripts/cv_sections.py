#!/usr/bin/env python3
r"""
Shared helper: read cv_diGiovanni.tex and return each section as clean text.

Used by check-cv-drift.py, and by hand when transcribing into src/data/cv.ts.
Strips LaTeX typesetting scaffolding that carries no meaning -- \phantom{},
\vspace{}, \bigskip, \newpage -- so that a change in spacing never registers as
a change in content.
"""
import re, sys, json, pathlib, subprocess

TEX = pathlib.Path.home() / 'Library/CloudStorage/Dropbox/CV/cv_diGiovanni.tex'

ACCENTS = [
    (r'\c{S}', 'Ş'), (r'\c{s}', 'ş'), (r'\c{C}', 'Ç'), (r'\c{c}', 'ç'),
    (r'\"{o}', 'ö'), (r'\"{O}', 'Ö'), (r'\"{u}', 'ü'), (r'\"{U}', 'Ü'),
    (r'\"{a}', 'ä'), (r'\"o', 'ö'), (r'\"O', 'Ö'), (r'\"u', 'ü'),
    (r"\'{e}", 'é'), (r"\'{a}", 'á'), (r"\'{i}", 'í'), (r"\'{o}", 'ó'),
    (r"\'{u}", 'ú'), (r"\'{c}", 'ć'), (r"\'{n}", 'ń'),
    (r"\'e", 'é'), (r"\'a", 'á'), (r"\'i", 'í'), (r"\'o", 'ó'), (r"\'u", 'ú'),
    (r'\`{e}', 'è'), (r'\`{a}', 'à'), (r'\`e', 'è'), (r'\`a', 'à'),
    (r'\^{e}', 'ê'), (r'\^{o}', 'ô'), (r'\^{a}', 'â'), (r'\^{i}', 'î'),
    (r'\~{n}', 'ñ'), (r'\~n', 'ñ'), (r'\o', 'ø'), (r'\ss', 'ß'),
    (r'\euro{}', '€'), (r'\euro', '€'), (r'\&', '&'), (r'\%', '%'), (r'\$', '$'),
]

# Scaffolding with no content. Order matters: the braced forms first.
NOISE = [
    r'\\phantom\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',
    r'\\vspace\{[^}]*\}', r'\\hspace\{[^}]*\}',
    r'\\bigskip', r'\\medskip', r'\\smallskip', r'\\newpage', r'\\clearpage',
    r'\\begin\{subentry1\}', r'\\end\{subentry1\}',
    r'\\begin\{itemize\}', r'\\end\{itemize\}',
    r'\\begin\{resume\}', r'\\end\{resume\}',
    r'\\sectionskip\S*',
]

def strip_comments(line: str) -> str:
    out, i = [], 0
    while i < len(line):
        if line[i] == '\\' and i + 1 < len(line):
            out.append(line[i:i+2]); i += 2; continue
        if line[i] == '%': break
        out.append(line[i]); i += 1
    return ''.join(out)

def detex(s: str) -> str:
    for a, b in ACCENTS: s = s.replace(a, b)
    for n in NOISE: s = re.sub(n, ' ', s)
    for _ in range(6):
        new = re.sub(r'\\(?:emph|textbf|textit|underline|text|bf|it|textsuperscript)\s*\{([^{}]*)\}', r'\1', s)
        if new == s: break
        s = new
    s = s.replace('---', '—').replace('--', '–')
    s = s.replace('``', '“').replace("''", '”')
    s = re.sub(r'\\item\s*(\[[^\]]*\])?', '\n• ', s)
    s = re.sub(r'\\\\', '\n', s)
    s = re.sub(r'\\[a-zA-Z]+\s*', ' ', s)
    s = s.replace('{', '').replace('}', '').replace('~', ' ')
    s = '\n'.join(re.sub(r'[ \t]+', ' ', l).strip() for l in s.split('\n'))
    return re.sub(r'\n{2,}', '\n', s).strip()

def sections(path=TEX):
    raw = path.read_text(encoding='utf-8')
    kept = [strip_comments(l) for l in raw.split('\n') if not l.lstrip().startswith('%')]
    clean = '\n'.join(kept)
    marks = [(m.start(), m.end(), m.group(1)) for m in re.finditer(r'\\section\{([^}]*)\}', clean)]
    out = {}
    for i, (s0, s1, name) in enumerate(marks):
        end = marks[i+1][0] if i + 1 < len(marks) else len(clean)
        out[name] = detex(clean[s1:end])
    return out

if __name__ == '__main__':
    secs = sections()
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(secs, indent=2, ensure_ascii=False))
    elif len(sys.argv) > 1:
        want = ' '.join(sys.argv[1:])
        for k, v in secs.items():
            if want.lower() in k.lower(): print(f'########## {k}\n{v}\n')
    else:
        for k, v in secs.items(): print(f'{k:36} {len(v):5} chars')
