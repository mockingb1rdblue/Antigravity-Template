import os
import json
import csv
import argparse

def load_mapping(mapping_file):
    """Loads mapping from JSON or CSV."""
    mapping = {}
    if mapping_file.endswith('.json'):
        with open(mapping_file, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
    elif mapping_file.endswith('.csv'):
        with open(mapping_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    mapping[row[0].strip().lower()] = row[1].strip()
    return mapping

def batch_rename(target_dir, mapping_file, dry_run=False):
    """Renames files in target_dir based on mapping_file."""
    mapping = load_mapping(mapping_file)
    # Ensure mapping keys are lowercase for case-insensitive matching
    mapping = {k.lower(): v for k, v in mapping.items()}
    
    print(f"Loaded {len(mapping)} renaming rules.")
    if dry_run:
        print("--- DRY RUN MODE ---")

    count = 0
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            lower_name = file.lower()
            if lower_name in mapping:
                new_name = mapping[lower_name]
                if file == new_name:
                    continue # Already named correctly
                    
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_name)
                
                print(f"Rename: '{file}' -> '{new_name}'")
                
                if not dry_run:
                    try:
                        os.rename(old_path, new_path)
                        count += 1
                    except Exception as e:
                        print(f"  Error: {e}")
                else:
                    count += 1
    
    print(f"Processed {count} files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch rename files based on a mapping")
    parser.add_argument("target_dir", help="Directory to scan")
    parser.add_argument("mapping_file", help="JSON or CSV file containing 'old_name' -> 'new_name' mapping")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without renaming")
    
    args = parser.parse_args()
    batch_rename(args.target_dir, args.mapping_file, args.dry_run)
