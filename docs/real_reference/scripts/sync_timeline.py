import re
import os

MARKDOWN_PATH = r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\EXHIBITS\Exhibit B - Timeline\Exhibit B - Financial Strangulation Timeline.md"
HTML_PATH = r"C:\Users\ad9840724\OneDrive - Nutrien\Documents\My Role\04_MEDIA_STRATEGY\Docs\260126_Mediation_Strategy\EXHIBITS\Exhibit B - Timeline\Exhibit B - Financial Strangulation Timeline.html"

def parse_markdown_table(md_content):
    """
    Extracts table rows from the markdown file.
    Returns a list of dicts: {Date, Event, Source, Significance}
    """
    table_regex = re.compile(r"^\| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$", re.MULTILINE)
    rows = []
    
    lines = md_content.splitlines()
    start_parsing = False
    
    for line in lines:
        if line.strip().startswith("| Date | Event |"):
            start_parsing = True
            continue
        if not start_parsing:
            continue
        if line.strip().startswith("| :---"):
            continue
        
        match = table_regex.match(line)
        if match:
            date = match.group(1).strip().replace("**", "") # simplistic bold removal
            event = match.group(2).strip().replace("**", "")
            source = match.group(3).strip().replace("`", "")
            significance = match.group(4).strip().replace("**", "").replace("*", "") # simplistic formatting removal
            
            rows.append({
                "date": date,
                "event": event,
                "source": source,
                "significance": significance
            })
    return rows

def update_html(html_content, rows):
    """
    This is a placeholder. A full implementation would require robust HTML parsing 
    or a templating engine (Jinja2) to reliably replace the table body 
    without destroying the custom CSS classes/styles (like .smoking-gun).
    
    For now, this script serves as a foundational step. Implementing 
    full automated sync without destroying manual HTML styling is complex 
    and risks breaking the 'beautiful' layout.
    
    Recommendation: Use a template system if full automation is desired.
    """
    print("Parsing successful. Identifed {} rows in Markdown.".format(len(rows)))
    print("NOTE: Full HTML injection is disabled to protect manual styling.")
    print("Please manually verify parity for now.")
    return html_content

def main():
    if not os.path.exists(MARKDOWN_PATH):
        print(f"Error: Markdown file not found at {MARKDOWN_PATH}")
        return

    with open(MARKDOWN_PATH, 'r', encoding='utf-8') as f:
        md_content = f.read()

    rows = parse_markdown_table(md_content)
    
    print("--- Extracted Breakdown ---")
    for row in rows:
        print(f"{row['date']}: {row['event']}")

if __name__ == "__main__":
    main()
