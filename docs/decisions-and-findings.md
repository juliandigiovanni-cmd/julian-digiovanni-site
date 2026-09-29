# Decisions and findings

## Errors found in source material

These were found while building. **All of them are now fixed in
`~/Dropbox/CV/cv_diGiovanni.tex`** and the CV has been recompiled (September 2026,
8 pages, no new overfull boxes). Timestamped backups sit beside it.

The one exception is the Başkaya spelling in item 4, which was corrected on the site
but is Julian's call in the `.tex`.

### In `~/Dropbox/CV/cv_diGiovanni.tex`

1. **Stale title.** *Following Germany's Lead* is listed as "…to **Identify** the
   Effect of Monetary Policy…". The published REStat article is "…to **Estimate**
   the Effect…"; "Identify" was the earlier IZA DP 1495 title. The live website
   already had it right. Corrected in the site.

2. **Misspelled coauthor.** "Muhammed A. Yildrim" should be **Yildirim**
   (confirmed against NBER and RePEc). Three entries affected.

3. **Misspelled coauthor.** "Camelia Minou" in the *Trade Uncertainty* entry; the
   *Geoeconomic Fragmentation* entry spells the same person **Minoiu**, which is
   correct (Federal Reserve, RePEc). Corrected throughout. The live website
   carries the same typo.

4. **Inconsistent coauthor spelling.** The same person appears as
   "Yu\c{s}uf S. Baskaya" (JIE 2017) and "Yusuf S. Ba\c{s}kaya" (REStud 2022) —
   the cedilla is on the wrong letter in the first. RePEc gives
   **Yusuf Soner Başkaya**. *Not yet normalised — Julian's call.*

5. **Typos.** "CEPR Discusion Paper 17906" (missing s); "American **Economics**
   Association: Papers & Proceedings" where every other entry says "Economic".
   Both corrected in the site.

8. **"Minesterio de Ciencia"** in the 2018–2020 grant → **Ministerio**. Fixed in the
   `.tex` and recompiled.

9. **"University of Pompeu Fabra"** in Previous Positions, where the same CV says
   **Universitat Pompeu Fabra** everywhere else → fixed in the `.tex` and recompiled.
   All four mentions now agree.

### On the live site

6. ***Does Trade Uncertainty Affect Bank Lending?*** is dated 12/19/24, but its
   own URL is `/2023/12/`. Seeded as **2023-12-19**. Worth confirming.

### In `~/Dropbox/CV/bio_JDG_2024.docx`

7. The bio says "Head of the Climate Risk Studies Department". The CV's Current
   Positions and the live site both say **Economic Research Advisor** since 2025.
   The docx is stale and was not used.

## Server hygiene

`julian.digiovanni.ca/Papers/` has **directory indexing enabled** — anyone can
browse it. It serves 73 PDFs; the CV links 32. Most of the other 41 are
legitimate (online appendices, supplements, slides), but some are superseded
drafts:

- `DNdiGDo_climate_inflation v1.pdf`, `v2.pdf`
- `diGiovanniRogers_Revision1_ARC22.pdf`, `_FinalDraft_ARC22.pdf`
- `TwoRicardo_SPresubmit3.pdf`
- `multi_revised3.pdf`
- `errmonetary_sept07.pdf`

All 73 are mirrored into `public/Papers/` so nothing breaks at cutover. The new
`.htaccess` should set `Options -Indexes`.

`DGJMP_ProcurementCreditFirmGrowth-OA.pdf`, the online appendix to *Buy Big or
Buy Small?*, was linked briefly on 2026-09-20 and then dropped at Julian's
request, and deleted from the repo and the server. Unlinking alone would have
left it downloadable at its URL. The only copy is now
`server-archive-2026-09-20/unpublished/`.

**Files in `/Papers/` that nothing links.** After the appendices were restored
the site links 51 of the 62 files there. The other eleven are mostly
working-paper versions of published work, plus three worth a decision:
`diGiovanni_Matsumoto_HumanCapitalWealth.pdf`, which has no paper entry on the
site at all; and `PPPNotev4.pdf` and `MAPaperWeb-JIE.pdf`, which are referenced
nowhere in this repo. `WebAppendix_errmonetary_sept07.pdf` was deleted from both the repo and the
server on 2026-09-20: it was byte-identical to
`diGiovanni_Shambaugh_Appendix_JIE08.pdf` (md5 b5b3ac83), the same appendix
under its pre-publication name, linked from nowhere on either the old site or
the new one. The JIE08 copy is the one the research page links.

**`/Papers/` is not only PDFs.** It also holds ten replication archives, about
247 MB, which exist nowhere in this repo -- the server is the only copy. Nine
are linked from the research page through `dataCode`; `China_replication.zip`
sits there linked from nothing, on the old site or the new one, and nobody has
worked out which paper it belongs to.

**Settled, 2026-09-20.** The 73 on the server were verified byte-identical to
`public/Papers/`, so the directory is left in place at cutover rather than
re-uploaded -- no paper URL is dead for even a moment, which matters because the
published CV and the RePEc listings carry about 28 links into it. Seven superseded
drafts were deleted from both the repo and the server, taking it to 66. The rest
stay live, and the new `.htaccess` sets `Options -Indexes` so the folder can no
longer be browsed; every direct URL still resolves. See `deploy-runbook.md`.

## Reconciliation

The `.tex` and the live research page agree on 33 entries after three fixes:

- GSCPI paper — listed as a working paper on the live site; in the `.tex` it sits
  under "Policy and Popular Writing". Added as a working paper to match the site.
- *Following Germany's Lead* — title, see above.
- *Buy Big or Buy Small* — `.tex` says "Conditionally accepted, AER, December
  2025"; the live site says "Forthcoming, AER". Same status, different wording.
  Using the CV's.

Counts now match the live site exactly: 7 working, 20 peer-reviewed, 6 other.

## The CV page

`/cv/` is **transcribed by hand** into `src/data/cv.ts`, not parsed. Six of the sixteen
`.tex` sections are prose held together with `\phantom{}` spacing hacks, `\\` line breaks
and `\vspace{-6pt}` — typesetting scaffolding for the PDF that carries no structure. A
build-time parser would be fragile exactly where the LaTeX is ugliest, and a parse failure
would surface as a mangled page rather than an error.

`npm run cv:check` is what makes that safe. It re-reads the `.tex`, strips the scaffolding,
and diffs each section against the snapshot in `data/cv-source.json`, naming the sections
that moved. Drift in a section the site renders is an error; drift in a PDF-only section is
reported as informational. After updating `cv.ts`, `npm run cv:accept` records the new
baseline.

Deliberately out of the web CV, and in the PDF only: the seminars and conferences list, the
discussant list, and four policy publications (the BIS paper, the CREI Opuscle, the IMF
volume chapter and the IMF working paper).

## Abstracts

31 of 33 papers carry an abstract. Five were taken verbatim from RePEc or NBER and are
exact. **Twenty-six were extracted from the PDFs automatically** by
`scripts/extract-abstracts.py` and, while all 31 now start at a real sentence, a
machine-extracted one can still stop early or pick up a stray line of front matter.
They are worth skimming before the site goes live. The review spreadsheet that used to
carry them went when the takeaway round-trip was removed, so read them on the built
Research page or in the `abstract:` field of `src/content/papers/*.md`.

The two without an abstract are the two without a local PDF: the GSCPI staff report and
the CEPR book chapter.

## The Coffee page

`/coffee/` carries two parts: Know your Grounds, the specialty coffee map Julian built,
and a section on the coffee supply chain — where the money in a kilogram goes, and what
climate and other disruption do to each stage of the chain.

Two things about it are worth knowing before editing. The value split is **German
national-brand ground coffee with the taxes stripped out**, because a flat excise of
EUR 2.19/kg is 31% of a private-label ground pack and 6% of a capsule, so it describes
the package rather than the coffee. The division of the pre-tax price is our own
arithmetic on the study's published euro figures, and the caption says so.

And **no café cost breakdown appears anywhere on the page**, deliberately. Nobody
publishes one credibly: the trade-press and consultancy figures are uncited, and several
recent ones appear machine-generated. The café stage rests on Starbucks' 10-K instead.

`docs/coffee-figures.md` has the figures that were cut, their data sources and licences,
and the widely-quoted numbers that were checked and rejected.

## Waiting on Julian

1. **Press & media list.** Schema and UI support it; nothing to show yet.
2. **Five policy posts have no paper cross-link** (see `writing-seed-report.md`) —
   they cover a theme or a series rather than one paper.

Two items that were on this list are settled.

**Takeaway lines** are gone, not pending. Julian cut them in September 2026: with 33
papers on one page and an abstract toggle on every entry, a one-sentence hook above each
abstract crowded the list. The text, the schema field and the spreadsheet round-trip
that authored them were all removed together.

**Which papers to feature on the homepage** no longer arises. The homepage is the hero
alone — no "Selected work" list — so nothing reads `featured` or `featuredOrder`. Both
stay in the schema, unused, in case that changes.
