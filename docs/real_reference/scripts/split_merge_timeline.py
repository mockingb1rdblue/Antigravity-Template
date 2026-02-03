import os
import subprocess
import time
import shutil
from pypdf import PdfReader, PdfWriter

# Configuration
MASTER_HTML = r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\EXHIBITS\Exhibit B - Timeline\Exhibit B - Financial Strangulation Timeline.html"
PDF_DIR = r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\EXHIBITS\Exhibit B - Timeline"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FINAL_PDF = os.path.join(PDF_DIR, "Exhibit B - Financial Strangulation Timeline.pdf")

def generate_pdf(html_content, zoom, output_path):
    temp_html = os.path.abspath("temp_section.html")
    output_pdf = os.path.abspath(output_path)
    
    zoom_style = f"<style>@media print {{ body {{ zoom: {zoom} !important; }} }}</style>"
    content = html_content.replace("</head>", f"{zoom_style}\n</head>")
    
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(content)
    
    cmd = [
        EDGE_PATH, "--headless", "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={output_pdf}",
        f"file:///{temp_html}"
    ]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stderr:
        print(f"Edge Stderr: {result.stderr}")
    
    for _ in range(20): # increased wait
        if os.path.exists(output_pdf) and os.path.getsize(output_pdf) > 0: 
            print(f"Found {output_path}")
            return True
        time.sleep(0.5)
    print(f"Failed to find {output_path}")
    return False

def main():
    print("Starting Split-Merge Generation...")
    
    with open(MASTER_HTML, 'r', encoding='utf-8') as f:
        full_html = f.read()
        
    head = full_html.split("</head>")[0] + "</head>"
    body_start = "<body><div class='container'>"
    body_end = "</div></body></html>"
    
    # 1. Extract Table
    table_content = full_html.split("<table>")[1].split("</table>")[0]
    table_html = f"{head}\n{body_start}\n<table>{table_content}</table>\n{body_end}"
    
    # 2. Extract Narrative
    narrative_content = full_html.split("<div class=\"narrative-arc\">")[1].split("</div>\n    </div>\n</body>")[0]
    # Remove the page-break-before from narrative for the standalone version
    narrative_content = narrative_content.replace("page-break-before: always;", "")
    narrative_html = f"{head}\n{body_start}\n<div class=\"narrative-arc\" style=\"page-break-before: avoid; margin-top: 0;\">{narrative_content}</div>\n{body_end}"

    # Optimization Logic
    # Table: 0.82 zoom fits nicely.
    # Narrative: 0.70 zoom (Re-evaluate if content is added/modified)
    
    table_pdf = "temp_table.pdf"
    narrative_pdf = "temp_narrative.pdf"
    
    print("Optimizing Table (Zoom 0.82)...")
    generate_pdf(table_html, 0.82, table_pdf)
    
    print("Optimizing Narrative (Zoom 0.70)...")
    generate_pdf(narrative_html, 0.70, narrative_pdf)
    
    # Merge
    print("Merging sections...")
    writer = PdfWriter()
    
    for pdf in [table_pdf, narrative_pdf]:
        reader = PdfReader(pdf)
        for page in reader.pages:
            writer.add_page(page)
            
    with open(FINAL_PDF, "wb") as f:
        writer.write(f)
        
    # Cleanup
    for f in ["temp_section.html", table_pdf, narrative_pdf]:
        if os.path.exists(f): os.remove(f)
        
    print(f"Final PDF generated: {FINAL_PDF}")

if __name__ == "__main__":
    main()
