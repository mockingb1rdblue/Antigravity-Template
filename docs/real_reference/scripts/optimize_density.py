import os
import subprocess
import time
from pypdf import PdfReader

# Configuration
HTML_PATH = r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\EXHIBITS\Exhibit B - Timeline\Exhibit B - Financial Strangulation Timeline.html"
PDF_DIR = r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\EXHIBITS\Exhibit B - Timeline"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def generate_pdf(zoom, output_path):
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()
    
    zoom_style = f"<style>@media print {{ body {{ zoom: {zoom} !important; }} }}</style>"
    modified_html = html.replace("</head>", f"{zoom_style}\n</head>")
    
    temp_html = "temp_zoom.html"
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(modified_html)
    
    cmd = [
        EDGE_PATH, "--headless", "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={output_path}",
        os.path.abspath(temp_html)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait for file
    for _ in range(10):
        if os.path.exists(output_path): return True
        time.sleep(0.5)
    return False

def analyze_density(pdf_path):
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)
    # Simple heuristic: last page occupancy
    # We can't easily measure whitespace without heavy tools, 
    # but we can look at the page count and user feedback.
    return num_pages

def main():
    print("Starting iteration through zoom levels for optimal density...")
    # The user reported 0.85 was 75% empty on pg 3.
    # We want to EITHER fit it on 2 pages (lower zoom) 
    # OR fill pg 3 better (higher zoom).
    
    zooms = [0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.0, 1.05, 1.10]
    results = []
    
    for z in zooms:
        out = os.path.join(PDF_DIR, f"Timeline_Zoom_{int(z*100)}.pdf")
        if generate_pdf(z, out):
            pages = analyze_density(out)
            print(f"Zoom {z*100:.0f}% -> {pages} pages")
            results.append((z, pages, out))
    
    print("\n✅ Iteration complete. Review the generated PDFs in the EXHIBITS folder.")

if __name__ == "__main__":
    main()
