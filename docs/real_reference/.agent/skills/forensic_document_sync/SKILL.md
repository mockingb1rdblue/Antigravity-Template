# SKILL: Forensic Document Synchronization

## Overview
This skill codifies the "Master -> Sync -> Send" architecture used for high-fidelity legal and audit document management. It ensures that source "work product" (markdown, HTML, spreadsheets) is kept separate from "release assets" (PDFs).

## Core Principles
1.  **Work Product Isolation**: All drafting, redesigning, and reworking occurs in a `50_MASTER_EXHIBITS` or similar designated source directory.
2.  **Headless PDF Generation**: Use established browser engines for consistent, premium PDF generation from HTML templates.
3.  **Path-Driven Synchronization**: The final release bundle is driven by a "Manifest" (e.g., a Mediation Statement) that uses standardized forensic paths.
4.  **Forensic Path Format**: Use plain-text URI references like `zip/EXHIBITS/Exhibit A/...` to allow non-technical reviewers to understand the archive structure without broken markdown links.

## Automations

### Headless PDF (Edge/Chrome)
To generate professional PDFs **without browser headers/footers** (CRITICAL for audit quality), always include the `--print-to-pdf-no-header` flag:
```powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" `
    --headless `
    --disable-gpu `
    --print-to-pdf-no-header `
    --print-to-pdf="C:\path\to\output.pdf" `
    "C:\path\to\input.html"
```

### Path-Based Parsing (Python)
Use regex to identify forensic paths in a manifest:
```python
# Regex to match zip/ references until the extension
import re
paths = re.findall(r"(zip/(?:EXHIBITS|STRATEGIC)/.*?\.pdf)", content, re.IGNORECASE)
```

### URI Encoding (Cross-Platform links)
Always encode spaces in markdown links to ensure clickability in older viewers:
```python
import urllib.parse
encoded_file = urllib.parse.quote(filename)
```

## Best Practices
*   **Signed Priority**: Synchronization scripts should check for a "Signed" suffix and prioritize it over base affidavits.
*   **Clean Targets**: Release folders should be cleaned before synchronization to prevent "ghost" files or outdated drafts from persisting.
*   **Plain Text Paths**: In the final Mediation Statement, prioritize readability over clickability to avoid broken interactions for conservative legal recipients.
