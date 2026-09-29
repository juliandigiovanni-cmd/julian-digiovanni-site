import * as Plot from '@observablehq/plot';
import { parseHTML } from 'linkedom';

/**
 * Render an Observable Plot spec to an SVG string at build time.
 *
 * The site ships no client-side JavaScript for figures. Plot normally needs a
 * DOM, so linkedom supplies a detached one and we take the markup back out.
 * The result is inlined into the page: no runtime library, no hydration, and
 * the chart is in the HTML for anything that reads it without running scripts.
 *
 * Colours come from the palette as literal values rather than var(--accent),
 * because Plot writes them into presentation attributes on individual marks
 * where a custom property would not resolve in every context. Keep them in
 * step with src/styles/theme.css.
 */
export const INK = '#1b2b3d';
export const INK_MUTED = '#45566a';
export const INK_FAINT = '#64758a';
export const RULE = '#dde4ec';
export const ACCENT = '#0b4f9e';
/** The recessive partner in every two-series figure. See the emphasis note below. */
export const NEUTRAL = '#8fa0b4';
/**
 * Stages of one supply chain are an ordered category, so they take a
 * single-hue ramp rather than five separate identities: dark at the farm,
 * light at the shelf. Checked with the dataviz validator in --ordinal mode --
 * monotone lightness, adjacent gaps over 0.06, light end clear of the surface,
 * hue spread 8 degrees. The site accent is the second step.
 */
export const CHAIN = ['#06305f', '#0b4f9e', '#2f6cb2', '#5b8cc6', '#8caed4'];

const FONT =
  '-apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, "Helvetica Neue", Arial, sans-serif';

export function renderPlot(options: Plot.PlotOptions, title: string): string {
  const { document } = parseHTML('<!doctype html><html><body></body></html>');
  const node = Plot.plot({
    ...options,
    document,
    style: { fontFamily: FONT, background: 'transparent', color: INK_MUTED, ...(options.style as object) },
  });
  const svg = node.tagName.toLowerCase() === 'svg' ? node : node.querySelector('svg');
  if (!svg) throw new Error('Plot returned no SVG');

  // Scale to the container rather than sitting at a fixed pixel width, so the
  // figure behaves at 375px like every other block on the page.
  svg.removeAttribute('width');
  svg.removeAttribute('height');
  svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-label', title);
  svg.style.maxWidth = '100%';
  svg.style.height = 'auto';
  // Deliberately NOT overflow:visible. Direct labels sit outside the plot area
  // but inside the viewBox -- that is what the right margin is for -- and
  // letting the SVG paint outside its box widens the whole document at 375px.

  return (node.tagName.toLowerCase() === 'svg' ? svg.outerHTML : node.outerHTML);
}
