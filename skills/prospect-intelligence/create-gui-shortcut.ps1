# Create-RevenueRitual-GUI-Shortcut.ps1
# Creates a desktop shortcut for the Revenue Ritual Prospect Auditor GUI

$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$TargetPath = "$PSScriptRoot\gui.py"

$Shortcut = $WshShell.CreateShortcut("$DesktopPath\Revenue Ritual - Auditor.lnk")
$Shortcut.TargetPath = "python.exe"
$Shortcut.Arguments = "`"$TargetPath`""
$Shortcut.WorkingDirectory = "$PSScriptRoot"
$Shortcut.Description = "Revenue Ritual Prospect Intelligence Auditor"
$Shortcut.IconLocation = "%SystemRoot%\System32\SHELL32.dll,14"
$Shortcut.WindowStyle = 1

$Shortcut.Save()

Write-Host "Desktop shortcut created: Revenue Ritual - Auditor" -ForegroundColor Green
Write-Host "Double-click to launch the branded GUI." -ForegroundColor Cyan
