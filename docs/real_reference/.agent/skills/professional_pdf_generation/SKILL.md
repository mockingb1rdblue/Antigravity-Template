---
name: Professional PDF Generation
description: Best practices and troubleshooting guide for generating professional PDFs from markdown with proper formatting, especially for legal documents
---

# Professional PDF Generation Skill

## Overview

This skill documents lessons learned from generating professional PDFs for legal mediation packages, including proper table formatting, exhibit lists, and styling.

## The Problem

We needed to convert markdown documents to PDFs suitable for attorney/mediator distribution, with specific formatting requirements:
- Professional styling (11px Segoe UI, navy headers, consistent spacing)
- Proper table rendering
- Bulleted exhibit lists with clear path separation
- No headers/footers
- Clean, readable output

## What Works ✅

### Method 1: Direct MD to PDF (RECOMMENDED)

**Use the existing `convert_md_to_pdf` skill** - it's the most reliable method.

```bash
python .agent/skills/convert_md_to_pdf/convert.py "path/to/file.md"
```

**Advantages:**
- Handles markdown tables correctly
- Proper list formatting
- No string escaping issues
- Consistent output
- Single-step process

**When to use:**
- Legal documents with tables
- Documents with complex markdown formatting
- Any time you need guaranteed fidelity to markdown source

### Method 2: HTML → PDF with Edge (FOR CUSTOM STYLING)

**Use only when you need custom CSS styling not available in markdown.**

```python
# Use the generate_pdf_edge.py script
python 05_scripts/generate_pdf_edge.py "input.html" "output.pdf"
```

**Key command:**
```bash
msedge --headless --disable-gpu --run-all-compositor-stages-before-draw \
  --print-to-pdf="output.pdf" \
  --no-pdf-header-footer \
  file:///absolute/path/to/file.html
```

**Critical flags:**
- `--no-pdf-header-footer` - Removes date/URL stamps
- `--run-all-compositor-stages-before-draw` - Ensures CSS renders before PDF generation
- `--disable-gpu` - Prevents rendering issues in headless mode

## What Doesn't Work ❌

### Anti-Pattern: Manual HTML Generation with Python String Formatting

**DO NOT:**
```python
html_template = """<!DOCTYPE html>
<style>
    body { margin: 0; }  <!-- BREAKS with .format() -->
</style>
{content}
"""
html = html_template.format(content=body)  # FAILS - CSS braces conflict
```

**Why it fails:**
- Python's `.format()` interprets CSS braces `{}` as placeholders
- Requires double-bracing all CSS (`{{ }}`) which is error-prone
- Complex markdown parsing logic prone to edge cases
- Table rendering is difficult to get right

**Alternative:**
If you must generate HTML programmatically, use literal string concatenation or Jinja2 templates.

## Common Issues & Solutions

### Issue 1: Tables Render Incorrectly in PDF

**Symptoms:**
- Table cells run together
- Column widths collapse
- Text overlaps

**Root Cause:**
Markdown tables have specific syntax requirements that get lost in manual HTML conversion.

**Solution:**
Use Method 1 (MD to PDF) for any document with tables. The pandoc-based converter handles tables correctly.

### Issue 2: Exhibit Lists Are Unreadable

**Problem:**
```markdown
Component 1 - Personal ADA Claims - Exhibit A: Written Policies - zip/EXHIBITS/...pdf - Exhibit B: Timeline - zip/EXHIBITS/...pdf
```

All runs together in PDF without clear separation.

**Solution:**
Format each exhibit on its own line with bullets:

```markdown
**Component 1 - Personal ADA Claims:**
- **Exhibit A: Written Policies**
  - `zip/EXHIBITS/Exhibit A - Written Policies/2024-01-01 - Policy Handbook.pdf`
- **Exhibit B: Timeline**
  - `zip/EXHIBITS/Exhibit B - Timeline/Timeline.pdf`
```

**Key principles:**
- One exhibit per line
- Indent file paths under exhibit name
- Use code blocks for paths to prevent line wrapping
- Bold exhibit labels

### Issue 3: Phone Numbers / Critical Data Wrong

**Problem:**
Generated PDFs contain old data from markdown that wasn't updated.

**Prevention:**
1. **Search first:** Always grep for old data before PDF generation
   ```bash
   grep -r "old-phone-number" .
   ```
2. **Update markdown source:** Fix markdown files first
3. **Regenerate PDFs:** Don't manually edit PDFs
4. **Verify:** Open PDF before sending

### Issue 4: Job Titles / Roles Incorrect

**Problem:**
Document mentions "Optimization Coordinator" when actual role was "Production Team Member 1"

**Solution:**
1. Grep for incorrect title across project
2. Replace with correct role and context:
   - Correct: "my actual duties on the production floor"
   - Correct: "Production Team Member 1 in Final Assembly 2"
   - Wrong: Generic title that doesn't match reality

## Best Practices

### 1. Markdown Source is Truth

Always edit markdown files, never PDFs directly. Treat PDFs as compiled artifacts.

### 2. Use Consistent Naming

**Good:**
- `2026-01-29 - Confidential Mediation Statement.md`
- `2026-01-29 - Confidential Mediation Statement.pdf`

**Bad:**
- `01_Confidential_Mediation_Statement.md`
- `mediation_stmt_v3_final.pdf`

### 3. Separate Masters from Distribution

**Folder structure:**
```
50_MASTER_EXHIBITS/        ← Source markdown + HTML
  └─ *.md, *.html

10_TRANSMISSION_BUNDLE/    ← PDFs only (ready to send)
  └─ *.pdf
```

**Why:**
- Prevents accidentally sending markdown/HTML
- Clear separation of build artifacts from sources
- Can zip transmission folder directly

### 4. Table Formatting in Markdown

For tables that will become PDFs:

```markdown
| Component | Description | Value |
|:----------|:------------|------:|
| 1. ADA    | Individual  | $3M   |
| 2. Reform | Systemic    | $3M   |
```

**Requirements:**
- Use alignment markers (`:---`, `:---:`, `---:`)
- Keep cell content concise
- Test table width doesn't exceed page margins
- Don't use line breaks inside cells

### 5. Pre-Flight Checklist

Before generating final PDFs:

- [ ] Grep for old phone numbers
- [ ] Grep for incorrect job titles
- [ ] Grep for placeholder data (XXX, TODO, TBD)
- [ ] Check all file paths are relative to zip root
- [ ] Verify exhibit lists have one item per line
- [ ] Test table rendering in markdown preview
- [ ] Regenerate all PDFs from updated markdown
- [ ] Open each PDF to verify formatting

## Workflow

### Standard Document → PDF Pipeline

1. **Write in Markdown:**
   ```markdown
   # Document Title
   
   Content with **bold** and *italic*.
   
   | Table | Works |
   |-------|-------|
   | Yes   | Good  |
   ```

2. **Generate PDF:**
   ```bash
   python .agent/skills/convert_md_to_pdf/convert.py "file.md"
   ```

3. **Verify Output:**
   - Open PDF
   - Check tables render correctly
   - Check exhibit lists are readable
   - Verify no placeholder data

4. **Move to transmission folder:**
   ```bash
   cp file.pdf 10_TRANSMISSION_BUNDLE/
   ```

### Custom Styled Document Pipeline

Only use when standard markdown styling is insufficient (e.g., colored boxes, complex layouts).

1. **Create HTML with inline CSS:**
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <style>
           body { font-family: 'Segoe UI'; font-size: 11px; }
           /* All CSS here */
       </style>
   </head>
   <body>
       <!-- Content here -->
   </body>
   </html>
   ```

2. **Generate PDF:**
   ```bash
   python 05_scripts/generate_pdf_edge.py "file.html" "file.pdf"
   ```

## Troubleshooting

### PDF is blank or very small (< 20KB)

**Cause:** HTML didn't render properly or CSS broke the layout

**Fix:**
1. Open HTML in browser to verify it displays correctly
2. Check for CSS syntax errors (missing semicolons, unclosed braces)
3. Ensure file paths are absolute when passing to Edge
4. Try regenerating from markdown source instead

### Tables are mangled

**Cause:** HTML generation broke markdown table syntax

**Fix:**
Use Method 1 (MD to PDF) - don't try to manually parse tables in Python

### Exhibit paths run together

**Cause:** All exhibits in single paragraph

**Fix:**
Reformat exhibit list with bullets and line breaks (see Issue 2 above)

### Old data in PDF

**Cause:** Markdown source wasn't updated before PDF generation

**Fix:**
1. `grep -r "old-data" .` to find all instances
2. Update markdown sources
3. Regenerate all PDFs
4. Never manually edit PDFs

## Tools Reference

### convert_md_to_pdf (Skill)
- **Location:** `.agent/skills/convert_md_to_pdf/convert.py`
- **Usage:** `python convert.py "file.md"`
- **Output:** `file.pdf` (same directory)
- **Dependencies:** pandoc, wkhtmltopdf
- **Best for:** Standard documents, tables, lists

### generate_pdf_edge (Script)
- **Location:** `05_scripts/generate_pdf_edge.py`
- **Usage:** `python generate_pdf_edge.py "in.html" "out.pdf"`
- **Dependencies:** Microsoft Edge
- **Best for:** Custom styled documents, complex layouts

## Validation Commands

```bash
# Check for old phone numbers
grep -r "970-420-7732" 10_TRANSMISSION_BUNDLE/

# Check for incorrect titles
grep -r "Optimization Coordinator" 10_TRANSMISSION_BUNDLE/

# Check PDF file sizes (should be > 10KB for multi-page docs)
find 10_TRANSMISSION_BUNDLE/ -name "*.pdf" -exec ls -lh {} \;

# Verify no markdown in transmission folder
find 10_TRANSMISSION_BUNDLE/ -name "*.md"
```

## Lessons Learned

1. **Don't reinvent the wheel:** The `convert_md_to_pdf` skill exists and works well. Use it.

2. **HTML generation is harder than it looks:** Python string formatting + CSS braces = pain. Use proper templating or concatenation.

3. **Tables are fragile:** Markdown table syntax is finicky. Don't try to parse/rebuild manually.

4. **Always grep before generating:** Old data in PDFs is embarrassing and undermines professionalism.

5. **Separate source from distribution:** Keep `.md`/`.html` in masters, only `.pdf` in transmission bundles.

6. **File naming matters:** Consistent, professional naming (date prefix, descriptive title) makes packages look polished.

7. **Pre-flight everything:** Open every PDF before sending. Automated generation doesn't mean automatic correctness.
