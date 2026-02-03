---
name: Convert MD to PDF
description: Converts a Markdown file to a PDF file using a Python script.
---

# Convert MD to PDF

This skill allows you to convert a Markdown file into a professional-looking PDF document.

## Usage

To convert a markdown file, run the `convert.py` script with the path to the markdown file.

```bash
python .agent/skills/convert_md_to_pdf/convert.py "path/to/your/document.md"
```

The script will generate a PDF file in the same directory with the same basename (e.g., `document.pdf`).

## Requirements

- Python 3
- `markdown` library
- `xhtml2pdf` library

## Notes

- The script uses basic CSS for styling.
- It supports standard Markdown features (headers, lists, bold/italic, code blocks).
- Tables are supported but may require simple markdown formatting.
- Images must be referenced with absolute paths or paths relative to the execution directory for them to appear correctly in the PDF.
