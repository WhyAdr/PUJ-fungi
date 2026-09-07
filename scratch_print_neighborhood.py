"""
scratch_print_neighborhood.py
Reads neighborhood_ta.json and neighborhood_af.json and prints clean summaries
to standard output or neighborhood_summary.txt.
"""

import json

def print_neighborhood(json_file, label, out_handle=None):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"\n==========================================", file=out_handle)
    print(f"=== {label} GENE NEIGHBORHOODS ===", file=out_handle)
    print(f"==========================================", file=out_handle)
    for target, info in data.items():
        print(f"\n>>> TARGET: {target} on {info['contig']} (Gene {info['target_idx']+1} of {info['total_genes_on_contig']} on contig) <<<", file=out_handle)
        print(f"{'Rel':<4} | {'Locus Tag':<11} | {'Gene':<8} | {'Str':<3} | {'AA':<5} | {'Product':<35} | {'Key Annotation / Pfam / EC'}", file=out_handle)
        print("-" * 110, file=out_handle)
        for g in info['flanking']:
            rel = f"{g['index_rel']:+d}" if g['index_rel'] != 0 else "TARGET"
            mark = "*" if g['is_target'] else " "
            str_strand = "+" if g['strand'] == 1 else "-"
            # Extract key annotation
            desc = ""
            if g.get('ec'):
                desc += f"EC:{g['ec']} "
            if g.get('db_xref'):
                pfams = [x for x in g['db_xref'] if 'PFAM:' in x]
                if pfams:
                    desc += f"{','.join(pfams[:2])} "
            if not desc and g.get('note'):
                desc = g['note'][0][:45]
            print(f"{mark}{rel:<3} | {g['locus_tag']:<11} | {g['gene']:<8} | {str_strand:<3} | {g['length_aa']:<5} | {g['product'][:35]:<35} | {desc}", file=out_handle)

if __name__ == "__main__":
    with open("neighborhood_summary.txt", "w", encoding="utf-8") as out:
        print_neighborhood("neighborhood_ta.json", "TRICHODERMA ASPERELLUM (TA-PUJ)", out_handle=out)
        print_neighborhood("neighborhood_af.json", "ASPERGILLUS FLAVUS (AF-PUJ)", out_handle=out)
    print("Wrote neighborhood_summary.txt successfully!")
