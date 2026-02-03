import argparse
import fitz  # pymupdf
import os

def highlight_text(pdf_path, output_path, search_text):
    doc = fitz.open(pdf_path)
    count = 0
    
    for page in doc:
        text_instances = page.search_for(search_text)
        for inst in text_instances:
            highlight = page.add_highlight_annot(inst)
            highlight.update()
            count += 1
            
    if not output_path:
        base, ext = os.path.splitext(pdf_path)
        output_path = f"{base}_highlighted{ext}"
        
    doc.save(output_path)
    print(f"Highlighted {count} instances of '{search_text}' in: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Highlight text in a PDF")
    parser.add_argument("pdf_path", help="Path to source PDF")
    parser.add_argument("search_text", help="Text to search and highlight")
    parser.add_argument("--output", help="Optional output path")
    
    args = parser.parse_args()
    highlight_text(args.pdf_path, args.output, args.search_text)
