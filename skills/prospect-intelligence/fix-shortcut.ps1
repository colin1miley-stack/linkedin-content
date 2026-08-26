# Fix-Desktop-Shortcut.ps1
# Updates the desktop shortcut to use the reliable batch launcher

$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$scriptDir = $PSScriptRoot

# Remove old shortcuts
$oldShortcuts = @(
    "$DesktopPath\Revenue Ritual - Prospect Auditor.lnk",
    "$DesktopPath\Revenue Ritual - Auditor.lnk"
)

foreach ($old in $oldShortcuts) {
    if (Test-Path $old) {
        Remove-Item $old -Force
        Write-Host "Removed: $(Split-Path $old -Leaf)" -ForegroundColor Yellow
    }
}

# Create new shortcut pointing to run-silent.bat
$batPath = "$scriptDir\run-silent.bat"

$Shortcut = $WshShell.CreateShortcut("$DesktopPath\Revenue Ritual - Auditor.lnk")
$Shortcut.TargetPath = $batPath
$Shortcut.WorkingDirectory = $scriptDir
$Shortcut.Description = "Revenue Ritual Prospect Intelligence Auditor"
$Shortcut.IconLocation = "%SystemRoot%\System32\imageres.dll,14"
$Shortcut.WindowStyle = 7
$Shortcut.Save()

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  SHORTCUT FIXED" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Name: Revenue Ritual - Auditor" -ForegroundColor White
Write-Host "Target: run-silent.bat" -ForegroundColor Gray
Write-Host ""
Write-Host "Double-click to launch." -ForegroundColor Cyan
Write-Host ""
