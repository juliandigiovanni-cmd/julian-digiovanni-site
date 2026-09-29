export const site = {
  name: 'Julian di Giovanni',
  url: 'https://julian.digiovanni.ca',
  title: 'Julian di Giovanni',
  description:
    'Economic Research Advisor at the Federal Reserve Bank of New York. Research on international spillovers and macroeconomic fluctuations.',
  email: 'juliandigiovanni@gmail.com',

  nav: [
    { url: '/', label: 'Home' },
    { url: '/research/', label: 'Research' },
    { url: '/policy-writing/', label: 'Policy Writing' },
    { url: '/coffee/', label: 'Coffee' },
    { url: '/cv/', label: 'CV' },
  ],

  roles: [
    { label: 'Economic Research Advisor, Research and Statistics Group', org: 'Federal Reserve Bank of New York', url: 'https://www.newyorkfed.org/research/economists/digiovanni' },
    { label: 'Research Fellow', org: 'CEPR', url: 'https://www.cepr.org/' },
    { label: 'Co-Director, International Trade and Macroeconomics', org: 'CEBRA', url: 'https://cebra.org/programs/itm/' },
    { label: 'Adjunct Professor of Economics', org: 'Columbia University', url: 'https://econ.columbia.edu/' },
  ],

  profiles: [
    { label: 'Google Scholar', url: 'https://scholar.google.com/citations?user=paYBFFcAAAAJ&hl=en' },
    { label: 'IDEAS/RePEc', url: 'https://ideas.repec.org/e/pdi67.html' },
    { label: 'New York Fed', url: 'https://www.newyorkfed.org/research/economists/digiovanni' },
  ],

  /** The disclaimer every Fed economist's personal site needs. */
  disclaimer:
    'Views expressed here are my own and do not necessarily reflect the position of the Federal Reserve Bank of New York or the Federal Reserve System.',
} as const;


export const sectionLabel: Record<string, string> = {
  'working-paper': 'Working Papers',
  'peer-reviewed': 'Peer-Reviewed Publications',
  'other-research': 'Other Research Publications',
};

/** Display labels for topic tags. Order here is the order of the filter bar. */
export const topicLabel: Record<string, string> = {
  'supply-chains': 'Supply chains',
  climate: 'Climate',
  inflation: 'Inflation',
  'monetary-policy': 'Monetary policy',
  'banking-credit': 'Banking & credit',
  'firm-dynamics': 'Firms & granularity',
  trade: 'Trade',
  'international-finance': 'International finance',
  migration: 'Migration',
};

