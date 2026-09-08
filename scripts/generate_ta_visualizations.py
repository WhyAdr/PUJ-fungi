#!/usr/bin/env python3
"""
generate_ta_visualizations.py

Generates publication-grade genomic visualizations using dna_features_viewer
for all 21 antiSMASH secondary metabolite BGC regions (including all 13 orphan BGCs)
and the 3 key biocontrol/rhizosphere micro-clusters of Trichoderma asperellum isolate TA-PUJ.

Outputs:
  - High-resolution PNG (300 DPI) and scalable vector SVG for each cluster into TA-viz/
  - Comprehensive interactive catalog document TA-viz/README.md with detailed gene tables,
    functional elaborations, collective architecture breakdowns, inline citations, and references.
"""

import os
import json
import re
from Bio import SeqIO
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from dna_features_viewer import GraphicFeature, GraphicRecord

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TA_DIR = os.path.join(BASE_DIR, "fungiSMASH-TA")
FULL_GBK = os.path.join(TA_DIR, "Funannotate-annotated-genome-TA.gbk")
OUT_DIR = os.path.join(BASE_DIR, "TA-viz")
os.makedirs(OUT_DIR, exist_ok=True)

# Functional Color Palette
COLOR_CORE = "#d1495b"        # Vibrant Crimson - Core Biosynthetic Synthase / Target Enzyme
COLOR_TAILORING = "#f58518"   # Amber Orange - Biosynthetic Tailoring / Modifying Enzyme
COLOR_TRANSPORT = "#2ca02c"   # Emerald Green - Transporter / Permease / Efflux
COLOR_REGULATORY = "#9467bd"  # Violet Purple - Transcription Factor / Kinase / Regulator
COLOR_OTHER = "#4c78a8"       # Steel Blue - Other CDS / Cellular Maintenance
COLOR_PSEUDO = "#bdbdbd"      # Muted Gray - Pseudogene / Fragment

# Pfam domain mappings for functional classification
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

def classify_gene(gene_info):
    """Classify gene into functional category and assign color and category name."""
    if gene_info.get("is_core", False):
        return COLOR_CORE, "Core Biosynthetic Synthase / Target Enzyme"
    
    prod = gene_info.get("product", "").lower()
    pfs = set(gene_info.get("pfam", []))
    
    if pfs & TRANSPORT_PFAMS or any(w in prod for w in ['transporter', 'permease', 'efflux', 'abc', 'carrier', 'mfs']):
        return COLOR_TRANSPORT, "Transport & Efflux"
    elif pfs & REGULATORY_PFAMS or any(w in prod for w in ['transcription', 'zinc finger', 'regulatory', 'regulator', 'kinase', 'dna-binding']):
        return COLOR_REGULATORY, "Regulation & Signaling"
    elif pfs & TAILORING_PFAMS or any(w in prod for w in ['synthase', 'synthetase', 'oxygenase', 'transferase', 'reductase', 'dehydrogenase', 'hydrolase', 'p450', 'oxidase', 'peptidase', 'transaminase', 'methyltransferase', 'esterase']):
        return COLOR_TAILORING, "Tailoring & Modifying Enzyme"
    else:
        return COLOR_OTHER, "Other CDS / Uncharacterized"

def format_gene_label(gene_info):
    """Generate compact two-line label for GraphicFeature."""
    symbol = gene_info.get("gene")
    tag = gene_info.get("locus_tag", "")
    prod = gene_info.get("product", "")
    pfs = gene_info.get("pfam", [])
    
    primary = symbol if symbol else tag
    
    # Secondary descriptor
    if symbol and tag:
        desc = tag
    elif prod and prod != "hypothetical protein":
        # Shorten product
        desc = prod
        desc = re.sub(r"\(.*?\)", "", desc).strip()
        if len(desc) > 18:
            desc = desc[:17] + "…"
    elif pfs:
        desc = pfs[0]
    else:
        desc = ""
        
    if desc:
        return f"{primary}\n{desc}"
    return primary

def render_cluster_figure(cluster, out_png, out_svg):
    """Render cluster using dna_features_viewer and matplotlib."""
    genes = cluster["genes"]
    if not genes:
        return
    
    start_pos = cluster["start"]
    end_pos = cluster["end"]
    span_len = end_pos - start_pos + 1
    
    graphic_features = []
    for g in genes:
        color, _ = classify_gene(g)
        label = format_gene_label(g)
        
        strand = g["strand"] if g["strand"] in (-1, 1) else 0
        graphic_features.append(
            GraphicFeature(
                start=g["start"],
                end=g["end"],
                strand=strand,
                color=color,
                linecolor="#2b2b2b",
                linewidth=1.2,
                label=label,
                fontdict={"fontsize": 8.5, "weight": "bold"}
            )
        )
        
    record = GraphicRecord(
        sequence_length=span_len,
        features=graphic_features,
        first_index=start_pos,
        plots_indexing="biopython"
    )
    
    # Dynamic figure dimensions
    n_genes = len(genes)
    fig_width = max(11.0, min(18.0, 1.25 * n_genes + (span_len / 4000.0)))
    fig_height = 4.2
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=300)
    
    # Render with dna_features_viewer
    record.plot(ax=ax, with_ruler=True)
    
    # Title & Subtitle banner
    cid = cluster["id"]
    scaff = cluster["scaffold"]
    ctype = cluster["type"]
    conf = cluster["confidence"]
    top_hit = cluster.get("top_hit")
    
    if top_hit:
        hit_text = f"MIBiG: {top_hit['compound']} (Score: {top_hit['score']}, ID: {top_hit['id_range']}) [Tier: {conf}]"
    elif conf == "ORPHAN":
        hit_text = "ORPHAN BGC (Novel Biosynthetic Candidate, No MIBiG Match)"
    else:
        hit_text = f"Functional Category: {cluster.get('name', ctype)} [Tier: {conf}]"
        
    title_str = f"Trichoderma asperellum TA-PUJ | {cid} ({scaff}) | Type: {ctype} | Span: {start_pos:,}–{end_pos:,} bp ({span_len:,} bp, {n_genes} CDSs)"
    ax.set_title(f"{title_str}\n{hit_text}", fontsize=10.5, weight="bold", pad=16, loc="left", color="#1a1a1a")
    
    # Custom functional legend
    legend_patches = [
        mpatches.Patch(color=COLOR_CORE, label="Core Synthase / Target Factor"),
        mpatches.Patch(color=COLOR_TAILORING, label="Tailoring / Modifying Enzyme"),
        mpatches.Patch(color=COLOR_TRANSPORT, label="Transport & Efflux"),
        mpatches.Patch(color=COLOR_REGULATORY, label="Regulation & Signaling"),
        mpatches.Patch(color=COLOR_OTHER, label="Other CDS / Uncharacterized"),
    ]
    ax.legend(handles=legend_patches, loc="upper right", bbox_to_anchor=(1.0, 1.30),
              ncol=5, frameon=False, fontsize=8)
    
    fig.tight_layout()
    fig.savefig(out_png, bbox_inches="tight", dpi=300)
    fig.savefig(out_svg, bbox_inches="tight")
    plt.close(fig)

print("generate_ta_visualizations.py template ready!")
