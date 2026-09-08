# Implementation Plan (Revision V2): Enhancing TA Gene Cluster Visualizations to Match Reference Aesthetic

**Document Version:** `VIZ-REVISION-V2`  
**Date:** September 9, 2026  
**Target Isolate:** *Trichoderma asperellum* isolate TA-PUJ (`fungiSMASH-TA`)  
**Target Directory:** `d:\W\fungi-PUJ\TA-viz/`  

---

## 1. Problem Diagnosis & Root Cause Analysis

Based on user review and direct comparison between initial outputs (`image.png`) and the target publication reference (`Screenshot 2026-09-09 053951.png`):
1. **White-on-White Text Overflow:** When `annotate_inline=True` (the default), `dna_features_viewer` checks only horizontal span (`x1 < start` or `x2 > end`) before selecting white font for dark/red arrows (e.g. `PUJ_001307`). Multi-line labels (locus tag + Pfam domain) overflow vertically outside the top boundary of the arrow, rendering white text directly over the white canvas background.
2. **Cramped Box Placement Without Leader Lines:** By default, `elevate_outline_annotations=False` in `dna_features_viewer`. This places text boxes directly on top of the feature arrows without vertical separation, obscuring arrow edges and eliminating leader line clearance.

---

## 2. Architectural & Styling Specifications

To match the clean, publication-grade aesthetics of `Screenshot 2026-09-09 053951.png`, the rendering pipeline implements the following design principles:

### A. Label Positioning & Leader Lines
- **Strict Elevated Outline Annotations (`annotate_inline=False`, `elevate_outline_annotations=True`):** All feature labels are systematically lifted above the arrow track into staggered multi-level boxes.
- **Vertical Leader Lines:** Explicit vertical connecting lines (`lw=0.6`, `c="#555555"`) extend from the base of each label box down to the center of the respective feature arrow.
- **Vertical Clearance (`level_offset=0.35`, `feature_level_height=1.8`, `labels_spacing=12`):** Generous vertical breathing room between the feature arrows and the lowest label level.

### B. Typography & Text Box Aesthetics
- **Consistent High-Contrast Typography:** All labels use `fontdict={"color": "#111111", "fontweight": "bold", "fontsize": 8.0}`, eliminating any white-on-white text.
- **Text Box Styling:** Clean rounded boxes (`boxstyle="round,pad=0.3"`, `box_color="#f8f9fa"`, `ec="#777777"`, `box_linewidth=0.8`).
- **Compact Multi-Line Content:** Locus tag / gene symbol on line 1, compact product / Pfam descriptor in parentheses on line 2 (e.g. `PUJ_001307\n(Type I PKS)` or `TATC6\n(PUJ_005301)`).

### C. Sub-Track Cluster Span & Boundary Bracket
- Beneath the feature track, an annotated horizontal span bracket indicates the core cluster boundaries, locus count, and boundary gaps (e.g. `equisetin-like PKS-NRPS cluster (10 loci)` or `ACC deaminase rhizosphere micro-cluster (6 loci)`).
- Clean genomic scale ruler with coordinate ticks and axis title (e.g. `contig_52 position (bp)` or `(kb)`).

---

## 3. Scope of Affected Clusters (All 24 Clusters)

1. `BGC_01_contig_52_c1_equisetin` (NRPS/T1PKS, 10 loci)
2. `BGC_02_contig_76_c1_orphan_terpene` (terpene, 3 loci)
3. `BGC_03_contig_470_c1_orphan_T1PKS` (T1PKS, 2 loci)
4. `BGC_04_contig_473_c1_orphan_NRPS` (NRPS, 8 loci)
5. `BGC_05_contig_579_c1_orphan_NRPS` (NRPS-like, 1 locus)
6. `BGC_06_contig_599_c1_orphan_terpene` (terpene, 3 loci)
7. `BGC_07_contig_627_c1_orphan_NRPS` (NRPS, 5 loci)
8. `BGC_08_contig_675_c1_orphan_terpene` (terpene, 3 loci)
9. `BGC_09_contig_697_c1_peramine` (NRPS, 5 loci)
10. `BGC_10_contig_703_c1_orphan_NRPS` (NRPS, 3 loci)
11. `BGC_11_contig_909_c1_orphan_terpene_precursor` (terpene-precursor, 4 loci)
12. `BGC_12_contig_1144_c1_cryptosporioptide_B` (T1PKS, 3 loci)
13. `BGC_13_contig_1170_c1_orphan_NRPS_like` (NRPS-like, 3 loci)
14. `BGC_14_contig_1317_c1_orphan_NRPS_like` (NRPS-like, 1 locus)
15. `BGC_15_contig_1342_c1_leucinostatin_A` (NRPS/PKS, 9 loci)
16. `BGC_16_contig_1364_c1_orphan_NRPS` (NRPS, 6 loci)
17. `BGC_17_contig_1419_c1_metachelin_C` (NRPS, 8 loci)
18. `BGC_18_contig_1710_c1_enniatin` (NRPS, 11 loci)
19. `BGC_19_contig_1778_c1_squalestatin_S1` (terpene, 9 loci)
20. `BGC_20_contig_1801_c1_orphan_NRPS` (NRPS, 6 loci)
21. `BGC_21_contig_1813_c1_trichobrasilenol` (terpene, 8 loci)
22. `CLUSTER_22_contig_1730_ACC_deaminase` (Rhizosphere micro-cluster, 6 loci)
23. `CLUSTER_23_contig_623_iron_assimilation_FET3_FTR1` (RIA complex, 9 loci)
24. `CLUSTER_24_contig_1705_chitinase_2_Tas_chit2` (Biocontrol locus, 7 loci)

---

## 4. Verification Protocol

- Generate 24 `.png` (300 DPI) and 24 `.svg` files in `TA-viz/`.
- Inspect rendered images via visual inspection to confirm:
  - Zero white-on-white text
  - Generous vertical separation between arrows and boxes
  - Clean leader lines connecting boxes to feature arrows
  - Distinct sub-track boundary span brackets
