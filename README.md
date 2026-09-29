# julian.digiovanni.ca

Static site built with [Astro](https://astro.build). Replaces the WordPress site
on Bluehost. No database, no plugins.

## Build

```sh
npm install
npm run dev      # http://localhost:4321, live reload
npm run build    # writes dist/
npm run preview  # serve dist/ locally
```

**Never `rm -rf dist`.** This repo lives inside Dropbox, and deleting then
recreating a directory under Dropbox produces "conflicted copy" duplicates.
Use `npm run clean`, which runs `find dist -mindepth 1 -delete`.

**Work from one machine at a time.** Dropbox syncing `.git` from two machines
at once can corrupt the repository.

`node_modules/` and `dist/` carry `xattr -w com.dropbox.ignored 1`. After a fresh
clone, re-apply it:

```sh
xattr -w com.dropbox.ignored 1 node_modules dist
```

## Where the content lives

All content is data. To change what appears, edit the Markdown in `src/content/`
and rebuild — the templates render whatever is there.

| What | Where |
|---|---|
| Papers (33) | `src/content/papers/*.md` |
| Policy writing (29) | `src/content/writing/*.md` |
| Nav, roles, profile links, disclaimer | `src/data/site.ts` |
| Topic labels and filter order | `src/data/site.ts` (`topicLabel`) |
| Schemas | `src/content.config.ts` |
| CV page content | `src/data/cv.ts` (transcribed by hand — see below) |
| Coffee page text and its figure | `src/pages/coffee.astro`, `src/lib/coffee-charts.ts` |
| Paper PDFs (73) | `public/Papers/` |

Every hook field on a paper is optional, so a half-filled entry renders
correctly. What is required is the minimum for an honest citation: `title`,
`section`, `status`.

`citation` is the display string and is always correct. `journal` / `year` are
best-effort extractions from the CV used only for sorting and filtering — if one
is wrong, display is unaffected.

## Scripts

| Script | Does |
|---|---|
| `scripts/parse-cv.py` | Bootstraps `src/content/papers/` from `~/Dropbox/CV/cv_diGiovanni.tex`. **Never overwrites an existing file**, so hand-written abstracts and topics survive a re-run. Writes `docs/cv-parse-report.md`. |
| `scripts/seed-writing.py` | Seeds `src/content/writing/` from the scraped live-site list. Same no-clobber rule. |
| `scripts/assign-topics.py` | Applies the topic tag mapping. Edit the table in the file and re-run. |
| `scripts/scrape-live-research.py` | Pulls the link layer off the live WordPress page: press, replication packages, coauthor homepages, series landing pages, version markers. **Only ever adds** — running it twice changes nothing. Writes `docs/live-scrape-report.md`. |
| `scripts/extract-abstracts.py` | Extracts abstracts from the mirrored PDFs into `data/abstracts.json`. Heuristic; writes `docs/abstract-extraction-report.md` naming anything it was unsure of. |
| `scripts/cv_sections.py` | Shared helper: reads the CV `.tex` and returns each section as clean text, stripping `\phantom{}` and friends. Run it directly to read a section: `python3 scripts/cv_sections.py Teaching`. |
| `scripts/check-cv-drift.py` | `npm run cv:check` — diffs the `.tex` against `data/cv-source.json` and names the sections that moved. `npm run cv:accept` records a new baseline. |
| `scripts/check-links.py` | `npm run links` — asserts the new-tab rule over `dist/`. |

## Things that are deliberate

**The filter is progressive enhancement.** With JavaScript disabled the filter
bar is inert and every paper stays visible, which is the right fallback for a
publication list. `/research/?topic=climate` deep-links a filter.

**Cross-links are `reference('papers')`, not strings.** A typo in a `paper:` slug
fails the build rather than rendering a dead link. All 24 currently resolve.

**The homepage is the hero alone.** An earlier version carried a "Selected work"
list; Julian asked for it out. `featured` / `featuredOrder` remain in the schema,
unused, in case that changes.

**Figures are rendered to SVG at build time.** `src/lib/chart.ts` runs Observable
Plot against a linkedom document and Astro inlines the markup, so a page with a
chart on it still ships no client JavaScript. Don't reach for a browser charting
library: the only figure on the site is static, and `<Figure>` expects an SVG
string. Data behind a figure is hard-coded in `src/lib/coffee-charts.ts` with its
source in a comment; there is no fetch step and nothing to refresh at build time.

**Light only. No dark mode.** Julian designs against light and wants every
visitor to see the same page, as on George's site. Don't reintroduce a
`prefers-color-scheme` block.

**Two sources, divided cleanly.** The CV gives the canonical citation; the live
WordPress page gives the link layer.

**Outbound links open in a new tab; internal ones do not.** One rule, in
`src/components/Link.astro`, covering every absolute URL to another host and
every PDF including our own. It is a component rather than a convention because
most links are generated from scraped data, and a rule people must remember at
each call site would be broken by the next scraper change. `npm run links`
enforces it over the built output.

**The CV page is transcribed, not parsed.** `src/data/cv.ts` holds it. Six `.tex`
sections are prose held together with `\phantom{}` spacing hacks, so a parser
would break where the LaTeX is ugliest. `npm run cv:check` reports drift when the
`.tex` changes.

**No takeaway lines on the research page.** Each entry used to carry a
hand-written one-sentence hook above the abstract toggle. With 33 papers on one
page it crowded the list, and the abstract is one click away on every entry, so
the hooks were cut in September 2026 — text, schema field and the spreadsheet
round-trip that authored them. Don't reinstate them.

**No chart on the homepage.** An early draft put the GSCPI series there. Julian
asked for it out: the index was many-authored and he no longer works on it, so
featuring it as a personal signature would overclaim. The GSCPI paper stays in
the working-paper list like any other. Don't reinstate it.

**Dark mode is token-only.** Every colour is a custom property in
`src/styles/theme.css`; `base.css` defines none. To drop dark mode, delete the
one `@media (prefers-color-scheme: dark)` block.

## Still to do

See `docs/decisions-and-findings.md` for the open questions. The one substantial
item left is the **deploy pipeline** — nothing has been uploaded anywhere yet.
The runbook for the first Bluehost cutover is `docs/deploy-runbook.md`, and the
`.htaccess` it uploads is `deploy/htaccess`.

Key figures are no longer outstanding: four were built for the Coffee page and one
kept. `docs/coffee-figures.md` records what the other three showed and where their
data came from, so any of them is rebuildable without redoing the research.
