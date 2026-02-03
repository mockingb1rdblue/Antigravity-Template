
import fitz
import os

BASE_DIR = r"c:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\originals"

# Keywords to find "Alternate Material" requests or "Motion Based" clarifications
TARGETS = [
    "alternate material",
    "lighter material",
    "motion based",
    "repetitive motion",
    "weight restriction",
    "630v",
    "cable",
    "ignored",
    "clarify",
    "misunderstood"
]

def search_evidence():
    print("Starting Evidence Search...")
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                path = os.path.join(root, file)
                try:
                    doc = fitz.open(path)
                    print(f"Scanning: {file}")
                    match_count = 0
                    for i, page in enumerate(doc):
                        text = page.get_text().lower()
                        for target in TARGETS:
                            if target in text:
                                # Find index for context
                                idx = text.find(target)
                                start = max(0, idx - 50)
                                end = min(len(text), idx + 100)
                                context = text[start:end].replace('\n', ' ')
                                
                                print(f"  [Page {i+1}] Found '{target}': ...{context}...")
                                match_count += 1
                                if match_count > 5: break # Don't spam if file is full of hits
                        if match_count > 5: break
                    doc.close()
                except Exception as e:
                    print(f"Error reading {file}: {e}")

if __name__ == "__main__":
    search_evidence()
