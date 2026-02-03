import argparse
import sys
import os

try:
    from pypdf import PdfReader
except ImportError:
    print("Error: pypdf is not installed. Please run 'pip install pypdf' to use this skill.")
    sys.exit(1)

def read_pdf(file_path):
    """
    Reads a PDF file and prints its content to stdout.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    try:
        reader = PdfReader(file_path)
        text = ""
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {i+1} ---\n"
                text += page_text
        
        print(text)

    except Exception as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read text from a PDF file.")
    parser.add_argument("file_path", help="Path to the PDF file")
    args = parser.parse_args()
    
    # Set stdout to use UTF-8
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
             # For older python versions if needed, though 3.13 is fine
            import codecs
            sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

    read_pdf(args.file_path)
