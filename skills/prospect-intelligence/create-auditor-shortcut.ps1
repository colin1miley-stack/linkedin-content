# Create-RevenueRitual-Auditor-Shortcut.ps1
# Removes old shortcuts, creates new branded shortcut with no console window

$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")

# Remove old shortcuts
$oldShortcuts = @(
    "$DesktopPath\Revenue Ritual - Prospect Auditor.lnk",
    "$DesktopPath\Revenue Ritual - Auditor.lnk"
)

foreach ($old in $oldShortcuts) {
    if (Test-Path $old) {
        Remove-Item $old -Force
        Write-Host "Removed old shortcut: $(Split-Path $old -Leaf)" -ForegroundColor Yellow
    }
}

# Create new shortcut pointing to VBS launcher (no console window)
$scriptDir = $PSScriptRoot
$vbsPath = "$scriptDir\launcher.vbs"

$Shortcut = $WshShell.CreateShortcut("$DesktopPath\Revenue Ritual - Auditor.lnk")
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = "`"$vbsPath`""
$Shortcut.WorkingDirectory = $scriptDir
$Shortcut.Description = "Revenue Ritual Prospect Intelligence Auditor. Find revenue leaks, map opportunities, generate proposals."

# Professional icon from Windows system
$Shortcut.IconLocation = "%SystemRoot%\System32\imageres.dll,14"
$Shortcut.WindowStyle = 7
$Shortcut.Save()

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  DESKTOP SHORTCUT CREATED" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Name: Revenue Ritual - Auditor" -ForegroundColor White
Write-Host "Target: launcher.vbs (silent, no console)" -ForegroundColor Gray
Write-Host "Icon: Professional gear icon" -ForegroundColor Gray
Write-Host ""
Write-Host "Double-click to launch the auditor." -ForegroundColor Cyan
Write-Host "No command window will appear." -ForegroundColor Cyan
Write-Host ""
