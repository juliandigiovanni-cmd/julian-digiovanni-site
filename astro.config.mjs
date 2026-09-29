// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Static output only. The build produces a plain dist/ that GitHub Pages serves
// as-is -- no server, no adapter, no host-specific features. It went to the
// Bluehost docroot the same way before, which is why the move needed no change
// here. .github/workflows/deploy.yml does the build and the publish.
export default defineConfig({
  site: 'https://julian.digiovanni.ca',
  // The host serves /research/ -> /research/index.html (Apache did, and Pages
  // does), so directory-style URLs are correct here and keep the old WordPress
  // paths working.
  build: { format: 'directory' },
  trailingSlash: 'ignore',
  // Emits /sitemap-index.xml and /sitemap-0.xml, which public/robots.txt points
  // at. The WordPress site had both; search engines were crawling without them
  // between the cutover and this being added.
  integrations: [sitemap()],
});
