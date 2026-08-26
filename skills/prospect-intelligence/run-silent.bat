@echo off
chcp 65001 >nul
setlocal

set SCRIPTDIR=%~dp0
set GUIPATH=%SCRIPTDIR%gui.py

REM Try pythonw first (no console window)
pythonw "%GUIPATH%" 2>nul
if %errorlevel% equ 0 goto :done

REM Fall back to python (may show brief console)
python "%GUIPATH%" 2>nul
if %errorlevel% equ 0 goto :done

REM Python not found
msg * /TIME:5 "Python not found. Please install Python and add it to your PATH."

:done
endlocal
