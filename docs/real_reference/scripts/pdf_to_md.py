import argparse
import fitz  # pymupdf
import os

def pdf_to_md(pdf_path, output_path=None):
    if not output_path:
        output_path = os.path.splitext(pdf_path)[0] + ".md"

    doc = fitz.open(pdf_path)
    text_content = []
    
    # Add Title
    title = doc.metadata.get('title') or os.path.basename(pdf_path)
    text_content.append(f"# {title}\n")
    
    for page_num, page in enumerate(doc):
        text_content.append(f"\n## Page {page_num + 1}\n")
        text = page.get_text()
        text_content.append(text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(text_content))
    
    print(f"Converted: {pdf_path} -> {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF text to Markdown")
    parser.add_argument("pdf_path", help="Path to source PDF")
    parser.add_argument("--output", help="Optional output path")
    
    args = parser.parse_args()
    pdf_to_md(args.pdf_path, args.output)
