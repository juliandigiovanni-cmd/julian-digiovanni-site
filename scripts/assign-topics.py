#!/usr/bin/env python3
"""Assign topic tags to papers. Hand-written mapping -- edit here, re-run."""
import pathlib, re

TOPICS = {
 'a-global-view-of-cross-border-migration': ['migration', 'trade'],
 'buy-big-or-buy-small-procurement-policies-firms-financing-and': ['firm-dynamics', 'banking-credit'],
 'capital-flows-and-the-international-credit-channel': ['international-finance', 'banking-credit'],
 'closing-the-border-the-impact-of-u-s-migration-and-trade': ['migration', 'trade'],
 'country-size-international-trade-and-aggregate-fluctuations-in': ['trade', 'firm-dynamics'],
 'firm-entry-trade-and-welfare-in-zipfs-world': ['trade', 'firm-dynamics'],
 'firms-destinations-and-aggregate-fluctuations': ['firm-dynamics', 'trade'],
 'firms-supply-chain-adaptation-to-carbon-taxes': ['climate', 'supply-chains', 'firm-dynamics'],
 'following-germanys-lead-using-international-monetary-linkages': ['monetary-policy'],
 'foreign-shocks-as-granular-fluctuations': ['firm-dynamics', 'trade'],
 'global-spillovers-of-climate-policy-shocks': ['climate'],
 'global-supply-chain-pressures-international-trade-and': ['supply-chains', 'inflation', 'trade'],
 'income-induced-expenditure-switching': ['international-finance', 'trade'],
 'international-spillovers-and-local-credit-cycles': ['banking-credit', 'international-finance'],
 'is-the-green-transition-inflationary': ['climate', 'inflation'],
 'large-firms-and-international-business-cycle-comovement': ['firm-dynamics', 'trade'],
 'pandemic-era-inflation-drivers-and-global-spillovers': ['inflation', 'supply-chains'],
 'power-laws-in-firm-size-and-openness-to-trade-measurement-and': ['firm-dynamics', 'trade'],
 'putting-the-parts-together-trade-vertical-linkages-and': ['trade', 'supply-chains'],
 'quantifying-the-inflationary-impact-of-fiscal-stimulus-under': ['inflation', 'supply-chains'],
 'remoteness-and-real-exchange-rate-volatility': ['international-finance', 'trade'],
 'stock-market-spillovers-via-the-global-production-network': ['monetary-policy', 'supply-chains'],
 'the-global-welfare-impact-of-china-trade-integration-and': ['trade'],
 'the-gscpi-a-new-barometer-of-global-supply-chain': ['supply-chains'],
 'the-impact-of-foreign-interest-rates-on-the-economy-the-role': ['monetary-policy', 'international-finance'],
 'the-impact-of-u-s-monetary-policy-on-foreign-firms': ['monetary-policy', 'firm-dynamics'],
 'the-micro-origins-of-international-business-cycle-comovement': ['firm-dynamics', 'trade'],
 'the-risk-content-of-exports-a-portfolio-view-of-international': ['trade'],
 'the-welfare-consequences-of-income-induced-expenditure': ['international-finance', 'trade'],
 'trade-openness-and-volatility': ['trade'],
 'trade-uncertainty-and-u-s-bank-lending': ['banking-credit', 'trade'],
 'what-drives-capital-flows-the-case-of-cross-border-m-a': ['international-finance'],
 'what-is-the-evidence-that-trade-uncertainty-affects-us-bank': ['banking-credit', 'trade'],
}

D = pathlib.Path(__file__).resolve().parent.parent / 'src/content/papers'

def main():
    files = {p.stem for p in D.glob('*.md')}
    missing = files - set(TOPICS)
    extra = set(TOPICS) - files
    for slug, topics in TOPICS.items():
        p = D / f'{slug}.md'
        if not p.exists(): continue
        s = p.read_text(encoding='utf-8')
        block = 'topics:\n' + '\n'.join(f'  - "{t}"' for t in topics)
        s = re.sub(r'^topics:.*?(?=^\w|^---)', block + '\n', s, count=1, flags=re.M | re.S)
        p.write_text(s, encoding='utf-8')
    print(f'tagged {len(TOPICS) - len(extra)} papers')
    if missing: print('NO TOPICS ASSIGNED:', *sorted(missing), sep='\n  ')
    if extra: print('SLUG NOT FOUND:', *sorted(extra), sep='\n  ')

if __name__ == '__main__':
    main()
