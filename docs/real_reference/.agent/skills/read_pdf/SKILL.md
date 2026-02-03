---
name: Read PDF
description: Extracts text from a PDF file using a Python script.
---

# Read PDF

This skill allows you to read the text content of a PDF file.

## Usage

To read a PDF file, run the `read_pdf.py` script with the path to the PDF file as an argument.

```bash
python .agent/skills/read_pdf/read_pdf.py "path/to/your/document.pdf"
```

## Requirements

- Python 3
- `pypdf` library (`pip install pypdf`)

## Notes

- The script outputs the text content of the PDF to standard output.
- It separates pages with `--- Page N ---`.
- If the PDF contains scanned images without OCR text layer, this script will strictly return empty text for those pages.
