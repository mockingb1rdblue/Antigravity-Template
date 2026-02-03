#!/usr/bin/env python3
"""
Remove PDF Highlights Selectively
Removes all PDF annotations EXCEPT in specified exhibit folders
"""

import fitz  # PyMuPDF
import os

def remove_all_annotations(pdf_path):
    """Remove all annotations from a PDF"""
    try:
        doc = fitz.open(pdf_path)
        
        annotation_count = 0
        for page in doc:
            # Get all annotations on the page
            annots = list(page.annots())
            for annot in annots:
                page.delete_annot(annot)
                annotation_count += 1
        
        # Save to temp file
        temp_path = pdf_path + ".temp"
        doc.save(temp_path, encryption=fitz.PDF_ENCRYPT_NONE, deflate=True)
        doc.close()
        
        # Replace original
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        os.rename(temp_path, pdf_path)
        
        return annotation_count
    except Exception as e:
        print(f"  [ERROR] {pdf_path}: {e}")
        return 0

def main():
    """
    Remove highlights from all PDFs except Exhibits D, K, and M
    """
    base_dir = "10_TRANSMISSION_BUNDLE"
    
    # Folders to KEEP highlights
    keep_highlights = [
        "Exhibit D - Executive Ratification",
        "Exhibit K - Regulatory Environment",
    ]
    
    print("\n" + "="*60)
    print("SELECTIVE HIGHLIGHT REMOVAL")
    print("="*60 + "\n")
    print("Removing highlights from all PDFs EXCEPT:")
    for folder in keep_highlights:
        print(f"  - {folder}")
    print()
    
    removed_count = 0
    file_count = 0
    
    # Walk through all PDFs
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if not file.endswith('.pdf'):
                continue
            
            file_path = os.path.join(root, file)
            
            # Check if this file is in a "keep" folder
            should_keep = any(keep_folder in root for keep_folder in keep_highlights)
            
            if should_keep:
                print(f"[KEEP] {file}")
            else:
                print(f"[REMOVE] {file}")
                count = remove_all_annotations(file_path)
                if count > 0:
                    print(f"  Removed {count} annotations")
                removed_count += count
                file_count += 1
    
    print(f"\n{'='*60}")
    print(f"COMPLETE: Removed {removed_count} annotations from {file_count} PDFs")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
