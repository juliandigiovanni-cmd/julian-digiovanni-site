# Coffee page figures

The `/coffee/` section on the coffee supply chain was worked up with four candidate
figures. Julian kept one and cut three. This records what the three were, so the
decision is legible and so the data plumbing can be rebuilt without redoing the
research.

## Kept

**Where the money goes in a kilogram of coffee.** Five chain stages in chain order,
the farmer's share split into production cost and income. Euro figures from BASIC et
al. (2024), *The Grounds for Sharing* (Global Coffee Platform, IDH, Solidaridad), as
reproduced in *Coffee Barometer 2026*, Fig. 7, p.59. Hard-coded in
`src/lib/coffee-charts.ts` — six numbers, no fetch step.

**The cappuccino index.** Minutes of barista work per cappuccino against real GDP per
capita, 36 countries, scatter on log-log with an OLS fit. Added later and for a
different section of the page; the sources and the gotchas are at the bottom of this
file. Also hard-coded in `src/lib/coffee-charts.ts`, 36 rows, no fetch step.

## Removed, and why

Julian's call after seeing all four in place: *"having the details of the chain was the
whole part. keep only this figure and drop the other 3."* The chain breakdown carried
the argument; the other three were context the section did not need.

### 1. World prices since 1960

Arabica and robusta, monthly, log scale, with the 1975, 1994 and 2021 Brazilian frosts
marked. Showed a freeze in Minas Gerais becoming a world price.

### 2. Brazil and Vietnam as a share of world production

1960–2026, from the arabica/robusta split. Showed Vietnam going from nothing to a sixth
of world output in two decades, and Brazil's biennial cycle as real sawtooth rather
than noise.

### 3. How far a price shock travels

World green price, US roaster-gate PPI and US retail CPI, each indexed to January 2020.
The best of the three for Julian's own research angle: green roughly doubled in the
year to February 2025, the roaster gate moved about half as far, retail about a
quarter, and each step later than the one above it — Nakamura and Zerom's incomplete
pass-through in public data.

## The data, if these are ever wanted again

The script that fetched all of it is gone. It was never committed, so the table below is
what survives; everything in it was verified live and is redistributable.

| Series | Source | Licence |
|---|---|---|
| Arabica and robusta, monthly, 1960– | World Bank Pink Sheet, `Monthly Prices` sheet, cols M/N | CC BY 4.0 |
| Production by country, 1960– | USDA FAS PSD, `psd_coffee_csv.zip` | US Gov, public domain |
| PPI roasted coffee `PCU3119203119201` | BLS, `pc/pc.data.4.Food` | US Gov, public domain |
| CPI coffee SA `CUSR0000SEFP01` | BLS, `cu/cu.data.11.USFoodBeverage` | US Gov, public domain |
| Avg price ground roast `APU0000717311` | BLS, `ap/ap.data.3.Food` | US Gov, public domain |

Five things that cost time to discover:

- **The Pink Sheet arabica and robusta columns are the ICO indicator prices.** The ICO
  sells its own history and publishes only a current-month PDF, so this is the lawful
  route to the same numbers, and it reaches back to 1960 rather than 1992.
- **Do not use FRED for the coffee price series.** They are IMF-copyrighted and FRED's
  terms forbid scraping. The BLS series are fine taken from BLS directly.
- **`download.bls.gov` returns 403 without a contact-identifying User-Agent.**
- **October 2025 is missing from the BLS consumer surveys** — the lapse in
  appropriations. It must stay a gap; a line drawn across it invents a month.
- **`M13` in the BLS flat files is the annual average, not a thirteenth month.** It has
  to be filtered out or it wrecks a time axis.

Also worth keeping: the Pink Sheet's first sheet is a QA artifact called
`Mismatch Details`, so the sheet must be named; its URL carries a document id that
rotates annually, so the link should be resolved from the commodity-markets page rather
than hard-coded; and the BLS `.0.Current` files are 8.5MB, 47MB and 64MB against the
per-topic cuts above at 6–9MB.

## Numbers that were checked and rejected

- **"Half of suitable coffee land gone by 2050."** That is the *highly suitable* class,
  which covers only ~36,000 km² globally against 5.7m km² of moderately suitable land.
  The class that carries world production falls about a third (Grüter et al., 2022).
- **The Panama Canal's floor of 18 transits a day.** Announced in Advisory A-48-2023 and
  never implemented; better rainfall arrived first. The realised trough was the low
  twenties. Widely misreported as fact.
- **"$1 billion in damage and 1.7 million jobs lost"** from the 2012–13 Central American
  rust crisis. Not in Avelino et al. (2015); no primary source found.
- **Café cost breakdowns.** No credible published source exists — the trade-press and
  consultancy numbers are uncited, and several 2026-dated ones appear machine-generated.
  The café stage rests on Starbucks' 10-K instead.
- **The German coffee tax as a share of the chain.** A flat €2.19/kg excise is 31% of a
  private-label ground pack and 6% of a capsule, so it describes the package rather than
  the coffee. It is taken out of the figure for that reason.

## The cappuccino index

Added after the supply-chain section was settled. It sits last on the page under
`#cappuccino`, behind a third anchor in the same `.section-nav`.

The index is James Hoffmann's, not ours. It is a country's mean cappuccino price divided
by its mean barista hourly wage, both converted to GBP first, expressed in minutes. The
currency conversion cancels out of the ratio, so no exchange rate enters the measure at
all. What is left is a relative price: a cappuccino valued in barista time. Note the
direction, which an earlier draft of the page got backwards — price over wage is a real
wage read upside down, so India's 172 minutes is the lowest real wage on the chart, not
the highest.

Two framings were written for this section and both were cut. The first set the index
against the Big Mac index, and went for not flowing — it came back later as a second
figure, which has its own section below. The second named Balassa-Samuelson,
and went for a better reason worth recording, because the flavour is real and someone
will notice it again: the paragraph had to claim that cappuccino prices rise with income,
while the only chart on the page slopes down. That asks a reader to take the claim on
faith against the one piece of evidence in front of them. Supporting it properly needs a
second figure plotting price and wage against income separately, and a section that
exists for fun does not carry two figures.

The check was run before the paragraph was cut, and the numbers are kept here so nobody
redoes them. The index is a ratio, so its slope decomposes exactly as
beta_index = beta_price - beta_wage. On log GDP per capita, PPP, 2024, n=36:

| Regressand (logs) | Slope | s.e. | R² |
|---|---|---|---|
| Cappuccino price, GBP | +0.35 | 0.06 | 0.49 |
| Barista hourly wage, GBP | +1.36 | 0.13 | 0.78 |
| Index, minutes | −1.02 | 0.12 | 0.69 |

The first row is the Balassa-Samuelson effect on a single, unusually clean nontradable:
under 4% of the cup crosses a border, which the supply-chain section of the same page
already establishes at 7 to 17 cents of green coffee in a $5 drink. The index falls
regardless, because wages rise with income faster than cappuccino prices do.

| Series | Source | Licence |
|---|---|---|
| Minutes per cappuccino, 36 countries | `Julian/Cappuccino Index 2026 (public).xlsx`, `index_(n≥10)` tab | Hoffmann, public workbook — credit him |
| GDP per capita, PPP, constant 2021 intl \$ | World Bank WDI `NY.GDP.PCAP.PP.KD`, 2024 | CC BY 4.0 |

Source workbook lives one directory up from the site, outside the repo. Its three tabs
are `full_data` (2,594 crowdsourced responses, wage and price per respondent),
`capp_index_all_countries` (all 87) and `index_(n≥10)` (the 36 used here). Hoffmann's
video is <https://www.youtube.com/watch?v=WtlE3BW9Nqs> and his dashboard is linked from
the page.

Things that cost time to discover:

- **Do not recompute the index from `full_data`.** Mean price over mean wage lands
  Australia at 10.075 against his published 10.067. He is using slightly different FX or
  rounding somewhere, and his published number is the one to reproduce. Only the 36
  published values are in the repo; the 2,594 raw responses are not.
- **Use the n≥10 tab.** The full 87-country tab has a long tail of countries resting on a
  single response, which is noise presented as a national average.
- **Python here has no CA bundle** and `urllib` fails TLS verification against the World
  Bank API. Use `curl`. `openpyxl` reads the workbook and needs no network.
- **Plot's log scale re-thins tick labels** after applying whatever `tickFormat` it is
  given, and drops the 90 while keeping its tick mark, leaving a bare dash on the axis.
  An explicit `Plot.axisY` mark over the same values, with `axis: null` on the scale,
  keeps all nine.
- **Plot's `dx`, `dy` and `textAnchor` are constant options, not channels.** A function
  passed for any of them is ignored without warning and every label lands on top of its
  own dot. Hence one `Plot.text` mark per distinct offset.
- **Fourteen of the 36 are labelled.** The fifteen countries between \$47k and \$76k are
  one pile that nothing can be written into legibly at 680px, so the labelled set is the
  points outside it plus the ones the prose names.
- **`Plot.linearRegressionY` would be wrong here.** It fits in data space; both scales are
  logarithmic, so the line that belongs on the figure is the one straight in logs. It is
  computed by hand: slope −1.02, R² 0.69 on the 36 shipped values.
- **The −1.02 slope is specific to PPP income.** Against GDP per capita at market exchange
  rates the index slope is −0.71, with price +0.23 and wage +0.95. The near-exact minus one
  is partly the deflator and should not be read as a law.
- **`full_data` spells New Zealand with a non-breaking space** (`New\xa0Zealand`), so it
  silently fails to join against the index tab and the country drops out with no error.
  Normalise before any join.
- **Two x-positions are not what they look like.** Ireland's GDP per capita carries
  multinational profit shifting and Singapore's is a city-state with no rural hinterland
  averaged in. The caption used to say so and no longer does -- it was cut as too much
  detail for this page, along with the note on which countries are labelled. Worth knowing
  before reading anything into where those two sit.

## The cappuccino as an exchange-rate index

The second figure in the same section, added after the first. The page calls the measure
the Cappuccino Exchange Rate Index, labelled "Cappuccino XR index" on the figure, and
gives it its own `h3` ("A new coffee-based measure of exchange-rate valuation") after the Hoffmann
credit and links, which close the barista-minutes part. Hoffmann's `full_data`
records each price in local currency, so the survey supports the Big Mac arithmetic: a
country's price over the American price is an implied exchange rate, and that over the
market rate is the over- or undervaluation against the dollar. The figure plots our
cappuccino valuation against the Economist's Big Mac valuation for the 34 countries in
both, with a 45-degree line. Pearson r is 0.69, Spearman 0.69, and 71% of countries take
the same sign.

The prose has been through one rewrite with Julian, and the section went live on 3 October 2026.
The first draft argued that the cappuccino is a better Big Mac than the Big Mac because
under four per cent of it ever crosses a border. That was cut because it gets the
economics backwards: purchasing power parity rests on arbitrage, which only pulls the
prices of traded goods together, so a good that barely trades is the weaker candidate,
and nontradables are where Balassa-Samuelson says prices drift with income. The
paragraph after the figure now attributes the disagreements to the goods, and the evidence
it gives against the nominal exchange rate is Italy against Germany: one currency, valued
at −57% and −9%. It names measurement and local preferences as likely contributors and
avoids presenting them as the only two. Julian asked for economics terms throughout
(implied exchange rate, overvalued, undervalued) and no spatial phrasing such as "further
below the dollar".

Working, with bootstrap intervals, a GDP-adjusted version and the robustness checks, is
in `Julian/analysis/cappuccino-ppp/` (which has its own README) one directory up from
the site: `cappuccino_ppp.py` regenerates `cappuccino_ppp.csv`, `report.html` and the
paste-ready `valuation.ts.txt`.
The 34 pairs shipped to the page are `VALUATION` in `coffee-charts.ts`.

| Series | Source | Licence |
|---|---|---|
| Cappuccino price in local currency, 36 countries | `Cappuccino Index 2026 (public).xlsx`, `full_data` tab | Hoffmann, public workbook — credit him |
| Big Mac price, market rate, index | `TheEconomist/big-mac-data`, `source-data/big-mac-source-data-v2.csv` and `output-data/big-mac-full-index.csv`, 2026-07-01 | The Economist, GitHub repo |

Method decisions, each of which moves numbers:

- **Geometric mean, not median.** Prices pile up on round numbers, so medians are lumpy:
  the American median is exactly $5.00 and the bootstrap intervals collapse onto their own
  end points. A mean of logs fixes that and the two sets of valuations correlate at 0.997.
- **Modal currency per country.** A handful of responses quote USD from outside the US.
  Keeping only each country's own currency drops them.
- **Outliers.** Log price more than 3 MADs from the country median, 88 of 2,594 responses.
  The n≥10 cut is applied before this, so it stays Hoffmann's 36 countries.
- **Exchange rates come from the workbook**, backed out as column H over column C, since
  it stores cached GOOGLEFINANCE values and no rate column. The date is not recorded. They
  sit within 0.5% of the Economist's July rates at the median, 4% at the worst (Chile),
  and swapping in the Economist's rates moves valuations by about that much.
- **Euro countries are reported separately**, using the Economist's source file, because
  its published index carries only a single euro area. Recomputing its `USD_raw` from that
  file reproduces the published figures to 5e-06, which is the check that the formula
  matches theirs. Pooling all EUR responses instead gives a euro area at −12%, against the
  Economist's +14%.
- **PPP income, not market income, for anything involving GDP.** The page's other figure
  already uses WDI `NY.GDP.PCAP.PP.KD`, and a dollar price regressed on a market-rate
  income has the same exchange rate in both variables. The script reads the 36 GDP values
  straight out of the `CAPPUCCINO` array in `coffee-charts.ts`, so the two figures cannot
  drift apart. On PPP income the cappuccino's dollar-price elasticity is 0.34 (s.e. 0.06),
  which reproduces the +0.35 in the table above, and the Big Mac's is 0.38 (s.e. 0.06).

Things worth knowing before reading the figure:

- **The level is anchored on the American price and the ranking is the safer half.** The
  cappuccino averages −16% against the Big Mac's −1%, because an American cappuccino is
  dear by international standards while an American Big Mac is not. A 10% higher American
  base makes every other country about 9% more undervalued. If the section ever grows, a
  sample-average numeraire is the defensible version of the level.
- **Italy is the outlier of the whole exercise**, at −57% on coffee against +21% on the
  burger. The €1.85 espresso-bar cappuccino is real, and so is its smaller cup.
- **Sampling noise is not what drives the gaps.** The median 90% bootstrap interval, over
  responses within each country and within the US base, is 8 points wide, and 94% of
  countries have an interval excluding zero.
- **The GDP-adjusted version was computed and not shipped.** Fitting the Economist's linear
  adjustment to each good over the same countries leaves r at 0.50, against 0.69 raw. It is
  in the CSV as `capp_adj` and `bm_adj_own` if it is ever wanted.
- **Restricting to urban responses changes nothing** (r = 0.999 with the baseline), which
  is worth knowing because the American sample leans suburban.
- **Square data area.** The 45-degree line only means what the caption says if the x and y
  ranges are equally long in pixels. `valuationChart` keeps the shared 680 width and
  a 480 height, close to the 440 the other figures use, and centres a square data area
  inside it with wide side margins.
