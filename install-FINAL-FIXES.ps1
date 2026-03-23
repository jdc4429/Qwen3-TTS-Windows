Param (
    [Parameter(Mandatory=$true)][ValidateSet("CU124", "CU126", "CU128", "CU130", "CPU")][string]$Device,
    [Parameter(Mandatory=$true)][ValidateSet("HF", "HF-Mirror", "ModelScope")][string]$Source,
    [switch]$DownloadUVR5
)
$global:ErrorActionPreference = 'Stop'
#$env:PYTHONWARNINGS = "ignore"

function Write-ErrorLog {
    param (
        [System.Management.Automation.ErrorRecord]$ErrorRecord
    )
    Write-Host "`n[ERROR] Command failed:" -ForegroundColor Red
    if (-not $ErrorRecord.Exception.Message){
    } else {
        Write-Host "Message:" -ForegroundColor Red 
        $ErrorRecord.Exception.Message -split "`n" | ForEach-Object {
            Write-Host "    $_"
        }
    }
    Write-Host "Command:" -ForegroundColor Red  -NoNewline
    Write-Host " $($ErrorRecord.InvocationInfo.Line)".Replace("`r", "").Replace("`n", "")
    Write-Host "Location:" -ForegroundColor Red -NoNewline
    Write-Host " $($ErrorRecord.InvocationInfo.ScriptName):$($ErrorRecord.InvocationInfo.ScriptLineNumber)"
    Write-Host "Call Stack:" -ForegroundColor DarkRed
    $ErrorRecord.ScriptStackTrace -split "`n" | ForEach-Object {
        Write-Host "    $_" -ForegroundColor DarkRed
    }

    exit 1
}
trap {
    $msg = $_.Exception.Message
    if ($msg -match "FutureWarning|DeprecationWarning|free.*channel") {
        continue
    }
    Write-ErrorLog $_
}
function Write-Info($msg) {
    Write-Host "[INFO]:" -ForegroundColor Green -NoNewline
    Write-Host " $msg"
}
function Write-Success($msg) {
    Write-Host "[SUCCESS]:" -ForegroundColor Blue -NoNewline
    Write-Host " $msg"
}
function Test-ZipValid {
    param([string]$Path)
    try {
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        $zip = [System.IO.Compression.ZipFile]::OpenRead($Path)
        $zip.Dispose()
        return $true
    } catch {
        return $false
    }
}
function Invoke-Conda {
    param (
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Args
    )

    & conda install -y -c conda-forge $Args
}
function Invoke-Pip {
    param (
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Args
    )
    $output = & pip install @Args 2>&1
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne 0) {
        $errorMessages = @()
        Write-Host "Pip Install $Args Failed" -ForegroundColor Red
        foreach ($item in $output) {
            if ($item -is [System.Management.Automation.ErrorRecord]) {
                $msg = $item.Exception.Message
                Write-Host "$msg" -ForegroundColor Red
                $errorMessages += $msg
            }
            else {
                Write-Host $item
                $errorMessages += $item
            }
        }
        throw [System.Exception]::new(($errorMessages -join "`n"))
    }
}
function Invoke-Download {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Uri,

        [Parameter()]
        [string]$OutFile
    )
    try {
        if ($OutFile -and (Test-Path $OutFile)) {
            $isZip = $OutFile -match "\.zip$"
            $isTar = $OutFile -match "\.tar\.gz$"
            if ($isZip -and -not (Test-ZipValid $OutFile)) {
                Write-Info "Removing corrupt/incomplete zip: $OutFile"
                Remove-Item $OutFile -Force
            } elseif ($isZip -and (Test-ZipValid $OutFile)) {
                Write-Info "$OutFile already exists and is valid, skipping download"
                return
            } elseif ($isTar) {
                Write-Info "Removing existing tar.gz to ensure clean download: $OutFile"
                Remove-Item $OutFile -Force
            }
        }
        $params = @{ Uri = $Uri }
        if ($OutFile) { $params["OutFile"] = $OutFile }
        $null = Invoke-WebRequest @params -ErrorAction Stop
    } catch {
        Write-Host "Failed to download:" -ForegroundColor Red
        Write-Host "  $Uri"
        throw
    }
}
function Invoke-Unzip {
    param($ZipPath, $DestPath)
    Expand-Archive -Path $ZipPath -DestinationPath $DestPath -Force
    Remove-Item $ZipPath -Force
}
chcp 65001
if ($PSScriptRoot) { Set-Location $PSScriptRoot }
Write-Info "Installing QWEN-TTS..."
Invoke-Pip -U qwen-tts
Write-Success "Installed QWEN-TTS"
switch ($Device) {
    "CU124" {
        Write-Info "Installing PyTorch For CUDA 12.4..."
        Invoke-Pip torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url "https://download.pytorch.org/whl/cu124"
    }
    "CU126" {
        Write-Info "Installing PyTorch For CUDA 12.6..."
        Invoke-Pip torch==2.10.0 torchvision==0.25.0 torchaudio==2.10.0 --index-url "https://download.pytorch.org/whl/cu126"
    }
    "CU128" {
        Write-Info "Installing PyTorch For CUDA 12.8..."
        Invoke-Pip torch==2.10.0 torchvision==0.25.0 torchaudio==2.10.0 --index-url "https://download.pytorch.org/whl/cu128"
    }
    "CU130" {
        Write-Info "Installing PyTorch For CUDA 13.0..."
        Invoke-Pip torch==2.10.0 torchvision==0.25.0 torchaudio==2.10.0 --index-url "https://download.pytorch.org/whl/cu130"
    }
    "CPU" {
        Write-Info "Installing PyTorch For CPU..."
        Invoke-Pip torch torchvision torchaudio --index-url "https://download.pytorch.org/whl/cpu"
    }
}
Write-Success "PyTorch Installed"
Write-Info "Installing Python Dependencies From requirements.txt..."
$global:ErrorActionPreference = 'Continue'
Invoke-Pip -r requirements.txt
Write-Success "Python Dependencies Installed"
$global:ErrorActionPreference = 'Stop'
Write-Success "Installation Completed"
