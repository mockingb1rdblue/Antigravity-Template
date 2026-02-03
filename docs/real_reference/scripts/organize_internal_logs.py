import os
import shutil

root_path = r"c:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy"
exhibits_path = os.path.join(root_path, "EXHIBITS")
target_folder = os.path.join(exhibits_path, "Exhibit L - Internal Supporting Logs")

if not os.path.exists(target_folder):
    os.makedirs(target_folder)
    print(f"Created folder: {target_folder}")

moves = [
    ("originals/Legal/My Journal.md", "2025-08-28 - Complainant Private Journal (Full).md"),
    ("originals/Legal/vestas_MASS.md", "2026-01-23 - Master Case Chronology (MASS).md"),
    ("archive/EMAIL_COMMUNICATIONS_LOG.md", "2026-01-28 - Email Communications Log.md"),
]

for old_rel, new_name in moves:
    old_path = os.path.join(root_path, old_rel)
    new_path = os.path.join(target_folder, new_name)
    
    if os.path.exists(old_path):
        try:
            shutil.copy2(old_path, new_path)
            print(f"Copied and Renamed: {old_rel} -> {new_name}")
        except Exception as e:
            print(f"Error moving {old_rel}: {e}")
    else:
        print(f"Skip (Not Found): {old_rel}")
