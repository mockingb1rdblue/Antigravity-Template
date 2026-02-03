import subprocess
import sys
import os
import time

def generate_pdf_edge(html_path, pdf_path):
    """
    Generates a PDF from an HTML file using MS Edge in headless mode.
    """
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_path):
        # Try alternate path
        edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

    if not os.path.exists(edge_path):
        print("Error: Could not find msedge.exe")
        return

    # Ensure absolute paths
    if not os.path.isabs(html_path):
        html_path = os.path.abspath(html_path)
    if not os.path.isabs(pdf_path):
        pdf_path = os.path.abspath(pdf_path)

    # File URL
    file_url = f"file:///{html_path.replace(os.sep, '/')}"

    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf=" + pdf_path,
        "--no-pdf-header-footer",
        file_url
    ]

    print(f"Running: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True, timeout=30)
        # Wait a moment for file release
        time.sleep(2)
        
        if os.path.exists(pdf_path):
            print(f"Success: PDF generated at {pdf_path}")
            print(f"Size: {os.path.getsize(pdf_path)} bytes")
        else:
            print("Error: PDF file was not created.")

    except subprocess.CalledProcessError as e:
        print(f"Error running Edge: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_pdf_edge.py <html_path> <pdf_path>")
    else:
        generate_pdf_edge(sys.argv[1], sys.argv[2])
