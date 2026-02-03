import markdown
import sys
import os

def generate_report():
    input_file = "docs/feature_audit_2026_01_31.md"
    output_html = "docs/feature_audit_2026_01_31.html"
    
    with open(input_file, 'r') as f:
        text = f.read()
        
    # Convert Markdown to HTML
    html_content = markdown.markdown(text, extensions=['tables'])
    
    # Custom CSS for "Beautiful Dark Mode"
    css = """
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #0d1117;
            color: #c9d1d9;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
        }
        h1, h2, h3 {
            color: #58a6ff;
            border-bottom: 1px solid #21262d;
            padding-bottom: 0.3em;
        }
        h1 { font-size: 2.5em; margin-bottom: 1em; }
        h2 { font-size: 1.8em; margin-top: 1.5em; }
        h3 { font-size: 1.3em; margin-top: 1.2em; color: #79c0ff; }
        strong { color: #d2a8ff; }
        code {
            background-color: #161b22;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            font-size: 0.9em;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
            background-color: #161b22;
            border-radius: 6px;
            overflow: hidden;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #21262d;
        }
        th {
            background-color: #21262d;
            color: #f0f6fc;
            font-weight: 600;
        }
        tr:last-child td { border-bottom: none; }
        hr {
            border: 0;
            height: 1px;
            background: #30363d;
            margin: 2em 0;
        }
        .status-mvp { color: #7ee787; font-weight: bold; }
        .status-planned { color: #8b949e; font-style: italic; }
        
        @media print {
            body { background-color: white; color: black; }
            h1, h2, h3 { color: #0969da; border-bottom: 1px solid #eaeef2; }
            strong { color: #663399; }
            code { background-color: #f6f8fa; border: 1px solid #eaeef2; }
            th { background-color: #f6f8fa; color: black; }
            table, th, td { border: 1px solid #d0d7de; }
        }
    </style>
    """
    
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>CarPiggy Feature Audit</title>
        {css}
    </head>
    <body>
        <div class="report-container">
            {html_content}
        </div>
    </body>
    </html>
    """
    
    with open(output_html, 'w') as f:
        f.write(full_html)
        
    print(f"✅ HTML Report generated: {output_html}")
    
    # Try to generate PDF if weasyprint is installed
    try:
        from weasyprint import HTML
        output_pdf = "docs/feature_audit_2026_01_31.pdf"
        HTML(string=full_html).write_pdf(output_pdf)
        print(f"✅ PDF Report generated: {output_pdf}")
    except ImportError:
        print("⚠️  WeasyPrint not found. Skipped PDF generation.")
        print("ℹ️  You can open the HTML file and 'Print to PDF' in your browser for best results.")

if __name__ == "__main__":
    generate_report()
