
import fitz  # pymupdf
import re
import os

# Base directory
BASE_DIR = r"c:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\originals"

# Files to extract from (Relative to BASE_DIR)
TARGET_FILES = [
    r"Employment\vestasASjobOfferSigned.pdf",
    r"E2600030468_Statement_of_Discrimination_.pdf",
    r"Financials\250207_EEPayrollPayCheckDetail.aspx.pdf",
    r"Medical\Records - AS .pdf" # If accessible
]

# Regex patterns
DATE_PATTERNS = [
    r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{1,2},? \d{4}\b', # Oct 10, 2024
    r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',      # 10/10/24 or 10/10/2024
    r'\b\d{4}-\d{2}-\d{2}\b',             # 2024-10-10
    r'Start Date[:\s]*\d{1,2}/\d{1,2}/\d{4}'
]

def extract_dates_from_pdf(rel_path):
    path = os.path.join(BASE_DIR, rel_path)
    if not os.path.exists(path):
        # Try finding it in root if not in subfolder
        basename = os.path.basename(path)
        path = os.path.join(BASE_DIR, basename)
        if not os.path.exists(path):
            print(f"Skipping (not found): {path}")
            return

    print(f"\n--- Scanning: {os.path.basename(path)} ---")
    try:
        doc = fitz.open(path)
        
        # Limit pages for large docs
        max_pages = 10 if "Medical" in path else 50
        
        for i, page in enumerate(doc):
            if i >= max_pages: break
            
            text = page.get_text()
            
            # Simple keyword search for Context
            if "Start Date" in text or "start date" in text:
                 print(f"  [Page {i+1}] Found 'Start Date' context:\n    " + text.replace('\n', ' ')[:200] + "...")

            # Regex Date Search
            found_dates = []
            for pattern in DATE_PATTERNS:
                matches = re.findall(pattern, text, re.IGNORECASE)
                found_dates.extend(matches)
            
            if found_dates:
                # Dedupe and print
                unique_dates = sorted(list(set(found_dates)))
                print(f"  [Page {i+1}] Dates found: {unique_dates}")

    except Exception as e:
        print(f"  ERROR: {e}")

if __name__ == "__main__":
    for f in TARGET_FILES:
        extract_dates_from_pdf(f)
