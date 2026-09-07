# Analysis Scripts & Intermediate Synteny Notes: PUJ Fungal Isolates

**Workspace:** `D:\W\fungi-PUJ`  
**Date:** September 7, 2026  
**Pipeline:** Funannotate 1.8.17 + antiSMASH 8.0.4  

---

## 1. Directory of Analysis & Pipeline Scripts

All python scripts used to parse GenBank annotations, extract gene neighborhoods, format syntenic windows, and generate reports are preserved directly in the workspace:

| Script Filename | Primary Role & Description | Output Generated |
| :--- | :--- | :--- |
| [`scratch_neighborhood.py`](file:///D:/W/fungi-PUJ/scratch_neighborhood.py) | Parses the primary Funannotate `.gbk` files (`Funannotate-annotated-genome-TA.gbk` and `Funannotate-annotated-genome-AF.gbk`). Scans for all CDS features on each contig/scaffold and slices out flanking genes within a window of $\pm 10$ genes around each target locus tag. | [`neighborhood_ta.json`](file:///D:/W/fungi-PUJ/neighborhood_ta.json)<br>[`neighborhood_af.json`](file:///D:/W/fungi-PUJ/neighborhood_af.json) |
| [`scratch_print_neighborhood.py`](file:///D:/W/fungi-PUJ/scratch_print_neighborhood.py) | Reads the structured JSON neighborhood extractions and formats them into an aligned plain-text terminal report containing relative position, locus tag, strand, protein length (aa), product description, and Pfam/EC annotations. | [`neighborhood_summary.txt`](file:///D:/W/fungi-PUJ/neighborhood_summary.txt) |
| [`inspect_neighborhoods.py`](file:///D:/W/fungi-PUJ/inspect_neighborhoods.py) | Refined parsing script producing high-density synteny tables with explicit Pfam accessions, EC numbers, and target boundaries across both isolates. | [`neighborhoods_clean.txt`](file:///D:/W/fungi-PUJ/neighborhoods_clean.txt) |
| [`update_review_v4.py`](file:///D:/W/fungi-PUJ/update_review_v4.py) | Standalone script that builds and outputs the comprehensive review markdown document, integrating sequence validation, synteny tables, and wet-lab protocols. | [`agriculture-support-biocontrol-fungal-isolate-review.md`](file:///D:/W/fungi-PUJ/agriculture-support-biocontrol-fungal-isolate-review.md) |

---

## 2. Directory of Intermediate Data Files & Synteny Notes

The intermediate extractions and raw neighborhood tables are stored in both structured JSON and human-readable text formats:

1. **Structured JSON Extractions:**
   - [`neighborhood_ta.json`](file:///D:/W/fungi-PUJ/neighborhood_ta.json): Contains complete feature dictionaries (coordinates, strand, aa length, product, EC, db_xref, Pfam, EggNOG, and notes) for flanking genes of:
     - `PUJ_004816` (ACC Deaminase on `contig_1730`)
     - `PUJ_005301` (Terpene Cyclase 6 / Brasilane Synthase on `contig_1813`)
     - `PUJ_004623` (Chitinase 2 on `contig_1705`)
     - `PUJ_001678` (Ferroxidase FET3 on `contig_623`)
     - `PUJ_003670` (Metachelin NRPS on `contig_1419`)
     - `PUJ_003355` (Destruxin PKS on `contig_1342`)
     - `PUJ_004657` (Siderophore NRPS on `contig_1710`)
   - [`neighborhood_af.json`](file:///D:/W/fungi-PUJ/neighborhood_af.json): Contains feature dictionaries for flanking genes of:
     - `PUJ_009393` (AflR master regulator on Scaffold 1340)
     - `PUJ_004419` (Aerobactin-like siderophore synthetase on Scaffold 471)
     - `PUJ_005557` (PHO2 transcription factor on Scaffold 482)
     - `PUJ_009297` (PHO81 CDK-inhibitor / sensor on Scaffold 1339)
     - `PUJ_000724` (PHO13 / IPP1 phosphate hydrolase cluster on Scaffold 24)

2. **Formatted Text Reports:**
   - [`neighborhood_summary.txt`](file:///D:/W/fungi-PUJ/neighborhood_summary.txt): Full textual table of all neighborhoods with extended qualifiers.
   - [`neighborhoods_clean.txt`](file:///D:/W/fungi-PUJ/neighborhoods_clean.txt): Concise, aligned synteny table highlighting relative gene index (`-10` to `+10`), strand (`+`/`-`), protein length, gene symbol, Pfam domains, and EC numbers.

---

## 3. Key Observations from Intermediate Analysis

### A. *Trichoderma asperellum* (TA-PUJ)
- **Rhizosphere Micro-cluster on `contig_1730`:** The ACC deaminase gene (`PUJ_004816`, `EC 3.5.99.7`) is bounded by an MFS solute transporter (`PUJ_004815`, `PF07690`) upstream, and a high-molecular-weight $\beta$-glucosidase (`PUJ_004817`, 1,141 aa, `EC 3.2.1.21`) + polarized growth regulator `RHO3` (`PUJ_004818`) downstream. This structural arrangement suggests co-regulation during plant root colonization.
- **Sesquiterpene Tailoring Cluster on `contig_1813`:** Terpene cyclase `TATC6` (`PUJ_005301`) is clustered with Glutathione S-transferase `GST2_2` (`PUJ_005302`), a Short-Chain Dehydrogenase/Reductase (`PUJ_005304`), and a Cytochrome P450 (`PUJ_005305`), representing a complete volatile organic compound (VOC) synthesis and modification unit.
- **Reductive Iron Assimilation (RIA) on `contig_623`:** Multicopper ferroxidase `FET3` (`PUJ_001678`) and iron permease `FTR1_1` (`PUJ_001679`) are physically contiguous, forming the canonical high-affinity iron scavenging complex.

### B. *Aspergillus flavus* (AF-PUJ)
- **Continuous 75-kb AF/CPA Super-Cluster on Scaffold 1340:** Across 21 consecutive loci (`PUJ_009383` to `PUJ_009403`), there are zero truncations or deletions. All canonical aflatoxin genes (`aflP`, `aflO`, `aflN`, `aflM`, `aflL`, `aflJ`, `aflV`, `aflT`, `aflD`/`ver-1`, `aflR`, `fas-2`, `fas-1`, `nor-1`, `pksA`, `aflT`) seamlessly merge into the cyclopiazonic acid cluster (`cpaT`, `cpaO`, `cpaA`, `cpaH`). This provides molecular confirmation of toxigenic lineage.
- **Phosphate Solubilizing Operon on Scaffold 24:** Proximity of `PHO13` (p-nitrophenyl phosphatase, `PUJ_00728`) and `IPP1` (inorganic pyrophosphatase, `PUJ_000730`) indicates active dual-action organic and inorganic phosphate mobilization.
