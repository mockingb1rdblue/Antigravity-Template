
import fitz  # pymupdf
import os

# Base directory for Exhibits
BASE_DIR = r"c:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\EXHIBITS"

# Map filename to specific subfolder if needed, or search locally
# We will walk the directory to find files on the fly

# Configuration: Filename -> List of phrases to highlight
TARGETS = {
    # Exhibit A
    "U.S. Employee Handbook.pdf": [
        "Interactive Process",
        "Accommodation",
        "Unpaid Leave",
        "Termination",
        "Zero Tolerance"
    ],
    "Vestas Personnel Guide.pdf": [
        "Interactive Process",
        "Accommodation"
    ],
    # Exhibit C
    "ADA2_transcript.pdf": [
        "normal process",
        "normal process for Vestas",
        "unpaid leave",
        "HR",
        "Colby"
    ],
    # Exhibit D
    "SVP_Lopez_Ticket_Closure.pdf": [
        "Emily Lopez",
        "Resolved",
        "Closed"
    ],
    # Exhibit E
    "Formal_Complaint.pdf": [
        "Retaliation",
        "Discrimination",
        "Hostile Work Environment"
    ],
    # Exhibit F
    "06_Payment Details _ My FAMLI+.pdf": [
        "Benefit End Date",
        "Exhausted"
    ],
    # Exhibit G
    "UNUM_Payment_$25.pdf": [
        "$25.00",
        "25.00"
    ],
    # Exhibit J
    "Exhibit J-1 - Job Posting.pdf": [
        "$3.00",
        "Night Shift",
        "differential",
        "3.00/hr"
    ],
    "Exhibit J-2 - Offer Letter.pdf": [
        "Salary",
        "Compensation",
        "Offer"
    ],
     "Exhibit J-1B - Shift Diff Proof.pdf": [
        "Shift Diff",
        "Differential",
        "0.00"
    ],
    # Exhibit K (Previously done, keeping for completeness)
    "01_Section_232_McGuireWoods.pdf": [
        "Commerce Department Launches Section 232 Tariff Investigation",
        "labor cost structures and domestic production capacity",
        "impact of foreign government subsidies",
        "artificially suppressed prices"
    ],
    "02_FTZ_Compliance_Guide_2025.pdf": [
        "Increased CBP audits",
        "ensure FTZ operators meet compliance standards",
        "Failure to comply",
        "hefty fines",
        "labor compliance standards",
        "suspension of FTZ benefits",
        "revocation of FTZ status"
    ],
    "02_FTZ_Vestas_Authorization.pdf": [
        "Vestas Nacelles America Inc.",
        "Subzone 123E"
    ],
    "03_IRA_Baker_Donelson.pdf": [
        "base applicable tax credit amount will be multiplied by five times",
        "multiplied by five times",
        "paid wages at rates not less than those set forth",
        "strict labor law compliance"
    ],
    "03_IRA_Prevailing_Wage_Reqs.pdf": [
        "recapture of the credit",
        "plus interest",
        "$5,000 penalty per affected worker"
    ]
}

def highlight_pdf_recursive():
    print("Starting comprehensive auto-highlighting...")
    
    # Walk through all directories starting from BASE_DIR
    for root, dirs, files in os.walk(BASE_DIR):
        for filename in files:
            if filename in TARGETS:
                phrases = TARGETS[filename]
                path = os.path.join(root, filename)
                
                print(f"Processing: {filename} in {root}")
                try:
                    doc = fitz.open(path)
                    found_count = 0
                    
                    for page in doc:
                        for phrase in phrases:
                            quads = page.search_for(phrase)
                            if quads:
                                page.add_highlight_annot(quads)
                                found_count += 1
                    
                    if found_count > 0:
                        # Save to a temporary file first then replace
                        tmp_path = path + ".tmp.pdf"
                        doc.save(tmp_path)
                        doc.close()
                        
                        # Replace original
                        os.replace(tmp_path, path)
                        print(f"  -> SUCCESS: Added {found_count} highlights.")
                    else:
                        print(f"  -> No phrases found to highlight for {filename}.")
                        doc.close()
                
                except Exception as e:
                    print(f"  -> ERROR checking {filename}: {e}")

if __name__ == "__main__":
    highlight_pdf_recursive()
