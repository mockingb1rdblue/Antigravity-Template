import sys
import asyncio
import os
from playwright.async_api import async_playwright

async def generate_pdf(html_path, pdf_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Convert local path to file URL
        file_url = f"file:///{html_path.replace(os.sep, '/')}"
        
        await page.goto(file_url)
        
        # PDF options
        await page.pdf(
            path=pdf_path,
            format="Letter",
            margin={
                "top": "0.5in",
                "right": "0.5in",
                "bottom": "0.5in",
                "left": "0.5in"
            },
            print_background=True,
            scale=0.85 
        )
        
        await browser.close()
        print(f"pdf_generated: {pdf_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_j5_pdf.py <html_path> <pdf_path>")
        sys.exit(1)
        
    html_file = sys.argv[1]
    pdf_file = sys.argv[2]
    
    # Use absolute paths if possible, but the script should handle what's passed
    if not os.path.isabs(html_file):
        html_file = os.path.abspath(html_file)
    if not os.path.isabs(pdf_file):
        pdf_file = os.path.abspath(pdf_file)

    asyncio.run(generate_pdf(html_file, pdf_file))
