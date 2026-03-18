<#
.SYNOPSIS
    Smart Project Backup Script using Robocopy
.DESCRIPTION
    This script backs up a source folder to a destination folder.
    - First run: Copies everything.
    - Subsequent runs: Only copies new or modified files (incremental update).
.PARAMETER SourcePath
    The full path of the project folder you want to backup.
.PARAMETER DestinationPath
    The full path where you want to store the backup.
.EXAMPLE
    .\smart_backup.ps1 -SourcePath "C:\MyProject" -DestinationPath "D:\Backups\MyProject"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$SourcePath,

    [Parameter(Mandatory=$true)]
    [string]$DestinationPath
)

# 1. Check if Source exists
if (-not (Test-Path -Path $SourcePath)) {
    Write-Error "Error: The source folder '$SourcePath' does not exist."
    exit 1
}

# 2. Check/Create Destination
if (-not (Test-Path -Path $DestinationPath)) {
    Write-Host "Creating backup destination folder: $DestinationPath" -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $DestinationPath | Out-Null
}

Write-Host "Starting backup from '$SourcePath' to '$DestinationPath'..." -ForegroundColor Green

# 3. Execute Robocopy
# /E   :: Copy subdirectories, including Empty ones.
# /XO  :: eXclude Older files. (Only copies if source is newer/changed).
# /R:3 :: Retry 3 times if a file is locked/busy.
# /W:5 :: Wait 5 seconds between retries.
# /MT:8 :: Multi-threaded copy using 8 threads (faster for many small files).
# /NjH :: No Job Header.
# /NJS :: No Job Summary. (Remove these flags if you want verbose output)

# Use invoke-expression or direct call. Robocopy returns exit codes that are not errors in Powershell.
$robocopyOptions = @("/E", "/XO", "/R:3", "/W:5", "/MT:8")
$process = Start-Process -FilePath "robocopy.exe" -ArgumentList "`"$SourcePath`" `"$DestinationPath`" $robocopyOptions" -NoNewWindow -Wait -PassThru

# Robocopy Exit Codes:
# 0: No errors occurred, and no copying was done. (Source and destination are in sync).
# 1: One or more files were copied successfully (that is, new files have arrived).
# 2: Some Extra files or directories were detected. No files were copied.
# 3: (2+1) Some files were copied. Additional files were present.
# 4: Some Mismatched files or directories were detected.
# 5: (4+1) Some Mismatched files were detected. Some files were copied.
# 6: (4+2) Mismatched files and Extra files were detected.
# 7: (4+1+2) Mismatched files, Extra files, and copied files.
# 8: Some files or directories could not be copied. (Copy errors occurred).

if ($process.ExitCode -lt 8) {
    Write-Host "Backup completed successfully!" -ForegroundColor Green
    if ($process.ExitCode -eq 0) {
        Write-Host "No changes detected. Backup is already up-to-date." -ForegroundColor Yellow
    } else {
        Write-Host "New or modified files have been updated." -ForegroundColor Cyan
    }
} else {
    Write-Error "Backup completed with errors. Exit Code: $($process.ExitCode). Check permissions or open files."
}
