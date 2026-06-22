## setup_datasets.ps1 - Download all required datasets for UserHealthMonitor
# ---------------------------------------------------------------
# Usage:  Open PowerShell, navigate to the project root (d:\Research\UserHealthMonitor) and run:
#         .\setup_datasets.ps1
# ---------------------------------------------------------------

# ---- Helper Functions ----------------------------------------------------
function Ensure-Dir([string]$path) {
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Force -Path $path | Out-Null
    }
}

function Download-Url([string]$url, [string]$destFile) {
    Write-Host "Downloading $url ..."
    try {
        Invoke-WebRequest -Uri $url -OutFile $destFile -UseBasicParsing
    } catch {
        Write-Error "Failed to download $url : $_"
    }
}

function Unzip-IfZip([string]$zipPath, [string]$target) {
    if ($zipPath -like "*.zip") {
        Write-Host "Extracting $zipPath to $target"
        Expand-Archive -Path $zipPath -DestinationPath $target -Force
        Remove-Item $zipPath -Force
    }
}

# ---- Define project layout ------------------------------------------------
$PROJECT_ROOT = "d:\Research\UserHealthMonitor"
$RAW_ROOT = Join-Path $PROJECT_ROOT "dataset\raw"

# Ensure all raw sub‑folders exist
@("posture", "eye", "lighting", "behaviour") | ForEach-Object { Ensure-Dir (Join-Path $RAW_ROOT $_) }

# ---- 1️⃣ MultiPosture (Zenodo) --------------------------------------------
$mpUrl = "https://zenodo.org/records/14230872/files/data.csv?download=1"
$mpDest = Join-Path (Join-Path $RAW_ROOT "posture") "data.csv"
Download-Url $mpUrl $mpDest

# ---- 2️⃣ Kaggle datasets ---------------------------------------------------
# NOTE: You need the Kaggle CLI installed and a valid API token at %USERPROFILE%\.kaggle\kaggle.json
$kaggleDatasets = @(
    @{ ds = "pandu301/sitting-posture-detect";      out = "posture" },
    @{ ds = "ismailnasri20/driver-drowsiness-dataset-ddd"; out = "eye" },
    @{ ds = "dheerajperumandla/drowsiness-dataset";   out = "eye" },
    @{ ds = "soumikrakshit/lol-dataset";               out = "lighting" },
    @{ ds = "valakhorasani/gym-members-exercise-dataset"; out = "behaviour" },
    @{ ds = "uciml/posture-reconstruction";            out = "behaviour" }
)

foreach ($item in $kaggleDatasets) {
    $dest = Join-Path $RAW_ROOT $item.out
    Write-Host "Downloading Kaggle dataset $($item.ds) → $dest"
    kaggle datasets download -d $item.ds -p $dest --unzip
}

# ---- 3️⃣ Roboflow (manual step) ------------------------------------------
Write-Host "\n=== MANUAL STEP REQUIRED ==="
Write-Host "Visit the following URL, create a free Roboflow account (if needed),"
Write-Host "download the ZIP for \"Posture Correction v4\" and unzip it into:"
Write-Host (Join-Path $RAW_ROOT "posture")
Write-Host "URL: https://universe.roboflow.com/posturecorrection/posture_correction_v4"

# ---- 4️⃣ ExDark (Git clone) ------------------------------------------------
$exDarkDir = Join-Path $RAW_ROOT "lighting\ExDark"
if (-not (Test-Path $exDarkDir)) {
    Write-Host "Cloning ExDark low‑light dataset..."
    git clone https://github.com/cs-chan/Exclusively-Dark-Image-Dataset.git $exDarkDir
}

Write-Host "\nAll automated downloads complete. Verify the folders under $RAW_ROOT.\n"
