# Implementation Plan (Revision V3): Transitioning Feature Labels to Standardized Gene Symbols

**Document Version:** `VIZ-REVISION-V3`  
**Date:** September 9, 2026  
**Target Isolate:** *Trichoderma asperellum* isolate TA-PUJ (`fungiSMASH-TA`)  
**Target Directory:** `d:\W\fungi-PUJ\TA-viz/`  

---

## 1. Problem Diagnosis & Objective

In the previous revision (V2), all feature arrows were lifted into elevated outline text boxes with vertical leader lines, completely resolving the white-on-white text spillage and box overlapping. However, the label content primarily displayed locus tags (e.g. `PUJ_004816\n(PF00291)`, `PUJ_000117\n(PF00106)`, or `TATC6\n(PUJ_005301)`).

In target reference figures (e.g. `Screenshot 2026-09-09 053951.png`):
1. **Gene Symbol Primacy:** Characterized genes are labeled directly with their recognized gene symbol (e.g. `pksA`, `aflR`, `acdS`, `eqx1`, `esyn1`, `fet3`, `chit2`).
2. **Single-Line Typography:** Labels are concise, single-line text items without multi-line locus tags or Pfam codes cluttering the box.
3. **Graceful Fallback:** Genes lacking an established gene symbol (such as novel uncharacterized orphan loci) gracefully fall back to their unique isolate locus tag (e.g. `PUJ_001306`, `PUJ_001307`).

---

## 2. Gene Symbol Mapping Specification

A comprehensive gene symbol dictionary is integrated into the rendering pipeline for all 24 clusters:

### A. Biocontrol & Rhizosphere Micro-Clusters
- **Cluster 22 (`contig_1730`, ACC Deaminase):**
  - `PUJ_004815`: `acdT` (MFS ACC permease)
  - `PUJ_004816`: `acdS` (*Tas-acdS*, 1-aminocyclopropane-1-carboxylate deaminase)
  - `PUJ_004817`: `acdR` (phospholipase D signaling enzyme)
  - `PUJ_004818`: `rho3` (Rho GTPase)
- **Cluster 23 (`contig_623`, Reductive Iron Assimilation):**
  - `PUJ_001677`: `fre1` (ferric reductase)
  - `PUJ_001678`: `fet3` (multicopper ferroxidase)
  - `PUJ_001679`: `ftr1` (high-affinity iron permease)
- **Cluster 24 (`contig_1705`, Chitinase 2 Biocontrol Locus):**
  - `PUJ_004618`: `vps21` (vacuolar protein sorting GTPase)
  - `PUJ_004623`: `chit2` (*Tas-chit2*, endochitinase 2)

### B. Characterized MIBiG Secondary Metabolite BGCs
- **BGC 01 (`contig_52_c1`, Equisetin-like):**
  - `PUJ_000110`: `eqx5` (MFS efflux permease)
  - `PUJ_000111`: `eqx6` (Zn2Cys6 transcription factor)
  - `PUJ_000112`: `eqx8` (tailoring hydrolase)
  - `PUJ_000113`: `eqx7` (SAM methyltransferase)
  - `PUJ_000114`: `eqx4` (cytochrome P450 monooxygenase)
  - `PUJ_000115`: `eqx3` (diels-alderase / esterase)
  - `PUJ_000116`: `eqx2` (enoyl reductase)
  - `PUJ_000117`: `eqx1` (core hybrid iterative PKS-NRPS mega-synthetase)
- **BGC 09 (`contig_697_c1`, Peramine-like):**
  - `PUJ_001843`: `perM` (MFS transporter)
  - `PUJ_001844`: `perO` (cytochrome P450)
  - `PUJ_001845`: `perT` (peptidase / tailoring)
  - `PUJ_001846`: `perA` (core peramine NRPS)
- **BGC 12 (`contig_1144_c1`, Cryptosporioptide B):**
  - `PUJ_002690`: `dmxR12` (short chain dehydrogenase)
  - `PUJ_002691`: `crpB` (esterase / lactonase)
  - `PUJ_002692`: `crpA` / `agnpks1` (core Type I PKS)
- **BGC 15 (`contig_1342_c1`, Leucinostatin A):**
  - `PUJ_003355`: `lcsA` (core PKS module)
  - `PUJ_003357`: `lcsC` (branched-chain aminotransferase)
  - `PUJ_003358`: `lcsD` (cytochrome P450)
  - `PUJ_003360`: `lcsE` (MFS transporter)
  - `PUJ_003361`: `lcsB` (core NRPS module)
- **BGC 17 (`contig_1419_c1`, Metachelin C):**
  - `PUJ_003663`: `brx1` (ribosome biogenesis factor)
  - `PUJ_003664`: `ypt31` (Rab GTPase)
  - `PUJ_003665`: `mchT` (siderophore exporter)
  - `PUJ_003666`: `mchC` (transacetylase)
  - `PUJ_003667`: `mchB` (ornithine monooxygenase)
  - `PUJ_003668`: `mchA` (core siderophore NRPS / `sidC`)
- **BGC 18 (`contig_1710_c1`, Enniatin):**
  - `PUJ_004649`: `cyp2` (P450 monooxygenase)
  - `PUJ_004650`: `mtr1` (methyltransferase)
  - `PUJ_004652`: `act1` (acetyltransferase)
  - `PUJ_004653`: `atp1` (ABC multidrug transporter)
  - `PUJ_004654`: `cyp1` (P450)
  - `PUJ_004656`: `kivR` (ketoisovalerate reductase)
  - `PUJ_004657`: `esyn1` (core cyclodepsipeptide NRPS)
  - `PUJ_004660`: `deh1` (dehydrogenase)
- **BGC 19 (`contig_1778_c1`, Squalestatin S1):**
  - `PUJ_005108`: `caj1` (DnaJ chaperone)
  - `PUJ_005110`: `erg9` (squalene synthase)
  - `PUJ_005113`: `gpi14` (GPI mannosyltransferase)
  - `PUJ_005114`: `sqsA` (core synthase)
- **BGC 21 (`contig_1813_c1`, Trichobrasilenol):**
  - `PUJ_005301`: `tatc6` (brasilane sesquiterpene cyclase)
  - `PUJ_005302`: `gst2` (glutathione S-transferase)
  - `PUJ_005306`: `mre11` (recombination factor)
  - `PUJ_005307`: `rad50` (recombination factor)

### C. Orphan BGCs with GenBank-Annotated Symbols
- `contig_599_c1`: `PUJ_001598` -> `rho1`
- `contig_675_c1`: `PUJ_001793` -> `erg7` (oxidosqualene cyclase)
- `contig_909_c1`: `PUJ_002252` -> `bts1` (GGPP synthase), `PUJ_002253` -> `pex29`, `PUJ_002254` -> `pom1`
- `contig_1170_c1`: `PUJ_002736` -> `lyp1`
- `contig_1801_c1`: `PUJ_005224` -> `rtg2`
- All other uncharacterized orphan loci retain their clean locus tags (`PUJ_xxxxxx`).

---

## 3. Implementation Steps

1. **Update Visualization Engine (`scripts/build_ta_viz_catalog.py`):**
   - Replace `format_gene_label(g)` with concise single-line `get_symbol_or_tag(g)`.
   - Ensure all `GraphicFeature` labels receive the clean gene symbol (if available) or locus tag.
   - Re-render all 24 PNG (300 DPI) and 24 SVG files into `TA-viz/`.
2. **Synchronize Catalog Tables (`TA-viz/README.md`):**
   - Update the "Gene Symbol" column in the markdown tables from empty `—` to the mapped gene symbols.
3. **Verification:**
   - Inspect rendered images to confirm single-line gene symbols in elevated boxes with leader lines.
   - Verify that all 48 files are updated and valid.
