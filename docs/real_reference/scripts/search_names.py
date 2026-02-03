
import fitz
import os

BASE_DIR = r"c:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\originals"

TARGETS = ["Dan Meng", "Jenny Martinez", "Daniel Meng", "Jennifer Martinez"]

def search_pdfs():
    print("Starting Deep Scan for Names...")
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                path = os.path.join(root, file)
                try:
                    doc = fitz.open(path)
                    found = False
                    for i, page in enumerate(doc):
                        text = page.get_text()
                        for target in TARGETS:
                            if target.lower() in text.lower():
                                print(f"MATCH FOUND: {target} in '{file}' (Page {i+1})")
                                print(f"   Context: {text.replace('\n', ' ')[:200]}...") # Print a bit of context
                                found = True
                    if found:
                        print("-" * 40)
                    doc.close()
                except Exception as e:
                    print(f"Error reading {file}: {e}")

if __name__ == "__main__":
    search_pdfs()
