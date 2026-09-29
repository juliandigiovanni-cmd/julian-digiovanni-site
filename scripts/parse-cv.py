#!/usr/bin/env python3
r"""
Parse cv_diGiovanni.tex into Astro content collection entries.

Run once to bootstrap src/content/papers/. After that the Markdown files are the
source of truth -- re-running will NOT clobber hand-written abstracts or topics
(see merge logic at the bottom).

The .tex is regular but not clean: LaTeX accents throughout, nested
\textbf{\emph{...}} for journal names, commented-out entries that have moved
between sections, and coauthor lists whose names contain periods. So:

  - `citation` is the full cleaned tail of the entry and is ALWAYS correct --
    it is what gets displayed.
  - journal / year / volume are best-effort extractions used only for sorting
    and filtering. Where they are wrong, display is unaffected.
"""
import re, sys, json, pathlib

TEX = pathlib.Path.home() / "Library/CloudStorage/Dropbox/CV/cv_diGiovanni.tex"
OUT = pathlib.Path(__file__).resolve().parent.parent / "src/content/papers"
DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"

# Longest patterns first so \"{o} is tried before \"o
ACCENTS = [
    (r'\c{S}', 'Ş'), (r'\c{s}', 'ş'), (r'\c{C}', 'Ç'), (r'\c{c}', 'ç'),
    (r'\"{o}', 'ö'), (r'\"{O}', 'Ö'), (r'\"{u}', 'ü'), (r'\"{U}', 'Ü'),
    (r'\"{a}', 'ä'), (r'\"{A}', 'Ä'), (r'\"o', 'ö'), (r'\"O', 'Ö'), (r'\"u', 'ü'),
    (r"\'{e}", 'é'), (r"\'{a}", 'á'), (r"\'{i}", 'í'), (r"\'{o}", 'ó'),
    (r"\'{u}", 'ú'), (r"\'{c}", 'ć'), (r"\'{n}", 'ń'),
    (r"\'e", 'é'), (r"\'a", 'á'), (r"\'i", 'í'), (r"\'o", 'ó'), (r"\'u", 'ú'),
    (r'\`{e}', 'è'), (r'\`{a}', 'à'), (r'\`e', 'è'), (r'\`a', 'à'),
    (r'\^{e}', 'ê'), (r'\^{o}', 'ô'), (r'\^{a}', 'â'), (r'\^{i}', 'î'),
    (r'\~{n}', 'ñ'), (r'\~n', 'ñ'), (r'\~{a}', 'ã'),
    (r'\o', 'ø'), (r'\ss', 'ß'),
]

def strip_comments(line: str) -> str:
    """Remove an unescaped % to end of line. \\% is a literal percent."""
    out, i = [], 0
    while i < len(line):
        if line[i] == '\\' and i + 1 < len(line):
            out.append(line[i:i+2]); i += 2; continue
        if line[i] == '%':
            break
        out.append(line[i]); i += 1
    return ''.join(out)

def balanced(s: str, start: int):
    """Given s[start] == '{', return (content, index_after_closing_brace)."""
    assert s[start] == '{'
    depth, i = 0, start
    while i < len(s):
        if s[i] == '\\':
            i += 2; continue
        if s[i] == '{': depth += 1
        elif s[i] == '}':
            depth -= 1
            if depth == 0:
                return s[start+1:i], i + 1
        i += 1
    return s[start+1:], len(s)

def detex(s: str) -> str:
    for pat, rep in ACCENTS:
        s = s.replace(pat, rep)
    # unwrap formatting commands, innermost first
    for _ in range(6):
        new = re.sub(r'\\(?:emph|textbf|textit|bf|it|text)\s*\{([^{}]*)\}', r'\1', s)
        if new == s: break
        s = new
    s = s.replace(r'\bf', '').replace(r'\em', '')
    s = s.replace(r'\&', '&').replace(r'\%', '%').replace(r'\$', '$').replace(r'\#', '#')
    s = s.replace('---', '\u2014').replace('--', '\u2013')
    s = s.replace('``', '\u201c').replace("''", '\u201d')
    s = s.replace('~', ' ')
    s = re.sub(r'\\[a-zA-Z]+\s*', '', s)      # any leftover command
    s = s.replace('{', '').replace('}', '')
    return re.sub(r'\s+', ' ', s).strip()

def slugify(t: str) -> str:
    t = detex(t).lower()
    t = t.replace('\u2019', '').replace("'", '')
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    words, out = t.split('-'), []
    for w in words:
        if len('-'.join(out + [w])) > 62: break
        out.append(w)
    return '-'.join(out) or 'untitled'

SECTIONS = {
    'Peer-Reviewed Publications': 'peer-reviewed',
    'Other Research Publications': 'other-research',
    'Working Papers': 'working-paper',
}

def sections(raw: str):
    """Yield (section_name, body) for the three publication sections."""
    marks = [(m.start(), m.group(1)) for m in re.finditer(r'\\section\{([^}]*)\}', raw)]
    for idx, (pos, name) in enumerate(marks):
        if name not in SECTIONS: continue
        end = marks[idx+1][0] if idx+1 < len(marks) else len(raw)
        yield name, raw[pos:end]

CUTS = [', in ', '. In ', r'\emph', r'\textbf', 'CEPR Disc', 'CEPR Working',
        'FRBNY Staff', 'NBER Working', 'Fed Board', 'IMF Working']

def parse_entry(chunk: str, section: str):
    chunk = chunk.strip()
    if not chunk: return None
    url, title = None, None
    h = chunk.find(r'\href')
    if h != -1:
        b1 = chunk.index('{', h)
        url, after = balanced(chunk, b1)
        b2 = chunk.index('{', after)
        title, after2 = balanced(chunk, b2)
        rest = chunk[after2:]
    else:
        m = re.search(r"``(.+?)''", chunk, re.S)
        if not m: return None
        title, rest = m.group(1), chunk[m.end():]

    title = detex(title).strip().rstrip(',.').strip('\u201c\u201d').rstrip(',').strip()

    # coauthors: from "with " up to the first venue marker
    coauthors = []
    venue_src = rest
    mw = re.search(r'\bwith\s', rest)
    if mw:
        tail = rest[mw.end():]
        cut = len(tail)
        for c in CUTS:
            p = tail.find(c)
            if p != -1: cut = min(cut, p)
        names = detex(tail[:cut]).strip().rstrip('.,').strip()
        names = re.sub(r',\s*and\s+', ', ', names)
        names = re.sub(r'\s+and\s+', ', ', names)
        coauthors = [n.strip() for n in names.split(',') if n.strip()]
        # The citation is the venue only. Authors render from `coauthors`, so
        # leaving the "with ..." clause in here printed every name twice.
        venue_src = tail[cut:]

    citation = detex(venue_src).lstrip('., ').strip()

    status = 'published'
    low = citation.lower()
    if 'conditionally accepted' in low: status = 'conditionally-accepted'
    elif 'revise' in low and 'resubmit' in low: status = 'r-and-r'
    elif 'forthcoming' in low: status = 'forthcoming'
    elif section == 'working-paper': status = 'working-paper'

    series = re.findall(r'((?:CEPR Discussion Paper|NBER Working Paper|FRBNY Staff Report No\.|Fed Board IFDP|IMF Working Paper No\.)\s*[\w/]+)', citation)

    # \b on both sides, or 'CEPR Discussion Paper 19644' parses as the year 1964.
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', citation)
    year = int(years[-1]) if years else None

    journal = None
    mj = re.search(r'\\(?:textbf|emph)\s*\{', rest)
    if mj:
        inner, _ = balanced(rest, rest.index('{', mj.start()))
        journal = detex(inner).strip().rstrip(',.').strip()
        if len(journal) > 90 or not journal: journal = None

    pdf = None
    if url and '/Papers/' in url:
        pdf = '/Papers/' + url.split('/Papers/')[-1].replace('&amp;', '&')

    return dict(title=title, coauthors=coauthors, citation=citation, status=status,
                section=section, series=series, year=year, journal=journal,
                pdf=pdf, url=(url if url and '/Papers/' not in url else None))

def main():
    raw = TEX.read_text(encoding='utf-8', errors='replace')
    lines = raw.split('\n')
    kept, dropped = [], []
    for ln in lines:
        s = ln.lstrip()
        if s.startswith('%'):
            if r'\item' in s and r'\href' in s:
                dropped.append(s)
            continue
        kept.append(strip_comments(ln))
    clean = '\n'.join(kept)

    entries = []
    for name, body in sections(clean):
        sec = SECTIONS[name]
        parts = body.split(r'\item')[1:]
        for p in parts:
            p = p.split(r'\end{subentry1}')[0]
            e = parse_entry(p, sec)
            if e and e['title']:
                entries.append(e)

    OUT.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    written, skipped = 0, 0
    for e in entries:
        slug = slugify(e['title'])
        path = OUT / f'{slug}.md'
        if path.exists():
            skipped += 1      # never clobber hand-written abstracts or topics
            continue
        fm = ['---']
        def y(k, v):
            if v in (None, '', [], False): return
            if isinstance(v, list):
                fm.append(f'{k}:')
                for i in v: fm.append(f'  - {json.dumps(i, ensure_ascii=False)}')
            elif isinstance(v, (int, bool)):
                fm.append(f'{k}: {json.dumps(v)}')
            else:
                fm.append(f'{k}: {json.dumps(v, ensure_ascii=False)}')
        y('title', e['title']); y('coauthors', e['coauthors'])
        y('section', e['section']); y('status', e['status'])
        y('journal', e['journal']); y('year', e['year'])
        y('citation', e['citation']); y('series', e['series'])
        y('pdf', e['pdf']); y('url', e['url'])
        fm += ['topics: []', 'featured: false', '---', '']
        path.write_text('\n'.join(fm), encoding='utf-8')
        written += 1

    report = ['# CV parse report', '',
              f'Source: `{TEX}`', '',
              f'- Entries parsed: **{len(entries)}**',
              f'- Files written: **{written}**',
              f'- Existing files left untouched: **{skipped}**',
              f'- Commented-out `\\item`s skipped: **{len(dropped)}**', '']
    if dropped:
        report += ['## Commented-out entries in the .tex (verify these are intentional)', '']
        for d in dropped:
            t = re.search(r'``(.+?),?\'\'', d)
            report.append(f'- {detex(t.group(1)) if t else d[:110]}')
        report.append('')
    counts = {}
    for e in entries: counts[e['section']] = counts.get(e['section'], 0) + 1
    report += ['## Counts by section', '']
    for k, v in counts.items(): report.append(f'- {k}: {v}')
    report += ['', '## Entries missing a parsed year or journal', '']
    for e in entries:
        miss = [f for f in ('year', 'journal') if not e[f]]
        if miss: report.append(f"- *{e['title'][:70]}* — missing {', '.join(miss)}")
    (DOCS / 'cv-parse-report.md').write_text('\n'.join(report) + '\n', encoding='utf-8')

    print(f'parsed {len(entries)} | wrote {written} | kept {skipped} | commented-out {len(dropped)}')
    for k, v in counts.items(): print(f'  {k}: {v}')

if __name__ == '__main__':
    main()
