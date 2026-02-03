import argparse
import markdown
from xhtml2pdf import pisa
import os

def convert_md_to_pdf(input_file, output_file=None):
    if not output_file:
        output_file = os.path.splitext(input_file)[0] + ".pdf"
    
    # Read Markdown
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            md_content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found {input_file}")
        return

    # Convert to HTML
    html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
    
    # Simple Styling
    styled_html = f"""
    <html>
    <head>
        <style>
            @page {{
                size: letter;
                margin: 1in;
            }}
            body {{
                font-family: Helvetica, sans-serif;
                font-size: 11pt;
                line-height: 1.5;
            }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            h2 {{ color: #34495e; margin-top: 20px; }}
            code {{ background-color: #f8f9fa; padding: 2px 4px; border-radius: 4px; font-family: monospace; }}
            pre {{ background-color: #f8f9fa; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Generate PDF
    with open(output_file, "wb") as f:
        pisa_status = pisa.CreatePDF(styled_html, dest=f)

    if pisa_status.err:
        print(f"Error converting PDF")
    else:
        print(f"Successfully created: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF")
    parser.add_argument("input_file", help="Path to markdown file")
    parser.add_argument("--output", help="Output PDF path (optional)")
    
    args = parser.parse_args()
    convert_md_to_pdf(args.input_file, args.output)
