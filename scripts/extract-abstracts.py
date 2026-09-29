#!/usr/bin/env python3
r"""
Extract abstracts from the mirrored paper PDFs into data/abstracts.json.

Journal front matter varies a great deal, so this is heuristic by design: it
finds a candidate, records which rule fired, and flags anything that looks wrong
rather than pretending every extraction succeeded. Review the report before use.
"""
import re, json, pathlib, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAPERS, PUB, DATA, DOCS = ROOT/'src/content/papers', ROOT/'public', ROOT/'data', ROOT/'docs'

LIG = {'ﬀ':'ff','ﬁ':'fi','ﬂ':'fl','ﬃ':'ffi','ﬄ':'ffl',
       '’':"'", '“':'"', '”':'"', 'ﬆ':'st'}

STOP = re.compile(r'\b(JEL\s*(classification|codes?)|Keywords?|'
                  r'1\.?\s+Introduction|I\.?\s+Introduction|'
                  r'\*\s*We\s+thank|We\s+thank)\b', re.I)

def clean(t):
    for a, b in LIG.items(): t = t.replace(a, b)
    t = unicodedata.normalize('NFKC', t)
    t = re.sub(r'-\n', '', t)            # de-hyphenate across line breaks
    return re.sub(r'\s+', ' ', t).strip()

def extract(pdf):
    import pypdf
    try:
        r = pypdf.PdfReader(str(pdf))
        txt = ' '.join((r.pages[i].extract_text() or '') for i in range(min(3, len(r.pages))))
    except Exception as e:
        return None, f'unreadable: {e}'
    t = clean(txt)
    if not t: return None, 'no text layer (scanned?)'

    m = re.search(r'\bABSTRACT\b|\bAbstract\b', t)
    if m:
        body = t[m.end():].lstrip(' .:—-')
        rule = 'after "Abstract"'
    else:
        # No heading: the abstract usually sits between the affiliation block
        # and the first section. Start after the last CEPR/NBER/university line.
        m2 = None
        for m2 in re.finditer(r'(CEPR\)|NBER\)|University|Bank of New York|Sciences Po)', t[:2500]):
            pass
        body = t[m2.end():] if m2 else t
        rule = 'after affiliation block' if m2 else 'from start (low confidence)'

    # Journal front matter (author footnotes, article history, running heads)
    # sits between the title and the abstract and defeats the rules above. The
    # abstract itself almost always opens one of a small set of ways, so find
    # that opening -- skipping acknowledgements, which also start "We ...".
    OPEN = re.compile(r'\b(This paper|This article|This study|This Article|'
                      r'We (?!thank|are grateful|acknowledge|would like|gratefully)|'
                      r'Using |I examine|I study|I use)')
    for m3 in OPEN.finditer(body[:4000]):
        after = body[m3.start():m3.start() + 300]
        if re.search(r'@|e-?mail|Street|Avenue|Department of|\bUniversity\b.{0,40}\bUSA\b', after):
            continue
        body = body[m3.start():]
        rule += ' + opening'
        break

    s = STOP.search(body)
    if s: body = body[:s.start()]
    body = body.strip(' .;:—-')
    # Trim to whole sentences and a sane length.
    if len(body) > 1800:
        body = body[:1800]
        body = body[:body.rfind('. ') + 1]
    body = body.strip()
    if body and not body.endswith('.'): body += '.'
    return (body or None), rule

def main():
    DATA.mkdir(exist_ok=True); DOCS.mkdir(exist_ok=True)
    out, report = {}, []
    for f in sorted(PAPERS.glob('*.md')):
        s = f.read_text(encoding='utf-8')
        title = re.search(r'^title: "(.*)"$', s, re.M).group(1)
        pdf_m = re.search(r'^pdf: "(.*)"$', s, re.M)
        if not pdf_m:
            report.append((f.stem, title, 'NO PDF', 0)); continue
        pdf = PUB / pdf_m.group(1).lstrip('/')
        if not pdf.exists():
            report.append((f.stem, title, 'PDF MISSING', 0)); continue
        body, rule = extract(pdf)
        n = len(body or '')
        if body and 150 <= n <= 2000:
            out[f.stem] = {'title': title, 'abstract': body, 'rule': rule}
            report.append((f.stem, title, rule, n))
        else:
            report.append((f.stem, title, f'REVIEW — {rule}, {n} chars', n))
            if body: out[f.stem] = {'title': title, 'abstract': body, 'rule': rule + ' (REVIEW)'}

    (DATA/'abstracts.json').write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')

    ok = [r for r in report if not r[2].startswith(('REVIEW', 'NO PDF', 'PDF MISSING'))]
    bad = [r for r in report if r not in ok]
    lines = ['# Abstract extraction report', '',
             f'- Extracted cleanly: **{len(ok)}**',
             f'- Need review: **{len(bad)}**', '',
             '## Needs review', '']
    lines += [f'- `{s}` — {t[:60]} — {r}' for s, t, r, _ in bad] or ['- none']
    lines += ['', '## Extracted', '']
    lines += [f'- `{s}` — {r}, {n} chars' for s, t, r, n in ok]
    (DOCS/'abstract-extraction-report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'clean {len(ok)} | review {len(bad)} | written to data/abstracts.json')
    for s, t, r, _ in bad: print(f'  REVIEW {s}: {r}')

if __name__ == '__main__':
    main()
