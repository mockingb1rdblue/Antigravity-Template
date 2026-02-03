
import fitz
import re
import os

BASE_DIR = r"c:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\originals\Financials"
TARGET = "EEPayrollPayCheckDetail.pdf"

def check_paycheck():
    path = os.path.join(BASE_DIR, TARGET)
    if not os.path.exists(path):
        print("File not found.")
        return

    print(f"Scanning {TARGET}...")
    try:
        doc = fitz.open(path)
        for page in doc:
            text = page.get_text()
            print(text[:500]) # Print first 500 chars to see headers/dates
            
            # Find dates
            dates = re.findall(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', text)
            print(f"Dates found: {dates}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    check_paycheck()
