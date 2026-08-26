' Revenue Ritual — Silent Launcher
' Launches gui.py without showing a command window

Set WshShell = CreateObject("WScript.Shell")
scriptDir = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\") - 1)

' Try pythonw first (no console), fall back to python
pythonPaths = Array("pythonw.exe", "python.exe")
launched = False

For Each py In pythonPaths
    Set cmd = WshShell.Exec("where " & py)
    path = cmd.StdOut.ReadLine()
    If path <> "" Then
        WshShell.Run """" & path & """ """ & scriptDir & "\gui.py""", 0, False
        launched = True
        Exit For
    End If
Next

If Not launched Then
    MsgBox "Python not found. Please install Python and add it to your PATH.", vbCritical, "Revenue Ritual"
End If
