import fitz  # PyMuPDF
import sys
import os
import argparse

def optimize_pdf(input_path, output_path=None, threshold_kb=0):
    """
    Replaces images in the PDF with a placeholder if they exceed the threshold.
    """
    if not output_path:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_optimized{ext}"

    print(f"Opening: {input_path}")
    try:
        doc = fitz.open(input_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return

    images_replaced = 0
    total_space_saved = 0

    for page_num, page in enumerate(doc):
        # Get image list
        images = page.get_images()
        
        # Iterate backwards to avoid index issues if we were modifying list (though here we just redact areas)
        for img in images:
            xref = img[0]
            
            # Check size of image stream
            try:
                stream = doc.extract_image(xref)
                size_bytes = len(stream["image"])
                size_kb = size_bytes / 1024
            except:
                size_kb = 0
            
            if size_kb < threshold_kb:
                continue

            # Find where this image is used on the page
            # get_image_rects returns a list of Rect objects
            rects = page.get_image_rects(xref)
            
            if not rects:
                continue

            print(f"  Page {page_num+1}: Redacting image ({size_kb:.1f} KB)")
            
            # Redact each instance of the image on this page
            for rect in rects:
                # 1. Draw a placeholder rectangle
                shape = page.new_shape()
                shape.draw_rect(rect)
                shape.finish(color=(0.9, 0.9, 0.9), fill=(0.9, 0.9, 0.9)) # Light gray
                shape.commit()

                # 2. Add text placeholder
                text = f"[Image Removed]\n({size_kb:.0f} KB saved)"
                
                # Calculate text size to fit? Just putting it in center.
                # insert_textbox is easier
                page.insert_textbox(rect, text, fontsize=10, color=(0, 0, 0), align=fitz.TEXT_ALIGN_CENTER)

                # 3. Mark the visible image area as redacted (handled by drawing over it effectively for visual)
                # But to save space, we need to remove the image object.
                # Redaction annotations are one way, but just removing the reference is better.
                # However, clean_contents() or redaction applier is needed.
                # Simplest 'space saving' method with PyMuPDF:
                # add a redaction annotation and apply it.
                page.add_redact_annot(rect, text="") # We already drew the box, this just cuts the underlying image
                page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)
            
            images_replaced += 1

    if images_replaced > 0:
        # If overwriting, save to temp first then move
        save_path = output_path
        temp_path = None
        
        if output_path == input_path:
            temp_path = f"{input_path}.tmp"
            save_path = temp_path
            
        print(f"Saving optimized version to: {save_path}")
        # garbage=4: aggressive garbage collection
        # deflate=True: compress streams
        doc.save(save_path, garbage=4, deflate=True)
        
        if temp_path:
            doc.close() # Close handle before moving
            import shutil
            shutil.move(temp_path, output_path)
        
        old_size = os.path.getsize(input_path)
        new_size = os.path.getsize(output_path)
        print(f"Original Size: {old_size/1024/1024:.2f} MB")
        print(f"New Size:      {new_size/1024/1024:.2f} MB")
        print(f"Reduction:     {(old_size-new_size)/1024/1024:.2f} MB")
    else:
        print("No images found or removed based on criteria.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Image Optimizer")
    parser.add_argument("input_path", help="Path to the PDF file")
    parser.add_argument("--threshold", type=int, default=0, help="Minimum image size in KB to remove (default 0)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the input file")
    
    args = parser.parse_args()
    
    output = None
    if args.overwrite:
        output = args.input_path
        
    optimize_pdf(args.input_path, output_path=output, threshold_kb=args.threshold)
