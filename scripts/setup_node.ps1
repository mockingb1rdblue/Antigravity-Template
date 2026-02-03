$ErrorActionPreference = "Stop"

$NodeVersion = "v20.11.0"
$NodeDist = "node-$NodeVersion-win-x64"
$ZipName = "$NodeDist.zip"
$Url = "https://nodejs.org/dist/$NodeVersion/$ZipName"

$ProjectRoot = Resolve-Path "$PSScriptRoot\.."
$NodeDir = Join-Path $ProjectRoot ".node"
$ZipPath = Join-Path $NodeDir $ZipName
$ExtractedPath = Join-Path $NodeDir $NodeDist

Write-Host "Setting up Node.js $NodeVersion in $NodeDir..."

# 1. Create directory
if (-not (Test-Path $NodeDir)) {
    New-Item -ItemType Directory -Path $NodeDir | Out-Null
    Write-Host "Created .node directory."
}

# 2. Download
if (-not (Test-Path $ZipPath)) {
    Write-Host "Downloading $Url..."
    Invoke-WebRequest -Uri $Url -OutFile $ZipPath
    Write-Host "Download complete."
}

# 3. Optimize Extraction (Cleanup & .NET ZipFile)
if (-not (Test-Path $ExtractedPath)) {
    # Check for partial extraction and remove
    if (Test-Path "$ExtractedPath") { 
        Write-Host "Cleaning up partial extraction..."
        Remove-Item "$ExtractedPath" -Recurse -Force 
    }

    Write-Host "Extracting to $NodeDir (using .NET API for speed)..."
    try {
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        [System.IO.Compression.ZipFile]::ExtractToDirectory($ZipPath, $NodeDir)
        Write-Host "Extraction complete."
    }
    catch {
        Write-Error "Extraction failed: $_"
        exit 1
    }
}
else {
    Write-Host "Node.js already extracted."
}

# 4. Create Launcher
$LauncherPath = Join-Path $ProjectRoot "nodeenv.bat"

$BatchContent = @"
@echo off
set "NODE_HOME=%~dp0.node\$NodeDist"
set "PATH=%NODE_HOME%;%PATH%"
echo Node.js environment initialized.
echo Node: %NODE_HOME%
cmd /k
"@

Set-Content -Path $LauncherPath -Value $BatchContent
Write-Host "Created launcher at $LauncherPath"

Write-Host "Setup complete! Run nodeenv.bat to start."
