@echo off
chcp 65001 >nul
title Revenue Ritual - Launching Auditor...
cd /d "%~dp0"
pythonw gui.py
if errorlevel 1 (
    echo.
    echo ERROR: Could not launch GUI.
    echo Make sure Python is installed and in your PATH.
    echo.
    pause
)
