---
name: Intelligent PDF Highlighting
description: Semantic, context-aware PDF highlighting using PyMuPDF for strategic document preparation
---

# Intelligent PDF Highlighting Skill

## Overview

This skill enables intelligent, context-aware highlighting of PDFs using PyMuPDF (fitz). Unlike lazy keyword search, this approach uses semantic analysis to identify and highlight the most strategically relevant content.

## Installation

```bash
pip install pymupdf
```

## Core Concept: Semantic vs. Keyword Highlighting

### ❌ Lazy Keyword Approach (Bad)
```python
# Don't do this - matches everywhere regardless of context
for page in doc:
    text = page.get_text()
    if "Vestas" in text:
        highlight_entire_page()  # Too broad!
```

### ✅ Intelligent Semantic Approach (Good)
```python
# Understand document structure and context
for page in doc:
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if is_settlement_value(block):
            highlight_with_color(yellow)
        elif is_legal_admission(block):
            highlight_with_color(orange)
        elif is_evidence_citation(block):
            highlight_with_color(green)
```

## PyMuPDF Basics

### Opening and Saving PDFs

```python
import fitz  # PyMuPDF

# Open PDF
doc = fitz.open("input.pdf")

# Iterate pages
for page in doc:
    # Work with page
    pass

# Save (incremental=True preserves existing annotations)
doc.save("output.pdf", incremental=False, encryption=fitz.PDF_ENCRYPT_NONE)
doc.close()
```

### Text Extraction Methods

**Method 1: Simple text (for search)**
```python
text = page.get_text()
```

**Method 2: Blocks with coordinates (for precise highlighting)**
```python
blocks = page.get_text("dict")["blocks"]
for block in blocks:
    bbox = block["bbox"]  # (x0, y0, x1, y1)
    text = get_block_text(block)
```

**Method 3: Word-level (most precise)**
```python
words = page.get_text("words")
# Returns: [(x0, y0, x1, y1, "word", block_no, line_no, word_no), ...]
```

## Highlighting Techniques

### Basic Highlight

```python
# Highlight a rectangular area
rect = fitz.Rect(x0, y0, x1, y1)
highlight = page.add_highlight_annot(rect)
highlight.set_colors(stroke=(1, 1, 0))  # Yellow RGB
highlight.update()
```

### Multi-line Highlight

```python
def highlight_quads(page, quads, color):
    """
    Highlight using quads (better for multi-line text)
    quads: list of fitz.Quad objects or 4-tuples
    """
    annot = page.add_highlight_annot(quads)
    annot.set_colors(stroke=color)
    annot.update()
```

### Color Coding Strategy

```python
COLORS = {
    "yellow": (1, 1, 0),      # Settlement values, dollar amounts
    "green": (0, 1, 0.5),     # Evidence citations, exhibits
    "orange": (1, 0.6, 0),    # Admissions, damaging statements
    "cyan": (0, 0.8, 1),      # Deadlines, dates
    "pink": (1, 0.7, 0.8),    # Legal standards, precedents
}
```

## Semantic Detection Patterns

### 1. Settlement Values

```python
import re

def is_settlement_value(text):
    """Detect dollar amounts in settlement context"""
    patterns = [
        r'\$[\d,]+(?:\.\d{2})?(?:\s*(?:million|M|K))?',  # $3.5M, $3,500,000
        r'(?:settlement|demand|value|exposure).*\$',     # Context + value
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False
```

### 2. Legal Admissions

```python
def is_legal_admission(text):
    """Detect admissions against interest"""
    admission_phrases = [
        "normal process",
        "we placed",
        "it is our practice",
        "we typically",
        "standard procedure",
    ]
    return any(phrase in text.lower() for phrase in admission_phrases)
```

### 3. Evidence Citations

```python
def is_evidence_citation(text):
    """Detect exhibit references"""
    patterns = [
        r'Exhibit\s+[A-M]',
        r'zip/EXHIBITS/',
        r'\d{4}-\d{2}-\d{2}\s+-\s+',  # Date-prefixed filenames
    ]
    return any(re.search(p, text) for p in patterns)
```

### 4. Critical Dates

```python
def is_critical_date(text):
    """Detect important dates and deadlines"""
    date_contexts = [
        r'(?:mediation|deadline|due|filed).*\d{1,2}/\d{1,2}/\d{4}',
        r'(?:June|July|August)\s+\d{1,2},\s+\d{4}',
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in date_contexts)
```

## Complete Working Example

```python
import fitz
import re

def highlight_pdf_intelligently(input_pdf, output_pdf):
    """
    Apply intelligent, context-aware highlighting
    """
    doc = fitz.open(input_pdf)
    
    for page_num, page in enumerate(doc):
        # Get text with coordinates
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if "lines" not in block:
                continue
            
            bbox = fitz.Rect(block["bbox"])
            text = ""
            for line in block["lines"]:
                for span in line["spans"]:
                    text += span["text"] + " "
            
            # Apply semantic rules
            if is_settlement_value(text):
                annot = page.add_highlight_annot(bbox)
                annot.set_colors(stroke=(1, 1, 0))  # Yellow
                annot.update()
            
            elif is_legal_admission(text):
                annot = page.add_highlight_annot(bbox)
                annot.set_colors(stroke=(1, 0.6, 0))  # Orange
                annot.update()
            
            elif is_evidence_citation(text):
                annot = page.add_highlight_annot(bbox)
                annot.set_colors(stroke=(0, 1, 0.5))  # Green
                annot.update()
    
    doc.save(output_pdf, encryption=fitz.PDF_ENCRYPT_NONE)
    doc.close()
    print(f"Highlighted PDF saved: {output_pdf}")

# Detection functions (as defined above)
def is_settlement_value(text):
    return bool(re.search(r'\$[\d,]+(?:\.\d{2})?(?:\s*(?:million|M))?', text))

def is_legal_admission(text):
    return "normal process" in text.lower() or "standard procedure" in text.lower()

def is_evidence_citation(text):
    return bool(re.search(r'Exhibit\s+[A-M]|zip/EXHIBITS/', text))
```

## Document-Specific Strategies

### Settlement/Demand Letters
**Highlight**:
- Dollar amounts (yellow)
- Settlement ranges (yellow)
- Deadlines (cyan)
- Representation status (green)

### Mediation Statements
**Highlight**:
- Key admissions (orange)
- Evidence citations (green)
- Legal standards (pink)
- Settlement framework tables (yellow)

### Evidence Exhibits
**Highlight**:
- Dates of key events (cyan)
- Names of decision-makers (pink)
- Incriminating statements (orange)

## Advanced Techniques

### Precise Word-Level Highlighting

```python
def highlight_specific_phrase(page, phrase):
    """
    Highlight exact phrase with precise boundaries
    """
    words = page.get_text("words")
    phrase_words = phrase.split()
    
    for i in range(len(words) - len(phrase_words) + 1):
        match = True
        quads = []
        
        for j, word in enumerate(phrase_words):
            if words[i + j][4].lower() != word.lower():
                match = False
                break
            quads.append(fitz.Rect(words[i + j][:4]))
        
        if match:
            page.add_highlight_annot(quads)
```

### Contextual Highlighting

```python
def highlight_if_context_matches(page, target, required_context):
    """
    Only highlight target if it appears near required context
    """
    blocks = page.get_text("dict")["blocks"]
    
    for block in blocks:
        text = extract_block_text(block)
        
        if target in text and required_context in text:
            bbox = fitz.Rect(block["bbox"])
            page.add_highlight_annot(bbox)
```

## Common Pitfalls

### 1. Over-Highlighting

**Problem**: Highlighting too much reduces impact.

**Solution**: Be selective - only highlight truly critical content (10-20% of document).

### 2. Highlighting Entire Pages

**Problem**: Lazy keyword search highlights every occurrence.

**Solution**: Use semantic rules to filter by context and importance.

### 3. Overlapping Annotations

**Problem**: Multiple highlights on same area create visual clutter.

**Solution**: Prioritize annotations (e.g., admissions > values > citations).

### 4. Not Testing Output

**Problem**: Highlights may not render correctly in all PDF viewers.

**Solution**: Always open output in Adobe Acrobat, Preview, Edge PDF to verify.

## Performance Considerations

- **Large PDFs**: Process page-by-page to avoid memory issues
- **Batch Processing**: Use multiprocessing for multiple files
- **Incremental Save**: Use `doc.save(incremental=True)` to preserve existing annotations

## Verification Checklist

- [ ] Open highlighted PDF in multiple viewers
- [ ] Verify highlights are semantically relevant
- [ ] Check color coding consistency
- [ ] Ensure no over-highlighting (< 20% of content)
- [ ] Confirm critical content is captured
- [ ] Test that PDF remains searchable

## See Also

- `05_scripts/intelligent_highlight.py` - Implementation script
- PyMuPDF documentation: https://pymupdf.readthedocs.io/
- PDF annotation standards: ISO 32000-2
