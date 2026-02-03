import os
import subprocess

# CSS from HTML_STYLE_GUIDE.md
STYLE_CSS = """
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
        font-size: 11px; /* Audit style */
        line-height: 1.4;
        color: var(--text);
        padding: 40px;
        max-width: 900px;
        margin: 0 auto;
    }
    header {
        border-bottom: 2px solid var(--primary);
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    h1 {
        color: var(--primary);
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0;
    }
    h2 {
        color: var(--secondary);
        font-size: 14px;
        border-bottom: 1px solid var(--border);
        padding-bottom: 5px;
        margin-top: 20px;
    }
    h3 {
        color: var(--primary);
        font-size: 12px;
        font-weight: bold;
        margin-top: 15px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        font-size: 11px;
    }
    th {
        background-color: var(--primary);
        color: white;
        text-align: left;
        padding: 6px 8px;
        text-transform: uppercase;
        font-size: 10px;
    }
    td {
        padding: 6px 8px;
        border-bottom: 1px solid #cbd5e0;
        vertical-align: top;
    }
    .finding-box {
        background: var(--highlight);
        border-left: 4px solid var(--accent);
        padding: 10px;
        margin: 15px 0;
    }
    ul {
        margin: 5px 0 10px 20px;
        padding: 0;
    }
    li {
        margin-bottom: 4px;
    }
    strong {
        color: var(--primary);
    }
"""

def create_j6_html(output_path):
    content = f"""<!DOCTYPE html>
<html>
<head><style>{STYLE_CSS}</style></head>
<body>
    <header>
        <h1>EXHIBIT J-6: Forced PTO Policy Violation & "Disparate Impact" Pay Disparity</h1>
    </header>

    <h2>1. EVIDENCE OF SYSTEMIC VIOLATION</h2>
    
    <h3>A. The "Use It or Lose It" Policy (Written vs. Practice)</h3>
    <ul>
        <li><strong>Written Policy:</strong> Vestas US Employee Handbook mentions "Paid Time Off" as a benefit for employee well-being (Exhibit A).</li>
        <li><strong>Actual Practice (Hourly):</strong> Vestas implements a <strong>4x10 shift structure</strong> (10-hour days) but caps Holiday Pay at <strong>8 hours</strong>. To maintain a full 40-hour paycheck, hourly workers are coerced to burn PTO.</li>
        <li><strong>Actual Practice (Salaried):</strong> Salaried staff (Supervisors, P&C, Management) were <strong>exempt</strong> from this gap. They received their full weekly salary during holiday weeks without being forced to deplete their PTO banks.</li>
    </ul>
    
    <div class="finding-box">
        <strong>Violation:</strong> This creates a discriminatory two-tier system where the lowest-paid workers effectively subsidize the plant's downtime with their benefits, while leadership retains their full compensation and time off.
    </div>

    <h3>B. The "Ground Truth" (Inevitable Discovery)</h3>
    <p>My sworn affidavit (Exhibit J-3) attests to the <strong>mandatory enforcement</strong> of PTO usage during shutdowns. I observed that while hourly employees were forced to burn PTO to maintain a paycheck, salaried leadership (including those enforcing the policy) suffered no such deduction.</p>
    
    <p><strong>Why This Creates Class Exposure:</strong><br>
    Discovery will reveal that this was not an isolated instruction to one employee. It was a <strong>standing order</strong> announced in "All Hands" meetings and enforced by the Time & Attendance system.</p>
    <ul>
        <li><strong>The Audit Trail:</strong> Payroll records will show distinct blocks of "PTO Usage" for the entire hourly workforce designated as "Maintenance Shutdowns" or "Inventory."</li>
        <li><strong>The Implication:</strong> Vestas cannot claim this was "voluntary" when 500+ employees simultaneously "chose" to take PTO on the exact same days the plant was closed.</li>
    </ul>

    <h2>2. EXPOSURE CALCULATION (The $18.7M Risk)</h2>
    
    <h3>Methodology for Class Damage Model</h3>
    <table>
        <tr><th>Variable</th><th>Conservative Estimate</th><th>Calculation Logic</th></tr>
        <tr><td><strong>Class Size</strong></td><td>1,000</td><td>Hourly employees (Windsor + Brighton)</td></tr>
        <tr><td><strong>Forced "Burn" Days</strong></td><td>12 / year</td><td>Holidays (6) + Inventory (4) + Retooling (2)</td></tr>
        <tr><td><strong>Uncompensated Hours</strong></td><td>120 / year</td><td>12 days × 10-hour shifts</td></tr>
        <tr><td><strong>Avg Hourly Rate</strong></td><td>$26.00</td><td>Weighted avg (Tech I - Tech III)</td></tr>
        <tr><td><strong>Annual Compensation Compliance</strong></td><td><strong>$3,120,000</strong></td><td>1,000 × 120 × $26</td></tr>
        <tr><td><strong>Lookback Period</strong></td><td>3 Years</td><td>FLSA "Willful Violation" Standard</td></tr>
        <tr><td><strong>Base Damages</strong></td><td>$9,360,000</td><td>3 years × $3.12M</td></tr>
        <tr><td><strong>Liquidated Damages</strong></td><td>$9,360,000</td><td>FLSA Automatic Double Damages</td></tr>
        <tr><td><strong>TOTAL EXPOSURE</strong></td><td><strong style="color:var(--accent); font-size:12px;">$18,720,000</strong></td><td><em>Plus Attorney Fees & Costs</em></td></tr>
    </table>

    <h2>3. LEGAL LIABILITY FRAMEWORK</h2>
    <p><strong>FLSA & Colorado Wage Act:</strong><br>
    By mandating PTO usage during employer-controlled shutdowns, Vestas effectively <strong>reduced the negotiated hourly wage</strong> and <strong>denied the benefit</strong> promised in the offer letter.</p>
    
    <ul>
        <li><strong>Willfulness:</strong> This was not a rogue supervisor's error. The practice was enforced across the entire facility (Brighton & Windsor) and administered by P&C, who processed the PTO deductions despite the contradiction with the handbook's stating purpose of "rest and well-being."</li>
        <li><strong>Commonality:</strong> The policy applied uniformly to all hourly staff, making Class Certification under Rule 23 highly probable.</li>
    </ul>
</body>
</html>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created J-6 HTML: {output_path}")

def create_m_html(output_path):
    content = f"""<!DOCTYPE html>
<html>
<head><style>{STYLE_CSS}</style></head>
<body>
    <header>
        <h1>EXHIBIT M: THE FINANCIAL STRANGULATION SYSTEM</h1>
    </header>
    
    <div style="font-size: 12px; margin-bottom: 20px; color: var(--secondary);">
        <strong>Subject:</strong> How Vestas's Wage Violations Create Structural Barriers to Accommodation
    </div>

    <h2>STEP 1: LIMITED PTO ACCRUAL</h2>
    <ul>
        <li>Hourly employees accrue [80-120] hours/year</li>
        <li>Salaried employees unaffected by shutdown policies</li>
    </ul>

    <h2>STEP 2: FORCED DEPLETION (Company Shutdowns)</h2>
    <ul>
        <li>Plant closes for holidays/inventory [X] days/year</li>
        <li><strong>Hourly:</strong> Must use PTO or go unpaid ([Y] hours/year lost)</li>
        <li><strong>Salaried:</strong> Paid regardless (disparate treatment)</li>
    </ul>
    <div class="finding-box">
        <strong>RESULT:</strong> Hourly employees lose [40-60]% of PTO to shutdowns
    </div>

    <h2>STEP 3: SHIFT DIFFERENTIAL Compensation Compliance</h2>
    <ul>
        <li>Promised $3/hr differential for "night shift work"</li>
        <li><strong>Withheld</strong> on PTO/holiday hours</li>
        <li>Employees "pay" $3/hr to use their own accrued PTO</li>
    </ul>
    <div class="finding-box">
        <strong>RESULT:</strong> Remaining PTO worth less than promised
    </div>

    <h2>STEP 4: SICK LEAVE RETALIATION BARRIER</h2>
    <ul>
        <li>Colorado mandates 48 hours paid sick leave (separate from PTO)</li>
        <li>Vestas retaliates if used without banked PTO</li>
        <li>After shutdown depletion, employees have no buffer</li>
    </ul>
    <div class="finding-box">
        <strong>RESULT:</strong> Work sick or face discipline
    </div>

    <h2>STEP 5: ACCOMMODATION DENIAL BY DESIGN</h2>
    <ul>
        <li>Employee with disability needs medical leave</li>
        <li>PTO already depleted by forced shutdowns</li>
        <li>Company policy: <strong>unpaid leave immediately</strong></li>
        <li>Financial pressure → benefit exhaustion → termination</li>
    </ul>
    <div class="finding-box" style="border-color: var(--accent);">
        <strong style="color: var(--accent);">RESULT:</strong> Accommodation = financial death sentence
    </div>

    <h2>CUMULATIVE EFFECT</h2>
    <ul>
        <li>[X] Hourly workers never take actual vacation</li>
        <li>[X] Medical needs create immediate financial crisis</li>
        <li>[X] Disability accommodation becomes constructive discharge</li>
        <li>[X] "Normal process" operates systemically, not accidentally</li>
    </ul>

    <h3 style="margin-top: 30px; border-top: 1px solid var(--border); padding-top: 10px;">Conclusion</h3>
    <p>This is the architecture that made my March 2025 accommodation request financially untenable, leading directly to my June 2025 termination.</p>
</body>
</html>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created M HTML: {output_path}")

def generate_pdf(html_path, pdf_path):
    cmd = ["python", "05_scripts/generate_pdf_edge.py", html_path, pdf_path]
    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    # J-6 Paths
    base_j = os.path.join(os.getcwd(), "50_MASTER_EXHIBITS", "Exhibit J - Compensation Compliance Audit")
    j6_html = os.path.join(base_j, "Exhibit-J-6-Forced-PTO.html")
    j6_pdf = os.path.join(base_j, "Exhibit-J-6-Forced-PTO.pdf")
    
    create_j6_html(j6_html)
    generate_pdf(j6_html, j6_pdf)
    
    # M Paths
    base_m = os.path.join(os.getcwd(), "50_MASTER_EXHIBITS", "Exhibit M - Financial Strangulation")
    m_html = os.path.join(base_m, "Exhibit M - Financial Strangulation System.html")
    m_pdf = os.path.join(base_m, "Exhibit M - Financial Strangulation System.pdf") # Standardizing name to Exhibit M...
    
    create_m_html(m_html)
    generate_pdf(m_html, m_pdf)
