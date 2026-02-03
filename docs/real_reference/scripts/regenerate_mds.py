import os
import fitz  # pymupdf

# Configuration
EXHIBIT_FILES = [
    r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\50_MASTER_EXHIBITS\Exhibit C - July 17 Recording\Exhibit C-1 - Normal Process Admission.pdf",
    r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\50_MASTER_EXHIBITS\Exhibit C - July 17 Recording\Exhibit C-2 - Termination Chain of Command.pdf",
    r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\50_MASTER_EXHIBITS\Exhibit G - Bad Faith Conduct\Exhibit G-4 - IP Obstruction.pdf",
    r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\50_MASTER_EXHIBITS\Exhibit G - Bad Faith Conduct\Exhibit G-5 - Impossible Monitoring Standard.pdf",
    r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\50_MASTER_EXHIBITS\Exhibit G - Bad Faith Conduct\Exhibit G-6 - Manager Approval Overruled.pdf",
    r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\50_MASTER_EXHIBITS\Exhibit J - Compensation Compliance Audit\Exhibit-J-3-Affidavit.pdf",
    r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\50_MASTER_EXHIBITS\Exhibit J - Compensation Compliance Audit\Exhibit-J-5-Exposure-Calculation.pdf",
    r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\50_MASTER_EXHIBITS\Exhibit M - Financial Strangulation\Exhibit M - Financial Strangulation System.pdf",
]

TARGET_DIRECTORIES = [
    r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\01_originals",
]

def pdf_to_md(pdf_path):
    output_path = os.path.splitext(pdf_path)[0] + ".md"
    
    try:
        doc = fitz.open(pdf_path)
        text_content = []
        
        # Add Title
        title = doc.metadata.get('title') or os.path.basename(pdf_path)
        text_content.append(f"# {title}\n")
        
        for page_num, page in enumerate(doc):
            text_content.append(f"\n## Page {page_num + 1}\n")
            text = page.get_text()
            text_content.append(text)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(text_content))
        
        print(f"Converted: {os.path.basename(pdf_path)} -> .md")
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")

def main():
    print("--- Starting Batch PDF Conversion ---")
    
    # 1. Process specific files
    print("\nProcessing Specific Exhibits...")
    for pdf_path in EXHIBIT_FILES:
        if os.path.exists(pdf_path):
            pdf_to_md(pdf_path)
        else:
            # Handle potential filename mismatches gracefully (e.g. if I assumed a .pdf ext and it's slightly different)
            # Just try to find it if possible, or skip. 
            # Given the previous `list_dir`, some might be named slightly differently or I might have assumed .pdf exists.
            # I will check if I need to find the file.
            print(f"File not found, skipping: {pdf_path}")

    # 2. Process directories
    print("\nProcessing Original Directories...")
    for folder in TARGET_DIRECTORIES:
        if not os.path.exists(folder):
            print(f"Directory not found: {folder}")
            continue
            
        print(f"Scanning {folder}...")
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_path = os.path.join(root, file)
                    pdf_to_md(pdf_path)

    print("\n--- Batch Conversion Complete ---")

if __name__ == "__main__":
    main()
