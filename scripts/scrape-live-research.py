#!/usr/bin/env python3
r"""
Enrich src/content/papers/ with the link layer from the live WordPress site.

The CV gives the canonical citation. The live research page gives what the CV
does not: press coverage, replication packages, coauthor homepages, landing-page
URLs for each working-paper series, and version markers.

This script only ADDS. It never touches abstract, topics, featured or citation,
so it is safe to re-run after the live site is updated. Re-running is
idempotent: fields it manages are replaced wholesale, not appended to.
"""
import re, html, json, pathlib, unicodedata, subprocess, sys

URL = 'https://julian.digiovanni.ca/research'
ROOT = pathlib.Path(__file__).resolve().parent.parent
PAPERS, DOCS = ROOT / 'src/content/papers', ROOT / 'docs'

PRESS = {'bloomberg.com': 'Bloomberg', 'ft.com': 'Financial Times',
         'nytimes.com': 'New York Times', 'wsj.com': 'Wall Street Journal',
         'marketplace.org': 'NPR Marketplace', 'economist.com': 'The Economist',
         'reuters.com': 'Reuters'}
SERIES_HOSTS = ('cepr.org/publications', 'hub.cepr.org', 'nber.org/papers',
                'newyorkfed.org/research/staff_reports', 'federalreserve.gov/econres/ifdp')
BLOG_HOSTS = ('libertystreeteconomics', 'voxeu', 'cepr.org/voxeu')

# The live WordPress page misspells a few coauthors. Corrected here so a re-run
# cannot reintroduce them, and so the names still match the CV's spelling when
# the page decides which author to link.
NAME_FIXES = {
    'Muhammed A. Yildrim': 'Muhammed A. Yildirim',
    'Camelia Minou': 'Camelia Minoiu',
    'Manuel-García Santana': 'Manuel García-Santana',
    'Sebnem Kalemli-Özcan': 'Şebnem Kalemli-Özcan',
}

def norm(s):
    s = html.unescape(s)
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]', '', s.lower())

def txt(h):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h))).strip()

def main():
    # curl rather than urllib: this Python has no configured CA bundle, and
    # curl uses the system trust store.
    r = subprocess.run(['curl', '-sSfL', '--max-time', '30', URL],
                       capture_output=True)
    if r.returncode:
        sys.exit(f'fetch failed: {r.stderr.decode().strip()}')
    raw = r.stdout.decode('utf-8', 'replace')
    paras = re.findall(r'<p>(.*?)</p>', raw, re.S)

    by_title = {}
    for f in PAPERS.glob('*.md'):
        m = re.search(r'^title: "(.*)"$', f.read_text(encoding='utf-8'), re.M)
        if m: by_title[norm(m.group(1))] = f

    matched, unmatched, log = {}, [], []
    for p in paras:
        links = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', p, re.S)
        if not links: continue
        title = txt(links[0][1])
        if len(title) < 12: continue
        key = norm(title)
        f = by_title.get(key)
        if not f:
            # The live site sometimes closes the title anchor mid-phrase, e.g.
            # "...International Trade, and" with "Inflation" left outside it.
            # Fall back to a unique prefix match before giving up.
            cands = [v for k, v in by_title.items() if k.startswith(key) and len(key) > 25]
            f = cands[0] if len(cands) == 1 else None
        if not f:
            unmatched.append(title); continue
        if f in matched.values(): continue

        press, series, coauth, datacode = [], [], {}, []
        for url, label in links[1:]:
            label, u = txt(label), html.unescape(url)
            if not label: continue
            host = u.lower()
            if any(h in host for h in PRESS):
                name = next(v for k, v in PRESS.items() if k in host)
                if not any(x['url'] == u for x in press):
                    press.append({'label': name, 'url': u})
            elif any(h in host for h in SERIES_HOSTS):
                if not any(x['label'] == label for x in series):
                    series.append({'label': label, 'url': u})
            elif 'downloadSupplement' in u or 'replication' in label.lower():
                datacode.append({'label': 'Replication package', 'url': u})
            elif any(h in host for h in BLOG_HOSTS):
                pass                      # cross-links live in the writing collection
            elif 'julian.digiovanni.ca' not in host:
                coauth[NAME_FIXES.get(label, label)] = u   # everything else is a person

        ver = re.search(r'\(v\.([A-Za-z]{3}\d{2})', p)
        matched[key] = f
        apply(f, press, series, coauth, datacode, ver.group(1) if ver else None, log)

    DOCS.mkdir(exist_ok=True)
    missed = [t for k, t in ((norm(x), x) for x in
              (re.search(r'^title: "(.*)"$', f.read_text(encoding='utf-8'), re.M).group(1)
               for f in PAPERS.glob('*.md'))) if k not in matched]
    rep = ['# Live-site scrape report', '', f'Source: <{URL}>', '',
           f'- Paragraphs matched to a paper: **{len(matched)}** of {len(by_title)}', '']
    if missed:
        rep += ['## Papers with no match on the live site', '',
                '(Expected for anything added since the live site was last updated.)', '']
        rep += [f'- {t}' for t in missed] + ['']
    if unmatched:
        rep += ['## Live-site entries that matched no content file', ''] + \
               [f'- {t}' for t in unmatched] + ['']
    rep += ['## What was added', ''] + log + ['']
    (DOCS / 'live-scrape-report.md').write_text('\n'.join(rep) + '\n', encoding='utf-8')
    print(f'matched {len(matched)}/{len(by_title)}; {len(unmatched)} live entries unmatched')

def apply(f, press, series, coauth, datacode, version, log):
    s = f.read_text(encoding='utf-8')
    fm_end = s.index('\n---', 4)
    fm, body = s[4:fm_end], s[fm_end:]

    def drop(key):
        nonlocal fm
        fm = re.sub(rf'^{key}:.*?(?=^[a-zA-Z]+:|\Z)', '', fm, flags=re.M | re.S)

    def block(key, val):
        if not val: return ''
        return key + ': ' + json.dumps(val, ensure_ascii=False) + '\n'

    for k in ('press', 'series', 'coauthorUrls', 'version', 'dataCode'):
        drop(k)
    fm = fm.rstrip('\n') + '\n'
    fm += block('series', series)
    fm += block('press', press)
    fm += block('dataCode', datacode)
    fm += block('coauthorUrls', coauth)
    if version: fm += f'version: "{version}"\n'

    f.write_text('---\n' + fm + body.lstrip('\n'), encoding='utf-8')
    bits = []
    if press: bits.append(f"{len(press)} press")
    if series: bits.append(f"{len(series)} series links")
    if coauth: bits.append(f"{len(coauth)} coauthor links")
    if datacode: bits.append("replication")
    if version: bits.append(f"v.{version}")
    if bits: log.append(f'- **{f.stem}** — ' + ', '.join(bits))

if __name__ == '__main__':
    main()
