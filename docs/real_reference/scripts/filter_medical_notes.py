import re
from datetime import datetime

input_path = r"c:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\medical_records_full.txt"
output_path = r"c:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\filtered_medical_notes.txt"

def parse_date(date_str):
    try:
        # Format: 01/29/2025 07:52 PM or 01/29/2025
        # Clean up string
        clean = date_str.strip().split()[0]
        return datetime.strptime(clean, "%m/%d/%Y")
    except:
        return None

def filter_notes():
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into pages
    pages = content.split("--- Page")
    
    start_date = datetime(2025, 3, 25)
    end_date = datetime(2025, 8, 28)

    relevant_entries = []

    for page in pages:
        if not page.strip():
            continue
            
        # Try to find the PRIMARY date of the note.
        # Usually it's "Date:\nMM/DD/YYYY"
        match = re.search(r"Date:\s*\n?\s*(\d{2}/\d{2}/\d{4})", page)
        
        # If not found, look for Service Date
        if not match:
             match = re.search(r"Service Date:\s*\n?\s*(\d{2}/\d{2}/\d{4})", page)

        if match:
            date_str = match.group(1)
            date_obj = parse_date(date_str)
            
            if date_obj and start_date <= date_obj <= end_date:
                relevant_entries.append(f"--- Page{page}")
                continue # Found valid date, add page

        # Fallback: check signature date if no other date found or other date out of range?
        # Actually, let's just check if ANY date in the page is in range.
        # Scan all dates
        all_dates = re.findall(r"(\d{2}/\d{2}/\d{4})", page)
        for d_str in all_dates:
             d_obj = parse_date(d_str)
             if d_obj and start_date <= d_obj <= end_date:
                 relevant_entries.append(f"--- Page{page}")
                 break # Add page once if any valid date found

    # Remove duplicates from relevant_entries (if logic added same page twice? No, logical flow prevents it)
    # But list might have duplicates if I iterate weirdly? No.

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Found {len(relevant_entries)} relevant entries.\n")
        for entry in relevant_entries:
            f.write(entry)
            f.write("\n" + "="*40 + "\n")

    print(f"Successfully filtered to {output_path}")

if __name__ == "__main__":
    filter_notes()
