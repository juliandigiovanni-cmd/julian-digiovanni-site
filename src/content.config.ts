import { defineCollection, reference, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * Every "hook" field is optional. Entries are bootstrapped from the CV parser
 * with only title/citation/section populated, then enriched by hand over time --
 * a half-filled entry must render correctly, not break the build. What IS
 * required is the minimum needed to display an honest citation.
 */
const link = z.object({
  label: z.string(),
  // Either an absolute URL, or a root-relative path for a file we host -- the
  // replication archives live at /Papers/ beside the PDFs, and hard-coding the
  // domain into content files would have to be rewritten if it ever changed.
  // Mirrors how `pdf` below is already expressed.
  url: z.union([z.string().url(), z.string().startsWith('/')]),
});

const papers = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/papers' }),
  schema: z.object({
    title: z.string(),
    coauthors: z.array(z.string()).default([]),
    section: z.enum(['working-paper', 'peer-reviewed', 'other-research']),
    status: z.enum([
      'working-paper',
      'r-and-r',
      'conditionally-accepted',
      'forthcoming',
      'published',
    ]),

    // Display citation. Always correct -- this is what renders.
    citation: z.string().optional(),
    // Best-effort structured fields, used only for sorting and filtering.
    journal: z.string().optional(),
    year: z.number().int().min(1990).max(2100).optional(),
    // Working-paper series. `url` where the live site linked a landing page.
    series: z.array(z.object({ label: z.string(), url: z.string().url().optional() })).default([]),
    // Version marker carried on the live site, e.g. "Mar26".
    version: z.string().optional(),
    // Coauthor name -> homepage, scraped from the live site. Names without an
    // entry render as plain text.
    coauthorUrls: z.record(z.string(), z.string().url()).default({}),

    pdf: z.string().startsWith('/').optional(),
    url: z.string().url().optional(),
    doi: z.string().optional(),

    // --- the extras ---
    abstract: z.string().optional(),
    topics: z.array(z.string()).default([]),
    appendix: z.string().optional(),
    dataCode: z.array(link).default([]),
    nonTechnical: z.array(link).default([]),
    press: z.array(link).default([]),

    featured: z.boolean().default(false),
    featuredOrder: z.number().int().optional(),
  }),
});

const writing = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/writing' }),
  schema: z.object({
    title: z.string(),
    outlet: z.enum(['liberty-street', 'voxeu', 'other']),
    outletName: z.string(),
    date: z.coerce.date(),
    url: z.string().url(),
    coauthors: z.array(z.string()).default([]),
    // The paper this piece explains. A reference(), not a string, so a bad
    // slug fails the build instead of rendering a dead cross-link.
    paper: reference('papers').optional(),
    topics: z.array(z.string()).default([]),
  }),
});

export const collections = { papers, writing };
