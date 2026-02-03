#!/usr/bin/env python3
"""
Professional PDF Generation Script
Generates styled HTML from markdown with proper table handling
Then converts to PDF using Edge headless mode
"""

import sys
import os
import subprocess

# Unified professional styling matching Exhibit J
PROFESSIONAL_STYLE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        @page {{
            size: letter;
            margin: {margin};
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            font-size: {font_size}; 
            line-height: 1.4; 
            color: #1a1a1a; 
            padding: {padding}; 
            max-width: 100%;
        }}
        .header {{ 
            text-align: center; 
            padding-bottom: 8px; 
            margin-bottom: 12px; 
            border-bottom: 2px solid #1e3a5f; 
        }}
        .confidential {{ 
            color: #c41e3a; 
            font-weight: bold; 
            font-size: {conf_size}; 
            margin-bottom: 2px; 
        }}
        .meta-info {{ 
            font-size: {meta_size}; 
            margin-bottom: 15px; 
            line-height: 1.5; 
        }}
        .meta-info strong {{ color: #1e3a5f; }}
        h1 {{ 
            color: #1e3a5f; 
            font-size: {h1_size}; 
            margin: 15px 0 10px 0; 
            page-break-after: avoid; 
        }}
        h2 {{ 
            color: #1e3a5f; 
            font-size: {h2_size}; 
            margin: 12px 0 8px 0; 
            border-bottom: 1px solid #ddd; 
            padding-bottom: 2px; 
            page-break-after: avoid; 
        }}
        h3 {{ 
            color: #1e3a5f; 
            font-size: {h3_size}; 
            margin: 10px 0 6px 0; 
            font-weight: bold; 
        }}
        p {{ margin-bottom: 6px; text-align: justify; }}
        ul, ol {{ margin-left: 18px; margin-bottom: 6px; margin-top: 3px; }}
        li {{ margin-bottom: 2px; }}
        strong, b {{ font-weight: 600; }}
        em, i {{ font-style: italic; }}
        hr {{ border: none; border-top: 1px solid #ccc; margin: 10px 0; }}
        
        /* PROFESSIONAL TABLE STYLING */
        table {{ 
            width: 100%; 
            border-collapse: collapse; 
            margin: 10px 0; 
            font-size: {table_size};
            page-break-inside: avoid;
        }}
        th, td {{ 
            border: 1px solid #1e3a5f; 
            padding: 8px; 
            text-align: left; 
            vertical-align: top;
            word-wrap: break-word;
        }}
        th {{ 
            background-color: #1e3a5f; 
            color: white; 
            font-weight: bold;
            font-size: {table_header_size};
        }}
        tr:nth-child(even) {{ background-color: #f5f5f5; }}
        
        /* Component numbers in tables */
        td:first-child {{ font-weight: 600; white-space: nowrap; }}
        
        /* Signature block */
        .signature {{ margin-top: 15px; page-break-inside: avoid; }}
        .signature-line {{ margin: 2px 0; }}
        
        /* Exhibit lists */
        code {{ 
            background-color: #f4f4f4; 
            padding: 2px 4px; 
            font-size: {code_size}; 
            font-family: 'Consolas', 'Courier New', monospace; 
        }}
    </style>
</head>
<body>
{content}
</body>
</html>
"""

def generate_html(content, title="Document", doc_type="standard"):
    """
    Generate HTML with appropriate styling based on document type
    
    doc_type options:
    - "cover_letter": Compact margins, fit on one page
    - "statement": Standard  margins, readable tables
    - "table": Tight layout for data-heavy tables
    """
    
    if doc_type == "cover_letter":
        params = {
            "title": title,
            "margin": "0.4in 0.5in",  # Tight margins for one-page fit
            "padding": "0",
            "font_size": "10.5px",
            "conf_size": "9px",
            "meta_size": "9.5px",
            "h1_size": "13px",
            "h2_size": "11.5px",
            "h3_size": "10.5px",
            "table_size": "9.5px",
            "table_header_size": "10px",
            "code_size": "9px"
        }
    elif doc_type == "table":
        params = {
            "title": title,
            "margin": "0.5in",
            "padding": "0",
            "font_size": "10px",
            "conf_size": "9px",
            "meta_size": "9.5px",
            "h1_size": "14px",
            "h2_size": "12px",
            "h3_size": "11px",
            "table_size": "9px",  # Smaller for data tables
            "table_header_size": "9.5px",
            "code_size": "8.5px"
        }
    else:  # statement (standard)
        params = {
            "title": title,
            "margin": "0.6in 0.7in",
            "padding": "0",
            "font_size": "11px",
            "conf_size": "10px",
            "meta_size": "10px",
            "h1_size": "14px",
            "h2_size": "12px",
            "h3_size": "11px",
            "table_size": "10px",
            "table_header_size": "10.5px",
            "code_size": "9.5px"
        }
    
    params["content"] = content
    return PROFESSIONAL_STYLE.format(**params)

def convert_to_pdf(html_path, pdf_path):
    """Convert HTML to PDF using Edge headless"""
    edge_cmd = [
        "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={os.path.abspath(pdf_path)}",
        "--no-pdf-header-footer",
        f"file:///{os.path.abspath(html_path).replace(os.sep, '/')}"
    ]
    
    result = subprocess.run(edge_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        size = os.path.getsize(pdf_path)
        print(f"SUCCESS: PDF generated: {pdf_path} ({size:,} bytes)")
        return True
    else:
        print(f"ERROR: PDF generation failed: {result.stderr}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python professional_pdf.py <html_file> <pdf_file> [doc_type]")
        print("doc_type: cover_letter, statement, or table")
        sys.exit(1)
    
    html_file = sys.argv[1]
    pdf_file = sys.argv[2]
    
    convert_to_pdf(html_file, pdf_file)
