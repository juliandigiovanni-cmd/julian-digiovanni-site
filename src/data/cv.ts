/**
 * The CV, transcribed once from ~/Dropbox/CV/cv_diGiovanni.tex (September 2026).
 *
 * Transcribed rather than parsed: six of the sixteen .tex sections are prose held
 * together with \phantom{} spacing hacks and \\ line breaks, which are typesetting
 * scaffolding for the PDF and carry no structure. A build-time parser would be
 * fragile exactly where the LaTeX is ugliest.
 *
 * When the .tex changes, run `npm run cv:check`. It diffs the .tex against
 * data/cv-source.json and names the sections that moved, so this file gets
 * updated deliberately rather than drifting in silence.
 *
 * Publications live in src/content/papers/ and render on /research/. The
 * seminars, conferences and discussant lists stay in the PDF by choice.
 */

export const cv = {
  pdf: '/cv_diGiovanni.pdf',
  pdfDate: 'September 2026',

  current: [
    { years: '2025–', role: 'Economic Research Advisor', org: "International Studies, Research & Statistics Group, Federal Reserve Bank of New York" },
    { years: '2022–', role: 'Adjunct Professor of Economics', org: 'Columbia University' },
  ],

  previous: [
    {
      institution: 'Federal Reserve Bank of New York, Research & Statistics Group',
      roles: [
        { years: '2022–2024', role: 'Department Head', detail: 'Climate Risk Studies' },
        { years: '2019–2022', role: 'Assistant Vice President', detail: 'International Studies' },
      ],
    },
    {
      institution: 'Universitat Pompeu Fabra, Barcelona School of Economics and CREI',
      roles: [
        { years: '2017–2021', role: 'ICREA Research Professor', detail: 'Dept. of Economics & Business, UPF' },
        { years: '2015–2017', role: 'Professor of Economics', detail: 'UPF' },
        { years: '2013–2015', role: 'Associate Professor of Economics', detail: 'UPF' },
        { years: '2015–2021', role: 'Research Professor', detail: 'BSE' },
        { years: '2016–2019', role: 'Deputy Director for Research', detail: 'BSE' },
        { years: '2013–2015', role: 'Affiliated Professor', detail: 'BSE' },
        { years: '2013–2021', role: 'Research Associate', detail: 'CREI' },
      ],
    },
    {
      institution: 'University of Toronto',
      roles: [
        { years: '2011–2012', role: 'Visiting Assistant Professor', detail: 'Department of Economics' },
      ],
    },
    {
      institution: 'International Monetary Fund',
      roles: [
        { years: '2006–2013', role: 'Economist', detail: 'Research Department (on leave 09/11–08/12)' },
        { years: '2004–2006', role: 'Economist Program (EP)', detail: 'Research and Middle East Departments' },
      ],
    },
  ],

  education: [
    {
      years: '1998–2004',
      degree: 'Ph.D., Economics',
      institution: 'University of California, Berkeley, USA',
      detail: [
        '“Essays on International Capital Flows, Exchange Rates and Monetary Policy”',
        'Advisors: Professors Maurice Obstfeld, Barry Eichengreen, Andrew K. Rose',
      ],
    },
    {
      years: '1994–1998',
      degree: 'B.A., Economics and Finance',
      institution: 'McGill University, Canada',
      detail: ['First class joint-honours, minor in Mathematics'],
    },
  ],

  affiliations: [
    { years: '2025–', role: 'Member', org: 'Institutional and Corporate Council, Barcelona School of Economics' },
    { years: '2019–', role: 'Co-Director', org: 'International Trade and Macroeconomics program, CEBRA' },
    { years: '2013–', role: 'Research Fellow', org: 'CEPR' },
  ],

  grants: [
    { years: '2018–2020', text: 'Ministerio de Ciencia, Innovación y Universidades, “Heterogeneidad microeconomica, fluctuaciones agregadas y politicas macroeconomica,” Project ECO2017-82596-P (PI; 66,650€)' },
    { years: '2017–2022', text: 'European Research Council Consolidator Grant, “Global Production Networks and Macroeconomic Interdependence,” ERC-2016-COG, Project 726168 (PI; 1,381,250€)' },
    { years: '2017', text: 'Becas Leonardo a Investigadores y Creadores Culturales, Fundación BBVA, “Proyectos públicos, financiación empresarial y productividad agregada” (PI; 39,530€)' },
    { years: '2014–2016', text: 'Marie Curie Actions–International Incoming Fellowships, “Firms, International Trade, and Aggregate Fluctuations,” FP7-PEOPLE-2013-IIF, Project 622959 (PI; 223,002€)' },
    { years: '2005–2007', text: 'Internal IMF Research Grants' },
    { years: '2003', text: 'Summer Intern, IF Division, Board of Governors of the Federal Reserve System' },
    { years: '2003', text: 'Academic Progress Award, U.C. Berkeley' },
    { years: '2001', text: 'Clausen Center Research Grant, U.C. Berkeley' },
    { years: '2001', text: 'Institute of Business and Economic Research Mini-Grant Award, U.C. Berkeley' },
    { years: '2000–2002', text: 'Social Science and Humanities Research Council Fellowship, Canada' },
    { years: '1998–2003', text: "Fonds pour la Formation de Chercheurs et l'Aide à la Recherche Fellowship, QC, Canada" },
    { years: '1998–1999', text: 'Block Grant Fellowship, Department of Economics, U.C. Berkeley' },
  ],

  teaching: [
    { years: '2022–', institution: 'Columbia University', courses: ["Macroeconomic Analysis I (Master's)"] },
    { years: '2014–2019', institution: 'Universitat Pompeu Fabra and Barcelona School of Economics', courses: ['Topics in Macroeconomics (PhD)', "Macroeconomics (Master's)", 'International Economics II (Undergraduate)', 'Topics in Macroeconomics (Undergraduate)'] },
    { years: '2011–2012', institution: 'Department of Economics, University of Toronto', courses: ["International Financial Markets (Master's)", 'International Monetary Economics (Undergraduate)'] },
  ],

  summerSchools: [
    { years: '2014–2018', text: 'CREI-BSE Barcelona Macroeconomics Summer School' },
    { years: '2014', text: 'Brixen Workshop & Summer School on International Trade and Finance' },
  ],

  miniPhd: [
    { years: '2018', text: 'University of Hong Kong, McGill University' },
  ],

  service: {
    editorial: [
      { org: 'FRBNY Economic Policy Review', role: 'Editor', years: '2020–present' },
      { org: 'Journal of International Economics', role: 'Associate editor', years: '2016–2021' },
      { org: 'Economic Policy', role: 'Panel member', years: '2014–2016' },
    ],
    policy: [
      { org: 'FRBNY', role: 'Member of Priority Leadership Team on Climate Change', years: '2021–2024' },
      { org: 'FRBNY', role: 'Member of Judgmental Forecasting Team (International Trade)', years: '2020–2022' },
    ],
    university: [
      { org: 'UPF', role: 'Junior Recruiting Chair', years: '2014–2018' },
      { org: 'UPF', role: 'Tenure Sub-Committee Chair', years: '2015–2016' },
    ],
    conferences: [
      'CEBRA ITM Program Annual Conference (2020–24), Scientific Program Committee',
      '33rd Annual Congress of the European Economic Association (2018), Scientific Program Committee',
      '12th Annual Meeting of the Portuguese Economic Journal (2018), Scientific Program Committee',
      '42nd Spanish Economic Association Meeting (2017), Local Committee Chair',
      'European Winter Meetings of the Econometric Society (2017), Local Committee Chair',
      '“Rethinking Competitiveness, Structural Reforms, and Macro Policy” Conference, Bank of Italy-CEPR-CEBR (2017), Co-Organizer',
      '“Firms in the Global Economy” Workshop, Barcelona GSE Summer Forum (2014–23), Co-Organizer',
      '31st Annual Congress of the European Economic Association (2016), Scientific Program Committee',
      '9th Annual Meeting of the Portuguese Economic Journal (2015), Scientific Program Committee',
      'IMF Research Department (2010–11), Seminar Committee Chair',
      '8th Jacques Polak IMF Annual Research Conference (2007), Committee Member',
    ],
    grantReviewer: 'National Science Foundation (USA), European Research Council, Fonds recherche Québec-société et culture (FRQSC, Canada), Methusalem Program (KULeuven, Belgium), Agencia Estatal de Investigación (Ministerio de Ciencia, Innovación y Universidades, Spain)',
    referee: 'American Economic Journal: Macroeconomics, American Economic Review, American Economic Review: Insights, B.E. Journal of Macroeconomics, Canadian Journal of Economics, Econometrica, Economic Journal, Economica, Economic Policy, IMF Economic Review, Journal of Applied Econometrics, Journal of Comparative Economics, Journal of Development Economics, Journal of the European Economic Association, Journal of International Economics, Journal of International Money and Finance, Journal of Money Credit and Banking, Journal of Monetary Economics, Journal of Political Economy, Japan and the World Economy, Macroeconomic Dynamics, Pacific Economic Review, Quarterly Journal of Economics, Quarterly Review of Economics and Finance, Review of Economic Dynamics, Review of Economics and Statistics, Review of Economic Studies, Review of International Economics, Review of World Economics/Weltwirtschafliches Archiv, Scandinavian Journal of Economics, World Economy',
  },

  discussions: [
    'Discussion of Johannes Van Biesebroeck, Jozef Konings, and Christian Volpe Martincus, “Did export promotion help firms weather the crisis?” <em>Economic Policy</em>, 31:88 (October 2016), 691–693.',
    'Discussion of Michael Brei and Leonardo Gambacorta, “Are bank capital ratios pro-cyclical? New evidence and perspectives” <em>Economic Policy</em>, 31:86 (April 2016), 398–399.',
    'Discussion of Kyuil Chung, Jong-Eun Lee, Elena Loukoianova, Hail Park, and Hyun Song Shin, “Global liquidity through the lens of monetary aggregates” <em>Economic Policy</em>, 30:82 (April 2015), 278–281.',
  ],

  shortTermVisits:
    '2025: Bank of England · 2018: University of Hong Kong, Federal Reserve Bank of New York, McGill University · 2017: Bank of England · 2016: IMF Research Department · 2014: MITRE Visiting Scholar, University of Michigan; Central Bank of the Republic of Turkey · 2010: CREI · 2008: Banque de France',

  other: {
    citizenship: 'Canada, Italy, United States',
    languages: 'English (native), French (fluent), Spanish (beginner-intermediate)',
  },
} as const;
