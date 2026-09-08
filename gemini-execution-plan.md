# Gemini Execution Plan: Revision of `agriculture-support-biocontrol-fungal-isolate-review.md`

**Document:** `GEMINI-EXECUTION-PLAN-V1` — companion to `audit-findings-agriculture-support-biocontrol-review.md`
**Executor:** Gemini (review author)
**Target artifact:** `agriculture-support-biocontrol-fungal-isolate-review.md` in `WhyAdr/PUJ-fungi` (repo `main`, commit `ec861c8`)
**Tooling mandated:** the **genbank-parser skill** (`https://github.com/WhyAdr/genbank-parser`, CLI `gbparse` 0.8.1) for all annotation queries.
**Goal:** transform the review from "plausible narrative with unreliable numbers" into "auditable, evidence-cited document whose every quantitative claim is reproducible by a script".

---

## 0. Non-Negotiable Ground Rules (read before any edit)

1. **Never assert what the files do not contain.** The GBKs carry NO KEGG KO qualifiers, NO CAZy family annotations, and NO product-level names for 70–76% of CDS. Inference from InterPro/EggNOG/MIBiG homology is allowed but MUST be labeled `inferred` in a dedicated column or footnote.
2. **Every number must name its method.** A count is only valid with: (a) the signature set (Pfam/EC/InterPro IDs), (b) the matching rule (union/intersection), and (c) the file it was computed from. If you cannot reproduce it with a command, delete it.
3. **Quote evidence by artifact.** Cite as `file -> region/locus -> line or table` (e.g. `fungiSMASH-AF/knownclusterblast/1340_c1.txt, hit #1`), never as "the database".
4. **Distinguish the four evidence tiers** now used in the revised review:
   - `T1 annotation-supported` — literal qualifier in the GBK (EC, InterPro, PFAM, product, gene symbol);
   - `T2 antiSMASH-supported` — region type/knownclusterblast result in the antiSMASH output;
   - `T3 inferred` — homology/literature inference by the reviewer;
   - `T4 unverifiable` — claim with no artifact in the repo (delete or move to "Limitations").
5. **Disambiguate loci by isolate** — `TA:PUJ_004816` vs `AF:PUJ_009393`. 5,098 locus tags exist in BOTH genomes with different genes (see audit M9). This notation is mandatory from V6 onward.
6. **The genbank-parser skill's epistemic discipline applies**: CLI parses, you read summaries; never paste whole GenBank files into context; mobilome/MEOR hits are not phenotype claims.
7. **Caveat first, verdict second.** TA absence claims must carry the assembly-completeness caveat (C1) until BUSCO/QUAST evidence is added.

---

## Phase 0 — Data & Environment Baseline (all later tasks depend on this)

### Task 0.1 — Recover the real (LFS) data
The repo's `*.gbk` / `Funannotate*.json` are LFS pointers. Clone and fetch:

```bash
git clone https://github.com/WhyAdr/PUJ-fungi.git && cd PUJ-fungi
# if git-lfs is unavailable, fetch directly (URL pattern for public repos):
BASE="https://media.githubusercontent.com/media/WhyAdr/PUJ-fungi/main"
curl -sL -o TA-input.gbk      "$BASE/fungiSMASH-TA/input/Funannotate-annotated-genome-TA.gbk"
curl -sL -o TA-antismash.gbk  "$BASE/fungiSMASH-TA/Funannotate-annotated-genome-TA.gbk"
curl -sL -o AF-antismash.gbk  "$BASE/fungiSMASH-AF/Funannotate-annotated-genome-AF.gbk"
sha256sum TA-input.gbk TA-antismash.gbk AF-antismash.gbk
```

**Acceptance criteria (AC-0.1):** sizes = 45,029,346 / 44,880,695 / 83,318,907 bytes; SHA-256 prefixes = `c07f6c6e379fec38` / `b27db6f44d8fe3e7` / `d3fb74bf367092e66`. Any mismatch → STOP, do not audit pointer files.

### Task 0.2 — Install the parser skill and note its one defect
```bash
git clone https://github.com/WhyAdr/genbank-parser.git && pip install -e ./genbank-parser
gbparse --help
```
**Known defect (do not work around silently):** `genbank_parser/io.py:_pfam_re` = `^(?:Pfam:)?(PF\d+)` is case-sensitive; these genomes write `PFAM:PFxxxxx`, so `gbparse extract` **drops all Pfam evidence**. Two options:
- (a) patch locally: `_pfam_re = re.compile(r'^(?:PFAM:|Pfam:)?(PF\d+)', re.IGNORECASE)` and re-install; or
- (b) use the raw-qualifier counter in Task 2.2 (provided below), which reads `/db_xref` directly with Biopython.
Either way, record which option you used in the review's Methods appendix.

### Task 0.3 — Baseline the ground truth numbers
```bash
gbparse summary TA-input.gbk | head -12
gbparse summary AF-antismash.gbk | head -12
gbparse extract TA-input.gbk TA.tsv && gbparse extract AF-antismash.gbk AF.tsv
```
**AC-0.3:** you can state, with file evidence: TA = 1,376 records / 20,289,144 bp / 5,229 CDS; AF = 97 records / 36,794,309 bp / 9,792 CDS. These numbers go into the new Section 1 (Task 1.1).

---

## Phase 1 — Correct Factual Errors (each task = one finding from the audit)

### Task 1.1 — Fix genome-structure claims (audit M1)
- Replace "TA: 21 BGC regions, **1,144 annotated contigs**" → "TA: 21 BGC regions; **1,376 contigs (1,309 with ≥1 annotated CDS), 20.29 Mb, 5,229 predicted CDS**".
- Replace "AF: 74 BGC regions, **27 annotated scaffolds/chromosomes**" → "AF: 74 BGC regions across **27 of 97 scaffolds** (36.79 Mb, 9,792 predicted CDS; 61 scaffolds carry CDS)".
- AC: numbers equal AC-0.3 outputs; no other instance of "1,144" or "27 scaffolds" survives (search the file).

### Task 1.2 — Rebuild the Validation Matrix counts (audit C3)
Replace the AF/TA hit counts with the audited values, each footnoted with its signature set:

| Matrix row | Replace TA/AF with | Signature set (footnote) |
|---|---|---|
| Chitinase | 14 / 17 | PF00704 ∪ EC 3.2.1.14 ∪ IPR001223 |
| Chitosanase | 7 / 18 | PF03240 ∪ IPR004840 |
| β-1,3-glucanase | 1 / 0 (EC 3.2.1.39); state GH16/55/64 = 0/0/0 and 0/3 | EC + named Pfams |
| GST | 18 / 24 | PF02798∪PF00043∪PF13409∪PF14497∪IPR004045/46/981∪EC 2.5.1.18 |
| Laccase/AA1 | 7 / 11 Cu-oxidase genes (incl. ferroxidases; 6/9 by IPR001117) | PF00394∪PF07731∪IPR001117 |
| Ferroxidase | 1 / 0 (EC 1.16.3.1) | EC |
| Phosphatase | delete "989"; use 179 (AF, broad InterPro) or 56 (product) with method | IPR005828∪IPR029034∪IPR017064∪IPR006349∪IPR006357∪IPR001952 vs product regex |
| Peroxidase | 24–27 (AF) with stated set; 12–14 (TA) | PF00141∪PF01325∪PF14595∪IPR002016∪IPR010255∪IPR012338∪IPR019780∪IPR023754 |
| Terpene cyclase | 7 / 21 | PF19086∪PF03936∪IPR008949∪IPR034686 |
| CAZy rows (41 AA7 etc.) | delete or mark `T4 unverifiable (no dbCAN output in repo)` | — |
| Auxin/nitrilase row | delete the 3 AF loci; optionally note nitrilase-family PF02979 = 4 TA / 7 AF | PF02979 |
- Also fix exec banner: "2 Laccases (AA1)" → 7 (incl. 1 ferroxidase-type); "8 Beta-glucanases (GH16/55/64)" → 1 EC-verified + note.
- AC: every number in §1 matrix and the exec banner appears in `family_counts.json` or is deleted; the recomputation script (Task 2.2) exits 0.

### Task 1.3 — Requalify "Validated KO" and Pfam columns (audit M2)
- Rename column "Validated KEGG KO" → "Inferred KO (reviewer; no KO qualifiers exist in annotation)".
- For each Pfam/InterPro cell, keep only accessions that literally appear in the locus's `/db_xref` (verify with `gbparse locus <file> <tag>`), and add a footnote: "InterPro→Pfam mapping applied where the GBK lists only InterPro".
- Delete or re-tier cells you cannot verify.
- AC: for a random sample of 10 rows, `gbparse locus` output contains each claimed accession.

### Task 1.4 — Fix coordinate and length errors (audit M3, m2, m3)
- `TA:PUJ_005301` location → `contig_1813:11,954..13,395 (-), 5 exons` (biological length 999 nt → 332 aa).
- `TA:PUJ_004623` location → `contig_1705:39,732..42,710 (+), 9 exons` (754 aa).
- `AF:PUJ_004419` → `72,805..76,008 (+)`; `TA:PUJ_004816` → `join(7641..7828,7895..8753)`.
- Lengths: PUJ_004899 → 804 aa; PUJ_004911 → 1,573 aa; PUJ_009785 → 688 aa; PUJ_009781 → 338 aa (state "A. oryzae reference lengths quoted in V5 by error").
- AC: `gbparse locus` reproduces every coordinate/length in §2 (script check V-3).

### Task 1.5 — Repair the aflatoxin/CPA cluster table (audit M5, M6)
- Fix duplicated labels: `aflD` only on PUJ_009396 (EC 1.1.1.349); `aflJ (estA)` on PUJ_009391 (EC 3.1.1.94); `aflM (ver-1)` on PUJ_009392 (EC 1.1.1.352); PUJ_009398 keeps `aflT` (MFS); aflK = `vbs`-family *accessory* vs aflL `verB` — or simply quote the annotation ECs and mark gene symbols `T3 inferred`.
- Replace "90–100% identity" with "51–97% vs top hit BGC0000007.3 (AflR 94%, PksA 97%); 99–100% vs BGC0000008.3 (rank #3)".
- Replace "unbroken, continuous cluster without gaps" with "21 loci across ~79.7 kb; intergenic gaps up to 4.2 kb at the aflatoxin→CPA boundary (243,317→247,518); first six loci (190.7–201.0 kb) lie upstream of the antiSMASH region start (201,074)".
- Align §4 and §7B on ONE aflatoxin row (top hit BGC0000007.3, 11 proteins, 16,946, 51–97%) and remove the 100%-identity claim; move BGC0000008.3 to a "secondary hit" note.
- Delete/re-tier: "BLAST score 6998.0 (cpaA)", "100% identity to XP_041142750.1/XP_041142754.1", UniProt identities without artifacts (m7) → `T4`.
- AC: table EC column equals the GBK EC qualifiers for all 21 loci (script check V-4).

### Task 1.6 — Delete or demote unsupported/contradicted rows (audit M4, M7, M8, m1, m4–m6)
- Remove the "Auxin: Nitrilase" AF row (internally contradicted; none of the three loci is a nitrilase) or rewrite as "Nitrilase-family (PF02979): TA 4 / AF 7 loci, none characterized".
- Add a note under ACC deaminase: "AF carries one EC-3.5.99.7-tagged PLP enzyme (AF:PUJ_008483, 401 aa) lacking the ACC-deaminase-specific IPR005965 — unverified candidate, not counted".
- Fix chitosanase row (7/18), ferroxidase AF (0), terpene cyclase TA (7).
- Fix CpaT Pfam listing (IPR011701 MFS; delete PF00083).
- AC: no row remains that contradicts another row (manual cross-read).

---

## Phase 2 — Add Missing Content (new sections, all `T1/T2`-cited)

### Task 2.1 — New section: "Assembly & Annotation Completeness Assessment"
Content requirements:
- TA: 20.29 Mb vs expected 33.5–40 Mb (~55–60%); 1,376 contigs, largest 62.8 kb, 0 contigs ≥100 kb, N50 (compute with `quast` or from lengths); 5,229 CDS vs ~10–12k expected; 70.5% hypothetical products.
- AF: 36.79 Mb (≈ complete vs NRRL 3357 36.9 Mb), 9,792 CDS, 75.6% hypothetical.
- Explicit caveat block quoted once and referenced everywhere: "**All TA-PUJ absence claims and count-based comparisons are lower bounds pending BUSCO (fungi_odb10) and completeness estimation.**"
- Action item: run BUSCO/QUAST if raw reads or the assembly are available; otherwise state "not assessable from repo artifacts".
- AC: the section exists, contains both isolate tables, and every "0 / not present" claim in the document links to the caveat.

### Task 2.2 — Reproducible counting pipeline (commit to repo)
Create `scripts/recount_families.py` (raw `/db_xref` parser, immune to the `PFAM:` case bug) that emits `family_counts.json` and exits non-zero on unexpected values:

```python
#!/usr/bin/env python3
"""Recount enzyme families from raw GBK db_xref qualifiers (PFAM: prefix-safe)."""
from Bio import SeqIO
import json, sys

GENOMES = {"TA": "TA-input.gbk", "AF": "AF-antismash.gbk"}
FAMILIES = {  # name -> (pfam set, ec set, interpro set)
 "chitinase_GH18": ({"PF00704"}, {"3.2.1.14"}, {"IPR001223"}),
 "chitosanase_GH75": ({"PF03240"}, {"3.2.1.132"}, {"IPR004840"}),
 "GST": ({"PF02798","PF00043","PF13409","PF14497"}, {"2.5.1.18"}, {"IPR004045","IPR004046","IPR010981"}),
 "laccase_CuOx": ({"PF00394","PF07731"}, {"1.10.3.2"}, {"IPR001117"}),
 "P450": ({"PF00067"}, set(), {"IPR001128","IPR002401"}),
 "ACC_deaminase_family": ({"PF00291"}, {"3.5.99.7"}, {"IPR005965"}),
 "terpene_cyclase": ({"PF19086","PF03936"}, set(), {"IPR008949","IPR034686"}),
 "nitrilase_family": ({"PF02979"}, {"3.5.5.1"}, {"IPR003010"}),
}

def norm(x):  # 'PFAM:PF00704' | 'Pfam:PF00704' | 'PF00704' | 'InterPro:IPR001223'
    return x.split(":")[-1] if ":" in x and not x.startswith("EC") else x

out = {}
for iso, path in GENOMES.items():
    counts = {f: set() for f in FAMILIES}
    for rec in SeqIO.parse(path, "genbank"):
        for feat in rec.features:
            if feat.type != "CDS": continue
            q = feat.qualifiers
            tags = set(q.get("db_xref", [])) | set(q.get("EC_number", []))
            normed = {norm(x) for x in tags}
            for fam, (pfs, ecs, iprs) in FAMILIES.items():
                if normed & (pfs | ecs | iprs):
                    counts[fam].add(q.get("locus_tag", ["?"])[0])
    out[iso] = {f: len(s) for f, s in counts.items()}

expected = {"TA": {"chitinase_GH18": 14, "chitosanase_GH75": 7, "GST": 18, "laccase_CuOx": 7,
                   "P450": 25, "ACC_deaminase_family": 6, "terpene_cyclase": 7, "nitrilase_family": 4},
            "AF": {"chitinase_GH18": 17, "chitosanase_GH75": 18, "GST": 24, "laccase_CuOx": 11,
                   "P450": 154, "ACC_deaminase_family": 16, "terpene_cyclase": 21, "nitrilase_family": 7}}
fail = False
for iso in expected:
    for fam, want in expected[iso].items():
        got = out[iso][fam]
        status = "OK" if got == want else "MISMATCH"
        if got != want: fail = True
        print(f"[{iso}] {fam}: {got} (expected {want}) {status}")
json.dump(out, open("family_counts.json", "w"), indent=1)
sys.exit(1 if fail else 0)
```
- Commit script + JSON to the repo; cite it as the single source for §1 matrix numbers.
- AC: `python scripts/recount_families.py` exits 0 with the expected values above.

### Task 2.3 — Expand the BGC inventory (audit C4)
Replace §7B's "6–74 Various" with a complete 74-row table from `regions.js` + `knownclusterblast/` with columns: `region, coordinates, type, top-3 MIBiG hits (BGC, compound, n_proteins, score, identity-range), confidence tier`. Minimum additions (all ≥T2):
- **703_c2 nitropropanoic-acid region** → new row in §4 biosafety table + Tier-5 panel note (3-NPA screen or explicit "no analytical standard available" note).
- ustiloxin B (418_c2), leporin B (480_c3), penicillin (904_c1), astellolide A, imizoquin, flavunoidine, dichlorodiaporthin, actinopolymorphol C, ditryptophenaline, asparasone A, DHMP, aflavarin, 8-methyldiaporthin, YWA1, heptelidic acid, aspercryptins, 6-MSA, dehydrocurvularin, fusaric acid, clavaric acid, zopfiellin, azaphilones (433_c2/486_c2).
- AF metachelin-type regions (827_c1, 471_c4) → fix §5 "Rhizosphere Iron Dynamics" row.
- State explicitly: "40 of 74 AF regions and 13 of 21 TA regions have no KnownClusterBlast match".
- AC: row count = 74 (AF) and 21 (TA); every score/identity matches the parsed `knownclusterblast` files (script check V-5).

### Task 2.4 — Locus-tag disambiguation + provenance metadata (audit M9, I-series)
- Adopt `TA:PUJ_xxxxx` / `AF:PUJ_xxxxx` notation throughout; add one paragraph explaining the 5,098 collisions and the risk.
- Add a "Data Provenance" box: the three LFS SHA-256 hashes, which file (input vs antiSMASH output) each claim was read from, and the note that Funannotate version claims are `T4` (no logs in repo; antiSMASH 8.0.4 is `T2`-confirmed by both run logs).
- AC: zero bare `PUJ_` citations without isolate prefix (regex `[^(A|T)F:|TA:]PUJ_` over the markdown returns only the explanation paragraph).

### Task 2.5 — Coverage gaps to close explicitly (short subsections, ≥150 words each)
- **Peptaibols**: largest TA NRPS is 3,931 aa (TA:PUJ_000117, contig_52); no ≥6,000-aa peptaibol synthetase detectable; unproven absence due to C1 — include the AbT1 (BGC0000307.4) note already in your data.
- **IAA pathway**: relabel as genus-level literature inference (`T3`); cite the actual annotation evidence found (anthranilate-synthase loci TA:PUJ_001036, TA:PUJ_001836 — tryptophan biosynthesis only).
- **Trichoderma-specific metabolite screen**: add harzianum-acid-like / trichothecene-like compounds to the Tier-5 discussion for TA (with the caveat that no BGC match exists in the current assembly).

---

## Phase 3 — Structural Rewrite for Verifiability

### Task 3.1 — Evidence-tier markers
- Convert §1 matrix "AF Hits / TA Hits" columns to `n (T1)` where annotation-supported.
- Add a legend for T1–T4 (Ground Rule 4) right after the header block.
- AC: every table row in §1–§7 carries at least one tier marker or is deleted.

### Task 3.2 — Methods appendix (new, final section)
Must document: (1) files parsed + SHA-256; (2) genbank-parser version + the `PFAM:` case bug and your workaround; (3) the family-count signature sets (link `scripts/recount_families.py`); (4) MIBiG confidence-tier definition (yours, not antiSMASH's — say so); (5) what was NOT run (BUSCO, BLAST vs NCBI, CAZy/dbCAN, InterProScan re-run).
- AC: a third party can regenerate every number in the document using only the appendix.

---

## Phase 4 — Verification (gate before publishing V6)

### Task 4.1 — Scripted checks (run all; all must pass)
```bash
# V-1 data integrity
[ "$(stat -c%s TA-input.gbk)" = "45029346" ] && [ "$(stat -c%s AF-antismash.gbk)" = "83318907" ] && echo PASS-1

# V-2 structure numbers
gbparse summary TA-input.gbk | grep -q "1376" && gbparse summary AF-antismash.gbk | grep -q "97" && echo PASS-2

# V-3 locus facts (sample; extend as needed)
gbparse locus TA-input.gbk PUJ_005301 | grep -q "11,954" && echo PASS-3a
gbparse locus TA-input.gbk PUJ_004623 | grep -q "39,732" && echo PASS-3b
gbparse locus AF-antismash.gbk PUJ_004419 | grep -q "72,805" && echo PASS-3c

# V-4 aflatoxin cluster ECs vs table
for pair in "PUJ_009383:2.1.1.110" "PUJ_009384:2.1.1.109" "PUJ_009391:3.1.1.94" \
            "PUJ_009392:1.1.1.352" "PUJ_009396:1.1.1.349" "PUJ_009397:2.3.1.221"; do
  tag=${pair%%:*}; ec=${pair##*:}
  grep -A 30 "locus_tag=\"$tag\"" AF-antismash.gbk | grep -q "EC_number=\"$ec\"" || echo "FAIL $tag"
done && echo PASS-4

# V-5 family counts
python scripts/recount_families.py && echo PASS-5

# V-6 forbidden numbers gone
! grep -n "1,144\|989 Phosphatase\|65 GST\|34 GST\|90% to 100% protein" agriculture-support-biocontrol-fungal-isolate-review.md && echo PASS-6

# V-7 BGC inventory completeness
[ "$(grep -c '^|' agriculture-support-biocontrol-fungal-isolate-review.md)" -gt 0 ] # plus manual: 74 AF rows / 21 TA rows in §7
```

### Task 4.2 — Human review checklist (sign-off)
- [ ] Every count in §1 and the exec banner has a signature-set footnote or is deleted.
- [ ] No "Validated" wording remains on inferred identifiers (KO/Pfam/UniProt identities).
- [ ] §4 biosafety table includes aflatoxin, CPA, aspirochlorine, aspergillic acid AND the nitropropionic-acid region, each with MIBiG/score/identity from `knownclusterblast` files.
- [ ] TA mycotoxin-risk row reads as "no known-mycotoxin match among 8 characterized regions; 13 orphan BGCs; constrained by partial assembly" — not "None detected".
- [ ] All locus citations use `TA:`/`AF:` prefixes.
- [ ] Assembly & Completeness section present with the caveat block referenced from every absence claim.
- [ ] §7 tables have 74 (AF) and 21 (TA) rows.
- [ ] Methods appendix allows independent regeneration of every number.
- [ ] Diff vs V5 reviewed line-by-line; nothing deleted silently (moved claims are marked `T4` or reworded, not vanished).

### Task 4.3 — Change log
Prepend to the document a "V5 → V6 changes" list mapping each edit to the audit finding ID (C1–C4, M1–M9, m1–m10) it resolves. Unmapped edits are not allowed.

---

## Definition of Done (all must hold)

1. All Phase 1 corrections applied and traceable to audit IDs.
2. Phase 2 additions present (completeness section, full BGC inventory, recount script committed, provenance box, coverage-gap subsections).
3. Phase 3 tier markers + methods appendix in place.
4. `scripts/recount_families.py` and all Phase 4 scripted checks exit 0.
5. Human checklist fully ticked, change log complete.
6. Version header bumped to `AGRI-BIOCONTROL-GENOMIC-SCRUTINY-V6` with date and "audit-corrected" note.

## What NOT to do
- Do not "fix" numbers by picking new ones without a signature-set method.
- Do not re-add external database identities (UniProt/RefSeq %) unless you actually BLAST and archive the output in the repo.
- Do not present mobilome/MEOR/xenobiotic-island output as phenotype or bioremediation capability (skill epistemic rules 4–5).
- Do not remove the two CAUTION blocks' regulatory directive for AF-PUJ — the toxigenic-lineage conclusion stands (the 21-locus cluster is present; the audit verified every locus length and the region coordinates); only the identity percentages and labeling needed repair.
