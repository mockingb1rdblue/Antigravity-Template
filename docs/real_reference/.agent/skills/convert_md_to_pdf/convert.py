import sys
import os
import markdown
from xhtml2pdf import pisa

def convert_md_to_pdf(md_file_path):
    if not os.path.exists(md_file_path):
        print(f"Error: File not found: {md_file_path}")
        return

    # 1. Read Markdown
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 2. Convert to HTML
    # Using 'extra' extension for tables, fences, etc.
    html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite'])

    # 3. Add Styling
    # Simple, professional CSS
    css = """
    <style>
        @page {
            size: letter;
            margin: 1in;
        }
        body {
            font-family: Helvetica, Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 0.3em;
            margin-top: 1.5em;
        }
        h2 {
            color: #2c3e50;
            border-bottom: 1px solid #7f8c8d;
            padding-bottom: 0.2em;
            margin-top: 1.2em;
        }
        h3 {
            color: #34495e;
            margin-top: 1em;
        }
        code {
            background-color: #f8f8f8;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: Consolas, "Courier New", monospace;
            font-size: 0.9em;
        }
        pre {
            background-color: #f8f8f8;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            border: 1px solid #ddd;
        }
        blockquote {
            border-left: 4px solid #3498db;
            padding-left: 10px;
            color: #555;
            font-style: italic;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 1em;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
    """

    full_html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        {css}
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # 4. Save as PDF
    output_pdf_path = os.path.splitext(md_file_path)[0] + ".pdf"
    
    with open(output_pdf_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(
            full_html, dest=pdf_file
        )

    if pisa_status.err:
        print(f"Error converting to PDF: {pisa_status.err}")
    else:
        print(f"Successfully converted '{md_file_path}' to '{output_pdf_path}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <path_to_markdown_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    convert_md_to_pdf(file_path)
