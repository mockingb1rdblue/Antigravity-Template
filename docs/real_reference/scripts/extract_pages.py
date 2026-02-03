import argparse
import fitz  # pymupdf
import os

def parse_page_ranges(pages_str):
    """
    Parses a string like "1,3-5, 10" into a list of 0-indexed page numbers.
    User input is expected to be 1-indexed.
    """
    pages = set()
    parts = pages_str.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            # Inclusive range, convert to 0-index
            for p in range(start - 1, end):
                pages.add(p)
        else:
            pages.add(int(part) - 1)
    return sorted(list(pages))

def extract_pages(pdf_path, output_path, pages_str):
    doc = fitz.open(pdf_path)
    page_indices = parse_page_ranges(pages_str)
    
    new_doc = fitz.open()  # empty document
    
    for page_idx in page_indices:
        if 0 <= page_idx < len(doc):
            new_doc.insert_pdf(doc, from_page=page_idx, to_page=page_idx)
    
    if not output_path:
        base, ext = os.path.splitext(pdf_path)
        output_path = f"{base}_extracted{ext}"
        
    new_doc.save(output_path)
    print(f"Extracted {len(new_doc)} pages to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract specific pages from a PDF")
    parser.add_argument("pdf_path", help="Path to source PDF")
    parser.add_argument("--pages", required=True, help="Pages to extract (e.g. '1,3-5')")
    parser.add_argument("--output", help="Optional output path")
    
    args = parser.parse_args()
    extract_pages(args.pdf_path, args.output, args.pages)
