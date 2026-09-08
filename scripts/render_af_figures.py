#!/usr/bin/env python3
"""
render_af_figures.py

Renders publication-grade gene cluster diagrams (PNG 300 DPI + vector SVG)
for all 77 gene clusters of Aspergillus flavus AF-PUJ into d:/W/fungi-PUJ/AF-viz/
Adheres strictly to Revision V3 styling standards:
- Single-line curated gene symbols
- Elevated outline boxes (#f8f9fa, rounded border)
- Fine vertical leader lines (#555555)
- Sub-track cluster span brackets (#b05d1a) with physical coordinates and locus counts
- Standardized functional role color coding
- Windows thumbnail locking retry protection
"""

import os
import sys
import time
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from dna_features_viewer import GraphicFeature, GraphicRecord

BASE_DIR = r"d:\W\fungi-PUJ"
AF_VIZ_DIR = os.path.join(BASE_DIR, "AF-viz")
os.makedirs(AF_VIZ_DIR, exist_ok=True)

DATA_PATH = os.path.join(r"C:\Users\LIHTR-UA\.gemini\antigravity-ide\brain\3fe8e0ad-dc1d-4879-8858-a6bd7587c92e\scratch", "af_cluster_data.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    clusters = json.load(f)

print(f"Loaded {len(clusters)} AF clusters from cache.")

# Color constants
COLOR_CORE = "#d1495b"        # Vibrant Crimson
COLOR_TAILORING = "#f58518"   # Amber Orange
COLOR_TRANSPORT = "#2ca02c"   # Emerald Green
COLOR_REGULATORY = "#9467bd"  # Violet Purple
COLOR_OTHER = "#4c78a8"       # Steel Blue

TAILORING_PFAMS = {
    'PF00067', 'PF00082', 'PF00106', 'PF00107', 'PF00132', 'PF00141', 'PF00149',
    'PF00155', 'PF00171', 'PF00248', 'PF00291', 'PF00385', 'PF00389', 'PF00393',
    'PF00394', 'PF00698', 'PF00704', 'PF00891', 'PF00933', 'PF01063', 'PF01261',
    'PF01370', 'PF01425', 'PF01915', 'PF02423', 'PF02668', 'PF02798', 'PF02826',
    'PF03446', 'PF04183', 'PF04185', 'PF04695', 'PF05704', 'PF06609', 'PF07731',
    'PF08787', 'PF13409', 'PF13410', 'PF13450'
}
TRANSPORT_PFAMS = {'PF00005', 'PF00083', 'PF00324', 'PF03239', 'PF07690', 'PF11915'}
REGULATORY_PFAMS = {'PF00046', 'PF00069', 'PF00096', 'PF00172', 'PF08493'}

def classify_gene(g):
    sym = g.get("gene_symbol", "").lower()
    prod = g.get("product", "").lower()
    pfs = set(g.get("pfam", []))
    
    # Specific known symbols
    if sym in ("pksa", "cpaa", "iuca", "asaa", "acla", "lepa", "asta", "dapa", "afva", "dtpa", "ywa1", "acva", "msas", "pho13", "ipp1"):
        return COLOR_CORE, "Core Synthase / Target Enzyme"
    if sym in ("aflr", "ustr", "pho2", "iucr"):
        return COLOR_REGULATORY, "Regulation & Signaling"
    if sym in ("aflt", "cpat", "asad", "aclt", "iuct"):
        return COLOR_TRANSPORT, "Transport & Efflux"
        
    if g.get("is_core", False):
        return COLOR_CORE, "Core Synthase / Target Enzyme"
        
    if pfs & TRANSPORT_PFAMS or any(w in prod for w in ['transporter', 'permease', 'efflux', 'abc', 'carrier', 'mfs']):
        return COLOR_TRANSPORT, "Transport & Efflux"
    elif pfs & REGULATORY_PFAMS or any(w in prod for w in ['transcription', 'zinc finger', 'regulatory', 'regulator', 'kinase', 'dna-binding']):
        return COLOR_REGULATORY, "Regulation & Signaling"
    elif pfs & TAILORING_PFAMS or any(w in prod for w in ['synthase', 'synthetase', 'oxygenase', 'transferase', 'reductase', 'dehydrogenase', 'hydrolase', 'p450', 'oxidase', 'peptidase', 'transaminase', 'methyltransferase', 'esterase', 'ketoreductase', 'amylase', 'glucosidase']):
        return COLOR_TAILORING, "Tailoring & Modifying Enzyme"
    else:
        return COLOR_OTHER, "Other CDS / Uncharacterized"

def get_file_slug(idx, c):
    if c["category"] == "BGC":
        cid = c["id"].replace("scaffold_", "")
        top = c.get("top_hit")
        if "1340" in cid:
            return f"BGC_{idx+1:02d}_scaffold_1340_c1_aflatoxin_CPA_supercluster"
        elif "471_c1" in cid:
            return f"BGC_{idx+1:02d}_scaffold_471_c1_aerobactin_NIS_siderophore"
        
        comp = top["compound"].split("/")[0].replace(" ", "_").replace("'", "").replace("-", "_").replace("(", "").replace(")", "").lower() if top else "orphan"
        ctype = c["type"].replace("-", "_").replace(" ", "_").lower()
        if comp == "orphan":
            return f"BGC_{idx+1:02d}_scaffold_{cid}_orphan_{ctype}"
        else:
            return f"BGC_{idx+1:02d}_scaffold_{cid}_{comp}"
    else:
        # Micro-clusters
        if "75" in c["id"]:
            return "CLUSTER_75_scaffold_24_phosphate_solubilizing_PHO13_IPP1"
        elif "76" in c["id"]:
            return "CLUSTER_76_scaffold_482_phosphate_regulator_PHO2_AMY3"
        else:
            return "CLUSTER_77_scaffold_1339_phosphate_sensor_PHO81_redox"

def render_cluster(idx, cl):
    slug = get_file_slug(idx, cl)
    png_path = os.path.join(AF_VIZ_DIR, f"{slug}.png")
    svg_path = os.path.join(AF_VIZ_DIR, f"{slug}.svg")
    
    genes = cl["genes"]
    start_pos = cl["start"]
    end_pos = cl["end"]
    span_len = end_pos - start_pos + 1
    n_genes = len(genes)
    
    features = []
    for g in genes:
        color, _ = classify_gene(g)
        label = g.get("gene_symbol", g["locus_tag"])
        features.append(
            GraphicFeature(
                start=g["start"],
                end=g["end"],
                strand=g["strand"] if g["strand"] in (-1, 1) else 0,
                color=color,
                linecolor="#222222",
                linewidth=1.2,
                thickness=18,
                label=label,
                fontdict={"color": "#111111", "fontweight": "bold", "fontsize": 8.0},
                box_color="#f8f9fa",
                box_linewidth=0.8,
                label_link_color="#555555"
            )
        )
        
    record = GraphicRecord(
        sequence_length=span_len,
        features=features,
        first_index=start_pos,
        feature_level_height=1.4,
        labels_spacing=10,
        plots_indexing="biopython"
    )
    
    fig_width = max(11.5, min(19.5, 1.25 * n_genes + (span_len / 5000.0)))
    fig_height = 4.2
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=300)
    record.plot(
        ax=ax,
        with_ruler=True,
        annotate_inline=False,
        elevate_outline_annotations=True,
        level_offset=0.30
    )
    
    # Calculate max text position to tighten vertical bounds
    texts = [t for t in ax.texts]
    max_ty = max(t.get_position()[1] for t in texts) if texts else 2.0
    ax.set_ylim(-0.85, max_ty + 1.2)
    
    # Sub-track cluster span bracket
    x_min_gene = min(g["start"] for g in genes)
    x_max_gene = max(g["end"] for g in genes)
    gene_span_kb = (x_max_gene - x_min_gene + 1) / 1000.0
    
    bracket_y = -0.45
    cap_h = 0.08
    bracket_color = "#b05d1a"
    ax.plot([x_min_gene, x_min_gene, x_max_gene, x_max_gene],
            [bracket_y + cap_h, bracket_y, bracket_y, bracket_y + cap_h],
            color=bracket_color, lw=1.5)
            
    cid = cl["id"]
    scaff = cl["scaffold"]
    ctype = cl["type"]
    conf = cl["confidence"]
    top_hit = cl.get("top_hit")
    
    if "1340" in cid:
        bracket_label = f"aflatoxin / cyclopiazonic acid super-cluster ({n_genes} CDSs, {gene_span_kb:.1f} kb)"
    elif "471_c1" in cid:
        bracket_label = f"aerobactin-like NIS siderophore cluster ({n_genes} CDSs, {gene_span_kb:.1f} kb)"
    elif top_hit:
        bracket_label = f"{top_hit['compound'].split('/')[0]} cluster ({n_genes} CDSs, {gene_span_kb:.1f} kb)"
    elif conf == "ORPHAN":
        bracket_label = f"{ctype} orphan cluster ({n_genes} CDSs, {gene_span_kb:.1f} kb)"
    else:
        bracket_label = f"{cl.get('name', ctype)} locus span ({n_genes} CDSs, {gene_span_kb:.1f} kb)"
        
    ax.text((x_min_gene + x_max_gene) / 2.0, bracket_y - 0.08,
            bracket_label,
            ha="center", va="top", color=bracket_color, fontsize=8.5, fontweight="bold", style="italic")
            
    ax.set_xlabel(f"{scaff} position (bp)", fontsize=9, color="#444444", labelpad=8)
    
    if top_hit:
        hit_text = f"MIBiG: {top_hit['compound']} (Score: {top_hit['score']}, ID: {top_hit['id_range']}) [Tier: {conf}]"
    elif conf == "ORPHAN":
        hit_text = "ORPHAN BGC (Novel Biosynthetic Candidate, No MIBiG Match)"
    else:
        hit_text = f"Functional Category: {cl.get('name', ctype)} [Tier: {conf}]"
        
    title_str = f"Aspergillus flavus AF-PUJ | {cid} ({scaff}) | Type: {ctype} | Span: {start_pos:,}–{end_pos:,} bp ({span_len:,} bp, {n_genes} CDSs)"
    ax.set_title(f"{title_str}\n{hit_text}", fontsize=10.5, weight="bold", pad=16, loc="left", color="#1a1a1a")
    
    legend_patches = [
        mpatches.Patch(color=COLOR_CORE, label="Core Synthase / Target Enzyme"),
        mpatches.Patch(color=COLOR_TAILORING, label="Tailoring / Modifying Enzyme"),
        mpatches.Patch(color=COLOR_TRANSPORT, label="Transport & Efflux"),
        mpatches.Patch(color=COLOR_REGULATORY, label="Regulation & Signaling"),
        mpatches.Patch(color=COLOR_OTHER, label="Other CDS / Uncharacterized"),
    ]
    ax.legend(handles=legend_patches, loc="upper right", bbox_to_anchor=(1.0, 1.30),
              ncol=5, frameon=False, fontsize=8)
              
    for attempt in range(5):
        try:
            fig.savefig(png_path, bbox_inches="tight", dpi=300)
            break
        except Exception as e:
            time.sleep(0.6)
            
    for attempt in range(5):
        try:
            fig.savefig(svg_path, bbox_inches="tight")
            break
        except Exception as e:
            time.sleep(0.6)
            
    plt.close(fig)
    return slug

def main():
    print("Starting batch rendering for 77 AF clusters...")
    start_time = time.time()
    
    for idx, cl in enumerate(clusters):
        t0 = time.time()
        slug = render_cluster(idx, cl)
        dt = time.time() - t0
        print(f"[{idx+1:02d}/77] Rendered {slug} in {dt:.2f}s")
        
    total_time = time.time() - start_time
    print(f"\nCompleted all 77 clusters in {total_time:.1f}s ({total_time/77:.2f}s per cluster)!")

if __name__ == "__main__":
    main()
