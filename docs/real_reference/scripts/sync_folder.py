import os
import shutil
import json
import argparse

def load_config(config_file):
    """
    Loads sync configuration.
    Expected Format:
    {
        "categories": [
            { "name": "Folder Name", "rules": ["keyword1", "keyword2"] },
            { "name": "ROOT", "rules": ["keyword3"] } 
        ],
        "ignore": ["private", "draft"]
    }
    """
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_category(filename, config):
    name = filename.lower()
    
    # Check ignore list first
    for ignore_kw in config.get("ignore", []):
        if ignore_kw.lower() in name:
            return None

    # Check categories
    for category in config.get("categories", []):
        folder_name = category["name"]
        rules = category.get("rules", [])
        
        for rule in rules:
            if rule.lower() in name:
                return folder_name
                
    # Default behavior? Could return "Unsorted" or None
    return None

def sync_folder(source_dir, dest_dir, config_file, dry_run=False):
    config = load_config(config_file)
    print(f"Syncing '{source_dir}' -> '{dest_dir}' using '{config_file}'")
    
    files_copied = 0
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # Determine destination category
            category = get_category(file, config)
            
            if category is None:
                continue # Ignored or not matched

            # Resolve destination path
            if category == "ROOT":
                target_folder = dest_dir
            else:
                target_folder = os.path.join(dest_dir, category)
            
            target_file = os.path.join(target_folder, file)
            source_file = os.path.join(root, file)

            # Check if copy needed
            should_copy = False
            if not os.path.exists(target_file):
                should_copy = True
            elif os.path.getmtime(source_file) > os.path.getmtime(target_file):
                should_copy = True
            
            if should_copy:
                print(f"[{category}] Copying: {file}")
                if not dry_run:
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    shutil.copy2(source_file, target_file)
                files_copied += 1

    print(f"Sync complete. {files_copied} files processed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync files with categorization rules")
    parser.add_argument("source_dir", help="Source directory")
    parser.add_argument("dest_dir", help="Destination directory")
    parser.add_argument("config_file", help="JSON configuration file")
    parser.add_argument("--dry-run", action="store_true", help="Simulate sync")
    
    args = parser.parse_args()
    sync_folder(args.source_dir, args.dest_dir, args.config_file, args.dry_run)
