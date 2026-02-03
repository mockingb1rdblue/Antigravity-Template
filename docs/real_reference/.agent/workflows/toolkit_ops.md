---
description: Auto-run common Documentation Toolkit scripts
---

# Toolkit Operations

// turbo-all

This workflow allows you to run common toolkit maintenance scripts without manual approval for every command.

## 1. Check Package Size
Run this to see if the Exhibits folder is under the email limit.
`ash
python scripts/check_size.py "EXHIBITS"
`

## 2. Sync Exhibits
Run this to update the exhibits from originals.
`ash
python scripts/sync_exhibits.py
`

## 3. Extract Pages from PDF
Template command to extract pages. Replace [PDF_PATH] and [PAGES].
`ash
python scripts/extract_pages.py "[PDF_PATH]" --pages "[PAGES]"
`

## 4. Highlight PDF
Template command to highlight text. Replace [PDF_PATH] and [TEXT].
`ash
python scripts/highlight_pdf.py "[PDF_PATH]" "[TEXT]"
`

## 5. Batch Rename
Run the batch renamer on a target directory.
`ash
python scripts/batch_rename.py "EXHIBITS" "rename_map.json" --dry-run
`

