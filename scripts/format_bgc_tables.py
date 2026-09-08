#!/usr/bin/env python3
"""Format the full 21 TA and 74 AF BGC tables from bgc_inventory.json and save to bgc_tables.md."""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, "bgc_inventory.json"), encoding="utf-8") as f:
    inv = json.load(f)

lines = []

lines.append("### A. Isolate TA-PUJ (*Trichoderma asperellum*) — Full 21 BGC Regions Inventory\n")
lines.append("> **Inventory Summary:** 21 antiSMASH BGC regions detected across 21 contigs. Exactly **8 regions** have characterized MIBiG reference matches; **13 regions are uncharacterized orphan BGCs** (highlighting genomic novelty and uncharacterized secondary metabolic potential).\n")
lines.append("| # | Contig | Region ID | antiSMASH Type | Coordinates / Length | Top MIBiG Hit | Compound Annotation | Score | Genes | Identity Range | Confidence Tier | Agricultural Function / Category |")
lines.append("| :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- |")

# Agricultural function mapping for TA
ta_funcs = {
    "contig_1342_c1": "Insecticidal linear depsipeptide (leucinostatin family) [T2]",
    "contig_1419_c1": "Hydroxamate siderophore (ferric iron competition/uptake) [T2]",
    "contig_1710_c1": "Ionophoric cyclodepsipeptide (antifungal membrane disruptor) [T2]",
    "contig_1813_c1": "Volatile brasilane sesquiterpene (plant ISR priming) [T2]",
    "contig_1144_c1": "Pigment / polyketide derivative (cryptosporioptide-like) [T2]",
    "contig_1778_c1": "Squalene synthase inhibitor terpene (squalestatin-like) [T2]",
    "contig_52_c1": "Hybrid PKS-NRPS antibiotic / phytotoxin inhibitor (equisetin-like) [T2]",
    "contig_697_c1": "Putative alkaloid / insect feeding deterrent (peramine-like, low confidence) [T2]",
}

for i, r in enumerate(inv["TA"], 1):
    scaff = r["scaffold"]
    reg_id = r["region_id"]
    btype = r["type"]
    span = f"{r['start']:,}..{r['end']:,} ({r['length']:,} bp)"
    th = r["top_hit"]
    if th:
        comp = th["compound"]
        bgc = th["bgc"]
        score = f"{int(th['score']):,}"
        genes = str(th["n_prot"])
        id_r = th["id_range"]
        conf = r["confidence"]
        func = ta_funcs.get(reg_id, "Secondary metabolite biosynthesis [T2]")
        comp_str = f"**{comp}**"
    else:
        comp_str = "No MIBiG match (Orphan)"
        bgc = "—"
        score = "—"
        genes = "0"
        id_r = "—"
        conf = "ORPHAN"
        func = "Novel uncharacterized BGC; requires metabolomic profiling [T2]"
    lines.append(f"| {i} | `{scaff}` | `{reg_id}` | `{btype}` | {span} | `{bgc}` | {comp_str} | {score} | {genes} | {id_r} | **{conf}** | {func} |")

lines.append("\n---\n")
lines.append("### B. Isolate AF-PUJ (*Aspergillus flavus*) — Full 74 BGC Regions Inventory\n")
lines.append("> [!IMPORTANT]\n> **AF-PUJ Inventory Summary & Audit Finding M1:** 74 antiSMASH BGC regions detected across 27 scaffolds. Exactly **34 regions** have MIBiG KnownClusterBlast matches, whereas **40 of 74 AF regions have zero KnownClusterBlast hits (unassigned orphan BGCs)**. AF-PUJ harbors **5 confirmed toxigenic BGCs** (Aflatoxin B1/G1, CPA, Aspirochlorine, Aspergillic acid, and 3-Nitropropanoic acid).\n")
lines.append("| # | Scaffold | Region ID | antiSMASH Type | Coordinates / Length | Top MIBiG Hit / Rule | Compound / Category | Score | Genes | Identity Range | Confidence Tier | Biosafety & Functional Impact |")
lines.append("| :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- |")

# Biosafety / functional annotations for AF characterized regions
af_notes = {
    "1340_c1": "⛔ **CRITICAL TOXIN:** Intact cluster encoding Aflatoxin B1/G1 and Cyclopiazonic acid (CPA); eliminates live agricultural use [T2]",
    "480_c2": "⚠️ **CYTOTOXIN:** Aspirochlorine epipolythiodioxopiperazine (ETP) cluster; 19 genes with 94–100% identity [T2]",
    "1924_c1": "⚠️ **HEPATOTOXIN:** Aspergillic acid pyrazinone cluster; 6 genes with 75–100% identity [T2]",
    "703_c2": "⚠️ **NEUROTOXIN / MITOCHONDRIAL POISON:** 3-Nitropropanoic acid (3-NPA) BGC matched by rule `(NpaA & NpaB)` (17,956 bp) [T2]",
    "471_c1": "Aerobactin-like NIS siderophore cluster; domain prediction (`IucA/IucC`), 0 MIBiG hits [T1/T2]",
    "480_c3": "Leporin B BGC; hybrid PKS-NRPS anti-insectan/antibiotic compound [T2]",
    "418_c2": "Ustiloxin B fungal RiPP anti-tubulin toxin [T2]",
    "24_c4": "Asparasone A aflatoxin-shunt/pigment polyketide [T2]",
    "258_c3": "Flavunoidine cyclic peptide [T2]",
    "258_c4": "Astellolide A sesquiterpene lactone [T2]",
    "471_c3": "Aflavarin / aflatrem-related indole diterpene [T2]",
    "471_c4": "Metachelin-type hydroxamate siderophore NRPS [T2]",
    "480_c1": "Imizoquin alkaloid BGC (protective cell wall pigment/antioxidant) [T2]",
    "827_c1": "Metachelin C / dimerumic acid hydroxamate siderophore NRPS [T2]",
    "1457_c1": "Aspergillic acid secondary homologous match [T2]",
}

for i, r in enumerate(inv["AF"], 1):
    scaff = r["scaffold"]
    reg_id = r["region_id"]
    btype = r["type"]
    span = f"{r['start']:,}..{r['end']:,} ({r['length']:,} bp)"
    th = r["top_hit"]
    
    # Special annotation for 703_c2 (3-NPA)
    if reg_id == "703_c2":
        comp_str = "⚠️ **3-Nitropropanoic acid (3-NPA)**"
        bgc = "Rule match `(NpaA & NpaB)`"
        score = "—"
        genes = "4"
        id_r = "Specific rule"
        conf = "MEDIUM"
        note = af_notes["703_c2"]
    elif th:
        comp = th["compound"]
        bgc = th["bgc"]
        score = f"{int(th['score']):,}"
        genes = str(th["n_prot"])
        id_r = th["id_range"]
        conf = r["confidence"]
        if "aflatoxin" in comp.lower() or "cyclopiazonic" in comp.lower():
            comp_str = f"⛔ **{comp}**"
        elif "aspirochlorine" in comp.lower() or "aspergillic" in comp.lower():
            comp_str = f"⚠️ **{comp}**"
        else:
            comp_str = f"**{comp}**"
        note = af_notes.get(reg_id, f"Secondary metabolite BGC related to {th['compound'].split('/')[0]} [T2]")
    else:
        comp_str = "No MIBiG match (Orphan)"
        bgc = "—"
        score = "—"
        genes = "0"
        id_r = "—"
        conf = "ORPHAN"
        note = af_notes.get(reg_id, "Uncharacterized orphan BGC (zero KnownClusterBlast hits) [T2]")
        
    lines.append(f"| {i} | `{scaff}` | `{reg_id}` | `{btype}` | {span} | `{bgc}` | {comp_str} | {score} | {genes} | {id_r} | **{conf}** | {note} |")

output_path = os.path.join(BASE_DIR, "bgc_tables.md")
with open(output_path, "w", encoding="utf-8") as out:
    out.write("\n".join(lines) + "\n")

print(f"Successfully generated {output_path}")
