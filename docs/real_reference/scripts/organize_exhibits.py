import os

base_path = r"c:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\50_MASTER_EXHIBITS"

renames = [
    # Exhibit A
    ("Exhibit A - Written Policies/Exhibit A - Attendance Policy.pdf", "Exhibit A - Written Policies/2024-01-01 - Attendance Policy.pdf"),
    ("Exhibit A - Written Policies/Exhibit A - Employee Handbook.pdf", "Exhibit A - Written Policies/2024-01-01 - U.S. Employee Handbook.pdf"),
    ("Exhibit A - Written Policies/Exhibit A - Hourly PTO Policy.pdf", "Exhibit A - Written Policies/2024-01-01 - Hourly PTO Policy.pdf"),
    ("Exhibit A - Written Policies/Exhibit A - Leave of Absence Policy.pdf", "Exhibit A - Written Policies/2024-01-01 - Leave of Absence Policy.pdf"),
    ("Exhibit A - Written Policies/Exhibit A - Performance Management Policy.pdf", "Exhibit A - Written Policies/2024-01-01 - Performance Management Policy.pdf"),
    ("Exhibit A - Written Policies/Exhibit A - Personnel Guide.pdf", "Exhibit A - Written Policies/2025-07-17 - Vestas Personnel Guide.pdf"),
    ("Exhibit A - Written Policies/Exhibit A - Termination Policy.pdf", "Exhibit A - Written Policies/2024-01-01 - Termination Policy.pdf"),
    
    # Exhibit B
    ("Exhibit B - Timeline/2025-03-25 - Liability Admission (Journal Snippet).pdf", "Exhibit B - Timeline/2025-03-25 - Liability Admission (Evidentiary Snippet).pdf"),
    ("Exhibit B - Timeline/2025-03-25 - Journal Entry (Locke Liability Admission).pdf", "Exhibit B - Timeline/2025-03-25 - Liability Admission (Internal Log).pdf"),
    
    # Exhibit C
    ("Exhibit C - July 17 Recording/2025-07-17 - Normal Process Admission (Transcript).pdf", "Exhibit C - July 17 Recording/2025-07-17 - Admission of Normal Process (Transcript Excerpt).pdf"),
    ("Exhibit C - July 17 Recording/2025-07-17 - Normal Process Admission (Log Snippet).pdf", "Exhibit C - July 17 Recording/2025-07-17 - Admission of Normal Process (Evidentiary Snippet).pdf"),
    ("Exhibit C - July 17 Recording/Exhibit C-2 - Termination Chain of Command.pdf", "Exhibit C - July 17 Recording/2025-07-17 - Admission of Termination Instruction (Excerpt).pdf"),
    
    # Exhibit G
    ("Exhibit G - Bad Faith Conduct/Exhibit G-4 - IP Obstruction.pdf", "Exhibit G - Bad Faith Conduct/2025-07-15 - Interactive Process Obstruction.pdf"),
    ("Exhibit G - Bad Faith Conduct/Exhibit G-5 - Impossible Monitoring Standard.pdf", "Exhibit G - Bad Faith Conduct/2025-07-25 - Impossible Monitoring Standard.pdf"),
    ("Exhibit G - Bad Faith Conduct/Exhibit G - Bad Faith (UNUM Payment).pdf", "Exhibit G - Bad Faith Conduct/2025-06-10 - UNUM Payment $25.75 (Evidence of Delay).pdf"),
]

for old_rel, new_rel in renames:
    old_path = os.path.join(base_path, old_rel)
    new_path = os.path.join(base_path, new_rel)
    if os.path.exists(old_path):
        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {old_rel} -> {new_rel}")
        except Exception as e:
            print(f"Error renaming {old_rel}: {e}")
    else:
        print(f"Skip (Not Found): {old_rel}")

# Cleanup Exhibit A-3 which is redundant
redundant_a3 = os.path.join(base_path, "Exhibit A - Written Policies/Exhibit A-3 - Mar 20 Accommodation Request.pdf")
if os.path.exists(redundant_a3):
    os.remove(redundant_a3)
    print("Removed redundant Exhibit A-3")
