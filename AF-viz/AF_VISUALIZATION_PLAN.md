# Implementation Plan: AF Isolate Visualization & Interactive Scientific Catalog (`AF-viz`)

## Executive Summary
This document establishes the architectural, bioinformatic, and visual specifications for generating publication-grade gene cluster diagrams and an interactive scientific catalog for *Aspergillus flavus* isolate **AF-PUJ**, housed in [`d:\W\fungi-PUJ\AF-viz/`](file:///d:/W/fungi-PUJ/AF-viz/). 

Building directly upon the approved **Revision V3** aesthetic and epistemic standards established in `TA-viz/`, this workflow visualizes all **74 antiSMASH secondary metabolite BGC regions** (covering 27 scaffolds, including characterized mycotoxins, pigments, siderophores, and novel orphan synthases) plus **3 verified non-BGC agricultural functional gene neighborhoods** (Phosphate Solubilization `PHO13`/`IPP1`, Phosphate TF `PHO2`/Amylase, and Phosphate Starvation Sensor `PHO81`/Redox dyad) for a total of **77 gene clusters**.

---

## 1. Scope & Master Cluster Inventory (77 Clusters)

### A. Secondary Metabolite BGCs (74 antiSMASH Regions)
1. **High-Confidence Characterized Clusters (16 BGCs):**
   - **`scaffold_1340_c1` (Scaffold 1340):** The canonical dual **Aflatoxin + Cyclopiazonic Acid (AF/CPA) Super-Cluster** (17 CDSs, 79.1 kb; `aflJ`–`aflU`, `cpaT`–`cpaH`).
   - **`scaffold_480_c2` (Scaffold 480):** **Aspirochlorine** ETP Antimicrobial / Mycotoxin Cluster (29 CDSs, 19 MIBiG hits, score 17,383; `aclA`–`aclS`).
   - **`scaffold_480_c3` (Scaffold 480):** **Leporin B** Hybrid PKS-NRPS Cluster (44 CDSs, 10 MIBiG hits, score 15,512; `lepA`–`lepH`).
   - **`scaffold_480_c1` (Scaffold 480):** **Imizoquin** Alkaloid / Pigment BGC (21 CDSs, 8 MIBiG hits, score 8,477; `imqA`–`imqH`).
   - **`scaffold_258_c4` (Scaffold 258):** **Astellolide A** Sesquiterpene Lactone BGC (20 CDSs, 8 MIBiG hits, score 8,724; `astA`–`astH`).
   - **`scaffold_258_c3` (Scaffold 258):** **Flavunoidine** Cyclic Peptide NRPS BGC (19 CDSs, 7 MIBiG hits, score 7,818).
   - **`scaffold_418_c2` (Scaffold 418):** **Ustiloxin B** Fungal RiPP Anti-Tubulin Mycotoxin BGC (20 CDSs, 13 MIBiG hits, score 7,477; `ustA`–`ustR`).
   - **`scaffold_1845_c1` (Scaffold 1845):** **Dichlorodiaporthin** Isochroman BGC (18 CDSs, 5 MIBiG hits, score 6,738; `dapA`–`dapE`).
   - **`scaffold_1924_c1` (Scaffold 1924):** **Aspergillic Acid** Pyrazinone Hydroxamate Mycotoxin BGC (19 CDSs, 6 MIBiG hits, score 6,227; `asaA`–`asaF`).
   - **`scaffold_24_c4` (Scaffold 24):** **Asparasone A** Aflatoxin-Shunt Pigment PKS BGC (28 CDSs, 5 MIBiG hits, score 5,862; `apaA`–`apaE`).
   - **`scaffold_485_c2` (Scaffold 485):** **Actinopolymorphol C / Piperazine** NRPS-like BGC (14 CDSs, 6 MIBiG hits, score 6,338).
   - **`scaffold_471_c3` (Scaffold 471):** **Aflavarin** Indole Diterpene BGC (19 CDSs, 4 MIBiG hits, score 5,687; `afvA`–`afvD`).
   - **`scaffold_433_c1` (Scaffold 433):** **8-Methyldiaporthin** PKS BGC (17 CDSs, 4 MIBiG hits, score 5,042).
   - **`scaffold_826_c1` (Scaffold 826):** **(-)-Ditryptophenaline** Dimeric Diketopiperazine BGC (14 CDSs, 3 MIBiG hits, score 6,216; `dtpA`–`dtpC`).
   - **`scaffold_826_c2` (Scaffold 826):** **YWA1 / Naphthopyrone** Pigment PKS BGC (17 CDSs, score 4,277; `ywa1`, `yg1`).
   - **`scaffold_904_c1` (Scaffold 904):** **Penicillin** $\beta$-Lactam Core BGC (17 CDSs, score 6,518; `acvA`, `ipnA`).
   - **`scaffold_960_c1` (Scaffold 960):** **6-Methylsalicylic Acid (6-MSA)** Core PKS BGC (17 CDSs, score 2,075; `msaS`).

2. **Medium/Low-Homology Characterized Clusters (17 BGCs):**
   - Siderophores: `scaffold_471_c4` (metachelin C), `scaffold_827_c1` (metachelin C).
   - Polyketides / Pigments: `scaffold_433_c2` (ankaflavin/monascin), `scaffold_486_c2` (monascorubrin), `scaffold_614_c2` (2,4'-dihydroxy-3'-methoxypropiophenone), `scaffold_641_c3` (azasperpyranone A), `scaffold_703_c1` (dehydrocurvularin), `scaffold_431_c1` (fusaric acid), `scaffold_431_c3` (zopfiellin).
   - Peptides & Terpenoids: `scaffold_24_c6` (choline), `scaffold_256_c1` & `scaffold_418_c1` (paspalinine), `scaffold_256_c3` (heptelidic acid), `scaffold_256_c7` (aspercryptins), `scaffold_480_c5` (nidulanin A), `scaffold_485_c1` & `scaffold_826_c3` (clavaric acid).

3. **Orphan Secondary Metabolite BGCs (41 BGCs):**
   - Uncharacterized novel clusters spanning PKS, NRPS, Terpene, Indole, and Betalactone synthases across scaffolds 24, 256, 258, 418, 431, 432, 433, 471 (including NIS Siderophore `471_c1`), 480, 482, 485, 486, 497, 614, 641, 702, 703 (including `nitropropanoic_acid`), 815, 904, 1334, and 2001.

### B. Agricultural Functional Gene Neighborhoods (3 Non-BGC Micro-Clusters)
- **`CLUSTER_75_scaffold_24_phosphate_solubilizing_PHO13_IPP1`:** Phosphate solubilizing syntenic cluster harboring vacuolar $\alpha$-mannosidase `ams1`, structural maintenance protein `smc1`, cell-cycle activator `cdh1`, target aminopeptidase `pepP`, organic phosphatase `pho13`, and inorganic pyrophosphatase `ipp1`.
- **`CLUSTER_76_scaffold_482_phosphate_regulator_PHO2_AMY3`:** Phosphate starvation regulatory hub harboring master homeodomain TF `pho2`, raw starch-degrading $\alpha$-amylase `amy3`, $\alpha$-glucosidase `aga1`, and phospholipid translocase `dnf3`.
- **`CLUSTER_77_scaffold_1339_phosphate_sensor_PHO81_redox`:** Orthophosphate starvation sensor `pho81` clustered with mitochondrial coenzyme Q prenyltransferase `coq2`, iron-sulfur glutaredoxin `grx5`, and peroxiredoxin `dot5`.

---

## 2. Visualization Specifications (Adhering to Revision V3)

The visualizations will be generated using `dna_features_viewer` driven by custom matplotlib styling to guarantee 100% adherence to the visual standards demonstrated in the user reference image (`media_1788907224979.png`):

1. **Standardized Single-Line Gene Symbols:**
   - Pre-mapped characterized symbols (`aflP`, `aflR`, `pksA`, `cpaA`, `iucA`, `asaA`, `aclA`, `lepA`, `pho13`, `ipp1`, `pho2`, `pho81`, etc.) rendered in bold, single-line format.
   - For uncharacterized or orphan loci, clean fallback to the official locus tag (`PUJ_xxxxxx`).
2. **Elevated Outline Annotation Boxes:**
   - Crisp rounded outline boxes (`box_color="#f8f9fa"`, `box_linewidth=0.8`, font size 8.0 pt bold dark `#111111`).
   - Vertical elevation (`elevate_outline_annotations=True`, `level_offset=0.30`) to eliminate collision with arrow tracks.
3. **Thin Vertical Leader Lines:**
   - Solid grey leader lines (`#555555`, 0.8 pt) connecting each box to its respective CDS arrow.
4. **Annotated Sub-Track Span Brackets:**
   - Dimensioned bracket below ruler (`#b05d1a`, 1.5 pt) indicating cluster product name, exact CDS count, and physical span in kilobases (e.g. *aflatoxin / cyclopiazonic acid super-cluster (17 CDSs, 77.8 kb)*).
5. **Functional Color Palette & Professional Legend:**
   - **Core Synthase / Target Enzyme (`#d1495b` Crimson):** PKS, NRPS, Terpene cyclase, RiPP precursor, NIS synthase, phosphatases.
   - **Tailoring & Modifying Enzyme (`#f58518` Amber):** P450 monooxygenases, ketoreductases, methyltransferases, dehydrogenases, halogenases, esterases.
   - **Transport & Efflux (`#2ca02c` Emerald):** MFS permeases, ABC transporters.
   - **Regulation & Signaling (`#9467bd` Purple):** Zn2Cys6 transcription factors, homeodomain TFs, ankyrin kinases.
   - **Other CDS / Uncharacterized (`#4c78a8` Steel Blue):** Accessory metabolic enzymes, hypothetical loci.
6. **Dual-Format Publication Export:**
   - High-resolution raster PNG (300 DPI) for instant preview.
   - Clean, infinite-resolution vector SVG for publication and web rendering.
   - Automated retry loop handling Windows file thumbnailer locks.

---

## 3. Structure of Interactive Scientific Catalog (`AF-viz/README.md`)

The catalog document will serve as an authoritative, self-contained genomic reference:
1. **Master Inventory & Quick Navigation Table:**
   - 77-row table with Index, Cluster ID, Scaffold, Type, Size/Span, Top MIBiG Hit, Confidence Tier, and Anchor Links.
2. **Cluster-by-Cluster Deep Dive:**
   - **Visual Embed:** Linked high-res PNG and vector SVG.
   - **Master Gene Qualifier Table:** Columns for Locus Tag, Curated Gene Symbol, Strand, Span/Coordinates, Length (aa), Putative Product & Enzyme Commission (EC), and Pfam / InterPro / GO domains.
   - **Putative Function & Product Elaboration:** Biochemical description of every gene product and catalytic mechanism.
   - **Collective Pathway Architecture & Biological Synergy:** Narrative explaining the integrated logic of the cluster (how core synthetases, tailoring enzymes, efflux pumps, and regulators operate as a concerted molecular assembly line).
   - **Definitive Biosafety & Agricultural Scrutiny:** Clear callout alerts emphasizing toxigenic lineage vs agricultural potential (highlighting aflatoxin, CPA, aspergillic acid, and ustiloxin risks vs phosphate solubilization).
3. **Comprehensive References Section:**
   - Full academic citations for all discussed clusters, enzymes, and pathway mechanisms.

---

## 4. Proposed Execution Sequence

1. **Phase 1: Build Rendering & Catalog Script**
   - Create [`d:\W\fungi-PUJ\scripts\build_af_viz_catalog.py`](file:///d:/W/fungi-PUJ/scripts/build_af_viz_catalog.py) combining:
     - 77-cluster batch rendering (PNG 300 DPI + SVG).
     - Markdown catalog generator producing `AF-viz/README.md`.
2. **Phase 2: Render Visualizations & Verify Quality**
   - Execute batch rendering for all 77 clusters (154 image files).
   - Inspect rendered images using `view_file` to confirm zero label collisions, proper box elevations, and accurate colors.
3. **Phase 3: Generate Catalog & Final Review**
   - Generate `AF-viz/README.md` with complete gene qualifier tables, pathway breakdowns, and references.
   - Update `walkthrough.md` with sample galleries and verification summaries.
