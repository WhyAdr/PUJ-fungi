#!/usr/bin/env python3
"""Extract full BGC inventories for TA-PUJ and AF-PUJ from antiSMASH 8.0.4 outputs.

Parses .region*.gbk and knownclusterblast/*_c*.txt to build auditable,
100% data-derived tables for Section 7 of the review.
"""
from Bio import SeqIO
import glob
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_kcb_file(kcb_path):
    """Parse KnownClusterBlast results file."""
    if not os.path.exists(kcb_path):
        return []

    with open(kcb_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if "Significant hits:" not in content:
        return []

    hits = []
    # Find all hit details blocks: >> \n \d+\. (BGC\d+\.\d+)
    blocks = re.split(r"\n>>\s*\n\d+\.\s*", content)
    for block in blocks[1:]:  # first block is header/query table
        lines = block.strip().split("\n")
        bgc_id = lines[0].strip()
        source = ""
        btype = ""
        n_prot = 0
        score = 0.0

        for line in lines[1:10]:
            if line.startswith("Source:"):
                source = line.split("Source:", 1)[1].strip()
            elif line.startswith("Type:"):
                btype = line.split("Type:", 1)[1].strip()
            elif line.startswith("Number of proteins with BLAST hits to this cluster:"):
                n_prot = int(line.split(":", 1)[1].strip())
            elif line.startswith("Cumulative BLAST score:"):
                score = float(line.split(":", 1)[1].strip())

        # Parse table of BLAST hits for identity range
        hits_matches = re.findall(
            r"PUJ_\d+\t[^\t]+\t(\d+)\t[0-9.]+\t[0-9.]+\t[0-9.e-]+", block
        )
        identities = [int(x) for x in hits_matches] if hits_matches else []
        id_str = f"{min(identities)}–{max(identities)}%" if identities else "—"
        max_id = max(identities) if identities else 0

        hits.append(
            {
                "bgc": bgc_id,
                "compound": source,
                "type": btype,
                "n_prot": n_prot,
                "score": score,
                "id_range": id_str,
                "max_id": max_id,
            }
        )

    return hits


def assign_confidence(top_hit):
    """Assign confidence tier according to review definition:

    HIGH: >=5 gene hits AND >=80% max identity
    MEDIUM: 2-4 gene hits OR 50-79% identity
    LOW: 1 gene hit OR <50% identity
    ORPHAN: No hits
    """
    if not top_hit:
        return "ORPHAN"
    n_prot = top_hit["n_prot"]
    max_id = top_hit["max_id"]
    if n_prot >= 5 and max_id >= 80:
        return "HIGH"
    elif n_prot >= 2 or max_id >= 50:
        return "MEDIUM"
    else:
        return "LOW"


def extract_inventory():
    inventory = {"TA": [], "AF": []}

    targets = [
        ("TA", os.path.join(BASE_DIR, "fungiSMASH-TA")),
        ("AF", os.path.join(BASE_DIR, "fungiSMASH-AF")),
    ]

    for iso, folder in targets:
        gbks = glob.glob(os.path.join(folder, "*region*.gbk"))
        # Sort naturally by scaffold/contig and region number
        def sort_key(p):
            base = os.path.basename(p)
            m = re.match(r"^(.*?)\.region(\d+)\.gbk$", base)
            scaff, reg = m.groups()
            scaff_num = int(re.sub(r"\D", "", scaff)) if re.search(r"\d", scaff) else 0
            return (scaff_num, scaff, int(reg))

        gbks = sorted(gbks, key=sort_key)

        for p in gbks:
            base = os.path.basename(p)
            m = re.match(r"^(.*?)\.region(\d+)\.gbk$", base)
            scaff, reg_num = m.groups()
            kcb_name = f"{scaff}_c{int(reg_num)}.txt"
            kcb_path = os.path.join(folder, "knownclusterblast", kcb_name)

            rec = SeqIO.read(p, "genbank")
            region_feat = next((f for f in rec.features if f.type == "region"), None)
            rtype = (
                region_feat.qualifiers.get("product", ["unknown"])[0]
                if region_feat
                else "unknown"
            )
            start_coord = int(region_feat.location.start) + 1 if region_feat else 1
            end_coord = int(region_feat.location.end) if region_feat else len(rec)
            reg_len = end_coord - start_coord + 1

            hits = parse_kcb_file(kcb_path)
            top_hit = hits[0] if hits else None
            tier = assign_confidence(top_hit)

            inventory[iso].append(
                {
                    "region_id": f"{scaff}_c{int(reg_num)}",
                    "scaffold": scaff,
                    "region_num": int(reg_num),
                    "start": start_coord,
                    "end": end_coord,
                    "length": reg_len,
                    "type": rtype,
                    "top_hit": top_hit,
                    "secondary_hits": hits[1:3] if len(hits) > 1 else [],
                    "confidence": tier,
                }
            )

    print(f"Parsed {len(inventory['TA'])} TA regions and {len(inventory['AF'])} AF regions.")

    out_json = os.path.join(BASE_DIR, "bgc_inventory.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2)
    print(f"Saved inventory JSON to {out_json}")
    return 0


if __name__ == "__main__":
    sys.exit(extract_inventory())
