#!/usr/bin/env python3
"""
Assert the new-tab rule over the built site.

Anything that leaves the site, or hands the reader a file, must open in a new tab
with rel="noopener". Anything that navigates within the site must not. Most links
here are generated from scraped data, so this runs over dist/ rather than trusting
that every call site remembered.
"""
import re, sys, pathlib
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
HOST = 'julian.digiovanni.ca'

def should_leave(h):
    if h.startswith('mailto:') or h.startswith('#'): return False
    # keep in step with leavesTheSite() in src/components/Link.astro
    if re.search(r'\.(pdf|zip|dta)($|[?#])', h, re.I): return True
    if re.match(r'https?://', h, re.I):
        return urlparse(h).netloc.lower().removeprefix('www.') != HOST
    return False

def main():
    if not DIST.exists(): sys.exit('dist/ not found -- run npm run build first')
    bad_missing, bad_extra, total = [], [], 0
    for f in DIST.rglob('*.html'):
        html = f.read_text(encoding='utf-8', errors='replace')
        for m in re.finditer(r'<a\b([^>]*)>', html):
            attrs = m.group(1)
            hm = re.search(r'href="([^"]*)"', attrs)
            if not hm: continue
            href = hm.group(1)
            total += 1
            blank = 'target="_blank"' in attrs
            noop = 'noopener' in attrs
            page = f.relative_to(DIST)
            if should_leave(href):
                if not blank: bad_missing.append((page, href, 'no target=_blank'))
                elif not noop: bad_missing.append((page, href, 'no rel=noopener'))
            elif blank:
                bad_extra.append((page, href, 'opens a new tab but stays on the site'))

    print(f'checked {total} links across {len(list(DIST.rglob("*.html")))} pages')
    for label, rows in (('should open in a new tab but does not', bad_missing),
                        ('should stay in this tab but opens a new one', bad_extra)):
        if rows:
            print(f'\n{len(rows)} {label}:')
            for page, href, why in rows[:25]:
                print(f'  {page}  {href[:70]}  ({why})')
            if len(rows) > 25: print(f'  ... and {len(rows)-25} more')
    if bad_missing or bad_extra:
        sys.exit(1)
    print('OK -- every outbound link and PDF opens in a new tab; no internal link does')

if __name__ == '__main__':
    main()
