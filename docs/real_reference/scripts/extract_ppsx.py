import os
import zipfile
import xml.etree.ElementTree as ET
import re
import sys

def extract_text_from_ppsx(ppsx_path, output_md_path):
    """
    Extracts text from a .ppsx/.pptx file by treating it as a zip and parsing XML.
    Bypasses strict format checks of python-pptx.
    """
    if not os.path.exists(ppsx_path):
        print(f"Error: File not found at {ppsx_path}")
        return

    try:
        with open(output_md_path, "w", encoding="utf-8") as out_f:
            out_f.write(f"# Content Extraction: {os.path.basename(ppsx_path)}\n\n")

            with zipfile.ZipFile(ppsx_path, 'r') as z:
                # Find all slide files
                slide_files = [f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
                # Sort by number (slide1, slide2, etc.)
                slide_files.sort(key=lambda x: int(re.search(r'slide(\d+)\.xml', x).group(1)))

                for i, slide_file in enumerate(slide_files):
                    slide_num = i + 1
                    xml_content = z.read(slide_file)
                    root = ET.fromstring(xml_content)

                    # Extract all text elements <a:t>
                    # Namespace map matches standard Office Open XML
                    namespaces = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
                    text_elements = root.findall('.//a:t', namespaces)

                    slide_text = []
                    for elem in text_elements:
                        if elem.text:
                            slide_text.append(elem.text)

                    out_f.write(f"## Slide {slide_num}\n\n")
                    if slide_text:
                        # Join text, simple heuristic for separating distinct text blocks
                        out_f.write("\n".join(slide_text))
                    else:
                        out_f.write("*(No text content)*")
                    out_f.write("\n\n---\n\n")

        print(f"Successfully extracted content to {output_md_path}")

    except Exception as e:
        print(f"Failed to extract text: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_ppsx.py <input_ppsx> <output_md>")
    else:
        extract_text_from_ppsx(sys.argv[1], sys.argv[2])
