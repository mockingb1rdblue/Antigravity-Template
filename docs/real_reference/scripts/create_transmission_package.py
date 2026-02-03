#!/usr/bin/env python3
"""
Universal Zip Packaging Script
Creates standard zip archive compatible with Windows/macOS/Linux native tools
"""

import zipfile
import os
from datetime import datetime

def create_transmission_package():
    """
    Create universal zip package of transmission bundle
    """
    # Configuration
    source_folder = "10_TRANSMISSION_BUNDLE"
    output_filename = "Scheurer_v_Vestas_Pre-Mediation_Package_2026-01-29.zip"
    
    print("\n" + "="*60)
    print("CREATING TRANSMISSION PACKAGE")
    print("="*60 + "\n")
    
    if not os.path.exists(source_folder):
        print(f"ERROR: Source folder '{source_folder}' not found")
        return False
    
    # Create zip file
    print(f"Source: {source_folder}/")
    print(f"Output: {output_filename}\n")
    
    file_count = 0
    total_size = 0
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        # Walk through all files in source folder
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(source_folder))
                
                # Add file to zip
                zipf.write(file_path, arcname)
                file_size = os.path.getsize(file_path)
                total_size += file_size
                file_count += 1
                
                print(f"  [OK] Added: {arcname} ({file_size:,} bytes)")
    
    # Get final zip size
    zip_size = os.path.getsize(output_filename)
    compression_ratio = (1 - zip_size / total_size) * 100 if total_size > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"PACKAGE CREATED SUCCESSFULLY")
    print(f"{'='*60}")
    print(f"Files: {file_count}")
    print(f"Uncompressed: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)")
    print(f"Compressed: {zip_size:,} bytes ({zip_size / 1024 / 1024:.2f} MB)")
    print(f"Compression: {compression_ratio:.1f}%")
    print(f"Location: {os.path.abspath(output_filename)}")
    print(f"{'='*60}\n")
    
    # Verify zip integrity
    print("Verifying zip integrity...")
    try:
        with zipfile.ZipFile(output_filename, 'r') as zipf:
            bad_file = zipf.testzip()
            if bad_file:
                print(f"  [ERROR] Corrupted file in archive: {bad_file}")
                return False
            else:
                print(f"  [OK] Zip integrity verified - all files OK\n")
    except Exception as e:
        print(f"  [ERROR] Verification failed: {e}\n")
        return False
    
    print("="*60)
    print("COMPATIBILITY TESTING")
    print("="*60)
    print("This zip can be opened with:")
    print("  - Windows: Right-click -> 'Extract All'")
    print("  - macOS: Double-click (Archive Utility)")
    print("  - Linux: unzip command")
    print("  - No special software required\n")
    
    return True

if __name__ == "__main__":
    success = create_transmission_package()
    exit(0 if success else 1)
