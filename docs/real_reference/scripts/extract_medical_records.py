import fitz  # PyMuPDF
import os

pdf_path = r"c:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\originals\Medical\Records - AS .pdf"
output_path = r"c:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\medical_records_full.txt"

def extract_text():
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return

    try:
        doc = fitz.open(pdf_path)
        with open(output_path, "w", encoding="utf-8") as f:
            for page_num, page in enumerate(doc):
                text = page.get_text()
                f.write(f"--- Page {page_num + 1} ---\n")
                f.write(text)
                f.write("\n\n")
        print(f"Successfully extracted text to {output_path}")
    except Exception as e:
        print(f"Error extracting text: {e}")

if __name__ == "__main__":
    extract_text()
