#!/usr/bin/env python3
"""
Generate Mediation Statement HTML from markdown
Handles the complex table formatting properly
"""

html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Confidential Mediation Statement</title>
    <style>
        @page { size: letter; margin: 0.6in 0.7in; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            font-size: 11px; 
            line-height: 1.4; 
            color: #1a1a1a;
        }
        .header { 
            text-align: center; 
            padding-bottom: 8px; 
            margin-bottom: 12px; 
            border-bottom: 2px solid #1e3a5f; 
        }
        .confidential { 
            color: #c41e3a; 
            font-weight: bold; 
            font-size: 10px; 
            margin-bottom: 2px; 
        }
        .meta-info { 
            font-size: 10px; 
            margin-bottom: 12px; 
            line-height: 1.5; 
        }
        .meta-info strong { color: #1e3a5f; }
        h2 { 
            color: #1e3a5f; 
            font-size: 12px; 
            margin: 14px 0 8px 0; 
            border-bottom: 1px solid #ddd; 
            padding-bottom: 2px; 
            page-break-after: avoid;
            page-break-inside: avoid;
        }
        h3 { 
            color: #1e3a5f; 
            font-size: 11px; 
            margin: 10px 0 6px 0; 
            font-weight: bold; 
        }
        p { margin-bottom: 7px; text-align: justify; }
        ul { margin-left: 18px; margin-bottom: 7px; margin-top: 3px; }
        li { margin-bottom: 2px; }
        strong { font-weight: 600; }
        hr { border: none; border-top: 1px solid #ccc; margin: 10px 0; }
        code { 
            background-color: #f4f4f4; 
            padding: 2px 4px; 
            font-size: 9.5px; 
            font-family: 'Consolas', 'Courier New', monospace; 
        }
        
        /* TABLE STYLING */
        table { 
            width: 100%; 
            border-collapse: collapse; 
            margin: 10px 0; 
            font-size: 10px;
            page-break-inside: avoid;
        }
        th, td { 
            border: 1px solid #1e3a5f; 
            padding: 7px; 
            text-align: left; 
            vertical-align: top;
        }
        th { 
            background-color: #1e3a5f; 
            color: white; 
            font-weight: bold;
            font-size: 10.5px;
        }
        tr:nth-child(even) { background-color: #f8f8f8; }
        .component-num { font-weight: 600; white-space: nowrap; }
        .value { font-weight: 600; color: #c41e3a; }
        .total-row { 
            background-color: #e6eef5 !important; 
            font-weight: bold; 
        }
        
        /* Prevent orphan/widow lines */
        p { orphans: 3; widows: 3; }
        
        .signature { margin-top: 15px; page-break-inside: avoid; }
        .signature-line { margin: 2px 0; }
    </style>
</head>
<body>"""

# Read the markdown file
with open('00_MASTERS_PREMED/01_Confidential_Mediation_Statement.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Build HTML body
html_content += """
    <div class="header">
        <div class="confidential">CONFIDENTIAL SETTLEMENT COMMUNICATION</div>
        <div class="confidential">SUBJECT TO C.R.E. 408 / F.R.E. 408</div>
    </div>
    
    <div class="meta-info">
        <strong>TO:</strong> Amber Hill Anderson (Mediator)<br>
        <strong>CC:</strong> Andrew Frazier (Vestas Corporate Counsel), Vestas General Counsel<br>
        <strong>FROM:</strong> Adam Scheurer<br>
        <strong>DATE:</strong> January 29, 2026<br>
        <strong>RE:</strong> CCRD Case #E2600030468 – Pre-Mediation Evidence Summary
    </div>
    
    <hr>
"""

# Process markdown content
in_table = False
skip_to_table_end = False
in_closing = False  # Track if we're in the closing signature

for i, line in enumerate(lines[11:], start=11):  # Skip header lines
    line = line.rstrip()
    
    # Skip the signature block from markdown (we add it manually)
    if 'I look forward to productive mediation' in line:
        in_closing = True
        continue
    if in_closing:
        # Skip all lines until end of file
        continue
    
    # Handle the settlement table specially
    if '### VIII. Five-Component Settlement Framework' in line:
        html_content += '<h2>VIII. Five-Component Settlement Framework</h2>'
        html_content += '<p><strong>The settlement framework below is modular.</strong> Vestas may elect to purchase:</p>'
        html_content += """
<table>
    <thead>
        <tr>
            <th style="width: 18%;">Component</th>
            <th style="width: 42%;">What Vestas is Buying</th>
            <th style="width: 20%;">Opening Demand</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="component-num">1. Personal ADA</td>
            <td>Resolution of my individual discrimination/retaliation/IIED claims</td>
            <td class="value">$3-3.5M</td>
        </tr>
        <tr>
            <td class="component-num">2. Systemic Reforms</td>
            <td>Funded ombudsman, audits, monitoring, training (prevents both classes)</td>
            <td class="value">$3-3.5M</td>
        </tr>
        <tr>
            <td class="component-num">3. Night Shift Class</td>
            <td>Evidence of unpaid shift differentials (~160-500 night shift employees)</td>
            <td class="value">$1.5-2M</td>
        </tr>
        <tr>
            <td class="component-num">4. Production Class</td>
            <td>Covenant not to sue regarding "Forced PTO" (~1,000 production employees)</td>
            <td class="value">$3-4M</td>
        </tr>
        <tr>
            <td class="component-num">5. ADA Pattern Opt-Out</td>
            <td>My July 17 recording + systemic audit + covenant not to serve as ADA class rep</td>
            <td class="value">$2.5-3M</td>
        </tr>
        <tr class="total-row">
            <td class="component-num">TOTAL (All Five)</td>
            <td></td>
            <td class="value">$13-16M</td>
        </tr>
    </tbody>
</table>
"""
        skip_to_table_end = True
        continue
    
    if skip_to_table_end:
        if '**See zip/STRATEGIC' in line or '### IX. Exhibits' in line:
            skip_to_table_end = False
            if '### IX. Exhibits' in line:
                html_content += '<p><strong>Components 3, 4, and 5 are optional purchases.</strong> If Vestas chooses not to acquire these components, I retain all associated rights and work product. A settlement limited to Components 1-2 releases only my individual discrimination claims, not systemic or class allegations. My absolute walk-away floor for Components 1+2 combined is <strong>$3.5M</strong>.</p>'
                html_content += '<hr><hr>'
                html_content += '<h2>IX. Exhibits Attached</h2>'
        continue
    
    # Skip original table markdown
    if line.startswith('| Component |') or line.startswith('|-----------|') or (line.startswith('|') and 'Personal ADA' in line):
        continue
    
    # Headers
    if line.startswith('### '):
        title = line.replace('###', '').strip()
        # No forced breaks - rely on page-break-after: avoid to prevent orphans
        html_content += f'<h2>{title}</h2>'
    elif line.startswith('**') and line.endswith('**') and len(line) < 80:
        title = line.replace('**', '').strip()
        if title.endswith(':'):
            html_content += f'<h3>{title}</h3>'
        else:
            html_content += f'<p><strong>{title}</strong></p>'
    elif line.startswith('- '):
        item = line[2:].replace('**', '<strong>').replace('**', '</strong>')
        item = item.replace('zip/EXHIBITS/', '<code>zip/EXHIBITS/').replace('.pdf', '.pdf</code>')
        html_content += f'<ul><li>{item}</li></ul>'
    elif line == '---':
        html_content += '<hr>'
    elif line and not line.startswith('<'):
        line = line.replace('**', '<strong>').replace('**', '</strong>')
        line = line.replace('*', '<em>').replace('*', '</em>')
        html_content += f'<p>{line}</p>'

# Add signature
html_content += """
    <hr>
    <p>I look forward to productive mediation.</p>
    <div class="signature">
        <div class="signature-line"><strong>Respectfully,</strong></div>
        <div class="signature-line"><strong>Adam Scheurer</strong></div>
        <div class="signature-line">563-552-6752</div>
        <div class="signature-line">ascheurer@pm.me</div>
    </div>
</body>
</html>
"""

# Write HTML
with open('00_MASTERS_PREMED/Mediation_Statement.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("SUCCESS: Mediation Statement HTML created")
