"""
inspect_neighborhoods.py
Generates a structured tabular text report (neighborhoods_clean.txt)
highlighting relative distance (-10 to +10), strand, protein length,
gene symbol, Pfam domains, EC numbers, and product description.
"""

import json

def generate_report():
    lines = []
    for fn, name in [('neighborhood_ta.json', 'TA-PUJ'), ('neighborhood_af.json', 'AF-PUJ')]:
        with open(fn, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for target, info in data.items():
            lines.append('=' * 95)
            lines.append(f"[{name}] TARGET: {target} on Contig/Scaffold {info['contig']} (Index {info['target_idx']+1}/{info['total_genes_on_contig']})")
            lines.append('=' * 95)
            lines.append(f"{'Rel':>7} | {'Locus Tag':<11} | {'Str':<3} | {'AA':<6} | {'Gene':<8} | {'Pfam':<17} | {'EC':<11} | {'Product'}")
            lines.append('-' * 95)
            for g in info['flanking']:
                rel = f"{g['index_rel']:+d}" if g['index_rel'] != 0 else "TARGET"
                tag = g['locus_tag']
                strnd = '+' if g['strand'] == 1 else '-'
                aa = f"{g['length_aa']}aa"
                gene = g['gene'] if g['gene'] else '-'
                prod = g['product']
                pf = [x.split(':')[1] for x in g.get('db_xref', []) if x.startswith('PFAM:')]
                pf_str = ','.join(pf[:2]) if pf else '-'
                ec = ','.join(g.get('ec', [])) if g.get('ec') else '-'
                lines.append(f"{rel:>7} | {tag:<11} | {strnd:<3} | {aa:<6} | {gene:<8} | {pf_str:<17} | {ec:<11} | {prod}")
            lines.append("")
    
    with open('neighborhoods_clean.txt', 'w', encoding='utf-8') as out:
        out.write('\n'.join(lines))
    print("Wrote neighborhoods_clean.txt successfully!")

if __name__ == '__main__':
    generate_report()
