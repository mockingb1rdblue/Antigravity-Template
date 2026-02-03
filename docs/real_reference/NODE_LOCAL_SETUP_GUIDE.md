# Local Node.js Setup Guide (Non-Admin / OneDrive Optimized)

This document details the process for establishing a fully functional Node.js environment (`node`, `npm`, `npx`) within the project root, specifically tailored for environments without administrator privileges and where OneDrive synchronization can cause severe performance issues.

## The Challenge

1.  **No Admin Rights**: Unable to install Node.js via standard MSI installers.
2.  **OneDrive Performance**: The standard PowerShell `Expand-Archive` cmdlet is incredibly slow on OneDrive-synced folders. It triggers a synthesis event for every single file in the `node_modules` or binary structure, causing the extraction to hang or take hours.
3.  **Path Pollution**: Adding to the global `%PATH%` can be messy or restricted.

## The Solution

We implement a **portable, local-only** Node.js installation contained entirely within the project directory.

### Key Components

1.  **Location**: `.node/` directory in the project root (git-ignored).
2.  **Method**: Direct download of the Windows binary (`.zip`).
3.  **Optimization**: **Crucial Step** - We use .NET's `System.IO.Compression.ZipFile` class via PowerShell instead of `Expand-Archive`. This bypasses the filesystem overhead that chokes OneDrive.

## Implementation Details

### 1. The Setup Script (`scripts/setup_node.ps1`)

This script automates the entire process.

**Core Logic:**
```powershell
# Load .NET Assembly for fast unzipping
Add-Type -AssemblyName System.IO.Compression.FileSystem

# ... download setup ...

# Extract using .NET (Fast) instead of Expand-Archive (Slow)
[System.IO.Compression.ZipFile]::ExtractToDirectory($ZipPath, $NodeDir)
```

### 2. The Launcher (`nodeenv.bat`)

A batch file created in the project root acts as the entry point. It sets the environment variables *only for that session*.

```batch
@echo off
set "NODE_HOME=%~dp0.node\node-v20.11.0-win-x64"
set "PATH=%NODE_HOME%;%PATH%"
cmd /k
```

## How to Replicate

To replicate this setup in another project or environment:

1.  **Copy the Script**: Copy `scripts/setup_node.ps1` to the new project.
2.  **Run with Bypass**: Execute the script using PowerShell.
    ```powershell
    powershell -ExecutionPolicy Bypass -File scripts/setup_node.ps1
    ```
3.  **Use**: A `nodeenv.bat` file will be generated. Double-click it to start working.

## Troubleshooting

-   **"Script cannot be loaded"**: Ensure you run with `-ExecutionPolicy Bypass`.
-   **Extraction Hangs**: If you revert to `Expand-Archive`, it will hang on OneDrive. Ensure the .NET method is preserved.
-   **Old Versions**: The script deletes previous partial extractions in `.node/` before starting to ensure a clean slate.
