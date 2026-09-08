#!/usr/bin/env python3
"""Automated Verification Suite V-1 through V-7 for AGRI-BIOCONTROL-GENOMIC-SCRUTINY-V6.

Exit code 0 on complete pass; non-zero if any check fails.
"""
import os
import re
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW_PATH = os.path.join(BASE_DIR, "agriculture-support-biocontrol-fungal-isolate-review.md")

with open(REVIEW_PATH, "r", encoding="utf-8") as f:
    review_text = f.read()

failures = []

def check(name, condition, msg=""):
    if condition:
        print(f"[PASS] {name}")
    else:
        print(f"[FAIL] {name}: {msg}")
        failures.append(f"{name}: {msg}")

print("=== RUNNING SUITE V-1: File Sizes & Payloads ===")
ta_in = os.path.join(BASE_DIR, "fungiSMASH-TA", "input", "Funannotate-annotated-genome-TA.gbk")
ta_out = os.path.join(BASE_DIR, "fungiSMASH-TA", "Funannotate-annotated-genome-TA.gbk")
af_out = os.path.join(BASE_DIR, "fungiSMASH-AF", "Funannotate-annotated-genome-AF.gbk")

check("V-1.1 TA Input GBK Size", os.path.getsize(ta_in) == 45029346, f"Got {os.path.getsize(ta_in)}")
check("V-1.2 TA Output GBK Size", os.path.getsize(ta_out) == 44880695, f"Got {os.path.getsize(ta_out)}")
check("V-1.3 AF Output GBK Size", os.path.getsize(af_out) == 83318907, f"Got {os.path.getsize(af_out)}")
check("V-1.4 TA Input Size in Review", "45,029,346" in review_text, "Missing 45,029,346 in review")
check("V-1.5 TA Output Size in Review", "44,880,695" in review_text, "Missing 44,880,695 in review")
check("V-1.6 AF Output Size in Review", "83,318,907" in review_text, "Missing 83,318,907 in review")

print("\n=== RUNNING SUITE V-2: Structural Numbers ===")
check("V-2.1 TA Contigs (1,376)", "1,376" in review_text, "Missing 1,376 contigs")
check("V-2.2 AF Scaffolds (97)", "97" in review_text, "Missing 97 scaffolds")
check("V-2.3 TA Assembly Completeness Warning", "~55–60%" in review_text or "~55-60%" in review_text, "Missing ~55-60% completeness")

print("\n=== RUNNING SUITE V-3: Correct Coordinates ===")
check("V-3.1 TA:PUJ_005301 Coordinates", "11,954..13,395" in review_text, "Coordinates 11,954..13,395 not found")
check("V-3.2 TA:PUJ_004623 Coordinates", "39,732..42,710" in review_text, "Coordinates 39,732..42,710 not found")
check("V-3.3 AF:PUJ_004419 Siderophore Operon", "AF:PUJ_004419" in review_text and "797 aa" in review_text, "AF:PUJ_004419 797 aa not found")

print("\n=== RUNNING SUITE V-4: Aflatoxin Cluster & 3-NPA ===")
check("V-4.1 Aflatoxin Top Hit BGC0000007.3", "BGC0000007.3" in review_text, "BGC0000007.3 not found")
check("V-4.2 CPA Hit BGC0000977.4", "BGC0000977.4" in review_text, "BGC0000977.4 not found")
check("V-4.3 Aspirochlorine Hit BGC0001123.5", "BGC0001123.5" in review_text, "BGC0001123.5 not found")
check("V-4.4 Aspergillic Acid Hit BGC0001516.5", "BGC0001516.5" in review_text, "BGC0001516.5 not found")
check("V-4.5 3-Nitropropanoic Acid (3-NPA) Included", "3-Nitropropanoic acid" in review_text and "703_c2" in review_text, "3-NPA / 703_c2 not found")
check("V-4.6 Five Toxigenic BGCs Declared", "five confirmed toxigenic BGCs" in review_text or "5 confirmed toxigenic BGCs" in review_text, "Five confirmed toxigenic BGCs not stated")

print("\n=== RUNNING SUITE V-5: recount_families.py Execution ===")
recount_script = os.path.join(BASE_DIR, "scripts", "recount_families.py")
res = subprocess.run([sys.executable, recount_script], capture_output=True, text=True)
check("V-5.1 recount_families.py exits 0", res.returncode == 0, f"Error: {res.stderr}")

print("\n=== RUNNING SUITE V-6: Absence of Forbidden / Deprecated Text ===")
check("V-6.1 No '1,144' (deprecated phosphatase count)", "1,144" not in review_text, "Found 1,144 in review text")
check("V-6.2 No '989 Phosphatase'", "989 Phosphatase" not in review_text, "Found 989 Phosphatase in review text")
check("V-6.3 No '90% to 100% protein'", "90% to 100% protein" not in review_text, "Found '90% to 100% protein' in review text")
check("V-6.4 No Legacy '34 GST'", "34 GST" not in review_text, "Found '34 GST' in review text")
check("V-6.5 No Legacy '65 GST'", "65 GST" not in review_text, "Found '65 GST' in review text")

print("\n=== RUNNING SUITE V-7: BGC Inventory Row Counts & Sections ===")
# Parse Section 7A and 7B table rows
sec7_text = review_text.split("## 7. Comprehensive BGC Inventory & MIBiG Evidence Summary")[1]
if "## 8. Coverage Gaps" in sec7_text:
    sec7_tables = sec7_text.split("## 8. Coverage Gaps")[0]
else:
    sec7_tables = sec7_text

ta_matches = re.findall(r'\|\s*\d+\s*\|\s*`contig_[^`]+`\s*\|\s*`contig_\d+_c\d+`', sec7_tables)
af_matches = re.findall(r'\|\s*\d+\s*\|\s*`\d+`\s*\|\s*`\d+_c\d+`', sec7_tables)
check("V-7.1 TA BGC Table Has Exactly 21 Rows", len(ta_matches) == 21, f"Found {len(ta_matches)} rows")
check("V-7.2 AF BGC Table Has Exactly 74 Rows", len(af_matches) == 74, f"Found {len(af_matches)} rows")
check("V-7.3 40 Orphan AF Regions Explicitly Declared", "40 of 74 AF regions have zero KnownClusterBlast hits" in review_text, "Missing 40 orphan declaration")
check("V-7.4 Section 8 Present with Subsections", "#### 8.1 Peptaibol" in review_text and "#### 8.2 Auxin" in review_text and "#### 8.3 Secondary Metabolite" in review_text, "Section 8 subsections missing")
check("V-7.5 Section 9 Methods Appendix Present", "## 9. Comprehensive Methods Appendix" in review_text, "Section 9 missing")
check("V-7.6 Section 10 Audit Change Log Present", "## 10. Audit Findings & Traceability Change Log" in review_text, "Section 10 missing")
check("V-7.7 Section 11 Attributions Present", "## 11. Database Attributions & Licensing Notices" in review_text, "Section 11 missing")

print("\n==========================================")
if failures:
    print(f"TOTAL FAILURES: {len(failures)}")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("ALL VERIFICATION CHECKS PASSED (EXIT 0)")
    sys.exit(0)
