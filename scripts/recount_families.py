#!/usr/bin/env python3
"""Recount enzyme families from raw GBK db_xref qualifiers (PFAM: prefix-safe).

Single source of truth for Section 1 Master Validation Matrix numbers in
agriculture-support-biocontrol-fungal-isolate-review.md (AGRI-BIOCONTROL-GENOMIC-SCRUTINY-V6).
"""
from Bio import SeqIO
import json
import os
import sys

# Repo-relative default paths with fallbacks
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENOMES = {
    "TA": os.path.join(BASE_DIR, "fungiSMASH-TA", "input", "Funannotate-annotated-genome-TA.gbk"),
    "AF": os.path.join(BASE_DIR, "fungiSMASH-AF", "Funannotate-annotated-genome-AF.gbk"),
}

# Family definitions: family_name -> (pfam_set, ec_set, interpro_set)
FAMILIES = {
    "chitinase_GH18": ({"PF00704"}, {"3.2.1.14"}, {"IPR001223"}),
    "chitosanase_GH75": ({"PF03240"}, {"3.2.1.132"}, {"IPR004840"}),
    "GST": (
        {"PF02798", "PF00043", "PF13409", "PF14497"},
        {"2.5.1.18"},
        {"IPR004045", "IPR004046", "IPR010981"},
    ),
    "laccase_CuOx": ({"PF00394", "PF07731"}, {"1.10.3.2"}, {"IPR001117"}),
    "P450": ({"PF00067"}, set(), {"IPR001128", "IPR002401"}),
    "ACC_deaminase_family": ({"PF00291"}, {"3.5.99.7"}, {"IPR005965"}),
    "terpene_cyclase": ({"PF19086", "PF03936"}, set(), {"IPR008949", "IPR034686"}),
    "nitrilase_family": ({"PF02979"}, {"3.5.5.1"}, {"IPR003010"}),
}

EXPECTED = {
    "TA": {
        "chitinase_GH18": 14,
        "chitosanase_GH75": 7,
        "GST": 18,
        "laccase_CuOx": 7,
        "P450": 25,
        "ACC_deaminase_family": 6,
        "terpene_cyclase": 7,
        "nitrilase_family": 4,
    },
    "AF": {
        "chitinase_GH18": 17,
        "chitosanase_GH75": 18,
        "GST": 24,
        "laccase_CuOx": 11,
        "P450": 154,
        "ACC_deaminase_family": 16,
        "terpene_cyclase": 21,
        "nitrilase_family": 7,
    },
}


def norm(x):
    """Normalize db_xref tags: PFAM:PF00704 -> PF00704, InterPro:IPR001223 -> IPR001223."""
    return x.split(":")[-1] if ":" in x and not x.startswith("EC") else x


def count_families():
    out = {}
    detailed_loci = {}
    for iso, path in GENOMES.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"Genome artifact not found: {path}")
        counts = {f: set() for f in FAMILIES}
        for rec in SeqIO.parse(path, "genbank"):
            for feat in rec.features:
                if feat.type != "CDS":
                    continue
                q = feat.qualifiers
                tags = set(q.get("db_xref", [])) | set(q.get("EC_number", []))
                normed = {norm(x) for x in tags}
                locus = q.get("locus_tag", ["?"])[0]
                for fam, (pfs, ecs, iprs) in FAMILIES.items():
                    if normed & (pfs | ecs | iprs):
                        counts[fam].add(locus)
        out[iso] = {f: len(s) for f, s in counts.items()}
        detailed_loci[iso] = {f: sorted(list(s)) for f, s in counts.items()}

    fail = False
    for iso in EXPECTED:
        for fam, want in EXPECTED[iso].items():
            got = out[iso][fam]
            status = "OK" if got == want else "MISMATCH"
            if got != want:
                fail = True
            print(f"[{iso}] {fam}: {got} (expected {want}) {status}")

    # Output machine-readable JSON
    output_path = os.path.join(BASE_DIR, "family_counts.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "summary_counts": out,
                "expected_counts": EXPECTED,
                "families_tested": {
                    k: {
                        "pfam": sorted(list(v[0])),
                        "ec": sorted(list(v[1])),
                        "interpro": sorted(list(v[2])),
                    }
                    for k, v in FAMILIES.items()
                },
                "loci_by_family": detailed_loci,
            },
            f,
            indent=2,
        )
    print(f"Wrote family counts to {output_path}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(count_families())
