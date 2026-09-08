#!/usr/bin/env python3
"""Build Sections 7, 8, 9, 10, and 11 for AGRI-BIOCONTROL-GENOMIC-SCRUTINY-V6."""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load BGC tables from bgc_tables.md
with open(os.path.join(BASE_DIR, "bgc_tables.md"), encoding="utf-8") as f:
    bgc_tables_text = f.read().strip()

# Section 8 Subsections (each >= 150 words)
sec8_1 = """#### 8.1 Peptaibol Synthetase Gap Analysis in TA-PUJ (*Trichoderma asperellum*)
Peptaibols are linear, non-ribosomal peptide antibiotics typically 7 to 20 amino acid residues in length, enriched in the non-proteinogenic amino acid alpha-aminoisobutyric acid (Aib), and characterized by an N-terminal acetyl cap and a C-terminal amino alcohol (such as phenylalaninol, leucinol, or valinol). Within the biocontrol genus *Trichoderma*, 18-to-20-residue peptaibols (including trichorzianines, peptavirins, and alamethicins) serve as powerful membrane-permeabilizing agents. They act synergistically with fungal cell-wall-degrading chitinases and beta-glucanases to perforate and lyse target phytopathogenic fungal hyphae (*Rhizoctonia*, *Fusarium*, *Pythium*).

In isolate TA-PUJ, antiSMASH region `contig_52_c1` encodes the largest non-ribosomal peptide synthetase detected in the entire assembly: locus `TA:PUJ_000117` (spanning coordinates 27,050..39,773 bp on `contig_52`, joining 12 exons, and translating to a 3,931-amino-acid polypeptide containing four complete adenylation modules). Crucially, canonical 18-to-20-residue peptaibol synthetases documented in benchmark *Trichoderma* biocontrol strains—such as *tex1* from *Trichoderma virens* (Gv29-8) or *pps1* from *Trichoderma atroviride*—exceed 6,000 to 7,000 amino acids in length across 18 to 20 catalytic modules. No such megasynthetase of >=6,000 aa was assembled in TA-PUJ.

However, KnownClusterBlast analysis of region `contig_1342_c1` reveals a secondary match to the AbT1 peptaibol BGC (`BGC0000300.5`, score 740, 1 protein hit, 57% identity), and `TA:PUJ_000117` exhibits partial domain architecture homologous to non-ribosomal peptaibol assembly lines. Crucially, as established under **Audit Finding C1**, the TA-PUJ assembly is fragmented into 1,376 contigs and represents only ~55–60% completeness relative to the typical 40-Mb genome size of *T. asperellum*. Highly repetitive multi-modular NRPS condensation and adenylation domains frequently collapse during short-read assembly, breaking megasynthetases across contig boundaries or failing to assemble entirely. Therefore, computational non-detection cannot be interpreted as physiological absence. Direct analytical validation via LC-MS/MS—specifically monitoring for the diagnostic MS/MS neutral loss of aminoisobutyric acid (Aib, 85 Da)—is mandatory in Tier 5 wet-lab screening before declaring TA-PUJ deficient in peptaibol-mediated antagonism."""

sec8_2 = """#### 8.2 Auxin (Indole-3-Acetic Acid) Biosynthesis Gap Analysis in TA-PUJ
Auxin (indole-3-acetic acid, IAA) production is a primary mechanism whereby fungal biocontrol agents stimulate host plant root elongation, enhance lateral root branching, and increase nutrient absorption capacity in the rhizosphere. Previous preliminary reviews of TA-PUJ erroneously attributed definitive autonomous auxin biosynthesis to the isolate under confident tier designations without demonstrating the presence of the terminal enzymatic machinery.

Rigorous re-annotation of the Funannotate gene models reveals that isolate TA-PUJ possesses the conserved upstream shikimate/tryptophan biosynthetic pathway, as evidenced by two co-existing anthranilate synthase components: locus `TA:PUJ_001036` on `contig_356` (719 aa, harboring anthranilate synthase and indole-3-glycerol phosphate synthase domains, Pfam `PF00290` and `PF00291`, EC 4.2.1.20) and locus `TA:PUJ_001836` on `contig_693` (761 aa, harboring Pfam `PF00117`, `PF00218`, and `PF00697`). These loci mediate primary metabolic synthesis of L-tryptophan from chorismate.

However, neither the canonical indole-3-pyruvic acid (IPA) pathway nor the indole-3-acetamide (IAM) pathway could be unequivocally confirmed at the genomic level in TA-PUJ. Specifically, no candidate locus exhibited confident homology to fungal flavin-containing monooxygenases of the *YUCCA* family (EC 1.14.13.168), nor to stereospecific indole-3-pyruvate decarboxylases (*ipdC*, EC 4.1.1.74). Although four nitrilase-family enzymes (`PF02979`, EC 3.5.5.1) are present in TA-PUJ (`TA:PUJ_000676`, `TA:PUJ_002829`, `TA:PUJ_003006`, `TA:PUJ_003664`), their involvement in indole-3-acetonitrile (IAN) hydrolysis remains uncharacterized in this strain.

Consequently, plant growth promotion via auxin synthesis is downgraded to **Tier 3 (Literature & Secondary Inference)**. Autonomous IAA secretion must not be claimed as an established genomic feature. The development team must perform in vitro verification using the Salkowski colorimetric reagent on cell-free supernatants supplemented with 1–5 mM L-tryptophan, followed by confirmatory high-resolution LC-MS/MS quantification ($m/z$ 176.07 $[M+H]^+$) to establish whether TA-PUJ produces functional auxins in the rhizosphere."""

sec8_3 = """#### 8.3 Secondary Metabolite Profile Gaps & Trichoderma-Specific Screening Protocol
While *Trichoderma asperellum* is widely regarded as a beneficial biocontrol agent, species within the genus *Trichoderma* exhibit substantial strain-level divergence in secondary metabolite production. Notably, certain strains produce volatile pyrones (such as 6-pentyl-alpha-pyrone, 6-PP), viridiofungins, trichodermin, or sesquiterpene trichothecenes (e.g., harzianum A). Trichothecenes are ribosome-inactivating mycotoxins whose presence in agricultural inoculants poses ecotoxicological hazards to non-target soil fauna, livestock, and farm workers.

In isolate TA-PUJ, antiSMASH identified 21 biosynthetic gene clusters, 8 of which share similarity with characterized MIBiG references (including leucinostatin, metachelin, enniatin, trichobrasilenol, squalestatin, and equisetin). However, **13 of the 21 BGC regions (61.9%) are uncharacterized orphan clusters** lacking significant similarity to any known secondary metabolite cluster in public databases. Furthermore, due to the ~55–60% assembly completeness of TA-PUJ, an unknown number of secondary metabolic clusters may reside in unassembled genomic regions.

To guarantee agricultural safety and regulatory compliance for field deployment, the development team must execute a rigorous *Trichoderma*-specific metabolomic screening protocol before commercial pilot trials:
1. **Harzianum Acid & Polyketide Profiling:** Culture TA-PUJ on potato dextrose broth (PDB) and malt extract broth (MEB) for 14 days under light/dark cycling. Extract culture broth and mycelia with ethyl acetate; perform untargeted UHPLC-Q-TOF-MS to screen for harzianum acid ($m/z$ 403.2 $[M-H]^-$), koninginins, and related trichoderma polyketides.
2. **Trichothecene Pathway Intermediates Screen:** Perform targeted MRM LC-MS/MS against trichothecene standards (harzianum A, trichodermin, and trichodermol). Verify that TA-PUJ does not accumulate epoxytrichothecene intermediates under plant-associated or stressed growth conditions.
3. **Peptaibol Neutral-Loss MS/MS:** Screen methanolic mycelial extracts on high-resolution Q-Exactive MS/MS for diagnostic neutral loss fragments of 85.05 Da (2-aminoisobutyric acid, Aib) and 99.07 Da (isovaline, Iva), establishing the exact molecular diversity of linear peptaibols produced by this isolate.
4. **Volatile Compound Profiling:** Utilize solid-phase microextraction gas chromatography-mass spectrometry (SPME-GC-MS) to characterize volatile organic compounds (VOCs), quantifying 6-pentyl-alpha-pyrone (6-PP, $m/z$ 166) and brasilane sesquiterpenes produced during confrontation with soil pathogens."""

sec9 = """## 9. Comprehensive Methods Appendix & Computational Provenance

### 9.1 Primary Data Payloads & Cryptographic Integrity
The analyses presented in this document derive directly from the primary annotated genome files and antiSMASH secondary metabolism output records. Cryptographic SHA-256 checksums and exact file sizes are documented below to ensure absolute reproducibility:

| File Role / Description | Repository Path | Exact Size (Bytes) | SHA-256 Checksum |
| :--- | :--- | :---: | :--- |
| **TA-PUJ Structural Annotation** | `fungiSMASH-TA/input/Funannotate-annotated-genome-TA.gbk` | 45,029,346 | `c07f6c6e379fec380ce81551c82c8839a427cbdf683a6bd2dc92be52b291964f` |
| **TA-PUJ antiSMASH BGC Output** | `fungiSMASH-TA/Funannotate-annotated-genome-TA.gbk` | 44,880,695 | `b27db6f44d8fe3e7661558cc97a6ce08358b38d3647f9c3b3a5d91bfde44236f` |
| **AF-PUJ antiSMASH BGC Output** | `fungiSMASH-AF/Funannotate-annotated-genome-AF.gbk` | 83,318,907 | `d3fb74bf367092e66358abfd09dbdb4a6f44e5e9c1aceddd9e12dc508c106508` |

### 9.2 Software Pipeline & Computational Environment
- **BGC Prediction:** antiSMASH version 8.0.4 with strict detection rules, KnownClusterBlast against the MIBiG secondary metabolism database, SubClusterBlast, and ActiveSiteFinder enabled.
- **Structural & Functional Annotation:** Funannotate version 1.8.17 combining Augustus, GeneMark-ES, Pfam-A HMMs, and InterProScan functional domain signatures.
- **Parsing & Auditing Toolchain:** Biopython version 1.84 and Python 3.12 executed under Windows x86_64 runtime environment.
- **Automated Verification Suite:** Repository scripts `scripts/recount_families.py` (family recounting and signature verification) and `scripts/extract_bgc_inventory.py` (BGC inventory extraction).

### 9.3 Parsing Workarounds & Pfam Identifier Sensitivity
During initial data audits, standard automated parsing tools (such as `gbparse/io.py`) failed to detect certain protein families due to a regular expression case-sensitivity constraint:
```python
# Legacy parser pattern:
re.match(r'^(?:Pfam:)?(PF\d+)', val)
```
Because Funannotate generates uppercase cross-reference qualifiers formatted as `/db_xref="PFAM:PF00704"`, parsers expecting lowercase `Pfam:` silently omitted valid functional domains. In this revision, the audit pipeline utilizes direct parsing of raw `/db_xref` strings with case-insensitive matching (`PFAM:` and `Pfam:`), resolving all discrepancies and establishing the single source of truth in `scripts/recount_families.py`.

### 9.4 Functional Family Signature Sets
Enzyme family counts in the Master Validation Matrix (Section 1) are defined by the following signature sets:

| Functional Family | Query Pfam Identifiers | Query EC Numbers | InterPro Signatures | Recount Script Reference |
| :--- | :--- | :--- | :--- | :--- |
| **GH18 Chitinases** | `PF00704` | `3.2.1.14` | `IPR001223` | `scripts/recount_families.py` |
| **GH75 Chitosanases** | `PF03240` | `3.2.1.132` | `IPR004840` | `scripts/recount_families.py` |
| **Glutathione S-Transferases (GST)**| `PF02798`, `PF00043`, `PF13409`, `PF14497` | `2.5.1.18` | `IPR004045`, `IPR004046`, `IPR010981` | `scripts/recount_families.py` |
| **Laccases / Multicopper Oxidases** | `PF00394`, `PF07731` | `1.10.3.2` | `IPR001117` | `scripts/recount_families.py` |
| **Cytochrome P450s** | `PF00067` | — | `IPR001128`, `IPR002401` | `scripts/recount_families.py` |
| **ACC Deaminase Family** | `PF00291` | `3.5.99.7` | `IPR005965` | `scripts/recount_families.py` |
| **Terpene Cyclases / Synthases** | `PF19086`, `PF03936` | — | `IPR008949`, `IPR034686` | `scripts/recount_families.py` |
| **Nitrilase Family** | `PF02979` | `3.5.5.1` | `IPR003010` | `scripts/recount_families.py` |

### 9.5 MIBiG KnownClusterBlast Confidence Tiers
To prevent over-interpretation of automated database alignments, all BGC assignments are categorized into four standardized confidence tiers:
- **HIGH CONFIDENCE:** Requires $\ge$5 homologous gene hits in the target cluster AND $\ge$80% maximum amino acid identity to the characterized MIBiG reference. Indicates robust cluster orthology.
- **MEDIUM CONFIDENCE:** Requires 2 to 4 homologous gene hits OR 50% to 79% maximum amino acid identity. Indicates homologous or related biosynthetic machinery, though end-product structure may vary.
- **LOW CONFIDENCE:** Exhibits only 1 homologous gene hit OR <50% maximum amino acid identity. Indicates domain-level similarity or shared tailoring enzymes, requiring experimental structural confirmation.
- **ORPHAN (UNASSIGNED):** Zero significant KnownClusterBlast hits to any characterized MIBiG reference. BGC is predicted solely based on antiSMASH signature profile rules (e.g., presence of core NRPS, PKS, or terpene synthases).

### 9.6 Methodological Boundaries: Analyses NOT Run
To maintain strict scientific transparency, the following analyses were **not performed** during this review and represent prospective avenues for further investigation:
1. **De Novo BUSCO Genome Completeness Assessment:** BUSCO was not re-run on the raw FASTA assemblies. The ~55–60% completeness estimate for TA-PUJ is derived by comparing assembly length (23.9 Mb) and gene count (6,009) to reference *T. asperellum* genomes (~40 Mb, ~11,000–12,000 genes).
2. **Dedicated dbCAN / HMMER CAZy Re-Annotation:** Glycosyl hydrolase and carbohydrate-active enzyme counts were extracted from existing Funannotate Pfam and EC annotations, without a dedicated run of the dbCAN3 meta-server.
3. **External BLAST Searches Against NCBI nr / Swiss-Prot:** Hypothetical proteins and orphan BGC genes were not subjected to exhaustive remote BLAST searches against the complete NCBI non-redundant database."""

sec10 = """## 10. Audit Findings & Traceability Change Log (V5 -> V6)

This revision represents a comprehensive overhaul from V5 to **AGRI-BIOCONTROL-GENOMIC-SCRUTINY-V6**, resolving all 24 findings identified during the external genomic audit (`audit-findings-agriculture-support-biocontrol-review.md`):

| Finding ID | Finding Classification | Summary of Issue Identified in V5 | Resolution Implemented in V6 | Review Section(s) |
| :---: | :---: | :--- | :--- | :---: |
| **C1** | **Critical** | TA-PUJ assembly is partial (~55–60% completeness), yet absence claims were treated as definitive | Added Assembly Completeness Assessment caveats; restricted negative claims; updated Data Provenance Box | Preamble, §0, §0.1, §5, §8 |
| **C2** | **Critical** | Absolute claims of complete absence of secondary toxins in TA-PUJ overlooked 13 orphan BGCs | Caveated all absence claims; detailed 13 orphan BGCs; instituted Trichoderma metabolite screening protocol | Exec Summary, §1, §4, §7A, §8.3 |
| **C3** | **Critical** | 5,098 locus tags collide between TA-PUJ and AF-PUJ (`PUJ_000001`–`PUJ_006009`), causing ambiguity | Mandated strict isolate prefixing (`TA:PUJ_xxxxx` vs. `AF:PUJ_xxxxx`) throughout all text, tables, and gene models | Throughout (§1, §2, §3, §4, §5, §8) |
| **C4** | **Critical** | 3-Nitropropanoic acid (`703_c2`) toxigenic BGC in AF-PUJ was omitted from biosafety review | Added 3-NPA as 5th toxigenic BGC; incorporated into biosafety alert, comparison table, and LC-MS/MS panel | §4, §5, §6, §7B |
| **M1** | **Major** | AF BGC inventory was truncated to 5 rows, obscuring 40 orphan BGCs and multiple secondary clusters | Expanded Section 7B to full 74-region inventory; declared 40 unassigned orphan BGCs explicitly | §7B |
| **M2** | **Major** | TA BGC inventory omitted 13 uncharacterized orphan clusters (rows 9–21 grouped as "Various") | Expanded Section 7A to full 21-region inventory; documented all 13 orphan BGC coordinates and types | §7A |
| **M3** | **Major** | Enzyme family counts in Section 1 conflicted with signature sets (e.g., GST 34 vs 18; CuOx 2 vs 7) | Re-counted all families using `scripts/recount_families.py`; validated exact counts against `family_counts.json` | §1, §2, §5, §9.4 |
| **M4** | **Major** | Aflatoxin cluster identity claims (75–100%) were inaccurate; AflR is 94%, PksA is 97% | Updated identity ranges to 51–97% for `BGC0000007.3`; cited secondary hit `BGC0000008.3` (99–100%) | Exec Summary, §3, §4, §7B |
| **M5** | **Major** | Aflatoxin cluster table contained unverified EC numbers not present in Funannotate records | Verified EC annotations against GBK records; corrected `nor-1` and `aflR` EC assignments | §3 (Aflatoxin Table) |
| **M6** | **Major** | ACC deaminase table included candidate `AF:PUJ_008483` without InterPro `IPR005965` verification | Explicitly noted `AF:PUJ_008483` lacks `IPR005965` signature; confirmed 0 verified ACC deaminases in AF | §1, §3, §5 |
| **M7** | **Major** | Siderophore operon locus coordinates and identities were misattributed | Corrected NIS synthetase to `AF:PUJ_004419` (797 aa); noted 0 MIBiG hits (domain prediction only) | §3, §4, §7B |
| **M8** | **Major** | Peptaibol absence claims failed to evaluate largest NRPS `TA:PUJ_000117` or secondary AbT1 hit | Added Section 8.1 dedicated peptaibol gap analysis; mandated Aib neutral-loss MS/MS screening | §8.1, §6 |
| **M9** | **Major** | Auxin (IAA) biosynthesis was over-interpreted as proven genomic trait | Re-tiered IAA to T3 literature inference; detailed anthranilate synthases; mandated Salkowski assay | §1, §5, §8.2 |
| **m1** | **Minor** | Brasilane sesquiterpene synthase locus coordinates were inverted | Corrected `TA:PUJ_005301` coordinates to 11,954..13,395 bp on `contig_1813` | §1, §2, §3, §5 |
| **m2** | **Minor** | Glucanase counts conflicted between Section 1 (8) and Section 5 (1) | Reconciled glucanase count to 1 EC-annotated glucanase in TA (`TA:PUJ_002476`, EC 3.2.1.39) | §1, §5 |
| **m3** | **Minor** | Phosphatase count in AF was ambiguous (6 loci in PHO regulon vs. 179 total across genome) | Clarified genome-wide total (179 phosphatases) vs. co-clustered PHO regulon loci (6 loci) | §1, §3, §5 |
| **m4** | **Minor** | Aflatoxin scaffold 1340 length was inaccurately cited | Corrected scaffold 1340 length to exact 135,160 bp | §3 (Cluster Narrative) |
| **m5** | **Minor** | CPA cluster reference lacked specific MIBiG identifier and gene count | Updated CPA reference to `BGC0000977.4` (4 gene hits, 90–97% identity, score 9,573) | §3, §4, §7B |
| **m6** | **Minor** | Aspirochlorine hit metrics lacked exact gene count and identity | Updated to `BGC0001123.5` (19 gene hits, 94–100% identity, score 17,383) | §4, §7B |
| **m7** | **Minor** | Aspergillic acid hit metrics lacked exact gene count and identity | Updated to `BGC0001516.5` (6 gene hits, 75–100% identity, score 6,227) | §4, §7B |
| **m8** | **Minor** | Document version header was outdated (V5) | Bumped document header to `AGRI-BIOCONTROL-GENOMIC-SCRUTINY-V6` | Header |
| **m9** | **Minor** | File provenance, sizes, and file paths were undocumented | Added Data Provenance Box at top of document and Methods Section 9.1 | Preamble, §9.1 |
| **m10** | **Minor** | Evidence confidence tiers lacked formal operational definitions | Formalized Confidence Tier Legend ([T1] to [T4]) and MIBiG tiers (HIGH/MED/LOW/ORPHAN) | Header, §7, §9.5 |
| **m11** | **Minor** | Database attributions and licensing notices needed retention and standardization | Retained and expanded comprehensive attribution notices for InterPro, UniProt, NCBI, and MIBiG | §11 |"""

sec11 = """## 11. Database Attributions & Licensing Notices

As required by scientific reproducibility standards, institutional data governance, and skill guidelines:
- **EBI InterPro Database:** Terms and licensing available at [https://www.ebi.ac.uk/interpro/](https://www.ebi.ac.uk/interpro/) and [https://www.ebi.ac.uk/about/terms-of-use/](https://www.ebi.ac.uk/about/terms-of-use/).
- **UniProt Knowledgebase (UniProtKB):** Terms and licensing available at [https://www.uniprot.org/help/license](https://www.uniprot.org/help/license).
- **NCBI Entrez Databases:** Terms and data policies available at [https://www.ncbi.nlm.nih.gov/home/about/policies/](https://www.ncbi.nlm.nih.gov/home/about/policies/).
- **antiSMASH 8.0.4 & Funannotate 1.8.17:** Used for underlying BGC identification and structural annotation.
- **MIBiG (Minimum Information about a Biosynthetic Gene cluster):** Reference database for all BGC compound assignments. MIBiG accession numbers cited throughout."""

# Build full replacement content for Section 7 to end
full_sec7_to_end = f"""## 7. Comprehensive BGC Inventory & MIBiG Evidence Summary

> [!NOTE]
> **MIBiG Confidence Tiers:** BGC assignments are graded as **HIGH** (>=5 gene hits AND >=80% max identity), **MEDIUM** (2–4 gene hits OR 50–79% identity), **LOW** (1 gene hit OR <50% identity), or **ORPHAN** (0 KnownClusterBlast hits; predicted purely by antiSMASH core profile rules). Confidence reflects the strength of the KnownClusterBlast match, not necessarily physiological production capacity, which requires wet-lab verification.

{bgc_tables_text}

---

## 8. Coverage Gaps & Biosynthetic Limitations

{sec8_1}

---

{sec8_2}

---

{sec8_3}

---

{sec9}

---

{sec10}

---

{sec11}
"""

with open(os.path.join(BASE_DIR, "phase5_replacement.md"), "w", encoding="utf-8") as out:
    out.write(full_sec7_to_end)

print("Successfully wrote phase5_replacement.md")
print(f"Length of phase5_replacement.md: {len(full_sec7_to_end)} chars, {len(full_sec7_to_end.splitlines())} lines")
