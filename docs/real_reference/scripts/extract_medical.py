
import sys

def extract_text_from_pdf(pdf_path):
    try:
        # Check if pypdf is installed
        try:
            from pypdf import PdfReader
            reader = PdfReader(pdf_path)
            full_text = ""
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    full_text += f"\n--- Page {i+1} ---\n{text}"
            return full_text
        except ImportError:
            return "Error: pypdf library is not installed."
        except Exception as e:
             return f"Error reading PDF with pypdf: {e}"

    except Exception as e:
        return f"General Error: {e}"

if __name__ == "__main__":
    pdf_path = r"c:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\originals\Medical\Records - AS .pdf" 
    text = extract_text_from_pdf(pdf_path)
    print(text[:5000]) # Print first 5000 chars to test, or save to file if huge.
    # We want to search for keywords in the full text
    
    keywords = ["March 2025", "April 2025", "May 2025", "June 2025", "unpaid", "leave", "quit", "resign", "termination", "interactive"]
    print("\n--- KEYWORD SEARCH ---\n")
    lines = text.split('\n')
    for i, line in enumerate(lines):
        for keyword in keywords:
            if keyword.lower() in line.lower():
                 print(f"Line {i}: {line.strip()}")

