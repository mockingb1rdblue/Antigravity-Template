import shutil
import os

base_path = r"c:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy"

operations = [
    ("move", r"EXHIBITS\Exhibit G - Bad Faith Conduct\Exhibit G-12 - July 22 Hostile Overrule (Email).pdf", r"EXHIBITS\Exhibit G - Bad Faith Conduct\2025-07-22 - Hostile Overrule of Manager Approval.pdf"),
    ("move", r"EXHIBITS\Exhibit G - Bad Faith Conduct\Exhibit G-13 - July 17 Formal Meeting Summary.pdf", r"EXHIBITS\Exhibit G - Bad Faith Conduct\2025-07-23 - HR Closure of Interactive Process.pdf"),
    ("copy", r"originals\Legal\250804_Re Ensuring Alignment for a Safe and Productive Return.pdf", r"EXHIBITS\Exhibit G - Bad Faith Conduct\2025-07-24 - RTW Proposal (Softer Cable solution).pdf"),
    ("copy", r"originals\Legal\250804_Re Ensuring Alignment for a Safe and Productive Return.pdf", r"EXHIBITS\Exhibit G - Bad Faith Conduct\2025-07-25 - Demand for Impossible Prohibited Task List.pdf"),
    ("move", r"EXHIBITS\Exhibit G - Bad Faith Conduct\Exhibit G-9 - Aug 4 Final Impasse.pdf", r"EXHIBITS\Exhibit G - Bad Faith Conduct\2025-08-04 - Final RTW Impasse (Email).pdf"),
    ("move", r"EXHIBITS\Exhibit G - Bad Faith Conduct\Exhibit G-10 - CCRD Statement (Harassment Incident).pdf", r"EXHIBITS\Exhibit G - Bad Faith Conduct\2025-08-05 - Record of Co-worker Harassment.pdf"),
    ("copy", r"originals\Medical\Records - AS .pdf", r"EXHIBITS\Exhibit H - Sealed Medical Records\2024-11-20 - Initial Medical Documentation.pdf"),
    ("move", r"EXHIBITS\Exhibit D - Executive Ratification\Exhibit D - Executive Ratification (Lopez Closure).pdf", r"EXHIBITS\Exhibit D - Executive Ratification\2025-04-18 - Internal Complaint (SVP Lopez Closure).pdf"),
]

for op_type, src_rel, dst_rel in operations:
    src = os.path.join(base_path, src_rel)
    dst = os.path.join(base_path, dst_rel)
    
    try:
        if op_type == "move":
            if os.path.exists(src):
                shutil.move(src, dst)
                print(f"MOVED: {src_rel} -> {dst_rel}")
            else:
                print(f"SKIP (Not Found): {src_rel}")
        elif op_type == "copy":
            if os.path.exists(src):
                shutil.copy2(src, dst)
                print(f"COPIED: {src_rel} -> {dst_rel}")
            else:
                print(f"SKIP (Not Found): {src_rel}")
    except Exception as e:
        print(f"ERROR on {src_rel}: {e}")
