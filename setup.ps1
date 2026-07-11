# Quick setup script for kenojose.site (PowerShell version)

# Unicode characters defined programmatically to avoid encoding/BOM issues
$CheckMark = [char]0x2713
$CrossMark = [char]0x2717

# Colors for output
$Green = "Green"
$Blue = "Cyan"
$Yellow = "Yellow"

Write-Host "=== kenojose.site Quick Setup ===" -ForegroundColor $Blue
Write-Host ""

# Check structure
Write-Host "Checking directory structure..."
if ((Test-Path "index.html" -PathType Leaf) -and (Test-Path "blog.html" -PathType Leaf) -and (Test-Path "css/style.css" -PathType Leaf)) {
    Write-Host "$CheckMark All files present" -ForegroundColor $Green
} else {
    Write-Host "$CrossMark Missing files. Run setup first." -ForegroundColor Red
    exit 1
}

# Check asset directory
if (-not (Test-Path "assets" -PathType Container)) {
    New-Item -ItemType Directory -Path "assets" -Force | Out-Null
    Write-Host "$CheckMark Created assets directory" -ForegroundColor $Green
} else {
    Write-Host "$CheckMark Assets directory exists" -ForegroundColor $Green
}

# Check avatar
if (-not (Test-Path "assets/avatar.png" -PathType Leaf)) {
    Write-Host "Note: Add your avatar to assets/avatar.png" -ForegroundColor $Yellow
} else {
    Write-Host "$CheckMark Avatar found" -ForegroundColor $Green
}

# Check/download marked.min.js
if (-not (Test-Path "js/marked.min.js" -PathType Leaf)) {
    Write-Host "Downloading marked.min.js for offline markdown rendering..." -ForegroundColor $Yellow
    if (-not (Test-Path "js" -PathType Container)) {
        New-Item -ItemType Directory -Path "js" -Force | Out-Null
    }
    try {
        Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/marked/marked.min.js" -OutFile "js/marked.min.js" -TimeoutSec 10
        Write-Host "$CheckMark Downloaded marked.min.js" -ForegroundColor $Green
    } catch {
        Write-Host "$CrossMark Failed to download marked.min.js. Please download manually or ensure internet connection." -ForegroundColor Red
    }
} else {
    Write-Host "$CheckMark Local copy of marked.min.js found" -ForegroundColor $Green
}

# Generate blog index
Write-Host "Generating blog index..."
if (Get-Command "python" -ErrorAction SilentlyContinue) {
    python generate_blog_index.py
} elseif (Get-Command "python3" -ErrorAction SilentlyContinue) {
    python3 generate_blog_index.py
} else {
    Write-Host "$CrossMark Python was not found in your PATH. Could not run generate_blog_index.py." -ForegroundColor Red
}

# Offer to start server
Write-Host ""
Write-Host "Ready to test locally?"
$reply = Read-Host "Start HTTP server on port 8000? (y/n)"
if ($reply -match "^[Yy]$" -or $reply -match "^[Yy]es$") {
    Write-Host "Starting server..." -ForegroundColor $Blue
    Write-Host "Visit http://localhost:8000"
    
    # Check if python or python3 is available
    if (Get-Command "python" -ErrorAction SilentlyContinue) {
        python -m http.server 8000
    } elseif (Get-Command "python3" -ErrorAction SilentlyContinue) {
        python3 -m http.server 8000
    } else {
        Write-Host "Error: Python was not found in your PATH." -ForegroundColor Red
    }
}
