#!/usr/bin/env python3
"""
verify_audit_remediation.py

Automated validation of all remediations for findings F1-F7 and O1-O3 from
PUJ-fungi_TA-AF-viz_Formal_Audit_Report_EN.md.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET

def test_ta_readme():
    print("Testing TA-viz/README.md...")
    ta_readme_path = os.path.join("TA-viz", "README.md")
    assert os.path.exists(ta_readme_path), "TA-viz/README.md missing!"
    with open(ta_readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # F7 / O1 / O3: Coordinate declaration & Bracket vs Span
    assert "Coordinate & Visualization Conventions" in content, "F7: Missing Coordinate Conventions section in TA"
    assert "1-based inclusive" in content.lower(), "F7: 1-based inclusive not declared in TA"
    assert "Figure Header vs. Sub-track Span" in content or "Header Span vs. Bracket Span" in content, "O3: Missing Header vs Bracket explanation in TA"

    # O2: Executive Biosafety & Agricultural Evaluation
    assert "Executive Biosafety & Agricultural Utility Evaluation" in content, "O2: Missing Biosafety & Ag evaluation in TA"
    assert "Qualified BSL-1 Equivalent" in content, "O2: BSL-1 status not stated"

    # F3: Bullet conflict fixes in TA
    # eqx1: 3,931 aa (not 3,091 aa)
    assert "3,931 aa" in content, "F3: eqx1 length 3,931 aa not found"
    assert "3,091 aa" not in content, "F3: eqx1 length 3,091 aa still present!"
    # eqx2: PF00107 / PF08240
    assert "PF00107" in content and "PF08240" in content, "F3: eqx2 Pfam domains not found"
    # eqx4: PF00155
    assert "PF00155" in content, "F3: eqx4 Pfam domain PF00155 not found"
    # eqx7: PF00891
    assert "PF00891" in content, "F3: eqx7 Pfam domain PF00891 not found"
    # perA: 1,054 aa
    assert "1,054 aa" in content, "F3: perA length 1,054 aa not found"
    assert "2,248 aa" not in content, "F3: perA length 2,248 aa still present!"
    # crpA: 1,382 aa
    assert "1,382 aa" in content, "F3: crpA length 1,382 aa not found"
    # crpB: no Pfam domain / uncharacterized
    assert "Cluster-associated uncharacterized protein (197 aa)" in content, "F3: crpB uncharacterized protein not found"
    # dmxR12: SDR (PF00106)
    assert "PF00106" in content, "F3: dmxR12 SDR PF00106 not found"
    # Literature-inferred tags
    assert "literature-inferred:" in content, "F3: Missing 'literature-inferred:' tags in TA"

    print(" -> TA-viz/README.md: PASSED all checks.")

def test_af_readme():
    print("Testing AF-viz/README.md...")
    af_readme_path = os.path.join("AF-viz", "README.md")
    assert os.path.exists(af_readme_path), "AF-viz/README.md missing!"
    with open(af_readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # F7 / O1: Coordinate declaration & Scaffold/LOCUS
    assert "Coordinate, Identifier & Visualization Conventions" in content or "Coordinate Conventions" in content, "F7: Missing Coordinate Conventions in AF"
    assert "1-based inclusive" in content.lower(), "F7: 1-based inclusive not declared in AF"
    assert "Scaffold vs. Locus Identifiers" in content or "Scaffold Identification Note" in content, "O1: Missing Scaffold/LOCUS note in AF"
    assert "Figure Header vs. Sub-track Span" in content or "Header Span vs. Bracket Span" in content, "O3: Missing Header vs Bracket explanation in AF"

    # F1: Clusters 75, 76, 77 1-based coordinates
    assert "273,772..342,848" in content, "F1: Cluster 75 span not 1-based"
    assert "778,830..880,781" in content, "F1: Cluster 76 span not 1-based"
    assert "208,819..273,028" in content, "F1: Cluster 77 span not 1-based"
    assert "273,771" not in content, "F1: Cluster 75 still has 0-based coordinate 273,771"
    assert "778,829" not in content, "F1: Cluster 76 still has 0-based coordinate 778,829"
    assert "208,818" not in content, "F1: Cluster 77 still has 0-based coordinate 208,818"

    # F2: BGC_71 Left-flank gene symbols
    bgc71_block = re.search(r"### 71\..*?(?=### 72|\Z)", content, re.DOTALL)
    assert bgc71_block, "BGC_71 section not found"
    bgc71_text = bgc71_block.group(0)
    assert "| `PUJ_009389` | `aflV` |" in bgc71_text, "F2: PUJ_009389 != aflV"
    assert "| `PUJ_009390` | `norA` |" in bgc71_text, "F2: PUJ_009390 != norA"
    assert "| `PUJ_009391` | `estA` |" in bgc71_text, "F2: PUJ_009391 != estA"
    assert "| `PUJ_009392` | `ver-1` |" in bgc71_text, "F2: PUJ_009392 != ver-1"

    # F4: Executive Summary & CAUTION standardization
    assert "17 CDSs (`PUJ_009389`–`PUJ_009405`)" in content or "17 continuous loci" in content, "F4: Executive summary does not specify 17 CDSs PUJ_009389-PUJ_009405"
    assert "51–97% identity (94–97% for core aflatoxin/CPA enzymes)" in content or "51–97% identity" in content, "F4: Executive summary identity range incorrect"
    assert "23 CDSs" not in bgc71_text, "F4: BGC_71 still claims 23 CDSs!"
    assert "23 CDSs" not in content[:3000], "F4: Executive summary still claims 23 CDSs for Scaffold 1340!"
    assert "99.8% identity" not in content, "F4: '99.8% identity' unqualified claim still present!"

    # F5: BGC_71 Pathway narrative
    assert "cpaO" in bgc71_text and "cpaD" in bgc71_text, "F5: cpaO or cpaD not mentioned in BGC_71 narrative"
    assert "FAD-dependent oxidoreductase" in bgc71_text or "FAD" in bgc71_text, "F5: cpaO FAD oxidoreductase missing"
    assert "not annotated" in bgc71_text or "cpaD" in bgc71_text, "F5: cpaD absence not clarified"
    assert "aflP" in bgc71_text and "aflO" in bgc71_text, "F5: aflP/aflO not mentioned"
    assert "BAK26563.1" in bgc71_text and "94% identity" in bgc71_text, "F5: CpaM / BAK26563.1 homology not cited"

    # F3: Siderophore & other bullet conflict fixes
    assert "literature-inferred:" in content, "F3: Missing 'literature-inferred:' tags in AF"

    print(" -> AF-viz/README.md: PASSED all checks.")

def test_af_figures():
    print("Testing AF-viz SVG figure files...")
    # Test BGC_71 SVG
    bgc71_svg = os.path.join("AF-viz", "BGC_71_scaffold_1340_c1_aflatoxin_CPA_supercluster.svg")
    assert os.path.exists(bgc71_svg), "BGC_71 SVG missing!"
    with open(bgc71_svg, "r", encoding="utf-8") as f:
        svg_text = f.read()
    assert "aflV" in svg_text, "F2: aflV not rendered in BGC_71 SVG"
    assert "norA" in svg_text, "F2: norA not rendered in BGC_71 SVG"
    assert "estA" in svg_text, "F2: estA not rendered in BGC_71 SVG"
    assert "ver-1" in svg_text, "F2: ver-1 not rendered in BGC_71 SVG"

    # Test CLUSTER_75, 76, 77 SVGs
    c75_svg = os.path.join("AF-viz", "CLUSTER_75_scaffold_24_phosphate_solubilizing_PHO13_IPP1.svg")
    c76_svg = os.path.join("AF-viz", "CLUSTER_76_scaffold_482_phosphate_regulator_PHO2_AMY3.svg")
    c77_svg = os.path.join("AF-viz", "CLUSTER_77_scaffold_1339_phosphate_sensor_PHO81_redox.svg")
    assert os.path.exists(c75_svg), "CLUSTER_75 SVG missing!"
    assert os.path.exists(c76_svg), "CLUSTER_76 SVG missing!"
    assert os.path.exists(c77_svg), "CLUSTER_77 SVG missing!"

    with open(c75_svg, "r", encoding="utf-8") as f:
        c75_text = f.read()
    assert "273,772" in c75_text, "F1: 273,772 not in CLUSTER_75 SVG"
    assert "273,771" not in c75_text, "F1: 0-based 273,771 still in CLUSTER_75 SVG"

    with open(c76_svg, "r", encoding="utf-8") as f:
        c76_text = f.read()
    assert "778,830" in c76_text, "F1: 778,830 not in CLUSTER_76 SVG"
    assert "778,829" not in c76_text, "F1: 0-based 778,829 still in CLUSTER_76 SVG"

    with open(c77_svg, "r", encoding="utf-8") as f:
        c77_text = f.read()
    assert "208,819" in c77_text, "F1: 208,819 not in CLUSTER_77 SVG"
    assert "208,818" not in c77_text, "F1: 0-based 208,818 still in CLUSTER_77 SVG"

    print(" -> AF-viz SVG figures: PASSED all checks.")

def test_intermediate_notes():
    print("Testing ANALYSIS_SCRIPTS_AND_INTERMEDIATE_NOTES.md...")
    notes_path = "ANALYSIS_SCRIPTS_AND_INTERMEDIATE_NOTES.md"
    assert os.path.exists(notes_path), "ANALYSIS_SCRIPTS_AND_INTERMEDIATE_NOTES.md missing!"
    with open(notes_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "0-based half-open" in content, "F6: 0-based half-open not documented"
    assert "1-based inclusive" in content, "F6: 1-based inclusive not documented"
    assert "BGC_71" in content, "F6: BGC_71 not mentioned in notes"
    print(" -> ANALYSIS_SCRIPTS_AND_INTERMEDIATE_NOTES.md: PASSED all checks.")

def main():
    test_ta_readme()
    test_af_readme()
    test_af_figures()
    test_intermediate_notes()
    print("\n=======================================================")
    print("ALL AUDIT REMEDIATION CHECKS PASSED SUCCESSFULLY (PASS)!")
    print("=======================================================")

if __name__ == "__main__":
    main()
