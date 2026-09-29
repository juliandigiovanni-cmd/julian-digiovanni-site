#!/usr/bin/env python3
"""
Seed src/content/writing/ from the policy-writing list scraped off the live site.

The CV does not enumerate individual posts -- its "Policy and Popular Writing"
section links only to the CEPR and NY Fed index pages -- so the live site is the
only source for this list.

`paper:` values are PROPOSED cross-links for Julian to confirm. Where a post
plainly explains one paper the mapping is obvious; where a post covers a theme
rather than a single paper, paper is left None and noted in the report.
"""
import re, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "src/content/writing"
DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"

# (title, date ISO, url, proposed paper slug or None)
LSE = [
 ("What Is a Carbon Tariff and Why Is the EU Imposing One?", "2026-01-07",
  "https://libertystreeteconomics.newyorkfed.org/2026/01/what-is-a-carbon-tariff-and-why-is-the-eu-imposing-one/",
  "firms-supply-chain-adaptation-to-carbon-taxes"),
 ("What Can Undermine a Carbon Tax?", "2026-01-07",
  "https://libertystreeteconomics.newyorkfed.org/2026/01/what-can-undermine-a-carbon-tax/",
  "firms-supply-chain-adaptation-to-carbon-taxes"),
 ("International Stock Markets' Reactions to EU Climate Policy Shocks", "2024-10-10",
  "https://libertystreeteconomics.newyorkfed.org/2024/10/international-stock-markets-reactions-to-eu-climate-policy-shocks/",
  "global-spillovers-of-climate-policy-shocks"),
 # Live site listed this as 12/19/24, but its own URL says /2023/12/. URL wins.
 ("Does Trade Uncertainty Affect Bank Lending?", "2023-12-19",
  "https://libertystreeteconomics.newyorkfed.org/2023/12/does-trade-uncertainty-affect-bank-lending/",
  "trade-uncertainty-and-u-s-bank-lending"),
 ("Flood-Prone Basement Housing in New York City and the Impact to Low- and Moderate-Income Renters", "2023-11-17",
  "https://libertystreeteconomics.newyorkfed.org/2023/11/flood-prone-basement-housing-in-new-york-city-and-the-impact-on-low-and-moderate-income-renters/",
  None),
 ("Blog Series on the Economic and Financial Impacts of Extreme Weather Events in the Fed's Second District", "2023-11-08",
  "https://libertystreeteconomics.newyorkfed.org/2023/11/blog-series-on-the-economic-and-financial-impacts-of-extreme-weather-events-in-the-feds-second-district/",
  None),
 ("Is the Green Transition Inflationary?", "2023-01-14",
  "https://libertystreeteconomics.newyorkfed.org/2023/01/is-the-green-transition-inflationary/",
  "is-the-green-transition-inflationary"),
 ("How Much Can the Fed's Tightening Contract Global Economic Activity?", "2023-02-14",
  "https://libertystreeteconomics.newyorkfed.org/2023/02/how-much-can-the-feds-tightening-contract-global-economic-activity/",
  "pandemic-era-inflation-drivers-and-global-spillovers"),
 ("Highlights from the Fifth Bi-annual Global Research Forum on International Macroeconomics and Finance", "2022-12-19",
  "https://libertystreeteconomics.newyorkfed.org/2022/12/highlights-from-the-fifth-bi-annual-global-research-forum-on-international-macroeconomics-and-finance/",
  None),
 ("Climate Change: Implications for Macroeconomics", "2022-07-07",
  "https://libertystreeteconomics.newyorkfed.org/2022/07/climate-change-implications-for-macroeconomics/",
  None),
 ("Global Supply Chain Pressure Index: May 2022 Update", "2022-05-18",
  "https://libertystreeteconomics.newyorkfed.org/2022/05/global-supply-chain-pressure-index-may-2022-update/",
  "the-gscpi-a-new-barometer-of-global-supply-chain"),
 ("Global Supply Chain Pressure Index: March 2022 Update", "2022-03-03",
  "https://libertystreeteconomics.newyorkfed.org/2022/03/global-supply-chain-pressure-index-march-2022-update/",
  "the-gscpi-a-new-barometer-of-global-supply-chain"),
 ("The Global Supply Side of Inflationary Pressures", "2022-01-28",
  "https://libertystreeteconomics.newyorkfed.org/2022/01/the-global-supply-side-of-inflationary-pressures/",
  "global-supply-chain-pressures-international-trade-and"),
 ("A New Barometer of Global Supply Chain Pressures", "2022-01-04",
  "https://libertystreeteconomics.newyorkfed.org/2022/01/a-new-barometer-of-global-supply-chain-pressures/",
  "the-gscpi-a-new-barometer-of-global-supply-chain"),
 ("When Will U.S. Exports Take Off?", "2022-01-03",
  "https://libertystreeteconomics.newyorkfed.org/2022/01/when-will-u-s-exports-take-off/",
  None),
 ("The International Spillover of U.S. Monetary Policy via Global Production Linkages", "2021-01-06",
  "https://libertystreeteconomics.newyorkfed.org/2021/01/the-international-spillover-of-us-monetary-policy-via-global-production-linkages.html",
  "stock-market-spillovers-via-the-global-production-network"),
 ("Firm-Level Shocks and GDP Growth: The Case of Boeing's 737 MAX Production Pause", "2020-02-13",
  "https://libertystreeteconomics.newyorkfed.org/2020/02/firm-level-shocks-and-gdp-growth-the-case-of-boeings-737-max-production-pause.html",
  "foreign-shocks-as-granular-fluctuations"),
]

VOX = [
 ("Carbon leakage through firms' supply chain adaptation", "2025-01-02",
  "https://cepr.org/voxeu/columns/carbon-leakage-through-firms-supply-chain-adaptation",
  "firms-supply-chain-adaptation-to-carbon-taxes"),
 ("Banks' responses to trade uncertainty", "2024-03-11",
  "https://cepr.org/voxeu/columns/banks-responses-trade-uncertainty",
  "trade-uncertainty-and-u-s-bank-lending"),
 ("Supply chains, trade, and inflation", "2023-01-07",
  "https://cepr.org/voxeu/columns/supply-chains-trade-and-inflation",
  "global-supply-chain-pressures-international-trade-and"),
 ("Government procurement and macroeconomic outcomes", "2022-03-15",
  "https://cepr.org/voxeu/columns/government-procurement-and-macroeconomic-outcomes",
  "buy-big-or-buy-small-procurement-policies-firms-financing-and"),
 ("International shock transmission through heterogeneous firms", "2020-12-14",
  "https://cepr.org/voxeu/columns/international-shock-transmission-through-heterogeneous-firms",
  "foreign-shocks-as-granular-fluctuations"),
 ("International spillovers and local credit cycles: Evidence from Turkey", "2019-09-01",
  "https://cepr.org/voxeu/columns/international-spillovers-and-local-credit-cycles-evidence-turkey",
  "international-spillovers-and-local-credit-cycles"),
 ("International business cycle co-movement through the lens of individual firms", "2016-02-11",
  "https://cepr.org/voxeu/columns/international-business-cycle-co-movement-through-lens-individual-firms",
  "the-micro-origins-of-international-business-cycle-comovement"),
 ("Income-induced expenditure switching: Supermarket scanner data evidence from the 2008-09 Crisis in Latvia", "2014-09-08",
  "https://cepr.org/voxeu/columns/income-induced-expenditure-switching-supermarket-scanner-data-evidence-2008-09-crisis",
  "income-induced-expenditure-switching"),
 ("A global view of cross-border migration", "2013-07-01",
  "https://cepr.org/voxeu/columns/global-view-cross-border-migration",
  "a-global-view-of-cross-border-migration"),
 ("The role of firms in aggregate fluctuations", "2012-10-16",
  "https://cepr.org/voxeu/columns/role-firms-aggregate-fluctuations",
  "firms-destinations-and-aggregate-fluctuations"),
 ("Can China's growth lower welfare in developed countries? A refutation of the Samuelson conjecture", "2012-04-02",
  "https://cepr.org/voxeu/columns/can-chinas-growth-lower-welfare-developed-countries-refutation-samuelson-conjecture",
  "the-global-welfare-impact-of-china-trade-integration-and"),
 ("International trade, vertical production linkages, and the transmission of shocks", "2009-11-11",
  "https://cepr.org/voxeu/columns/international-trade-vertical-production-linkages-and-transmission-shocks",
  "putting-the-parts-together-trade-vertical-linkages-and"),
]

def slugify(t):
    t = t.lower().replace("'", "").replace("’", "")
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    words, out = t.split('-'), []
    for w in words:
        if len('-'.join(out + [w])) > 58: break
        out.append(w)
    return '-'.join(out)

def esc(s): return s.replace('"', '\\"')

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    unmapped, written, kept = [], 0, 0
    for items, outlet, name in ((LSE, 'liberty-street', 'Liberty Street Economics'),
                                (VOX, 'voxeu', 'VoxEU / CEPR')):
        for title, date, url, paper in items:
            path = OUT / f'{slugify(title)}.md'
            if path.exists():
                kept += 1; continue
            fm = ['---', f'title: "{esc(title)}"', f'outlet: "{outlet}"',
                  f'outletName: "{name}"', f'date: {date}', f'url: "{url}"']
            if paper: fm.append(f'paper: "{paper}"')
            else: unmapped.append(f'{name}: {title}')
            fm += ['topics: []', '---', '']
            path.write_text('\n'.join(fm), encoding='utf-8')
            written += 1

    rep = ['# Writing seed report', '',
           f'- Entries written: **{written}** (Liberty Street {len(LSE)}, VoxEU {len(VOX)})',
           f'- Existing files left untouched: **{kept}**', '',
           '## Posts with no paper cross-link proposed', '',
           'These cover a theme, a series, or someone else\'s work rather than one paper.',
           'If any should point at a paper, add a `paper:` slug to its file.', '']
    rep += [f'- {u}' for u in unmapped]
    rep += ['', '## Date correction applied', '',
            'The live site lists *Does Trade Uncertainty Affect Bank Lending?* as 12/19/24,',
            'but its own URL is `/2023/12/`. Seeded as **2023-12-19**. Worth confirming.', '']
    (DOCS / 'writing-seed-report.md').write_text('\n'.join(rep) + '\n', encoding='utf-8')
    print(f'wrote {written}, kept {kept}, unmapped {len(unmapped)}')

if __name__ == '__main__':
    main()
