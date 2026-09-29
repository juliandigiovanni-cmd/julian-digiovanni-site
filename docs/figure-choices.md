# Key figures — decided against

A figure per paper was one of the agreed hooks and was built: schema fields, a rendering
slot in `PaperEntry.astro`, styles, and one live example on *Trade Uncertainty and U.S.
Bank Lending*.

**Julian removed it after seeing it in place:** *"putting figures in would make the page
too crowded."* Fair — by then each entry already carried a rail, title, authors, venue,
takeaway (itself since removed), an abstract toggle, links and sometimes a press row.
A chart on top of that is one element too many.

So the support is gone, not just the image. Leaving `figure:` in the schema with no renderer
would have been a trap for whoever set it next.

## What was removed

- `figure` / `figureCaption` / `figureSource` from `src/content.config.ts`
- the `<figure>` block from `src/components/PaperEntry.astro`
- `.pub__figure` rules from `src/styles/base.css`
- `src/assets/figures/trade-uncertainty-index.png`

## If it is ever wanted again

The figure that was used, and why it was chosen: the **trade uncertainty index, 2002–2019**,
from `~/Dropbox/Research/BanksTradeUncertainty/voxinvite/voxeu_figure1.png` — Figure 1 of the
VoxEU column "Banks' responses to trade uncertainty", March 2024. It shows the identifying
variation directly: flat for sixteen years, then a spike through the 2018–19 trade war. 1223×890,
legible at 440px.

Other candidates surveyed, in `~/Dropbox/Apps/Overleaf/Fragmentation/figures/` —
`Inflation_decomp_US3.png`, `Inflation_decomp_EA3.png`, `supply_demand_constrained.png`,
`network.png`. These were **never used**, because the Overleaf project name does not map onto
a paper title and several papers share an inflation-decomposition exercise. Attaching a
figure to the wrong paper is worse than having none.

A better home for a chart, if one is wanted, is the Coffee page, where a figure is the point
rather than an addition.

**That is what happened.** The Coffee page now carries one — the coffee supply chain
split by stage — rendered to SVG at build time rather than shipped as an image. See
`docs/coffee-figures.md` for it, for the three candidates that were cut, and for the
data sources behind all four.
