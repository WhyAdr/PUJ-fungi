# Independent Audit: `agriculture-support-biocontrol-fungal-isolate-review.md` (V5)

**Auditor:** Super Z (GLM) — independent re-analysis commissioned by repository owner
**Audit date:** 2026-09-08
**Subject:** Gemini's review `AGRI-BIOCONTROL-GENOMIC-SCRUTINY-V5` (582 lines) in `WhyAdr/PUJ-fungi`
**Reference data:** Funannotate GBKs + antiSMASH 8.0.4 outputs for both isolates, repo commit `ec861c8` (`main`)
**Tooling:** `gbparse` 0.8.1 (WhyAdr/genbank-parser skill) + raw Biopython cross-parsing of `/db_xref` qualifiers

---

## 0. Data Provenance (what was actually audited)

All `*.gbk` and `Funannotate*.json` files in the repo are **Git LFS pointers**. The real payloads were fetched from `media.githubusercontent.com` and byte-verified against the LFS manifest:

| Artifact | SHA-256 (first 16) | Size | Role |
|---|---|---|---|
| `fungiSMASH-TA/input/Funannotate-annotated-genome-TA.gbk` | `c07f6c6e379fec38` | 45,029,346 B | TA Funannotate annotation (antiSMASH input) |
| `fungiSMASH-AF/Funannotate-annotated-genome-AF.gbk` | `d3fb74bf367092e66` | 83,318,907 B | AF Funannotate annotation **with antiSMASH region features merged** |
| `fungiSMASH-TA/Funannotate-annotated-genome-TA.gbk` | `b27db6f44d8fe3e7` | 44,880,695 B | TA antiSMASH **output** (distinct from input) |

Genome-level ground truth established by the audit (none of these numbers appear in the review):

| Metric | TA-PUJ (*T. asperellum*) | AF-PUJ (*A. flavus*) |
|---|---|---|
| Records (contigs/scaffolds) | **1,376** | **97** |
| Records with ≥1 CDS | 1,309 | 61 (36 tiny scaffolds 1.4–17.8 kb carry no CDS) |
| Total length | **20,289,144 bp** | **36,794,309 bp** |
| Total CDS | **5,229** | **9,792** |
| Largest record | 62,752 bp (contig_1716) | 2,400,610 bp (scaffold 1) |
| Records ≥ 100 kb | **0** | 39 |
| GC content | 48.68% | 48.15% |
| tRNA features | 134 | 259 |
| Product = "hypothetical protein" | **70.5%** (3,688/5,229) | **75.6%** (7,399/9,792) |
| antiSMASH BGC regions | 21 ✓ (review correct) | 74 ✓ (review correct) |
| Scaffolds bearing BGC regions | 21 | 27 |

---

## 1. Executive Verdict

The review is a **mixed document**: its locus-level directory (Section 2) and synteny tables (Section 3) are largely faithful to the annotation — protein lengths, strands, contig assignments, EC numbers, and the flanking-gene order reproduce almost exactly (dozens of spot-checks passed). The MIBiG evidence quoted for the eight TA clusters and the four AF toxigenic clusters is accurate to the score level.

However, the review is **numerically unreliable everywhere it aggregates**, **overstates evidence provenance**, and **misses material findings**: inflated enzyme-family counts that match no reproducible counting method; a "Validated KEGG KO" column with zero basis in the files; two fabricated genomic coordinates; a mycotoxin-risk verdict for TA-PUJ that its own data cannot support; ~25 significant MIBiG matches in AF never reported (including a nitropropionic-acid BGC); and — most consequential — **no assembly-completeness assessment of a TA genome that is only ~20.3 Mb (~55–60% of the expected ~34–40 Mb for *T. asperellum*)**, which silently invalidates every "not present / 0 hits" conclusion in the document.

**Bottom line:** keep Sections 2–3 as a scaffold, correct the numbers, demote inferred annotations from "validated" to "inferred", add the completeness caveat, and rebuild Sections 4–7 around the full BGC inventory. The companion `gemini-execution-plan.md` specifies this task-by-task.

---

## 2. Critical Findings (materially change conclusions or safety posture)

### C1 — TA-PUJ assembly is ~half a genome; the review never assesses completeness
**Claim (review, throughout):** "exhaustive gene-, protein-, and synteny-level dissection"; absence-type verdicts such as "AF: ACC Deaminase Not present", "Mycotoxin Risk Profile (TA): None detected".
**Evidence:** TA = 20.29 Mb / 5,229 CDS / 1,376 contigs / largest 62.8 kb / 0 contigs ≥100 kb (vs. *T. asperellum* references ≈33.5–40 Mb and 10–12k genes; e.g. CBS 433.97). AF = 36.79 Mb / 9,792 CDS — essentially complete by comparison. No BUSCO/N50/genome-size statement exists anywhere in the review.
**Consequence:** every count-based and absence-based TA claim is a lower bound at ~50–60% completeness. The document's "exhaustive" framing and its zero-risk conclusions are unsupported.
**Correction:** add an Assembly & Completeness section (see plan Task 2.1) and requalify all TA absence claims.

### C2 — "Mycotoxin Risk Profile: TA — None detected (GRAS standard BCA)" is not defensible
**Claim (review §5):** "None detected (GRAS standard BCA)… TA-PUJ safe for field release."
**Evidence:** 13 of 21 TA BGC regions have **no significant MIBiG match** (uncharacterized NRPS/terpene/PKS clusters on contigs 1170, 1317, 1364, 1801, 470, 473, 579, 599, 627, 675, 703, 76, 909); the assembly is ~half a genome (C1); 70.5% of TA CDS are hypothetical. GRAS is a regulatory status, not a genome-derivable property, and *Trichoderma* spp. are known producers of harzianum acid, trichothecene-like compounds and peptaibols in other strains.
**Correction:** downgrade to "No known mycotoxin BGC match among the 8 MIBiG-annotated regions; risk assessment constrained by partial assembly; 13 orphan BGCs uncharacterized; wet-lab screen (already Tier 5) should include Trichoderma-typical metabolites."

### C3 — Systematically inflated family counts (Executive Summary + Validation Matrix)
**Claim vs. actual (best-supported union of Pfam/EC/InterPro from raw qualifiers):**

| Family | Review (TA/AF) | Actual (TA/AF) | Method note |
|---|---|---|---|
| Chitinase GH18 | 18 / 21 | **14 / 17** | union of PF00704, EC 3.2.1.14, IPR001223 |
| β-1,3-Glucanase | 8 / 5 (GH16/55/64) | **GH16=0/0, GH55=0/0, GH64=0/3; EC 3.2.1.39 = 1/0; product "glucanase" = 4/2** | none of the named families reproduce the claim |
| Chitosanase GH75 | 2 / 0 | **7 / 18** | PF03240/IPR004840 — AF direction inverted |
| GST | 34 / 65 | **18 / 24** | PF02798/PF00043/PF13409/PF14497 + IPR004045/46/981 + EC 2.5.1.18 (EC alone: 7/9) |
| Laccase/multicopper oxidase | 2 (banner) vs 6 (matrix) / 7 | **7 / 11** Cu-oxidase-domain genes (IPR001117 alone: 6/9; includes ferroxidases) | internally inconsistent + inflated |
| Acid/all phosphatase loci (AF) | "989 Phosphatase Loci" | **179** (broad InterPro set) / 136 (acid-P Pfams) / 56 (product) | 989 matches nothing derivable from the files |
| Peroxidase (AF) | 26 | **24–27** depending on signature set; 3 by product | roughly right numerically, but no method stated |
| AF CAZy "41 AA7, 30 AA3, 22 GH3, 13 GH13" | — | **no CAZy/dbCAN annotations exist anywhere in the repo** | unverifiable as stated |

**Correction:** replace every count with a reproducible definition (family = signature set, method stated), cite the recomputation script (plan Task 2.2), and add error bars ("≥" given TA incompleteness).

### C4 — Missed BGC findings of biosafety / agricultural significance (AF)
The review's §7B collapses 68 of 74 regions into "Various". Actual KnownClusterBlast evidence never reported:

| Region | MIBiG match | Score | Genes | Identity | Why it matters |
|---|---|---|---|---|---|
| **703_c2** | (type: **nitropropanoic acid**, 17,956 bp) | — (no KCB hits) | — | — | **3-NPA is an acute mitochondrial mycotoxin of *A. flavus*; a "4 toxigenic BGCs" biosafety section that omits an NPA-type region is incomplete** |
| 418_c2 | ustiloxin B (BGC0000627.4, fungal-RiPP) | 7,477 | 13 | 46–100% | 3rd-ranked MIBiG match in genome; ribosomal-peptide toxin class |
| 480_c3 | leporin B (BGC0001445.5) | 15,512 | 10 | 85–100% | 4th-ranked region; unreported |
| 904_c1 | penicillin (BGC0000404.4) | 6,518 | 2 | 79–85% | antibacterial repertoire |
| 258_c4 | astellolide A | 8,724 | 8 | 97–99% | unreported |
| 480_c1 | imizoquin | 8,477 | 8 | 85–100% | unreported |
| 258_c3 | flavunoidine | 7,818 | 7 | 93–100% | unreported |
| 1845_c1 | dichlorodiaporthin | 6,738 | 5 | 96–100% | unreported |
| 485_c2 | actinopolymorphol C | 6,338 | 6 | 99–100% | unreported |
| 24_c4 | asparasone A | 5,862 | 5 | 97–100% | unreported *A. flavus* metabolite |
| 826_c1 | (−)-ditryptophenaline | 6,216 | 3 | 91–99% | unreported |
| 614_c2 | DHMP | 5,797 | 2 | 97–100% | unreported |
| 471_c3 | aflavarin | 5,687 | 4 | 94–99% | unreported |
| 433_c1 | 8-methyldiaporthin | 5,042 | 4 | 88–100% | unreported |
| 826_c2 | YWA1 | 4,277 | 1 | 100% | unreported |
| 256_c3 | heptelidic acid | 2,420 | 4 | 97–99% | unreported |
| 256_c1 / 418_c1 | paspalinine-type indole-diterpenes | 1,482 / 1,274 | 3/3 | 52–72% | banner mentions "Paspalinine/Shearinine" without evidence tiers |
| 827_c1 / 471_c4 | **metachelin-type siderophore NRPS in AF** | 1,714 / 1,052 | 2/2 | 46–59% | review attributes metachelin exclusively to TA |
| 256_c7 | aspercryptins | 1,800 | 3 | 47–67% | unreported |
| 960_c1 | 6-methylsalicylic acid | 2,075 | 1 | 60% | unreported |
| 703_c1 | dehydrocurvularin | 1,043 | 3 | 47–54% | unreported |
| 431_c1 | fusaric acid | 829 | 2 | 62–72% | unreported |
| 826_c3 / 485_c1 | clavaric acid | 744 / 704 | 1/1 | ~51/48% | unreported |
| 431_c3 | zopfiellin | 528 | 2 | 54–55% | unreported |

40 of 74 AF regions have **zero** KnownClusterBlast hits (incl. the 17,956 bp NPA region and 815_c1 at 81,698 bp) — the review should say so explicitly instead of "Various".

---

## 3. Major Findings

### M1 — Genome-structure numbers are wrong or misleading
- "TA: 1,144 annotated contigs" — actual: 1,376 records (1,309 with ≥1 CDS, 1,130 with ≥2). No threshold reproduces 1,144.
- "AF: 27 annotated scaffolds/chromosomes" — actual: 97 records (61 with CDS). **27 = number of scaffolds bearing BGC regions** — a different (unstated) metric.
- Basic stats (20.29 Mb / 36.79 Mb; 5,229 / 9,792 CDS; GC; N50) are absent from the review entirely.

### M2 — "Validated KEGG KO" column has no basis in the data
**Zero** CDS in either genome carry a KEGG KO qualifier (checked via `gbparse extract` + raw qualifiers). Every KO ID in the matrix (K01505, K01183, K15316, K04787, K01501 …) is Gemini's inference presented as "Validated". Same problem for many "Pfam Accessions" columns: the GBK files contain `InterPro:IPRxxxxx` and `PFAM:PFxxxxx` db_xrefs — where a Pfam is present it usually maps from the InterPro entry, but the review never distinguishes annotated vs derived.

### M3 — Fabricated genomic coordinates for two TA loci
- `PUJ_005301` claimed at `contig_1813:[3345:4459](-)` — actual `11,954..13,395 (-)`, 5 exons.
- `PUJ_004623` claimed at `join{[35028:36528],[36592:37354]}` — actual `39,732..42,710 (+)`, 9 exons.
(For contrast, `PUJ_004816` join{[7641,7828],[7895,8753]} and `PUJ_004419` 72,805..76,008 match within ±1 bp — so the document *can* be precise when it checks.)

### M4 — AF "nitrilase" row is unsupported and internally contradicted
Matrix: "Auxin: Nitrilase EC 3.5.5.1 — AF 3 hits: PUJ_000724, PUJ_004944, PUJ_007889."
Actual: PUJ_000724 = EC **3.4.11.21** Xaa-Pro aminopeptidase (IPR001948; the review's own §3.B.2 labels it aminopeptidase); PUJ_004944 = no EC, no InterPro; PUJ_007889 = ADH/Rossmann folds (IPR000073/IPR029058). None carries the nitrilase family PF02979 — which actually has 4 TA / 7 AF members the review never examined.

### M5 — Identity claims overstated; two aflatoxin rows disagree
- "all 21 genes … 90% to 100% identity" — actual top aflatoxin hit (BGC0000007.3): **51–97%** (AflR 94%, PksA 97%). The "100% identity to XP_041142750.1 / XP_041142754.1" claims have no BLAST artifact in the repo.
- §4 table: aflatoxin = BGC0000007.3, 11 hits, 16,946, "Max ID 100%" (actual max 97%). §7B: BGC0000008.3, 10 hits, 16,592, "100%" — that hit exists (99–100% id) but is **rank #3**, presented as rank #2. Internal inconsistency.
- Aspirochlorine "19 of 19 genes at 94–100%": true only after excluding one 48% secondary alignment row (PUJ_004914 vs AO090001000039) — acceptable, but the method is undefined.

### M6 — Aflatoxin/CPA cluster table contains gene-labeling errors
- `aflD (nor-1)` assigned to **both** PUJ_009392 and PUJ_009396; `aflT` assigned to both PUJ_009391 and PUJ_009398; aflK and aflL both labeled `vbs`.
- PUJ_009391 carries EC 3.1.1.94 (versiconal hemiacetal acetate esterase = **aflJ/estA** activity) yet the row is labeled "aflT (vahA)".
- PUJ_009392 carries EC 1.1.1.352 (versicolorin reductase = **aflM/ver-1** activity) yet the row is labeled "aflD (nor-1)".
- "unbroken, continuous cluster without gaps": real gaps are 2,761 bp (009392→009393), **4,201 bp** (009399→009400 — the aflatoxin/CPA boundary), 2,847 bp (009402→009403).
- The first six genes (PUJ_009383–009388, 190.7–201.0 kb) lie **outside** the antiSMASH region (starts 201,074) — fine to include biologically, but should be stated.

### M7 — AF carries an EC-tagged ACC-deaminase candidate the review misses
`PUJ_008483` (scaffold 826, +, 401 aa, **EC 3.5.99.7**, IPR001926/PLP) lacks the ACC-deaminase-specific IPR005965, so "AF: 0" is defensible under a strict criterion — but a scrutiny document should report the unverified candidate, not a flat zero. (PF00291-family breadth: TA 6, AF 16 loci.)

### M8 — Chitosanase direction inverted between isolates
Review: TA 2, AF 0. Actual PF03240/IPR004840: TA 7, **AF 18** — directly relevant to the mycoparasitism comparison.

### M9 — 5,098 cross-genome locus-tag collisions, never flagged
Both isolates use the `PUJ_` prefix with overlapping numeric ranges (TA max 5,363; AF max 10,052); 5,098 tags exist in **both** genomes denoting different genes (e.g., PUJ_000001: TA = ser/thr kinase, AF = hypothetical). Every cross-isolate citation in the review is ambiguous without an isolate qualifier, and any programmatic join on locus_tag will silently cross-contaminate evidence. The execution plan mandates `TA:PUJ_xxxxx` / `AF:PUJ_xxxxx` notation.

---

## 4. Minor Findings

- **m1.** Internal inconsistency: banner "2 Laccases (AA1)" vs matrix "TA 6" vs actual 7 Cu-oxidase-domain genes (incl. FET3-type ferroxidases).
- **m2.** Reference-length copy errors: PUJ_004899 claimed 932 aa (actual 804 — 932 is the *A. oryzae* reference), PUJ_004911 claimed 1,594 (actual 1,573), PUJ_009785 claimed 706 (actual 688), PUJ_009781 claimed 355 (actual 338).
- **m3.** Off-by-one coordinates: PUJ_004419 "72804..76008" vs actual 72805..76008; PUJ_004816 "[7640:7828],[7894:8753]" vs actual [7641,7828],[7895,8753].
- **m4.** Matrix "Ferroxidase AF hits: 1" — EC 1.16.3.1 count in AF = 0 (TA = 1 ✓).
- **m5.** "Terpene Cyclase TA: 1 (TATC6)" — actual 7 terpene-cyclase-domain genes in TA (PF19086/PF03936).
- **m6.** CpaT "(PF00083, PF07690)": PUJ_009400 carries only InterPro IPR011701/020846/036259 in the file; PF00083 is a carboxylesterase domain, not MFS — the listing mixes derived and wrong accessions.
- **m7.** Verifiability gaps: "Funannotate 1.8.17" (no funannotate logs in repo — antiSMASH 8.0.4 **is** confirmed by both run logs); "InterPro Release 2026", "BLAST score 6998.0 for cpaA", UniProt identities (A0A024TLC7, A0A0F6WTL4, Q9P8N2) — no supporting artifacts exist in the repo.
- **m8.** CPA hit identities: BGC0000977.4 = 4 genes, 9,573, **90–97%** (review's "97%" is the max — fine, but state range).
- **m9.** §7A "TA 9–21 orphan clusters" is correct (13 regions, no KCB hits) ✓ — but the confidence tiers (HIGH/MEDIUM/LOW) are the review's own construction, not antiSMASH output; they should be labeled as such (they are defensible for the rows shown).
- **m10.** The review never states which TA file it parsed (input vs antiSMASH output — both exist in the repo with different content sizes).
- **m11.** "Pr1 Cuticle Proteases" (TA banner): no TA gene is annotated Pr1/cuticle-associated; the honest evidence is S8 subtilisin-family loci — TA 16, AF 7 (PF00082 ∪ IPR000159/015500) — family-level, with specific Pr1 identity unproven (and assembly-limited per C1).

---

## 5. Verified Claims (credit where due)

To keep the revision efficient, the following review elements **reproduced exactly** under audit and should be preserved:

1. **AA lengths** (24/28 spot-checked): PUJ_004816 (348), PUJ_005301 (332), PUJ_004623 (754), PUJ_001678 (606), PUJ_001679 (367), PUJ_003670 (1,415), PUJ_004657 (2,204), PUJ_003355 (2,143), PUJ_003361 (1,963), PUJ_003357 (264), PUJ_004649 (746), PUJ_004624 (224), PUJ_001674 (496), PUJ_001677 (301); AF PUJ_009393 (444), PUJ_009397 (2,109), PUJ_009400 (664), PUJ_009401 (455), PUJ_009402 (3,867), PUJ_009403 (395), PUJ_005557 (605), PUJ_009297 (772), PUJ_002731 (606), PUJ_000728 (306), PUJ_004419 (797), PUJ_009783 (1,021), PUJ_000724 (498), and all 15 super-cluster row lengths PUJ_009383–009402.
2. **BGC region counts**: TA 21 / AF 74 ✓ (regions.js + file counts).
3. **antiSMASH 8.0.4** ✓ (both run logs).
4. **All 8 TA MIBiG rows in §7A** verified to the digit: leucinostatin BGC0001358.4 (4 genes, 3,862, 52–86%), metachelin BGC0002710.2 (2, 2,034, 50–62%), enniatin BGC0000342.4 (1, 2,390, 54%), trichobrasilenol BGC0002260.3 (2, 906, 58–61%), cryptosporioptide BGC0002063.3 (2, 2,191, 64–67%), squalestatin BGC0001839.3 (2, 863, 60–61%), equisetin BGC0001255.4 (2, 765, 46–51%), peramine BGC0002164.2 (1, 80, 50%) — plus the destruxin/cyclosporin secondary-hit note and the aerobactin "zero KCB hits" caveat ✓.
5. **Aspergillic acid** (BGC0001516.5: 6, 6,227, 75–100%; BGC0002602.2: 6, 6,208, 95–99%) and **aspirochlorine** (BGC0001123.5: 19, 17,383; 94–100% over the 19 primary rows) ✓.
6. **Neighborhood architecture** (§3): flanking order, strands, ECs and lengths of contig_1730, contig_1813, contig_623 (incl. the FET3(−)/FTR1(+) head-to-head arrangement ✓), contig_1705, contig_1342, contig_1419, contig_1710, scaffold 1340 run, scaffold 24, 482, 1339, 471 — all match the annotation.
7. Gene symbol claims that exist verbatim in the GBK: `TATC6`, `CHT2_2`, `FET3`, `FTR1_1`, `RHO3`, `PHO5`, `PHO2`, `PHO88` (product "phosphate transporter (Pho88)").

---

## 6. Additional Findings Beyond the Review (new material for the revision)

1. **AF nitropropionic-acid BGC** (scaffold 703, region 2, 403,874–421,829, 17,956 bp) — see C4; belongs in the §4 biosafety table and the Tier-5 LC-MS/MS panel discussion.
2. **AF metachelin-type NRPS regions** (827_c1, 471_c4) — the "rhizosphere iron dynamics" comparison in §5 must stop attributing metachelin-type matches only to TA.
3. **Peptaibol status in TA**: no NRPS exceeds 3,931 aa (largest: PUJ_000117, contig_52) — no classic 18–20-module peptaibol synthetase (≥6,000 aa) is detectable; given C1, the absence is unproven, and the review's silence on peptaibols (a signature *Trichoderma* biocontrol metabolite class) is a coverage gap to close explicitly.
4. **IAA/auxin claim**: no indole-3-pyruvate decarboxylase / aldehyde-oxidase / nitrilase-homologous locus is annotated in TA; the banner bullet "Auxin (IAA) via Tryptophan" is biological inference (from genus-level literature), not annotation evidence — must be labeled as such (anthranilate-synthase etc. only support tryptophan biosynthesis).
5. **Annotation depth**: 70.5% (TA) / 75.6% (AF) of CDS are "hypothetical protein"; the review's confident product narratives are largely InterPro/EggNOG-derived and should be labeled.
6. **Mobilome** (`gbparse mobilome`): 4 raw hits (TA) / 9 (AF), 0 eligible at min-evidence 2; no plasmid/TE declarations in the records. Consistent with a funannotate output lacking topology metadata — worth one caveat line, nothing more.
7. **MEOR/xenobiotic engines**: `gbparse meor` reports 9 (TA) / 28 (AF) weak hits; `discover --ruleset xenobiotics` fires false positives on housekeeping genes for these files (e.g. `catA` rule matching kinases) — do **not** use these outputs as bioremediation evidence without manual curation.
8. **Skill defect discovered during audit**: `genbank_parser/io.py` `_pfam_re` matches `Pfam:`/bare `PF\d+` but not uppercase `PFAM:PFxxxxx` used by these files, so **`gbparse extract` silently drops all Pfam evidence** (TA has 5,731 `PFAM:` xrefs; AF 14,227). Family counts must be recomputed from raw `/db_xref` (as done here) or after an upstream fix. Rfam regex already has `IGNORECASE`; Pfam's should too.
9. **Repo hygiene**: LFS-only payloads make the review unauditable from a plain clone; recommend committing compressed TSV derivatives (as produced by `gbparse extract` + a Pfam-aware pass) or documenting the LFS fetch step in the README.

---

## 7. Corrected Reference Numbers (drop-in replacements)

| Metric | Corrected value | Source |
|---|---|---|
| TA contigs | 1,376 records (1,309 with ≥1 CDS) | `gbparse summary`, recomputation |
| TA genome | 20,289,144 bp, 5,229 CDS, GC 48.68% | recomputation |
| AF scaffolds | 97 records (61 with CDS; 27 bear BGCs) | recomputation |
| AF genome | 36,794,309 bp, 9,792 CDS, GC 48.15% | recomputation |
| TA/AF chitinases | 14 / 17 (GH18 union) | `family_counts.json` |
| TA/AF chitosanases | 7 / 18 (PF03240/IPR004840) | same |
| TA/AF GSTs | 18 / 24 (signature union); 7/9 by EC | same |
| TA/AF laccase-like | 7 / 11 Cu-oxidase genes (6/9 by IPR001117) | same |
| AF phosphatase loci | ≤179 (InterPro union), 56 by product | same |
| AF P450 | 154 (PF00067 union) | same |
| Aflatoxin identities | 51–97% (top hit), AflR 94% / PksA 97% | `1340_c1.txt` |
| CPA identities | 90–97% | same |
| TA "1,144 contigs" | unsupported — replace | — |
| "989 phosphatases" | unsupported — replace | — |
| KO column | re-label "Inferred KO (no annotation basis)" | `gbparse extract` |

*(Machine-readable evidence: `/home/z/my-project/data/genome_stats.json`, `family_counts.json`, `knownclusterblast_all.json`, `TA/AF_regions_inventory.tsv`, `TA/AF_annotations.tsv`; scripts in `/home/z/my-project/scripts/audit_*.py`.)*
