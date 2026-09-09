# Formal Audit Report for PUJ-fungi `TA-viz/` + `AF-viz/` Visualization and Scientific Catalogs

**Repository**: `https://github.com/WhyAdr/PUJ-fungi` (main) · **Audit date**: 2026-09-09 · **Audit tools**: gbparse / Biopython / custom cross-validation scripts (`/home/z/my-project/scripts/`)
**Audit scope**: All PNG/SVG figures in TA-viz (*Trichoderma asperellum* TA-PUJ, 24 clusters) and AF-viz (*Aspergillus flavus* AF-PUJ, 77 clusters), both README catalog tables, and their ground-truth consistency with the source data (`fungiSMASH-TA/`, `fungiSMASH-AF/`, annotated whole-genome GBK files, and neighborhood JSON files).

---

## 1. Overall Assessment

| Directory | Assessment | One-sentence conclusion |
|---|---|---|
| **TA-viz** | **Conditional Pass** | Figures and tables are 100% consistent with the archived data; defects are concentrated in the gene-detail bullet text: 19 bullets contain Pfam/EC/length claims that conflict with the archive (affecting 8 clusters), and the directory can be upgraded to Pass once the wording is corrected. |
| **AF-viz** | **Conditional Pass** | The figure and table foundation is solid (all 101 graphical acceptance checks passed; 0 coordinate errors in the main table), but three mandatory correction classes remain: ① clusters 75–77 use 0-based start coordinates; ② four gene symbols on the left flank of the aflatoxin cluster (BGC_71) conflict with their own archived domain evidence, suggesting a systematic assignment shift; ③ the Executive Summary claim of “21 loci / 94–97% identity” conflicts with the archive and has propagated into the CAUTION biosafety statement. |

The **biosafety dichotomy in both directories—the boundary between statements about characterized toxin clusters and agronomically beneficial functions—has been strictly maintained**, and no experimental procedures were found that would operationalize toxin production.

---

## 2. Audit Methods and Data Sources

1. **Ground-truth construction**: Biopython was used to parse `fungiSMASH-TA/*.region*.gbk` (21 regions) and `fungiSMASH-AF/*.region*.gbk` (74 regions), extracting for every CDS the 1-based coordinates, strand, amino-acid length, EC annotations, and all `db_xref` Pfam entries (including both `PFAM:`-prefixed and bare `PFxxxxx.NN` formats, plus sec_met domain features). Funannotate-annotated whole-genome GBKs were then parsed to construct TA/AF genome-wide gene indices, used for the manually curated microclusters 22–24 / 75–77. Critical coordinates were manually checked line-by-line against the original GBK feature locations (e.g., the ground-truth 1-based coordinates for `PUJ_000714` are 273,772..275,470).
2. **README parsing**: Structured extraction of the main catalog tables from both READMEs, 95 antiSMASH cluster gene tables + 6 microcluster gene tables, all bullet sections, figure links, and anchors.
3. **Cross-validation**: Coordinates (1-based), strand, aa length, CDS counts, within-cluster gene order (collinearity), EC subsets, two-layer verification of Pfam claims, type labels, Executive Summary numbers, and spot checks of neighborhood JSON fidelity (63 TA + 105 AF records).
4. **Graphical acceptance testing**: Completeness, 300 DPI, and non-empty status of 101 PNG/SVG file pairs; programmatic inspection of all 101 SVGs (`#f8f9fa` raised label boxes, `#555555` leader lines, `#b05d1a` span brackets, bracket text containing kb + CDS counts, and label nomenclature); plus manual visual inspection of 7 representative PNGs (TA-01 equisetin, TA-12 cryptosporioptide B, TA-23 iron uptake, AF-01 orphan betalactone, AF-04 asparasone A, AF-71 aflatoxin/CPA supercluster, AF-75 phosphate-solubilization microcluster).
5. **Scientific review**: Pathway architecture, catalytic-mechanism statements, spot-checking of references (10 papers), and boundaries of biosafety language.

---

## 3. Validation Matrix

| Validation item | TA-viz | AF-viz | Assessment |
|---|---|---|---|
| Complete PNG/SVG file pairs (24+77 clusters) | 24/24 | 77/77 | ✅ PASS |
| PNGs non-zero-byte, 300 DPI; vector SVGs valid | 0 defects | 0 defects | ✅ PASS |
| All README image/vector links resolve | 48/48 | 154/154 (231 references) | ✅ PASS |
| Anchor navigation (explicit `<a id>` anchors) | 24/24 resolved | 77/77 resolved | ✅ PASS |
| Label-box style: `#f8f9fa` background + gray outline | present in 24/24 SVGs | present in 77/77 SVGs | ✅ PASS |
| Leader lines `#555555`, span brackets `#b05d1a` | 24/24 | 77/77 | ✅ PASS |
| Brackets contain physical span (kb) + CDS count | 24/24 (e.g., “equisetin cluster (10 CDSs, 44.8 kb)”; measured gene span 480..45,230 = 44.75 kb ✔) | 77/77 (e.g., “aflatoxin / cyclopiazonic acid super-cluster (17 CDSs, 77.8 kb)” ✔) | ✅ PASS |
| Zero white-on-white text / zero font clipping / zero label overlap (7 manual inspections + structural checks of all SVGs) | Pass | Pass | ✅ PASS |
| Nomenclature: characterized loci use canonical one-line symbols (afl/cpa/acd/eqx/fet/ftr/pho/iuc/asa/acl); orphan loci use plain `PUJ_xxxxxx` | Symbol families = eqx/acd/fet/ftr + known flanking gene names (erg7, rho1, perA, etc.); 0 README↔figure-label mismatches | Symbol families = afl/cpa/acl/asa/iuc/pho + known flanking names; 0 README↔figure-label mismatches | ✅ PASS (but the **assignment targets** of 4 symbols within AF-71 are incorrect; see F2) |
| Main catalog table: coordinates/span/CDS count vs. ground truth | 0 errors (24/24 rows) | Clusters 1–74: 0 errors; **clusters 75–77 use 0-based starts (63 genes + 3 cluster-span starts)** | ⚠️ AF FAIL→F1 |
| Gene tables: coordinates/strand/aa length/EC vs. ground truth | 0 errors (all 24 tables) | Clusters 1–74: 0 errors; clusters 75–77: each of 63 starts is off by 1 | ⚠️ Same as above |
| Two-layer verification of Pfam claims in gene tables (regional GBK ↔ whole-genome InterProScan) | Table-listed Pfams are 100% consistent with regional GBKs | Same as left (the 119 “unverifiable” calls in the initial audit were due to the parser missing sec_met features; after correction, **119/119 are supported in the regional GBKs**) | ✅ PASS |
| Collinearity: README gene order vs. antiSMASH region gene order | 0 mis-orderings | 0 mis-orderings | ✅ PASS |
| Type labels vs. antiSMASH products | All 74 display-name differences are documented editorial conventions (“Orphan X” prefix + MIBiG compound names) | Same as left | ✅ PASS (convention is reasonable) |
| Microclusters (manually curated neighborhoods) | Clusters 22–24: correctly 1-based, 0 errors | Clusters 75–77: 0-based starts | ⚠️ F1 |
| Figure header consistency with catalog numbers | Pass (header = regional span 53,953 bp; bracket = gene span 44.8 kb; both semantics are explicitly defined by the V3 plan) | Clusters 1–74 pass; cluster 75–77 header starts inherit 0-based coordinates | ⚠️ F1 |
| Executive Summary numbers | (TA has no Executive Summary section; see O2) | “21 continuous loci PUJ_009383–009403” is actually **17 CDSs (PUJ_009389–009405)**; “94–97%” is actually KCB **51–97% (11 proteins)** | ❌ F4 |
| Pathway/mechanistic narrative vs. archive | BGC_12 bullets conflict with the archive (3 items) | BGC_71 left-flank symbols are shifted; cpaO/cpaD are conflated; cpaH lacks domain evidence; etc. | ❌ F2/F3/F5 |
| Fidelity of neighborhood JSON intermediates | Spot-check of 63 records: coordinates are 0-based half-open (start−1); 0 strand/length errors | 105 records: same as left | ⚠️ F6 (intermediate-data convention) |
| Biosafety dichotomy | Biological content is restricted to an anti-phytopathogen framing, with no mammalian-virulence-enabling content | CAUTION block explicitly disqualifies AF-PUJ from uncontained agricultural use; WARNING block flags aspergillic-acid hepatotoxicity; no toxin-production procedures found | ✅ PASS |
| Reference spot-check | Skory 1992, Meyers 1998, Zhou & Linz 1999, Yu 2004, etc. are genuine and appropriately cited | Georgianna & Payne 2009, Ehrlich 1999/2014, Chang 1995, Crawford 2006, Clevenger 2017, Townsend 2014, etc. are genuine | ✅ PASS |

---
## 4. Discrepancy Log (Ordered by Remediation Priority)

> Severity: 🔴 Mandatory fix (affects factual correctness) / 🟡 Should fix (affects verifiability and consistency) / 🟢 Recommendation (improves standardization)

### 🔴 F1 · Systematic 0-based Coordinates in AF-viz Clusters 75/76/77 (Microclusters)
- **Observation**: The **start coordinates in the README gene tables and figure headers are uniformly 1 bp lower than the ground truth** (end coordinates are correct). Example: the table reports `PUJ_000714` as `273,771..275,470`, whereas the Funannotate GBK ground truth in 1-based coordinates is `273,772..275,470` (individually confirmed with Biopython against the original feature location `join{[273771:274043],[274275:275470]}(+)`). Across the three clusters, **63 CDS starts** + 3 cluster-span starts (`273,771→273,772`, `778,829→778,830`, `208,818→208,819`) are affected; the headers of the corresponding three `CLUSTER_7x_*.png/svg` figures are affected as well.
- **Root cause**: The tables and figures for clusters 75–77 were generated directly from `neighborhood_af.json` (0-based half-open intervals) without applying the `+1` conversion, whereas clusters 1–74 use the antiSMASH regional GBK (1-based) pipeline. TA microclusters 22–24 are unaffected because their pipeline performs the conversion correctly.
- **Remediation steps**:
  1. In the AF README generation script, add `+1` to every start column in tables 75–77 (leave end coordinates unchanged).
  2. Correct the header spans in the three figures (`273,772–342,848` / `778,830–880,781` / `208,819–273,028`) and re-render PNG+SVG.
  3. After correction, automatically verify that start1/end1 in all 101 cluster tables exactly match the ground truth.
- **Affected scope**: Three tables in AF-viz/README.md and 3 figure pairs; clusters 1–74 are unaffected.

### 🔴 F2 · AF-viz BGC_71 (Aflatoxin/CPA Supercluster): Left-Flank Gene-Symbol Assignments Conflict with Their Archived Domains (Likely Symbol-Chain Shift)
The Pfams listed in the README tables (which exactly match the regional GBK) are incompatible with the gene families asserted by the bullet text/figure labels:

| Locus | Archived domain/EC (ground truth) | README symbol and bullet claim | Conflict |
|---|---|---|---|
| PUJ_009389 (742 aa) | **PF00067 P450** + PF00106 + PF08659 + PF13561 | `aflJ` (“aflJ/estA-associated, PF00135”) | aflJ is a small esterase-like protein, not a P450; even the Pfam number claimed in the bullet conflicts with the table. |
| PUJ_009390 (388 aa) | **PF00248 aldo-keto reductase (AKR)** | `aflV` (“cypX P450, EC 1.14.14.1, PF00067”) | cypX must contain PF00067; the archive instead shows an AKR (characteristic of the nor family). |
| PUJ_009391 (308 aa) | **PF07859 α/β hydrolase** + EC 3.1.1.94 (esterase) | `ver-1` (“aflM SDR, PF00106”) | ver-1/aflM is an SDR; an α/β hydrolase + esterase EC is characteristic of an **estA/aflJ-type** protein. |
| PUJ_009392 (278 aa) | **PF00106 SDR** + EC 1.1.1.352 | `estA` (“esterase, PF00135, EC 3.1.1.1”) | SDR + 1.1.1.352 is precisely a **ver-1/aflM-type** signature; it is the opposite of estA. |

- **Diagnosis**: The symbols assigned to PUJ_009391 and 009392 appear to be **pairwise swapped** (estA↔ver-1); 009389/009390 may be collectively shifted one position to the right. KnownClusterBlast (BGC0000007.3, 11 proteins at 51–97%) supports this region as an aflatoxin cluster (pksA=PUJ_009397 at 97%, aflT=PUJ_009398 at 97% MFS, aflR=PUJ_009393 with PF00172, etc.; the middle/right-side symbols are consistent with the archive), so the error is confined to the four left-flank genes.
- **Remediation steps**:
  1. BLASTP each locus against the KCB reference proteins: PUJ_009389↔AAS90009.1, 009390↔AAS90007.1, 009391↔AAS90006.1, 009392↔AAS90005.1; then reassign symbols according to the reference gene names.
  2. At minimum, first swap 9391↔9392 (estA↔ver-1), and change the symbols and bullets for 9389/9390 to domain-consistent families (P450 family / AKR family).
  3. Synchronize the four labels in the BGC_71 figure, the “Gene Symbol” table entries, the bullet text, and cascade descriptions such as `AflV (P450)` and `EstA (esterase)` in “Collective Pathway Architecture”.
  4. Cross-check every symbol change against the MIBiG BGC0000007.3 gene-name table.

### 🔴 F3 · Systematic “Narrative-vs.-Archive” Conflicts at the Bullet Layer: 54 Across Both READMEs (TA 19 / AF 35)
Programmatic auditing (`scripts/audit_bullets.py`; ground truth = all regional GBK features + whole-genome annotation) found:
- **40 Pfam claims** are absent from the archived domain set for the corresponding gene. Major hotspots:
  - AF **iuc family** (PUJ_004414–004426, siderophore cluster), 13 cases: bullets imported PF00583/PF00743/PF00117, etc. from aerobactin literature, while the archived domains are entirely different (e.g., 004418 archive = PF02668, bullet = PF00743). **The suitability of the symbol system itself (iucA–Y) for the archived evidence therefore also requires re-evaluation.**
  - AF **asa family** (PUJ_009781–009786), 4 cases, and **acl family** (aclT/aclC/aclN/aclB), 4 cases: same class of problem.
  - TA equisetin cluster: `eqx7` (bullet PF00106 vs. archive PF00891), `eqx4` (PF00067 vs. PF00155), `eqx2` (PF08787 vs. PF00107/PF08240), plus one case each in the flanking genes `erg7/perM/perO/perT/pex29/pom1/caj1/mchT/rtg2`.
  - TA BGC_12: the `dmxR12` bullet says “PF00891 SAM methyltransferase”, whereas both the archive and the table list **PF00106 SDR** (the table is correct; the bullet is wrong); the `crpB` bullet claims PF00144, while the archive contains no domain annotation at all.
- **8 EC claims** are absent from the archive: 5 of them are genuine literature-derived values (e.g., `fet3` EC 1.16.3.1 ferroxidase, `iucD` EC 1.14.13.59, `iucB` EC 2.3.1.102), representing “literature enrichment without archival support” and therefore requiring explicit provenance labels; `bts1` EC 2.5.1.29 and `gh31` EC 3.2.1.20 fall into the same category.
- **6 amino-acid-length conflicts**: `eqx1` (bullet 3,972 vs. archive 3,931), `perA` (2,120 vs. 1,054; the bullet used the *Aspergillus nidulans* reference length), `crpA` (2,150 vs. 1,382; same reason), `aclN` (457 vs. 422), `asaB` (502 vs. 519), and `asaD` (532 vs. 428). **The bullet text directly copied literature/homolog values without reconciling them to the actual local CDSs**; all lengths in the README tables are correct.
- **Pattern**: The README table layer is 100% faithful to the archive; all errors occur in the rhetorical bullet layer, where literature-derived data were not reconciled to local CDSs or domain identifiers were simply asserted without archival evidence.
- **Remediation steps**:
  1. **Regenerate** every evidence-bearing clause in the bullets from archived domains/ECs/lengths; literature-derived values must be explicitly labeled (e.g., “(literature, *A. nidulans* PerA)”).
  2. Perform BLASTP verification of symbol assignments for the iuc/asa/acl families before revising the prose.
  3. Add a CI validation script requiring every PF/EC/aa value in bullet text either to match the archived value or to be explicitly marked as divergent/literature-derived (`audit_bullets.py` can be reused directly).

### 🔴 F4 · Numerical Errors in the AF Executive Summary and CAUTION Block (Already Propagated into the Biosafety Statement)
- “21 continuous loci across 79.1 kb (`AF:PUJ_009383`–`AF:PUJ_009403`)”: antiSMASH region `1340.region001` (79,127 bp) actually contains **17 CDSs (PUJ_009389–PUJ_009405)**; `PUJ_009383–009388` are six upstream non-cluster genes in the region (PF00891×2, PF13460, PF08592, PF00067, PF14087), while `PUJ_009404/009405` were omitted.
- “with 94–97% identity to MIBiG `BGC0000007.3`”: the KCB archive reports **51–97% (11 proteins)**; only the cluster-detail section correctly states “Identity: 51–97%”. The CAUTION-block statement “all 21 genes ... with 94–97% identity” inherits both errors.
- **Remediation**: Standardize the Executive Summary and CAUTION block to: “17 CDSs (`PUJ_009389`–`PUJ_009405`); 11 protein BLAST hits to BGC0000007.3, with 51–97% identity (94–97% for core enzymes).” The biosafety conclusion itself—that AF-PUJ possesses the complete genetic basis for toxin production and is disqualified from uncontained use—**is unaffected**, because the presence of key genes such as aflR/pksA/cpaA and their 96–97% identities are firmly supported.

### 🟡 F5 · Detailed Errors in the BGC_71 Pathway Narrative
- “FAD-dependent oxidoreductase `CpaO` (DMATS)”: **cpaO is not DMATS** (DMATS = dimethylallyl transferase, encoded by **cpaD**). The bullet phrase “cpaO / cpaD” similarly conflates the two. It should be changed to “CpaO (FAD oxidoreductase); cpaD (DMATS) is not annotated in this region”, unless a cpaD locus is subsequently confirmed by BLAST.
- “Late-stage tailoring by two O-methyltransferases (`AflP`, `AflO`)”: among the 17 CDSs in this region, **none is annotated as an O-methyltransferase** (no CDS carries PF00591/PF08242 or equivalent domains). The pathway narrative exceeds the support provided by its own data and should instead state: “OmtA/OmtB homologs were not detected, indicating that additional HMMER/BLAST analysis is required or that pathway incompleteness must be acknowledged.”
- The `cpaH` (PUJ_009403) bullet claims PF00067 (P450), but the archive contains no domain annotation—another F3-class “unsupported domain claim”. Directly assigning a 395-aa domainless protein as a P450 has low confidence and should be verified by BLASTP against a BGC0000977 reference.

### 🟡 F6 · `neighborhood_ta.json` / `neighborhood_af.json` Use 0-based Half-open Coordinates
- All 168/168 spot-checked records show start−1 (with 0 errors in end coordinates, strand, or aa length). The intermediate representation itself may legitimately use 0-based coordinates, but both READMEs either state or are required to use 1-based coordinates, and the AF 75–77 tables directly propagated the intermediate values, causing F1.
- **Remediation**: Explicitly document the JSON coordinate convention (0-based half-open) in `ANALYSIS_SCRIPTS_AND_INTERMEDIATE_NOTES.md`, and enforce `+1` at the README-generation layer.

### 🟡 F7 · README Does Not Declare the Coordinate Convention
Neither README (nor the figure captions) explicitly states “all coordinates are 1-based inclusive on the <contig/scaffold>”. The absence of this sentence is precisely what allowed F1 to survive silently. Add a coordinate-convention declaration to the metadata at the top of each README.

### 🟢 O1 · AF Identifier “scaffold_24” vs. Assembly LOCUS “24”
The actual record name in antiSMASH/the assembly is `24` (LOCUS line: `LOCUS 24 2350691 bp`), while the README/figures consistently display `scaffold_24`. This is a presentation convention and does not hinder lookup, but the README should state “scaffold_NN = assembly record NN”.

### 🟢 O2 · TA-viz Lacks an “Executive Biosafety & Agricultural Evaluation” Section Symmetric with AF-viz
TA contains several strongly bioactive compounds (equisetin is a mitochondrial ATPase inhibitor; trichobrasilenol is a pore-forming cyclic depsipeptide, etc.), but these are only mentioned piecemeal within individual cluster descriptions. Add a summary section defining human/animal/environmental safety boundaries, aligned in strength with the AF-viz statement. This is not a compliance defect, but a consistency improvement.

### 🟢 O3 · Semantics of Figure Header Span vs. Bracket Span
The figure header “Span: 1–53,953 bp” (regional window) coexists with the bracket “44.8 kb” (physical CDS span). Measurement confirms that both are correct and consistent with the V3 plan (bracket = physical span of the subtrack). Clarify the meaning of the two spans in the figure caption to prevent readers from mistaking them for an inconsistency.

---
## 5. Free Review (Findings Outside the Checklist)

1. **Overall figure quality is publication-grade**: None of the 7 manually inspected samples (covering characterized clusters, orphan clusters, microclusters, and a supercluster) showed white-on-white text, font clipping, or label overlap. Leader-line lengths are restrained, and color semantics (red = core synthase/target enzyme, orange = tailoring enzyme, green = transport/efflux, purple = regulation, blue = uncharacterized) are consistent across the entire library. SVGs are rendered by matplotlib as vector glyph paths with `<!-- symbol -->` comments and are therefore machine-parseable; this audit used that property to verify nomenclature across 1,838 labels.
2. **Type-label conventions are reasonable and self-consistent**: The README uses the “Orphan X” prefix for clusters without MIBiG hits (strictly corresponding to the catalog’s “Orphan (No MIBiG match)” field) and uses MIBiG compound names (asparasone A, heptelidic acid, etc.) for characterized homologous clusters. All 74 literal differences from antiSMASH product strings are explained by this convention and do not constitute ground-truth errors.
3. **Functional curation of the microclusters is credible**: Symbols in TA-23 (fet3/ftr1/fre1 high-affinity iron uptake, T1_VERIFIED) and AF-75 (pho13/ipp1 phosphate-solubilization neighborhood) are consistent with archived domain/product annotations. All symbols in this subsection were rechecked against domain evidence and are correct; the coordinate issue described in F1 is the only defect.
4. **Numerical-consistency spot checks passed**: AF whole genome = 61 scaffolds / 36.6 Mb; TA contig count and total length; per-cluster CDS counts; and MIBiG scores and identity ranges in the cluster-detail sections all match values recalculated from the archive. The cumulative score of 16,946.0 for `BGC0000007.3`, for example, matches the original KCB output directly.
5. **Reference spot-check: 10/10 genuine**: Skory et al. 1992 (ver-1), Meyers et al. 1998 (aflJ), Zhou & Linz 1999 (nor-1), Yu et al. 2004 (cluster sequencing), Georgianna & Payne 2009, Ehrlich et al. 1999 (aflR binding sites), Chang et al. 1995, Crawford et al. 2006 (PksA SAT domain), Clevenger et al. 2017 (CPA cluster), and Townsend 2014. Sources, authors, arguments, and cited claims all match.
6. **V6 audit-version PDF/PPTX review artifacts are present in the repository root**: Their conclusions are consistent with the data layer of this report, but the PDF predates the current F1–F5 findings; update its version number in parallel with remediation.

## 6. Remediation Priority and Basis for Assessment

| Priority | Item | Estimated effort | Blocks upgrade to Pass? |
|---|---|---|---|
| P0 | F1 (AF 75–77 coordinates +1 and re-render 3 figure pairs) | ~0.5 day | Yes (AF) |
| P0 | F2 (reassign BGC_71 left-flank symbols + synchronize figure/table/bullets) | ~1 day (including BLAST confirmation) | Yes (AF) |
| P0 | F4 (correct Executive Summary/CAUTION numbers) | ~0.2 day | Yes (AF) |
| P1 | F3 (regenerate 54 evidence-bearing bullet statements + verify iuc/asa/acl symbols) | ~2–3 days | TA requires only the 19 TA-side items to reach Pass; AF requires the 35 AF-side items |
| P1 | F5 (correct cpaO/cpaD, AflP/AflO, cpaH narrative) | ~0.3 day | No (but strongly recommended alongside F2) |
| P2 | F6/F7/O1/O2/O3 | ~0.5 day | No |

**Summary of assessment basis**: The objective data layer of both directories (coordinates, strand, length, EC, table-listed Pfam, gene order, figure completeness, nomenclature consistency, anchors/links, and the biosafety dichotomy) passed with **0 defects or a demonstrated 100% consistency rate**. Defects are concentrated in the **narrative/rhetorical layer** (bullets/summary) and **a single pipeline coordinate-convention issue** (AF microclusters). All are localized and mechanically correctable and do not overturn any cluster-level conclusion, including identification of the aflatoxin/CPA supercluster or its biosafety interpretation. Both directories are therefore rated **Conditional Pass**; AF-viz can be upgraded to Pass after the three P0 items are completed, while TA-viz can be upgraded after its F3-side corrections are completed.

---

## Appendix A · Audit Artifact Inventory (Re-runnable)

| File | Purpose |
|---|---|
| `scripts/index_genomes.py` / `genome_index.json` | Genome-wide gene index (ground truth) |
| `scripts/extract_ground_truth.py` / `gt_regions.json` | antiSMASH regional ground truth (CDSs/order/products) |
| `scripts/parse_readmes.py` / `readme_parsed.json` | Structured parsing of both READMEs |
| `scripts/crosscheck_v2.py` / `discrepancies_v2.json` | Full table-layer cross-validation of coordinates/strand/length/EC/Pfam (final version: the only remaining hard differences are type-label conventions) |
| `scripts/verify_micro_and_claims.py` / `discrepancies_micro.json` | Microcluster/Executive Summary/neighborhood JSON validation (294 raw flags; see F1/F4/F6 after classification) |
| `scripts/verify_pfam_v2.py` | Two-layer Pfam validation after parser correction (119/119 supported) |
| `scripts/audit_bullets.py` / `bullet_issues.json` | Full list of 54 bullet-layer conflicts (complete evidence for F3) |
| `scripts/audit_file_integrity.py` / `integrity_report.json` | Integrity of 101 PNG/SVG pairs (0 defects) |

## Appendix B · Sampling and Coverage Statement

- **Manual figure inspection**: 7/101 PNGs (TA 3, AF 4; covering characterized/orphan/microcluster/supercluster/iron-uptake/phosphate-solubilization categories) + programmatic acceptance testing of 101/101 SVGs.
- **Coordinate ground truth**: Full gene-by-gene comparison of 95 antiSMASH cluster tables (TA 21 + AF 74; ~1,470 CDSs total) and all 6 microcluster tables (126 CDSs); disputed critical points (`PUJ_000714`, `PUJ_009389–009405`) were additionally checked manually against the original GBK feature locations.
- **Nomenclature**: Full parsing of 1,838 SVG labels + bidirectional README↔figure comparison (0 mismatches).
- **Literature**: 10 references spot-checked (all genuine; claims matched); remaining references were not individually verified.
