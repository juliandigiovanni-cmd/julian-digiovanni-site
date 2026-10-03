import * as Plot from '@observablehq/plot';
import { renderPlot, INK, INK_MUTED, RULE, ACCENT, NEUTRAL, CHAIN } from './chart';

const WIDTH = 680;

/**
 * Where the money goes in a kilogram of coffee.
 *
 * Bars run in CHAIN ORDER, not sorted by size: the order is the argument. The
 * colour ramp runs dark at the farm to light at the shelf, so position in the
 * chain is encoded twice.
 *
 * Figures are euros per kilogram of German national-brand ground coffee, 2021,
 * from BASIC et al. (2024) as reproduced in Coffee Barometer 2026, Figure 7.
 * The published components are:
 *
 *   farmer cost 1.56, farmer income 0.41, export 0.29, trader 0.35,
 *   roaster 1.03, retail 1.71, coffee tax 2.19, VAT 0.53  =  8.07
 *
 * against a published retail price of 8.06 -- a cent of rounding. Taking out
 * the two taxes leaves a 5.34 base, and the shares below are that division,
 * which is our arithmetic rather than theirs. Taxes come out because a flat
 * German excise of 2.19/kg is a fact about Germany, not about coffee: the same
 * levy is 31% of a private-label ground pack and 6% of a capsule.
 *
 * "Farmgate" is the term of art for the first bar and is not used here. It
 * means what the farmer is paid at the farm, before anything is done to move
 * the coffee, and it is split into its two published parts because the split
 * is the point: most of it is the cost of growing, not income.
 */
const PRE_TAX = 5.34;

const STAGES = [
  { stage: 'The farmer', part: 'what growing it costs', eur: 1.56 },
  { stage: 'The farmer', part: 'left as income', eur: 0.41 },
  { stage: 'Export', part: '', eur: 0.29 },
  { stage: 'Trade and shipping', part: '', eur: 0.35 },
  { stage: 'Roasting', part: '', eur: 1.03 },
  { stage: 'Retail', part: '', eur: 1.71 },
];

export function chainChart() {
  const order = ['The farmer', 'Export', 'Trade and shipping', 'Roasting', 'Retail'];
  const colour = Object.fromEntries(order.map((s, i) => [s, CHAIN[i]]));

  // The farmer's bar is the only one with two parts, so it stacks; the rest
  // are single segments that happen to start at zero.
  let run = 0;
  const bars = STAGES.map((d) => {
    const prev = d.stage === 'The farmer' ? run : 0;
    const pct = (100 * d.eur) / PRE_TAX;
    if (d.stage === 'The farmer') run += pct;
    return { ...d, pct, x1: prev, x2: prev + pct };
  });

  const totals = order.map((s) => ({
    stage: s,
    pct: bars.filter((b) => b.stage === s).reduce((a, b) => a + b.pct, 0),
  }));

  return renderPlot(
    {
      width: WIDTH,
      height: 300,
      marginLeft: 132,
      marginRight: 56,
      marginTop: 8,
      marginBottom: 40,
      x: {
        domain: [0, 40],
        label: '% of what a kilogram costs before tax',
        labelAnchor: 'left',
        grid: true,
        tickFormat: (d: number) => String(d),
      },
      y: { domain: order, label: null },
      style: { fontSize: '12px' },
      marks: [
        Plot.ruleX([0], { stroke: RULE }),
        Plot.barX(bars, {
          x1: 'x1', x2: 'x2', y: 'stage',
          fill: (d: any) => colour[d.stage],
          // The farmer's income segment is drawn a shade lighter than the cost
          // segment beside it, so the two parts separate without a sixth hue.
          fillOpacity: (d: any) => (d.part === 'left as income' ? 0.55 : 1),
          insetRight: 1, insetTop: 6, insetBottom: 6,
        }),
        // Totals at the bar end. The 5% export bar is far too short to carry a
        // label inside it, so every total sits outside, past the bar.
        Plot.text(totals, {
          x: 'pct', y: 'stage', text: (d: any) => `${Math.round(d.pct)}%`,
          dx: 6, textAnchor: 'start', fontSize: 12, fontWeight: 600, fill: INK,
        }),
        // The farmer's two parts, named inside their own segments -- below the
        // bar they crowded the row beneath. White on the dark cost segment,
        // ink on the lighter income one.
        Plot.text(bars.filter((d) => d.part), {
          x: (d: any) => (d.x1 + d.x2) / 2, y: 'stage',
          text: (d: any) => d.part,
          fontSize: 11, textAnchor: 'middle',
          fill: (d: any) => (d.part === 'left as income' ? INK : '#ffffff'),
        }),
      ],
    },
    'Where the money goes in a kilogram of coffee, by stage of the supply chain',
  );
}

/**
 * The cappuccino index: minutes of barista work per cappuccino, against income.
 *
 * `min` is James Hoffmann's published index (Cappuccino Index 2026), read off the
 * n>=10 tab of his public workbook and rounded to a tenth of a minute. It is a
 * country's mean cappuccino price divided by its mean barista hourly wage, both
 * converted to GBP first, expressed in minutes. The conversion cancels: a ratio
 * of two prices in the same currency is the same number whatever currency that
 * is, which is the whole point of the measure and the reason no exchange rate
 * appears anywhere below.
 *
 * Do not recompute these from his response-level data. Doing so lands Australia
 * at 10.075 against his published 10.067 -- he is using slightly different FX or
 * rounding somewhere, and his published number is the one to reproduce.
 *
 * `n` is his count of responses behind each country. Only countries with n >= 10
 * are here; his full file has 87, but the tail is countries resting on a single
 * response and they are noise.
 *
 * `gdp` is World Bank WDI NY.GDP.PCAP.PP.KD -- GDP per capita, PPP, constant 2021
 * international dollars -- for 2024, the last year with a complete reading for all
 * 36. Retrieved from the WDI API, database updated 2026-07-13, CC BY 4.0.
 *
 * The fitted line is ours, not his: an OLS of log(min) on log(gdp), which on these
 * 36 points has a slope of -1.02 and an R-squared of 0.69. An elasticity of about
 * minus one means doubling income per head roughly halves the barista time a
 * cappuccino costs.
 */
const CAPPUCCINO = [
  { country: 'Australia', min: 10.1, gdp: 60310, n: 171 },
  { country: 'Italy', min: 11.8, gdp: 53285, n: 15 },
  { country: 'New Zealand', min: 12.8, gdp: 48325, n: 35 },
  { country: 'Switzerland', min: 14.4, gdp: 85448, n: 18 },
  { country: 'Netherlands', min: 14.9, gdp: 70494, n: 73 },
  { country: 'Germany', min: 15.0, gdp: 62655, n: 167 },
  { country: 'Norway', min: 15.5, gdp: 94804, n: 22 },
  { country: 'Belgium', min: 15.8, gdp: 63311, n: 19 },
  { country: 'Ireland', min: 16.0, gdp: 118833, n: 45 },
  { country: 'Canada', min: 16.2, gdp: 57534, n: 130 },
  { country: 'Finland', min: 16.4, gdp: 55901, n: 16 },
  { country: 'UK', min: 17.5, gdp: 53412, n: 595 },
  { country: 'USA', min: 17.9, gdp: 75698, n: 600 },
  { country: 'Sweden', min: 18.2, gdp: 62558, n: 20 },
  { country: 'Israel', min: 18.8, gdp: 47389, n: 14 },
  { country: 'Spain', min: 19.0, gdp: 48460, n: 30 },
  { country: 'Austria', min: 19.0, gdp: 63788, n: 13 },
  { country: 'Denmark', min: 19.4, gdp: 71035, n: 36 },
  { country: 'France', min: 21.3, gdp: 54799, n: 31 },
  { country: 'Singapore', min: 25.2, gdp: 134549, n: 20 },
  { country: 'Slovakia', min: 25.3, gdp: 40302, n: 10 },
  { country: 'Czechia', min: 28.4, gdp: 47973, n: 67 },
  { country: 'Poland', min: 29.4, gdp: 45153, n: 100 },
  { country: 'Portugal', min: 30.0, gdp: 42228, n: 13 },
  { country: 'Hungary', min: 30.4, gdp: 40747, n: 17 },
  { country: 'Greece', min: 35.5, gdp: 37474, n: 23 },
  { country: 'Romania', min: 40.8, gdp: 40504, n: 17 },
  { country: 'Chile', min: 48.9, gdp: 30268, n: 10 },
  { country: 'Russia', min: 52.2, gdp: 41891, n: 14 },
  { country: 'Brazil', min: 56.8, gdp: 19652, n: 14 },
  { country: 'Argentina', min: 60.2, gdp: 26772, n: 22 },
  { country: 'Malaysia', min: 67.2, gdp: 34116, n: 18 },
  { country: 'Turkey', min: 73.0, gdp: 36154, n: 10 },
  { country: 'Mexico', min: 74.5, gdp: 21970, n: 24 },
  { country: 'Philippines', min: 110.5, gdp: 10378, n: 11 },
  { country: 'India', min: 172.0, gdp: 9416, n: 11 },
];

// Thirty-six labels will not fit in 680px, and the fifteen countries between
// $47k and $76k are a single pile that nothing can be legibly written into. So
// the labelled set is the points that sit outside that pile, plus the ones the
// prose names; the caption says the rest are unlabelled.
//
// Plot treats dx, dy and textAnchor as constant options rather than channels, so
// a function passed for any of them is quietly ignored and every label lands on
// top of its own dot. One text mark per distinct offset is the way round it,
// which is what PLACEMENT is grouped into below.
//
// The offsets are hand-tuned against the rendered figure. If a value moves,
// re-check its neighbours rather than trusting these numbers: 'end' is used at
// the right edge, where a label running outwards would be clipped, and inside
// the tight pairs where two labels would otherwise run into each other.
type Placement = { anchor: 'start' | 'end' | 'middle'; dx: number; dy: number };

const PLACEMENT: Record<string, Placement> = {
  India: { anchor: 'start', dx: 8, dy: 0 },
  Philippines: { anchor: 'start', dx: 8, dy: 0 },
  Mexico: { anchor: 'start', dx: 8, dy: 0 },
  Turkey: { anchor: 'start', dx: 8, dy: 0 },
  USA: { anchor: 'start', dx: 8, dy: 0 },
  Australia: { anchor: 'start', dx: 8, dy: 0 },
  Brazil: { anchor: 'end', dx: -8, dy: 0 },
  Singapore: { anchor: 'end', dx: -8, dy: 0 },
  'New Zealand': { anchor: 'end', dx: -8, dy: 0 },
  Malaysia: { anchor: 'end', dx: -8, dy: 12 },
  Italy: { anchor: 'end', dx: -8, dy: 12 },
  Poland: { anchor: 'middle', dx: 0, dy: -13 },
  Ireland: { anchor: 'middle', dx: 0, dy: -14 },
  Switzerland: { anchor: 'middle', dx: 0, dy: 13 },
};

const MINUTE_TICKS = [10, 15, 20, 30, 45, 60, 90, 120, 180];

export function cappuccinoChart() {
  // OLS in logs. Plot.linearRegressionY would fit in data space, which is the
  // wrong space here: both scales are logarithmic, so the line that belongs on
  // this figure is the one that is straight in logs.
  const n = CAPPUCCINO.length;
  const xs = CAPPUCCINO.map((d) => Math.log(d.gdp));
  const ys = CAPPUCCINO.map((d) => Math.log(d.min));
  const mx = xs.reduce((a, b) => a + b, 0) / n;
  const my = ys.reduce((a, b) => a + b, 0) / n;
  const slope =
    xs.reduce((a, x, i) => a + (x - mx) * (ys[i] - my), 0) /
    xs.reduce((a, x) => a + (x - mx) ** 2, 0);

  // Drawn across the data only, not the padded domain: extending a fit past the
  // last observation claims more than the 36 points support.
  const lo = Math.min(...CAPPUCCINO.map((d) => d.gdp));
  const hi = Math.max(...CAPPUCCINO.map((d) => d.gdp));
  const fit = [lo, hi].map((gdp) => ({
    gdp,
    min: Math.exp(my + slope * (Math.log(gdp) - mx)),
  }));

  // One mark per distinct offset, see the note on PLACEMENT above.
  const groups = new Map<string, { place: Placement; rows: typeof CAPPUCCINO }>();
  for (const d of CAPPUCCINO) {
    const place = PLACEMENT[d.country];
    if (!place) continue;
    const key = `${place.anchor}|${place.dx}|${place.dy}`;
    if (!groups.has(key)) groups.set(key, { place, rows: [] });
    groups.get(key)!.rows.push(d);
  }

  return renderPlot(
    {
      width: WIDTH,
      height: 440,
      marginLeft: 54,
      marginRight: 24,
      marginTop: 10,
      marginBottom: 46,
      // Padded past the data on both axes so that Singapore and Ireland at the
      // right edge, and India at the top, keep their dots off the frame.
      x: {
        type: 'log',
        domain: [8400, 155000],
        label: 'Real GDP per capita, PPP (constant 2021 $, log scale)',
        labelAnchor: 'left',
        ticks: [10000, 20000, 50000, 100000],
        tickFormat: (d: number) => `$${d / 1000}k`,
        grid: true,
      },
      // The axis is drawn as a mark rather than by the scale. Plot's log scale
      // runs its own label-thinning over whatever tickFormat it is given and
      // silently drops the 90, leaving a tick with no number beside it; an
      // explicit axisY over the same values keeps all nine.
      y: { type: 'log', domain: [9, 200], axis: null },
      style: { fontSize: '12px' },
      marks: [
        Plot.gridY(MINUTE_TICKS, { stroke: RULE }),
        Plot.axisY(MINUTE_TICKS, {
          tickFormat: (d: number) => String(d),
          label: 'Minutes of barista work per cappuccino',
          labelAnchor: 'top',
        }),
        Plot.line(fit, {
          x: 'gdp', y: 'min',
          stroke: NEUTRAL, strokeWidth: 1.5, strokeDasharray: '4,3',
        }),
        Plot.dot(CAPPUCCINO, {
          x: 'gdp', y: 'min',
          r: 4, fill: ACCENT, fillOpacity: 0.85,
        }),
        ...[...groups.values()].map(({ place, rows }) =>
          Plot.text(rows, {
            x: 'gdp', y: 'min',
            text: 'country',
            fontSize: 11,
            fill: INK_MUTED,
            textAnchor: place.anchor,
            dx: place.dx,
            dy: place.dy,
          }),
        ),
      ],
    },
    'Minutes of barista work needed to buy one cappuccino, against real GDP per capita, 36 countries',
  );
}


/**
 * The same survey read as an exchange-rate index, against the Big Mac.
 *
 * Hoffmann's `full_data` records each price in local currency, and a cappuccino is
 * about as nontradable as a good gets, so the Economist's Big Mac arithmetic applies:
 * a country's price over the American price is an implied exchange rate, and that over
 * the market rate is how far the currency sits from the dollar. Both numbers below are
 * that calculation, in per cent.
 *
 * `capp` is ours. Country price is the geometric mean of the responses quoted in the
 * country's own currency, for the 36 countries answered at least ten times, against an
 * American base of $4.91. Market rates are the GOOGLEFINANCE values cached in the
 * workbook, which sit within half a per cent of the Economist's July rates. A mean of
 * logs rather than a median because prices pile up on round numbers -- the American
 * median is exactly $5.00 -- though the two give valuations correlated at 0.997.
 *
 * `bigmac` is the Economist's July 2026 index, github.com/TheEconomist/big-mac-data.
 * Individual euro countries are computed here from its source file by the same formula,
 * since the published index carries only a single euro area; where both exist they agree
 * to five decimal places.
 *
 * Two of the 36 are missing: the United States, which is zero on both by construction,
 * and Russia, which McDonald's left in 2022.
 *
 * Working, including bootstrap intervals and a GDP-adjusted version, is in
 * analysis/cappuccino-ppp/ one directory up from the site.
 */
const VALUATION = [
  { country: 'Italy', capp: -57, bigmac: 21 },
  { country: 'Philippines', capp: -55, bigmac: -56 },
  { country: 'India', capp: -48, bigmac: -61 },
  { country: 'Brazil', capp: -42, bigmac: -24 },
  { country: 'Malaysia', capp: -37, bigmac: -43 },
  { country: 'Argentina', capp: -35, bigmac: -5 },
  { country: 'Spain', capp: -34, bigmac: 8 },
  { country: 'New Zealand', capp: -33, bigmac: -17 },
  { country: 'Slovakia', capp: -31, bigmac: -8 },
  { country: 'Chile', capp: -29, bigmac: -13 },
  { country: 'Romania', capp: -29, bigmac: -36 },
  { country: 'Greece', capp: -28, bigmac: -10 },
  { country: 'Mexico', capp: -25, bigmac: 1 },
  { country: 'Czechia', capp: -25, bigmac: -13 },
  { country: 'Canada', capp: -24, bigmac: -7 },
  { country: 'Australia', capp: -24, bigmac: -4 },
  { country: 'Portugal', capp: -22, bigmac: 4 },
  { country: 'Turkey', capp: -20, bigmac: 11 },
  { country: 'Hungary', capp: -18, bigmac: -15 },
  { country: 'Poland', capp: -15, bigmac: 0 },
  { country: 'Singapore', capp: -11, bigmac: -7 },
  { country: 'Germany', capp: -9, bigmac: 29 },
  { country: 'Netherlands', capp: -7, bigmac: 15 },
  { country: 'Ireland', capp: -5, bigmac: 21 },
  { country: 'Belgium', capp: -5, bigmac: -1 },
  { country: 'Austria', capp: -4, bigmac: 4 },
  { country: 'Israel', capp: 0, bigmac: 23 },
  { country: 'Sweden', capp: 5, bigmac: 15 },
  { country: 'UK', capp: 5, bigmac: 19 },
  { country: 'Finland', capp: 6, bigmac: 17 },
  { country: 'France', capp: 10, bigmac: 3 },
  { country: 'Norway', capp: 17, bigmac: 29 },
  { country: 'Switzerland', capp: 41, bigmac: 45 },
  { country: 'Denmark', capp: 42, bigmac: 13 },
];

// Eight labels out of 34. The four corners of the argument -- Italy and Denmark off the
// line, Switzerland and India on it -- plus Germany, which the prose sets against Italy,
// and three more that sit clear of their neighbours. The rest would collide at 680px.
const VAL_PLACEMENT: Record<string, Placement> = {
  Italy: { anchor: 'start', dx: 8, dy: 4 },
  Denmark: { anchor: 'end', dx: -8, dy: 0 },
  Switzerland: { anchor: 'end', dx: -8, dy: 12 },
  India: { anchor: 'start', dx: 8, dy: 0 },
  Philippines: { anchor: 'start', dx: 8, dy: 10 },
  Germany: { anchor: 'middle', dx: 0, dy: -12 },
  Spain: { anchor: 'middle', dx: 0, dy: -12 },
  Argentina: { anchor: 'end', dx: -8, dy: 0 },
};

export function valuationChart() {
  // Pearson r, computed here so the caption cannot drift from the data above.
  const n = VALUATION.length;
  const mx = VALUATION.reduce((a, d) => a + d.bigmac, 0) / n;
  const my = VALUATION.reduce((a, d) => a + d.capp, 0) / n;
  const sxy = VALUATION.reduce((a, d) => a + (d.bigmac - mx) * (d.capp - my), 0);
  const sxx = VALUATION.reduce((a, d) => a + (d.bigmac - mx) ** 2, 0);
  const syy = VALUATION.reduce((a, d) => a + (d.capp - my) ** 2, 0);
  const r = sxy / Math.sqrt(sxx * syy);

  const groups = new Map<string, { place: Placement; rows: typeof VALUATION }>();
  for (const d of VALUATION) {
    const place = VAL_PLACEMENT[d.country];
    if (!place) continue;
    const key = `${place.anchor}|${place.dx}|${place.dy}`;
    if (!groups.has(key)) groups.set(key, { place, rows: [] });
    groups.get(key)!.rows.push(d);
  }

  // One domain on both axes, or the 45-degree line would not be at 45 degrees and
  // a point's distance from it would stop meaning what the caption says it means.
  const DOMAIN: [number, number] = [-66, 52];
  const TICKS = [-60, -40, -20, 0, 20, 40];

  return renderPlot(
    {
      width: WIDTH,
      // The plot width plus the vertical margins, so the data area is square and,
      // with the shared domain above, the 45-degree line is drawn at 45 degrees.
      height: WIDTH - 58 - 24 + 10 + 46,
      marginLeft: 58,
      marginRight: 24,
      marginTop: 10,
      marginBottom: 46,
      x: {
        domain: DOMAIN,
        ticks: TICKS,
        tickFormat: (d: number) => (d > 0 ? `+${d}%` : `${d}%`),
        label: 'Big Mac index, July 2026',
        labelAnchor: 'left',
        grid: true,
      },
      y: {
        domain: DOMAIN,
        ticks: TICKS,
        tickFormat: (d: number) => (d > 0 ? `+${d}%` : `${d}%`),
        label: 'Cappuccino XR index',
        labelAnchor: 'top',
        grid: true,
      },
      style: { fontSize: '12px' },
      marks: [
        Plot.line(
          [
            { x: DOMAIN[0], y: DOMAIN[0] },
            { x: DOMAIN[1], y: DOMAIN[1] },
          ],
          { x: 'x', y: 'y', stroke: NEUTRAL, strokeWidth: 1.5, strokeDasharray: '4,3' },
        ),
        Plot.ruleX([0], { stroke: RULE }),
        Plot.ruleY([0], { stroke: RULE }),
        Plot.dot(VALUATION, {
          x: 'bigmac', y: 'capp',
          r: 4, fill: ACCENT, fillOpacity: 0.85,
        }),
        ...[...groups.values()].map(({ place, rows }) =>
          Plot.text(rows, {
            x: 'bigmac', y: 'capp',
            text: 'country',
            fontSize: 11,
            fill: INK_MUTED,
            textAnchor: place.anchor,
            dx: place.dx,
            dy: place.dy,
          }),
        ),
      ],
    },
    `Over- and undervaluation against the US dollar on two indices, 34 countries, correlation ${r.toFixed(2)}`,
  );
}
