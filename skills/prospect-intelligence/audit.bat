@echo off
chcp 65001 >nul
title Revenue Ritual - Prospect Auditor
cls

echo.
echo    +==============================================================+
echo    ^|                                                              ^|
echo    ^|     REVENUE RITUAL                                           ^|
echo    ^|                                                              ^|
echo    ^|     Your sales team is leaking revenue.                      ^|
echo    ^|     Find it. Fix it.                                         ^|
echo    ^|                                                              ^|
echo    +==============================================================+
echo.
echo  +--------------------------------------------------------------+
echo  ^|  PROSPECT INTELLIGENCE AUDITOR v1.0                          ^|
echo  ^|  Audit any website. Find revenue leaks. Map opportunities.    ^|
echo  +--------------------------------------------------------------+
echo.
echo.
echo  Enter the website URL to audit:
echo  Examples: https://flowerpop.ie   https://example.com
echo.
set /p URL="URL: "
echo.

if "%URL%"=="" (
    echo  [ERROR] No URL provided.
    pause
    exit /b 1
)

echo  Analyzing: %URL%
echo  --------------------------------------------------------------
echo.

cd /d "%~dp0scripts"
python audit.py --url "%URL%" --output-dir "%~dp0..\..\prospect-audits"

echo.
echo  ==============================================================
echo   AUDIT COMPLETE
echo   Report saved to: prospect-audits\
echo   Full path: %~dp0..\..\prospect-audits\
echo  ==============================================================
echo.
explorer "%~dp0..\..\prospect-audits"
echo.
pause
