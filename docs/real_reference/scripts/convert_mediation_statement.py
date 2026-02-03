#!/usr/bin/env python3
import re

# Read the markdown file
with open('99_SEND_PRE-MEE/01_Confidential_Mediation_Statement.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Create HTML with J-series styling
html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Confidential Mediation Statement</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 11px; line-height: 1.5; color: #1a1a1a; padding: 35px 45px; max-width: 850px; margin: 0 auto; }}
        .header {{ text-align: center; padding-bottom: 8px; margin-bottom: 12px; border-bottom: 2px solid #1e3a5f; }}
        .confidential {{ color: #c41e3a; font-weight: bold; font-size: 10px; margin-bottom: 2px; }}
        .meta-info {{ font-size: 10px; margin-bottom: 15px; line-height: 1.6; }}
        .meta-info strong {{ color: #1e3a5f; }}
        h3 {{ color: #1e3a5f; font-size: 12px; margin-top: 15px; margin-bottom: 6px; border-bottom: 1px solid #ddd; padding-bottom: 2px; page-break-after: avoid; }}
        h4 {{ color: #1e3a5f; font-size: 11px; margin-top: 10px; margin-bottom: 5px; font-weight: bold; }}
        p {{ margin-bottom: 7px; text-align: justify; }}
        ul, ol {{ margin-left: 20px; margin-bottom: 7px; margin-top: 3px; }}
        li {{ margin-bottom: 2px; }}
        strong, b {{ font-weight: 600; }}
        em, i {{ font-style: italic; }}
        .section-break {{ border-top: 1px solid #ccc; margin: 12px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 8px 0; font-size: 10px; }}
        th, td {{ border: 1px solid #1e3a5f; padding: 5px; text-align: left; vertical-align: top; }}
        th {{ background-color: #1e3a5f; color: white; font-weight: bold; }}
        .signature {{ margin-top: 15px; }}
        .exhibit-list {{ font-size: 10px; }}
    </style>
</head>
<body>
{{content}}
</body>
</html>
"""

# Process markdown to HTML
html_body = """    <div class="header">
        <div class="confidential">CONFIDENTIAL SETTLEMENT COMMUNICATION</div>
        <div class="confidential">SUBJECT TO C.R.E. 408 / F.R.E. 408</div>
    </div>
    
    <div class="meta-info">"""

lines = md_content.split('\n')
in_list = False
in_meta = False

for line in lines[5:10]:  # Get meta info
    if 'TO:' in line or 'CC:' in line or 'FROM:' in line or 'DATE:' in line or 'RE:' in line:
        parts = line.split(':', 1)
        html_body += f"\n        <strong>{parts[0].strip()}:</strong> {parts[1].strip()}<br>"

html_body += "\n    </div>\n"

# Process main content
for line in lines[13:]:
    line = line.rstrip()
    
    if not line or line == '---':
        if in_list:
            html_body += '\n    </ul>'
            in_list = False
        if line == '---':
            html_body += '\n    <div class="section-break"></div>'
        continue
    
    # Headers
    if line.startswith('###'):
        if in_list:
            html_body += '\n    </ul>'
            in_list = False
        title = line.replace('###', '').strip()
        html_body += f'\n    <h3>{title}</h3>'
    elif line.startswith('**') and line.endswith('**:'):
        title = line.replace('**', '').replace(':', '').strip()
        html_body += f'\n    <h4>{title}:</h4>'
    # Lists
    elif line.startswith('- ') or line.startswith('* '):
        if not in_list:
            html_body += '\n    <ul>'
            in_list = True
        item = line[2:].strip()
        item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
        item = re.sub(r'zip/EXHIBITS/', '', item)
        html_body += f'\n        <li>{item}</li>'
    # Table
    elif '|' in line and not '---' in line:
        # Skip table processing for now - keep simple
        pass
    else:
        if in_list:
            html_body += '\n    </ul>'
            in_list = False
        if line and not line.startswith('<'):
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'\*([^\*]+?)\*', r'<em>\1</em>', line)
            line = re.sub(r'zip/EXHIBITS/', '', line)
            if line.strip():
                html_body += f'\n    <p>{line}</p>'

if in_list:
    html_body += '\n    </ul>'

html_body += """
    
    <div class="signature">
        <p><strong>Respectfully,<br>Adam Scheurer</strong></p>
    </div>"""

final_html = html_template.format(content=html_body)

with open('99_SEND_PRE-MEE/01_Confidential_Mediation_Statement.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Mediation Statement HTML created successfully")
