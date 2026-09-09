# Analysis Scripts & Intermediate Data Conventions

This document formalizes the internal data conventions, coordinate systems, and pipeline architecture across the *Trichoderma asperellum* (TA-PUJ) and *Aspergillus flavus* (AF-PUJ) genomic and biosynthetic analyses.

---

## 1. Coordinate Systems & Indexing Conventions

### Public Presentation & Catalog Layer (`README.md`, Figure Titles & Gene Tables)
- **Convention:** **1-based inclusive** (`[start, end]`).
- **Semantics:** 
  - A CDS spanning bases 100 to 200 has `start = 100` and `end = 200`, yielding a sequence length of `200 - 100 + 1 = 101 bp`.
  - All antiSMASH regional GenBank files (`*.region*.gbk`) and Funannotate genome-wide GenBank files are parsed using Biopython into 1-based inclusive feature spans.
  - All figures rendered with `dna_features_viewer` specify `plots_indexing="biopython"` and 1-based sequence lengths (`end - start + 1`) to ensure perfect alignment with 1-based genomic coordinates.

### Intermediate JSON Layer (`neighborhood_ta.json`, `neighborhood_af.json`)
- **Convention:** **0-based half-open** (`[start, end)`).
- **Semantics:**
  - Python slice notation where `start` is 0-indexed and `end` is non-inclusive (equal to the 1-based inclusive end coordinate).
  - Example: A feature spanning 1-based `273,772..275,470` is stored in intermediate neighborhood JSON as:
    ```json
    {
      "start": 273771,
      "end": 275470
    }
    ```
- **Pipeline Ingestion Rule:**
  - Any pipeline consuming `neighborhood_*.json` to produce user-facing catalogs, markdown tables, or figures **MUST** apply `start_1based = json_record["start"] + 1` (with `end_1based = json_record["end"]`).

---

## 2. Genomic Identifier Conventions

- **Assembly Records vs. Scaffolds:**
  - In AF-PUJ, raw assembly records in FASTA and GenBank files use numerical LOCUS tags (e.g., `LOCUS 24 2350691 bp`, `LOCUS 1340 79127 bp`).
  - Catalogs and figures consistently format these as `scaffold_NN` or `Scaffold NN` (e.g., `scaffold_24` $\equiv$ assembly record LOCUS `24`) to provide human-readable identifiers.

---

## 3. Figure Header vs. Sub-track Span Semantics

- **Header Span (`Span: X–Y bp (Z bp, N CDSs)`):**
  - Represents the total candidate biosynthetic window defined by antiSMASH (including candidate boundary margins and flanking context) or the full curated regulatory/metabolic neighborhood.
- **Sub-track Bracket Span (`{name} cluster (N CDSs, X.X kb)`):**
  - Represents the precise physical span of the annotated CDSs within the cluster, measured from `min(CDS.start)` to `max(CDS.end)`.

---

## 4. Special Curation Notes: AF BGC_71 (Aflatoxin / CPA Supercluster)

- **Genomic Contig & Scope:**
  - `BGC_71_scaffold_1340_c1_aflatoxin_CPA_supercluster` resides on assembly record `LOCUS 1340` (Scaffold 1340, total length 79,127 bp).
  - Region file `1340.region001.gbk` encompasses exactly **17 annotated CDSs** (`PUJ_009389`–`PUJ_009405`), all situated continuously between coordinates 1,304 and 79,127 bp.
- **Gene Symbol Curation:**
  - Upstream aflatoxin cluster flank genes `PUJ_009389`–`PUJ_009392` were corrected in the post-audit remediation:
    - `PUJ_009389` $\rightarrow$ `aflV` / `cypX` (cytochrome P450 monooxygenase; MIBiG `AAS90009.1`)
    - `PUJ_009390` $\rightarrow$ `norA` / `aflE` (aldo-keto reductase; MIBiG `AAS90007.1`)
    - `PUJ_009391` $\rightarrow$ `estA` / `aflJ` (aflatoxin esterase; MIBiG `AAS90006.1`)
    - `PUJ_009392` $\rightarrow$ `ver-1` / `aflM` (versicolorin A dehydrogenase; MIBiG `AAS90005.1`)
- **Pathway Completeness:**
  - `aflP` and `aflO` reside upstream on the chromosome outside this specific scaffold contig boundary.
  - In the CPA operon, `cpaA` (PKS-NRPS), `cpaO` (FAD-dependent oxidoreductase), `cpaT` (MFS transporter), and `cpaH` (CpaM homolog, 94% identity to `BAK26563.1`) are fully annotated; `cpaD` (DMATS) is not annotated on this contig edge.

