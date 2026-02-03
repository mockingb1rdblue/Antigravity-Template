import os
import subprocess

def create_html(output_path):
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Liability Admission Snippet</title>
    <style>
        :root {
            --primary: #1a365d;   /* Deep Navy - Headers */
            --secondary: #2c5282; /* Lighter Navy - Subheaders */
            --accent: #c53030;    /* Dark Red - Alerts/Liabilities */
            --bg: #ffffff;        /* White Background */
            --text: #2d3748;      /* Dark Gray Text (Not Black) */
            --border: #e2e8f0;    /* Light Gray Borders */
            --highlight: #fff5f5; /* Light Red Background for Findings */
        }
        body {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            font-size: 14px; /* Slightly larger for readability as snippet */
            line-height: 1.5;
            color: var(--text);
            padding: 40px;
            max-width: 800px;
            margin: 0 auto;
        }
        header {
            border-bottom: 2px solid var(--primary);
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        h1 {
            color: var(--primary);
            font-size: 24px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 0;
        }
        strong {
            color: var(--primary);
            font-weight: 700;
        }
        .meta-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
        }
        .meta-table td {
            padding: 8px 0;
            vertical-align: top;
        }
        .meta-label {
            width: 160px;
            font-weight: bold;
            color: var(--secondary);
        }
        .finding-box {
            background: var(--highlight);
            border-left: 4px solid var(--accent);
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 0 4px 4px 0;
        }
        .verification {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
            font-style: italic;
            font-size: 12px;
            color: #718096;
        }
        h3 {
            color: var(--secondary);
            border-bottom: 1px solid var(--border);
            padding-bottom: 5px;
            margin-top: 0;
        }
    </style>
</head>
<body>
    <header>
        <h1>Evidentiary Snippet: March 25, 2025</h1>
    </header>

    <table class="meta-table">
        <tr>
            <td class="meta-label">Source Document:</td>
            <td>Complainant's Contemporaneous Journal</td>
        </tr>
        <tr>
            <td class="meta-label">Date of Entry:</td>
            <td>March 25, 2025</td>
        </tr>
        <tr>
            <td class="meta-label">Significance:</td>
            <td>Documents the initial <strong>"regarded as disabled"</strong> statement ("liability") and the initiation of forced unpaid leave.</td>
        </tr>
    </table>

    <div class="finding-box">
        <h3>Objective Summary</h3>
        <p>On March 25, 2025, Supervisor Kevin Locke contacted the Complainant by phone and instructed them not to report for work, explicitly characterizing the Complainant as a <strong style="color: var(--accent);">"liability."</strong></p>
        
        <p>Locke placed the Complainant on involuntary, unpaid leave and directed them to open a claim with the third-party administrator (Unum). Despite the Complainant informing Locke that Team Lead Colby had already identified feasible workarounds for the restrictions, Locke maintained the requirement for involuntary leave and suggested the Complainant use **personal PTO** to cover the resulting loss of income.</p>
    </div>

    <div class="verification">
        <strong>Verification Note:</strong> This snippet is an objective summary of contemporaneous documentation. The full original journal entry is available to the Mediator upon request.
    </div>
</body>
</html>"""
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Created HTML: {output_path}")

def generate_pdf(html_path, pdf_path):
    # Use existing script logic by calling it via subprocess
    cmd = ["python", "05_scripts/generate_pdf_edge.py", html_path, pdf_path]
    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    base_dir = os.path.join(os.getcwd(), "50_MASTER_EXHIBITS", "Exhibit B - Timeline")
    html_file = os.path.join(base_dir, "2025-03-25 - Liability Admission (Evidentiary Snippet).html")
    pdf_file = os.path.join(base_dir, "2025-03-25 - Liability Admission (Evidentiary Snippet).pdf")
    
    create_html(html_file)
    generate_pdf(html_file, pdf_file)
