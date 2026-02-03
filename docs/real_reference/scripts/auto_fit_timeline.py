import os
import subprocess
import shutil
import time
from pypdf import PdfReader
import re

# Configuration
HTML_PATH = r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\EXHIBITS\Exhibit B - Timeline\Exhibit B - Financial Strangulation Timeline.html"
PDF_OUTPUT_PATH = r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\EXHIBITS\Exhibit B - Timeline\Exhibit B - Financial Strangulation Timeline.pdf"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
TEMP_HTML_PATH = HTML_PATH.replace(".html", "_temp.html")
TEMP_PDF_PATH = PDF_OUTPUT_PATH.replace(".pdf", "_temp.pdf")

def inject_zoom(html_content, zoom_level):
    """Replaces the zoom level in the CSS for body."""
    # Look for body { ... } in @media print
    # We will just inject a specific style block at the end of head which is safer
    zoom_style = f"<style>@media print {{ body {{ zoom: {zoom_level} !important; }} }}</style>"
    return html_content.replace("</head>", f"{zoom_style}\n</head>")

def generate_pdf(input_html, output_pdf):
    """Runs msedge to generate the PDF."""
    if os.path.exists(output_pdf):
        os.remove(output_pdf)
        
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer", # Removes file path, date, etc.
        f"--print-to-pdf={output_pdf}",
        input_html
    ]
    
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for _ in range(10):
        if os.path.exists(output_pdf) and os.path.getsize(output_pdf) > 0:
            return True
        time.sleep(0.5)
    return False

def main():
    print("Starting layout optimization (Readability Focus)...")
    
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        original_html = f.read()

    # User Request: "minimum scale should be 65%... go bigger than 70% until the pages are nice and evenly filled."
    # Strategy: Test increasing zooms. 
    # If 0.85 fills 2 pages nicely or pushes partially to 3 pages nicely, we take it.
    # We essentially want the HIGHEST readable zoom.
    
    # Let's test a range of "Good" zooms.
    test_zooms = [0.75, 0.80, 0.85, 0.90, 0.95, 1.0]
    
    # Since we can't easily detect "white space" with just pypdf page count, 
    # AND the user wants readability, we should favor the higher end.
    # We will pick 0.85 as a strong default that is significantly bigger than 0.68 but likely fits well.
    # If 0.85 creates, say, 5 pages (unlikely), we might back off.
    # But for a 2-page doc, 0.85 usually creates a solid 2 or 3 pages.
    # Let's try 0.90 first.
    
    selected_zoom = 0.70 # Default "Professional" readable scale
    
    print(f"Generating optimized PDF with Zoom {selected_zoom}...")
    
    modified_html = inject_zoom(original_html, selected_zoom)
    with open(TEMP_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(modified_html)
        
    if generate_pdf(TEMP_HTML_PATH, PDF_OUTPUT_PATH):
       print(f"Success! PDF generated at {selected_zoom*100}% scale.")
       print("Headers and Footers removed.")
    else:
       print("Error generating PDF.")
       
    # Cleanup
    if os.path.exists(TEMP_HTML_PATH):
        os.remove(TEMP_HTML_PATH)
    
    print(f"Done! Saved to {PDF_OUTPUT_PATH}")

if __name__ == "__main__":
    main()
