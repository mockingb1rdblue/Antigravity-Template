import os
import shutil
import re
import urllib.parse
from datetime import datetime

# Configuration
MANIFEST_FILE = "99_SEND_PRE-MEE/01_Confidential_Mediation_Statement.md"
MASTER_EXHIBITS_DIR = "50_MASTER_EXHIBITS"
STRATEGIC_MASTER_DIR = r"50_MASTER_EXHIBITS\00_Strategic_Master"
TARGET_DIR = "99_SEND_PRE-MEE"
EXHIBITS_BUNDLE_DIR = os.path.join(TARGET_DIR, "03_Exhibits_Bundle")
STRATEGIC_DOCS_DIR = os.path.join(TARGET_DIR, "02_Strategic_Documents")

def normalize_path(path):
    """Normalizes separators and decodes URL-encoded characters."""
    decoded = urllib.parse.unquote(path)
    return os.path.normpath(decoded).replace('/', os.sep)

def find_references(md_path):
    """Parses zip/EXHIBITS and zip/STRATEGIC paths from markdown."""
    if not os.path.exists(md_path):
        print(f"ERROR: Manifest not found: {md_path}")
        return []
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Matches zip/EXHIBITS/... or zip/STRATEGIC/... until .pdf (case insensitive)
    paths = re.findall(r"(zip/(?:EXHIBITS|STRATEGIC)/.*?\.pdf)", content, re.IGNORECASE)
    
    cleaned = []
    for p in paths:
        cleaned.append(p.strip())
    return list(set(cleaned))

def clean_targets():
    """Robustly cleans release folders using shutil.rmtree."""
    def on_error(func, path, exc_info):
        """Error handler to make read-only files writable and retry."""
        import stat
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except Exception as e:
            print(f"  [WAIT] Could not remove {os.path.basename(path)}: {e}")

    for folder in [EXHIBITS_BUNDLE_DIR, STRATEGIC_DOCS_DIR]:
        if os.path.exists(folder):
            print(f"Cleaning {folder}...")
            try:
                shutil.rmtree(folder, onerror=on_error)
            except Exception as e:
                print(f"  [SKIP] Folder cleanup error: {e}")

def sync():
    print(f"Manifest: {MANIFEST_FILE}")
    print(f"Dest:     {TARGET_DIR}")
    print("---------------------------------------------------")

    clean_targets()
    refs = find_references(MANIFEST_FILE)
    if not refs:
        print("WARNING: No zip/ references found.")
        return

    synced_count = 0
    missing_count = 0

    for ref in sorted(refs):
        if ref.startswith("zip/EXHIBITS/"):
            rel_path = ref.replace("zip/EXHIBITS/", "").replace("/", os.sep)
            src_path = os.path.join(MASTER_EXHIBITS_DIR, rel_path)
            dest_path = os.path.join(EXHIBITS_BUNDLE_DIR, rel_path)
        elif ref.startswith("zip/STRATEGIC/"):
            file_name = ref.replace("zip/STRATEGIC/", "").split("/")[-1]
            src_path = os.path.join(STRATEGIC_MASTER_DIR, file_name)
            dest_path = os.path.join(STRATEGIC_DOCS_DIR, file_name)
        else:
            continue

        # Signed Affidavit Priority
        if "Affidavit" in src_path and not "Signed" in src_path:
            signed_path = src_path.replace(".pdf", " Signed.pdf")
            if os.path.exists(signed_path):
                src_path = signed_path
                dest_path = dest_path.replace(".pdf", " Signed.pdf")

        if os.path.exists(src_path):
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
            print(f"[FILE]  Synced: {os.path.basename(src_path)}")
            synced_count += 1
        else:
            print(f"[ERR]   Missing: {src_path}")
            missing_count += 1

    print("---------------------------------------------------")
    print(f"Summary: {synced_count} files synced. {missing_count} missing.")

if __name__ == "__main__":
    sync()
