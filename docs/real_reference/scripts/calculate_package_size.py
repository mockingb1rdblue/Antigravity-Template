import os

def format_size(size_bytes):
    """Formats bytes to MB with 2 decimal places."""
    return f"{size_bytes / (1024 * 1024):.2f} MB"

def get_file_size_info(base_dir):
    file_info = []
    total_size = 0
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            total_size += size
            
            # Relative path for display
            rel_path = os.path.relpath(file_path, base_dir)
            file_info.append((rel_path, size))
            
    # Sort by size descending
    file_info.sort(key=lambda x: x[1], reverse=True)
    return total_size, file_info

def generate_report():
    base_dir = os.getcwd()
    exhibits_dir = os.path.join(base_dir, "99_SEND_PRE-MEE", "03_Exhibits_Bundle")
    report_path = os.path.join(base_dir, "02_PRE_MEDIATION_PACKAGE_SIZE.md")
    
    if not os.path.exists(exhibits_dir):
        print(f"Directory not found: {exhibits_dir}")
        return

    total_bytes, files = get_file_size_info(exhibits_dir)
    total_mb = total_bytes / (1024 * 1024)
    limit_mb = 25.0
    
    # Header logic
    status_icon = "✅" if total_mb <= limit_mb else "⚠️"
    status_text = "READY TO SEND" if total_mb <= limit_mb else "OVER LIMIT (25MB)"
    
    content = []
    content.append(f"# {status_icon} Total Package Size: {total_mb:.2f} MB ({status_text})\n")
    
    if total_mb > limit_mb:
        content.append("> [!WARNING]")
        content.append(f"> The total size ({total_mb:.2f} MB) exceeds the standard email attachment limit of 25 MB.")
        content.append("> **Note**: ZIP compression often provides minimal reduction for PDF files. You may need to split the email or use a download link.\n")
    else:
        content.append(f"> [!TIP]")
        content.append(f"> The total size ({total_mb:.2f} MB) is within the safe send limit of 25 MB.\n")

    content.append("## File Breakdown (Descending Size)\n")
    content.append("| File Name | Size (MB) | Size (KB) |")
    content.append("| :--- | :--- | :--- |")
    
    for name, size in files:
        mb_size = size / (1024 * 1024)
        kb_size = size / 1024
        content.append(f"| `{name}` | **{mb_size:.2f}** | {kb_size:.0f} |")
        
    content.append(f"\n_Generated on {os.popen('date /t').read().strip()}_")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
        
    print(f"Report generated: {report_path}")
    print(f"Total Size: {total_mb:.2f} MB")

if __name__ == "__main__":
    generate_report()
