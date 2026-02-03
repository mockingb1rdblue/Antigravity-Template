$AgentDir = ".agent"
$WorkflowsDir = Join-Path $AgentDir "workflows"

# Ensure directories exist
if (-not (Test-Path $WorkflowsDir)) {
    New-Item -ItemType Directory -Path $WorkflowsDir -Force | Out-Null
    Write-Host "Created $WorkflowsDir"
}

# 1. PIP Operations Workflow
$PipOpsContent = @"
---
description: Auto-run pip install commands
---

# PIP Operations

// turbo-all

This workflow allows you to run pip commands without manual approval.

## Install Packages
```bash
pip install [packages]
```

## Install from Requirements
```bash
pip install -r requirements.txt
```

## Upgrade PIP
```bash
python -m pip install --upgrade pip
```
"@

$PipOpsFile = Join-Path $WorkflowsDir "pip_ops.md"
Set-Content -Path $PipOpsFile -Value $PipOpsContent -Encoding UTF8
Write-Host "Created $PipOpsFile"

# 2. Toolkit Operations Workflow
$ToolkitOpsContent = @"
---
description: Auto-run common Documentation Toolkit scripts
---

# Toolkit Operations

// turbo-all

This workflow allows you to run common toolkit maintenance scripts without manual approval for every command.

## 1. Check Package Size
Run this to see if the Exhibits folder is under the email limit.
```bash
python scripts/check_size.py "EXHIBITS"
```

## 2. Sync Exhibits
Run this to update the exhibits from originals.
```bash
python scripts/sync_exhibits.py
```

## 3. Extract Pages from PDF
Template command to extract pages. Replace [PDF_PATH] and [PAGES].
```bash
python scripts/extract_pages.py "[PDF_PATH]" --pages "[PAGES]"
```

## 4. Highlight PDF
Template command to highlight text. Replace [PDF_PATH] and [TEXT].
```bash
python scripts/highlight_pdf.py "[PDF_PATH]" "[TEXT]"
```

## 5. Batch Rename
Run the batch renamer on a target directory.
```bash
python scripts/batch_rename.py "EXHIBITS" "rename_map.json" --dry-run
```
"@

$ToolkitOpsFile = Join-Path $WorkflowsDir "toolkit_ops.md"
Set-Content -Path $ToolkitOpsFile -Value $ToolkitOpsContent -Encoding UTF8
Write-Host "Created $ToolkitOpsFile"

Write-Host "`nSUCCESS: Auto-approval workflows created."
Write-Host "Copy this script to any new project and run it to enable these permissions instantly."
