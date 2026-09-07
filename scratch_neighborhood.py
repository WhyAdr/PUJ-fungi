"""
scratch_neighborhood.py
Extracts gene neighborhoods (flanking window of ±10 genes) for key functional loci
from Funannotate GenBank files of Trichoderma asperellum (TA-PUJ) and Aspergillus flavus (AF-PUJ).
Outputs neighborhood_ta.json and neighborhood_af.json.
"""

import json
import os
from Bio import SeqIO

def extract_neighborhoods(gbk_path, target_loci, window=10):
    print(f"Loading {gbk_path}...")
    # Map contig/record ID -> list of CDS features
    contig_cds = {}
    
    # We parse records
    for record in SeqIO.parse(gbk_path, "genbank"):
        cds_list = []
        for feat in record.features:
            if feat.type == "CDS":
                qual = feat.qualifiers
                locus_tag = qual.get("locus_tag", [""])[0]
                gene = qual.get("gene", [""])[0]
                product = qual.get("product", ["hypothetical protein"])[0]
                prot_id = qual.get("protein_id", [""])[0]
                ec = qual.get("EC_number", qual.get("ec_number", []))
                db_xref = qual.get("db_xref", [])
                note = qual.get("note", [])
                
                # Length in aa
                trans = qual.get("translation", [""])[0]
                length_aa = len(trans) if trans else int(len(feat.location) / 3)
                
                cds_info = {
                    "locus_tag": locus_tag,
                    "gene": gene,
                    "product": product,
                    "protein_id": prot_id,
                    "ec": ec,
                    "db_xref": db_xref,
                    "note": note,
                    "length_aa": length_aa,
                    "start": int(feat.location.start),
                    "end": int(feat.location.end),
                    "strand": feat.location.strand,
                    "contig": record.id
                }
                cds_list.append(cds_info)
        if cds_list:
            contig_cds[record.id] = cds_list

    print(f"Loaded {len(contig_cds)} contigs with CDS features.")

    # Find each target
    results = {}
    for target in target_loci:
        found = False
        for cid, cds_list in contig_cds.items():
            for idx, c in enumerate(cds_list):
                if c["locus_tag"] == target or (c["gene"] and c["gene"].lower() == target.lower()):
                    found = True
                    start_idx = max(0, idx - window)
                    end_idx = min(len(cds_list), idx + window + 1)
                    flanking = cds_list[start_idx:end_idx]
                    
                    # annotate relative position
                    flanking_annot = []
                    for f in flanking:
                        f_copy = dict(f)
                        f_copy["index_rel"] = cds_list.index(f) - idx
                        f_copy["is_target"] = (f["locus_tag"] == c["locus_tag"])
                        flanking_annot.append(f_copy)
                        
                    results[target] = {
                        "target_locus": c["locus_tag"],
                        "target_gene": c["gene"],
                        "contig": cid,
                        "target_idx": idx,
                        "total_genes_on_contig": len(cds_list),
                        "window": window,
                        "flanking": flanking_annot
                    }
                    break
            if found:
                break
        if not found:
            print(f"Warning: target '{target}' not found!")

    return results

if __name__ == "__main__":
    ta_targets = [
        "PUJ_004816", # Tas-acdS (ACC Deaminase)
        "PUJ_005301", # TATC6 (Terpene Cyclase 6)
        "PUJ_004623", # CHT2_2 (Chitinase 2)
        "PUJ_001678", # FET3 (Ferroxidase)
        "PUJ_003670", # Metachelin NRPS
        "PUJ_003355", # Destruxin PKS
        "PUJ_004657", # Siderophore NRPS
    ]
    ta_gbk = r"D:\W\fungi-PUJ\fungiSMASH-TA\Funannotate-annotated-genome-TA.gbk"
    ta_results = extract_neighborhoods(ta_gbk, ta_targets, window=10)
    with open("neighborhood_ta.json", "w", encoding="utf-8") as f:
        json.dump(ta_results, f, indent=2)
    print("Saved neighborhood_ta.json")

    af_targets = [
        "PUJ_009393", # aflR (Aflatoxin master regulator)
        "PUJ_004419", # IucA_IucC (Aerobactin-like siderophore synthetase)
        "PUJ_005557", # PHO2 (Homeodomain TF)
        "PUJ_009297", # PHO81 (Phosphate sensor / CDK-I)
        "PUJ_000724", # Xaa-Pro aminopeptidase / PHO13 neighborhood
    ]
    af_gbk = r"D:\W\fungi-PUJ\fungiSMASH-AF\Funannotate-annotated-genome-AF.gbk"
    af_results = extract_neighborhoods(af_gbk, af_targets, window=10)
    with open("neighborhood_af.json", "w", encoding="utf-8") as f:
        json.dump(af_results, f, indent=2)
    print("Saved neighborhood_af.json")
