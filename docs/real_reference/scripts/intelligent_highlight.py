#!/usr/bin/env python3
"""
Exhibit-Focused PDF Highlighting Script
Highlights key sections in exhibits to show "why" each document is included
Removes highlighting from strategic documents (too much looks unprofessional)
"""

import fitz  # PyMuPDF
import re
import os

# Color definitions (RGB 0-1 scale)
COLORS = {
    "yellow": (1, 1, 0),      # Key values, settlements
    "green": (0, 1, 0.5),     # Supporting evidence
    "orange": (1, 0.6, 0),    # Admissions, smoking guns
    "cyan": (0, 0.8, 1),      # Dates, deadlines
}

def extract_block_text(block):
    """Extract text from a block dictionary"""
    if "lines" not in block:
        return ""
    text = ""
    for line in block["lines"]:
        for span in line["spans"]:
            text += span["text"] + " "
    return text.strip()

# ============================================================================
# EXHIBIT-SPECIFIC HIGHLIGHTING STRATEGIES
# ============================================================================

def highlight_july17_transcript(doc, filename):
    """
    Exhibit C: July 17 Recording Transcripts
    Highlight: "normal process" admission, termination instruction
    """
    print(f"  Analyzing: {filename}")
    
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            text = extract_block_text(block)
            if not text:
                continue
            
            bbox = fitz.Rect(block["bbox"])
            
            # Highlight the smoking gun admission
            if ("normal process" in text.lower() and "vestas" in text.lower()) or \
               "termination instruction" in text.lower():
                annot = page.add_highlight_annot(bbox)
                annot.set_colors(stroke=COLORS["orange"])
                annot.update()
                print(f"    [HIGHLIGHT] Smoking gun admission")

def highlight_executive_ratification(doc, filename):
    """
    Exhibit D: Executive Ratification
    Highlight: SVP Emily Lopez closure/approval
    """
    print(f"  Analyzing: {filename}")
    
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            text = extract_block_text(block)
            if not text:
                continue
            
            bbox = fitz.Rect(block["bbox"])
            
            # Highlight SVP approval
            if "emily lopez" in text.lower() or ("svp" in text.lower() and "closed" in text.lower()):
                annot = page.add_highlight_annot(bbox)
                annot.set_colors(stroke=COLORS["orange"])
                annot.update()
                print(f"    [HIGHLIGHT] Executive ratification")

def highlight_compensation_audit(doc, filename):
    """
    Exhibit J: Compensation Compliance Audit
    Highlight: Shift differential breaches, promise vs. reality
    """
    print(f"  Analyzing: {filename}")
    
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            text = extract_block_text(block)
            if not text:
                continue
            
            bbox = fitz.Rect(block["bbox"])
            
            # Highlight shift differential issues
            if re.search(r'\$3\.00.*differential|shift.*differential.*withh', text, re.IGNORECASE) or \
               re.search(r'holiday.*shift|PTO.*training|breach', text, re.IGNORECASE):
                annot = page.add_highlight_annot(bbox)
                annot.set_colors(stroke=COLORS["orange"])
                annot.update()
                print(f"    [HIGHLIGHT] Compensation breach")
            
            # Highlight job posting promise
            elif "night.*shift" in text.lower() and "$" in text:
                annot = page.add_highlight_annot(bbox)
                annot.set_colors(stroke=COLORS["yellow"])
                annot.update()
                print(f"    [HIGHLIGHT] Promise of differential")

def highlight_regulatory_docs(doc, filename):
    """
    Exhibit K: Regulatory Environment
    Highlight: IRA prevailing wage, FTZ status, tariff exposure
    """
    print(f"  Analyzing: {filename}")
    
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            text = extract_block_text(block)
            if not text:
                continue
            
            bbox = fitz.Rect(block["bbox"])
            
            # Highlight prevailing wage requirements
            if re.search(r'prevailing.*wage|IRA.*requirement|\$\d+.*wage', text, re.IGNORECASE):
                annot = page.add_highlight_annot(bbox)
                annot.set_colors(stroke=COLORS["orange"])
                annot.update()
                print(f"    [HIGHLIGHT] Regulatory requirement")
            
            # Highlight tariff exposure
            elif re.search(r'section 232|tariff', text, re.IGNORECASE):
                annot = page.add_highlight_annot(bbox)
                annot.set_colors(stroke=COLORS["yellow"])
                annot.update()
                print(f"    [HIGHLIGHT] Tariff exposure")

def highlight_timeline(doc, filename):
    """
    Exhibit B: Timeline
   Highlight: Key dates of economic coercion events
    """
    print(f"  Analyzing: {filename}")
    
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            text = extract_block_text(block)
            if not text:
                continue
            
            bbox = fitz.Rect(block["bbox"])
            
            # Highlight key coercion events
            if re.search(r'july 17|july 21|august 28|termination', text, re.IGNORECASE):
                annot = page.add_highlight_annot(bbox)
                annot.set_colors(stroke=COLORS["orange"])
                annot.update()
                print(f"    [HIGHLIGHT] Key timeline event")

def highlight_financial_strangulation(doc, filename):
    """
    Exhibit M: Financial Strangulation
    Highlight: Calculated economic coercion, timeline of pressure
    """
    print(f"  Analyzing: {filename}")
    
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            text = extract_block_text(block)
            if not text:
                continue
            
            bbox = fitz.Rect(block["bbox"])
            
            # Highlight financial pressure tactics
            if re.search(r'unpaid.*leave|economic.*pressure|calculated|strangulation', text, re.IGNORECASE):
                annot = page.add_highlight_annot(bbox)
                annot.set_colors(stroke=COLORS["orange"])
                annot.update()
                print(f"    [HIGHLIGHT] Economic coercion tactic")

def highlight_policies(doc, filename):
    """
    Exhibit A: Written Policies
    Highlight: Relevant policy sections that were violated
    """
    print(f"  Analyzing: {filename}")
    
    # Only highlight specific sections, not entire docs
    # Look for ADA, accommodation, termination sections
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            text = extract_block_text(block)
            if not text:
                continue
            
            bbox = fitz.Rect(block["bbox"])
            
            # Highlight ADA/accommodation sections
            if re.search(r'disability|accommodation|ada|interactive process', text, re.IGNORECASE) and \
               len(text) < 200:  # Only highlight headers/key sections, not entire paragraphs
                annot = page.add_highlight_annot(bbox)
                annot.set_colors(stroke=COLORS["green"])
                annot.update()
                print(f"    [HIGHLIGHT] Policy section")

def highlight_contemporaneous_objection(doc, filename):
    """
    Exhibit E: Contemporaneous Objection
    Highlight: Formal objection to executives, notice of discrimination
    """
    print(f"  Analyzing: {filename}")
    
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            text = extract_block_text(block)
            if not text:
                continue
            
            bbox = fitz.Rect(block["bbox"])
            
            # Highlight objection and discrimination references
            if re.search(r'discrimin|ADA|interactive process|objection|concern', text, re.IGNORECASE):
                annot = page.add_highlight_annot(bbox)
                annot.set_colors(stroke=COLORS["orange"])
                annot.update()
                print(f"    [HIGHLIGHT] Objection to discrimination")

def highlight_evidence_of_malice(doc, filename):
    """
    Exhibit F: Evidence of Malice
    Highlight: Liability admission, knowledge of wrongdoing
    """
    print(f"  Analyzing: {filename}")
    
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            text = extract_block_text(block)
            if not text:
                continue
            
            bbox = fitz.Rect(block["bbox"])
            
            # Highlight liability admissions
            if re.search(r'liability|wrongful|knew|aware|malice', text, re.IGNORECASE):
                annot = page.add_highlight_annot(bbox)
                annot.set_colors(stroke=COLORS["orange"])
                annot.update()
                print(f"    [HIGHLIGHT] Evidence of malice")

# ============================================================================
# STRATEGIC DOCUMENTS (NO HIGHLIGHTING - TOO UNPROFESSIONAL)
# ============================================================================

def no_highlighting(doc, filename):
    """
    Strategic documents: No highlighting (user feedback - looks unprofessional)
    """
    print(f"  Skipping highlighting: {filename} (strategic doc)")
    return

# ============================================================================
# MAIN PROCESSING
# ============================================================================

def process_pdf(input_path, strategy_func):
    """
    Apply highlighting strategy to a PDF
    """
    try:
        doc = fitz.open(input_path)
        filename = os.path.basename(input_path)
        strategy_func(doc, filename)
        
        # Save to temporary file first
        temp_path = input_path + ".temp"
        doc.save(temp_path, encryption=fitz.PDF_ENCRYPT_NONE, deflate=True)
        doc.close()
        
        # Replace original with highlighted version
        if os.path.exists(input_path):
            os.remove(input_path)
        os.rename(temp_path, input_path)
        
        return True
    except Exception as e:
        print(f"  [ERROR] {input_path}: {e}")
        return False

def main():
    """
    Main execution: Focus on exhibits, skip strategic docs
    """
    base_dir = "10_TRANSMISSION_BUNDLE"
    
    # Strategic documents - NO highlighting (user feedback: too much, unprofessional)
    strategic_docs = [
        (os.path.join(base_dir, "i - Pre-Mediation Cover Letter.pdf"), no_highlighting),
        (os.path.join(base_dir, "ii - Settlement Allocation Table.pdf"), no_highlighting),
        (os.path.join(base_dir, "iii - Confidential Mediation Statement.pdf"), no_highlighting),
        (os.path.join(base_dir, "iv - Mediator Quick Reference.pdf"), no_highlighting),
    ]
    
    # Exhibits - FOCUSED highlighting to show "why" each is included
    exhibit_mapping = {
        "Exhibit A - Written Policies": highlight_policies,
        "Exhibit B - Timeline": highlight_timeline,
        "Exhibit C - July 17 Recording": highlight_july17_transcript,
        "Exhibit D - Executive Ratification": highlight_executive_ratification,
        "Exhibit E - Contemporaneous Objection": highlight_contemporaneous_objection,
        "Exhibit F - Evidence of Malice": highlight_evidence_of_malice,
        "Exhibit J - Compensation Compliance Audit": highlight_compensation_audit,
        "Exhibit K - Regulatory Environment": highlight_regulatory_docs,
        "Exhibit M - Financial Strangulation": highlight_financial_strangulation,
    }
    
    print("\n" + "="*60)
    print("EXHIBIT-FOCUSED PDF HIGHLIGHTING")
    print("="*60 + "\n")
    
    print("Phase 1: Removing highlighting from strategic documents...")
    for path, strategy in strategic_docs:
        if os.path.exists(path):
            process_pdf(path, strategy)
    
    print("\nPhase 2: Highlighting exhibits to show 'why' included...")
    success_count = 0
    
    # Process exhibits
    exhibits_dir = os.path.join(base_dir, "03_Exhibits_Bundle")
    for root, dirs, files in os.walk(exhibits_dir):
        for file in files:
            if not file.endswith('.pdf'):
                continue
            
            file_path = os.path.join(root, file)
            
            # Find appropriate strategy based on exhibit folder
            strategy = None
            for exhibit_name, exhibit_strategy in exhibit_mapping.items():
                if exhibit_name in root:
                    strategy = exhibit_strategy
                    break
            
            if strategy:
                if process_pdf(file_path, strategy):
                    success_count += 1
            else:
                print(f"  [SKIP] {file} (no strategy)")
    
    print(f"\n{'='*60}")
    print(f"COMPLETE: {success_count} exhibits highlighted")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
