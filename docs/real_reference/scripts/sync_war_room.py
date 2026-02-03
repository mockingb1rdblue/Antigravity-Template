import os
import shutil
import datetime
import urllib.parse

# Configuration
SOURCE_DIR = "50_MASTER_EXHIBITS"
STRATEGIC_DIR = r"50_MASTER_EXHIBITS\00_Strategic_Master"
TARGET_DIR = r"99_WAR_ROOM\02_Exhibits_Full"
INDEX_FILE = r"99_WAR_ROOM\WAR_ROOM_INDEX.md"

# Critical Documents (Keywords/Substrings to flag)
CRITICAL_FLAGS = [
    "Liability_Admission",          # Exhibit F
    "Normal Process",               # Exhibit C
    "Exposure-Calculation",         # Exhibit J-5
    "Financial Strangulation",      # Exhibit M
    "Forced-PTO",                   # Exhibit J-6
    "Executive Ratification",       # Exhibit D
    "Affidavit_signed",             # Exhibit J-3
    "Shift Diff Breach",            # Exhibit J-1B
    "Bomb Threat",                  # Exhibit F
    "Sealed Medical"                # Exhibit H (Bring up if needed)
]

def sync_war_room():
    print(f"--- War Room Sync Started {datetime.datetime.now().strftime('%H:%M:%S')} ---")
    
    # 1. Clean Target (Robustly)
    if os.path.exists(TARGET_DIR):
        print(f"Cleaning {TARGET_DIR}...")
        def on_error(func, path, exc_info):
            import stat
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except Exception as e:
                print(f"  [WAIT] {os.path.basename(path)} locked/in use: {e}")

        try:
            shutil.rmtree(TARGET_DIR, onerror=on_error)
        except Exception as e:
             print(f"  [SKIP] Cleanup error on {TARGET_DIR}: {e}")
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    # 2. Copy All Files (Recursive) & Build Index
    index_content = ["# WAR ROOM EXHIBIT INDEX", "", "**Use this checklist during Mediator Breakout sessions.**", ""]
    
    # Process Strategic Documents First
    if os.path.exists(STRATEGIC_DIR):
        index_content.append(f"## Strategic Master Documents")
        dest_folder = os.path.join(TARGET_DIR, "00_Strategic_Master")
        os.makedirs(dest_folder, exist_ok=True)
        for file in os.listdir(STRATEGIC_DIR):
            if file.lower().endswith('.pdf'):
                shutil.copy2(os.path.join(STRATEGIC_DIR, file), os.path.join(dest_folder, file))
                encoded_file = urllib.parse.quote(file)
                link = f"[{file}](02_Exhibits_Full/00_Strategic_Master/{encoded_file})"
                index_content.append(f"- {link}")
        index_content.append("")

    for root, dirs, files in os.walk(SOURCE_DIR):
        # Determine relative path structure
        rel_path = os.path.relpath(root, SOURCE_DIR)
        
        # skip root folder files and strategic master (already processed)
        if rel_path == "." or rel_path == "00_Strategic_Master":
            continue

        dest_folder = os.path.join(TARGET_DIR, rel_path)
        os.makedirs(dest_folder, exist_ok=True)
        
        index_content.append(f"## {rel_path}")
        
        for file in files:
            # Enforce PDF only for War Room
            if not file.lower().endswith('.pdf'):
                continue
            
            # Signed Affidavit Priority Logic
            if "Affidavit" in file and not "Signed" in file:
                signed_version = file.replace(".pdf", " Signed.pdf")
                if signed_version in files:
                    continue # Skip unsigned version if signed exists
                
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_folder, file)
            
            shutil.copy2(src_file, dst_file)
            
            # Check for critical flags
            is_critical = False
            for val in CRITICAL_FLAGS:
                if val.lower() in file.lower() or val.lower() in rel_path.lower():
                    is_critical = True
                    break
            
            # Format flag
            flag = "🚨 **[CRITICAL - SHOW IN BREAKOUT]**" if is_critical else ""
            
            # Encode spaces in the path for clickability
            encoded_rel_path = urllib.parse.quote(rel_path.replace(os.sep, '/'))
            encoded_file = urllib.parse.quote(file)
            
            link = f"[{file}](02_Exhibits_Full/{encoded_rel_path}/{encoded_file})"
            index_content.append(f"- {flag} {link}")
            
        index_content.append("")
        
    # 3. Write Index
    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(index_content))
        
    print(f"Sync Complete. Index created at {INDEX_FILE}")

if __name__ == "__main__":
    sync_war_room()
