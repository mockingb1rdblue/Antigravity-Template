import os
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

# Use absolute path or relative to project root
BRAIN_DIR = Path("docs/brain")

def get_date_range(folder_path):
    mtimes = []
    # Scan all files recursively
    for item in folder_path.rglob('*'):
        if item.is_file() and not item.name.startswith('.'):
            try:
                mtimes.append(item.stat().st_mtime)
            except OSError:
                continue
            
    if not mtimes:
        return None, None
        
    min_ts = min(mtimes)
    max_ts = max(mtimes)
    
    start_dt = datetime.fromtimestamp(min_ts)
    end_dt = datetime.fromtimestamp(max_ts)
    
    return start_dt, end_dt

def extract_project(folder_path, current_name):
    # Scan files for "file:///Users/mock1ng/Documents/Projects/Antigravity-Github/([^/]+)/"
    project_regex = re.compile(r'file:///Users/mock1ng/Documents/Projects/Antigravity-Github/([^/]+)/')
    
    counts = {}
    
    # Limit scan to .md and .json files to be fast and relevant
    for item in folder_path.rglob('*'):
        if item.is_file() and item.suffix in ['.md', '.json']:
            try:
                with open(item, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    matches = project_regex.findall(content)
                    for m in matches:
                        counts[m] = counts.get(m, 0) + 1
            except Exception:
                continue
    
    if counts:
        # Return most frequent project
        return max(counts, key=counts.get)
        
    return None

def extract_title(folder_path, current_name):
    # 1. Try task.md
    task_file = folder_path / "task.md"
    if task_file.exists():
        try:
            with open(task_file, "r") as f:
                first_line = f.readline().strip()
                # Remove markdown headers and whitespace
                clean_line = re.sub(r'^#+\s*', '', first_line)
                if clean_line:
                    return clean_line
        except Exception:
             pass
    
    # 2. Try parsing current name
    clean_name = current_name
    
    # Regex for YYYY-MM-DD
    date_re = r'\d{4}-\d{2}-\d{2}'
    time_re = r'\d{4}'
    
    # Check range with times
    match = re.match(f"^{date_re}_{time_re}_to_{time_re}_(.+)", current_name)
    if match: clean_name = match.group(1)
    else:
        # Check range dates
        match = re.match(f"^{date_re}_to_{date_re}_(.+)", current_name)
        if match: clean_name = match.group(1)
        else:
            # Check single date
            match = re.match(f"^{date_re}_(.+)", current_name)
            if match: clean_name = match.group(1)

    if len(clean_name) == 36 and clean_name.count('-') >= 4:
         return "Untitled"

    return clean_name

def sanitize_name(name):
    # Replace non-alphanumeric with _
    clean = re.sub(r'[^a-zA-Z0-9]', '_', name)
    # Remove duplicate underscores
    clean = re.sub(r'_+', '_', clean)
    return clean.strip('_')

def organize():
    if not BRAIN_DIR.exists():
        print(f"Directory {BRAIN_DIR} does not exist.")
        return

    print("Organizing brain folders...")

    # Iterate over directories
    items = [item for item in BRAIN_DIR.iterdir() if item.is_dir()]
    
    for item in items:
        start_dt, end_dt = get_date_range(item)
        
        if not start_dt:
            print(f"Skipping empty/no-file folder: {item.name}")
            continue

        project = extract_project(item, item.name)
        raw_title = extract_title(item, item.name)
        
        # Avoid duplicating project name in title
        if project:
            p_clean = sanitize_name(project)
            t_clean = sanitize_name(raw_title)
            # Check if title starts with project (case insensitive)
            if t_clean.lower().startswith(p_clean.lower()):
                # Remove project prefix from title title
                # We need to remove it from raw_title, dealing with underscores
                # Simple approach: remove the first len(project) + delimiters chars
                raw_title = re.sub(f"^{re.escape(project)}[_ ]?", "", raw_title, flags=re.IGNORECASE)
                raw_title = re.sub(f"^{re.escape(p_clean)}[_ ]?", "", raw_title, flags=re.IGNORECASE)

        sanitized_title = sanitize_name(raw_title)
        if not sanitized_title: sanitized_title = "Untitled"
        
        # Format logic
        start_date_str = start_dt.strftime("%Y-%m-%d")
        end_date_str = end_dt.strftime("%Y-%m-%d")
        
        if start_date_str == end_date_str:
            # Same day: Include times
            start_time_str = start_dt.strftime("%H%M")
            end_time_str = end_dt.strftime("%H%M")
            
            # YYYY-MM-DD_HHMM_to_HHMM
            date_prefix = f"{start_date_str}_{start_time_str}_to_{end_time_str}"
        else:
            # Different days
            date_prefix = f"{start_date_str}_to_{end_date_str}"
            
        if project:
            sanitized_project = sanitize_name(project)
            new_folder_name = f"{date_prefix}_{sanitized_project}_{sanitized_title}"
        else:
            new_folder_name = f"{date_prefix}_{sanitized_title}"
        
        # Skip if already named correctly
        if item.name == new_folder_name:
            continue
            
        target_path = BRAIN_DIR / new_folder_name
        
        print(f"Processing {item.name} -> {new_folder_name}")
        
        if target_path.exists():
            if target_path == item:
                continue
                
            print(f"  Target {target_path} exists. Merging...")
            # Merge item content into target_path
            for file in item.iterdir():
                dest_file = target_path / file.name
                if dest_file.exists():
                    if dest_file.is_dir():
                        shutil.rmtree(dest_file)
                    else:
                        os.remove(dest_file)
                
                shutil.move(str(file), str(dest_file))
            
            try:
                item.rmdir() 
            except OSError:
                shutil.rmtree(item)
            print("  Merged and removed source.")
        else:
            print(f"  Renaming to {new_folder_name}")
            item.rename(target_path)

if __name__ == "__main__":
    organize()
