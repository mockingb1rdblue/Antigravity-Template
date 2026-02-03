import os
import argparse

def format_size(size_bytes):
    """Formats bytes to MB with 2 decimal places."""
    return f"{size_bytes / (1024 * 1024):.2f} MB"

def get_file_size_info(base_dir):
    file_info = []
    total_size = 0
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                total_size += size
                # Relative path for display
                rel_path = os.path.relpath(file_path, base_dir)
                file_info.append((rel_path, size))
            except OSError:
                pass # Skip files we can't access
            
    # Sort by size descending
    file_info.sort(key=lambda x: x[1], reverse=True)
    return total_size, file_info

def generate_report(target_dir, threshold_mb, output_file):
    if not os.path.exists(target_dir):
        print(f"Error: Directory not found: {target_dir}")
        return

    total_bytes, files = get_file_size_info(target_dir)
    total_mb = total_bytes / (1024 * 1024)
    
    # Header logic
    status_icon = "✅" if total_mb <= threshold_mb else "⚠️"
    status_text = "WITHIN LIMIT" if total_mb <= threshold_mb else f"OVER LIMIT ({threshold_mb}MB)"
    
    content = []
    content.append(f"# {status_icon} Folder Size Report: {total_mb:.2f} MB ({status_text})\n")
    content.append(f"**Target**: `{target_dir}`\n")
    
    if total_mb > threshold_mb:
        content.append("> [!WARNING]")
        content.append(f"> Total size receives the {threshold_mb} MB threshold.")
    else:
        content.append(f"> [!TIP]")
        content.append(f"> Total size is within the {threshold_mb} MB threshold.")

    content.append("\n## File Breakdown (Descending Size)\n")
    content.append("| File Name | Size (MB) | Size (KB) |")
    content.append("| :--- | :--- | :--- |")
    
    for name, size in files:
        mb_size = size / (1024 * 1024)
        kb_size = size / 1024
        # Stop seeing tiny files in the list if desired, but for now list all
        content.append(f"| `{name}` | **{mb_size:.2f}** | {kb_size:.0f} |")
        
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
        print(f"Report generated: {output_file}")
    else:
        print("\n".join(content))

    print(f"Total Size: {total_mb:.2f} MB")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate folder size and generate report")
    parser.add_argument("target_dir", help="Directory to analyze")
    parser.add_argument("--threshold", type=float, default=25.0, help="Size warning threshold in MB (default: 25.0)")
    parser.add_argument("--output", help="Path to save markdown report (optional)")
    
    args = parser.parse_args()
    
    generate_report(args.target_dir, args.threshold, args.output)
