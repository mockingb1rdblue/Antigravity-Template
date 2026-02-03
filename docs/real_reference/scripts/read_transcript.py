
import fitz
import os

BASE_DIR = r"c:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\originals\Legal"
TARGET = "ADA2_transcript.pdf"

def read_transcript():
    path = os.path.join(BASE_DIR, TARGET)
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    print(f"Reading {TARGET}...")
    try:
        doc = fitz.open(path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        
        print("--- START TRANSCRIPT ---")
        print(full_text)
        print("--- END TRANSCRIPT ---")
            
    except Exception as e:
        print(e)

if __name__ == "__main__":
    read_transcript()
