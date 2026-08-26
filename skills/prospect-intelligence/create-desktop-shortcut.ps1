# Create-RevenueRitual-Shortcut.ps1
# Creates a branded desktop shortcut for the Revenue Ritual Prospect Auditor

$WshShell = New-Object -ComObject WScript.Shell

# Desktop path
$DesktopPath = [Environment]::GetFolderPath("Desktop")

# Target script
$TargetPath = "$PSScriptRoot\audit.bat"

# Create shortcut
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\Revenue Ritual - Prospect Auditor.lnk")
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = "$PSScriptRoot"
$Shortcut.Description = "Revenue Ritual Prospect Intelligence Auditor - Find revenue leaks in any business website"
$Shortcut.IconLocation = "%SystemRoot%\System32\SHELL32.dll,14"
$Shortcut.WindowStyle = 1  # Normal window

# Save shortcut
$Shortcut.Save()

Write-Host "✅ Desktop shortcut created: Revenue Ritual - Prospect Auditor" -ForegroundColor Green
Write-Host "   Target: $TargetPath" -ForegroundColor Gray
Write-Host "   Location: $DesktopPath" -ForegroundColor Gray
Write-Host ""
Write-Host "Double-click the shortcut on your desktop to start auditing prospects." -ForegroundColor Cyan
