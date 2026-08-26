#!/usr/bin/env python3
"""
Revenue Ritual — PDF Export Utility
Convert HTML audit reports to branded PDFs automatically.
Uses Microsoft Edge headless (Windows 10/11 built-in) or Chrome fallback.

Usage:
    python pdf_export.py --input report.html --output report.pdf
    python pdf_export.py --input report.html  # auto-names output

Author: Revenue Ritual
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime


def find_edge_executable() -> str:
    """Find Microsoft Edge executable on Windows."""
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for path in edge_paths:
        if Path(path).exists():
            return path
    return None


def find_chrome_executable() -> str:
    """Find Google Chrome executable on Windows."""
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.environ.get("USERNAME", "")),
    ]
    for path in chrome_paths:
        if Path(path).exists():
            return path
    return None


def html_to_pdf_edge(input_html: str, output_pdf: str) -> bool:
    """Use Microsoft Edge headless to convert HTML to PDF."""
    edge = find_edge_executable()
    if not edge:
        return False
    
    # Convert to absolute path
    input_path = Path(input_html).resolve()
    output_path = Path(output_pdf).resolve()
    
    # Edge headless print-to-PDF
    cmd = [
        edge,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={output_path}",
        f"file:///{input_path}"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return output_path.exists() and output_path.stat().st_size > 1000
    except Exception as e:
        print(f"Edge PDF export failed: {e}")
        return False


def html_to_pdf_chrome(input_html: str, output_pdf: str) -> bool:
    """Use Google Chrome headless to convert HTML to PDF."""
    chrome = find_chrome_executable()
    if not chrome:
        return False
    
    input_path = Path(input_html).resolve()
    output_path = Path(output_pdf).resolve()
    
    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={output_path}",
        f"file:///{input_path}"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return output_path.exists() and output_path.stat().st_size > 1000
    except Exception as e:
        print(f"Chrome PDF export failed: {e}")
        return False


def export_pdf(input_html: str, output_pdf: str = None) -> str:
    """Export HTML to PDF using best available method."""
    input_path = Path(input_html)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_html}")
        return None
    
    if output_pdf is None:
        # Auto-name: report.html → report.pdf
        output_pdf = str(input_path.with_suffix(".pdf"))
    
    print(f"Exporting PDF: {input_path.name}")
    print(f"Output: {output_pdf}")
    
    # Try Edge first (most reliable on Windows)
    print("  -> Trying Microsoft Edge...")
    if html_to_pdf_edge(input_html, output_pdf):
        print(f"  ✅ PDF created with Microsoft Edge")
        return output_pdf
    
    # Fallback to Chrome
    print("  -> Trying Google Chrome...")
    if html_to_pdf_chrome(input_html, output_pdf):
        print(f"  ✅ PDF created with Google Chrome")
        return output_pdf
    
    # Fallback: instructions
    print("  ❌ No browser found for headless PDF export.")
    print("  ")
    print("  Manual workaround:")
    print("  1. Open the HTML file in your browser")
    print("  2. Press Ctrl+P (or Cmd+P on Mac)")
    print("  3. Select 'Save as PDF' as the printer")
    print("  4. Click Save")
    print("  ")
    print("  Or install Microsoft Edge / Google Chrome for automatic export.")
    return None


def main():
    parser = argparse.ArgumentParser(description="Export HTML audit report to PDF")
    parser.add_argument("--input", "-i", required=True, help="Input HTML file path")
    parser.add_argument("--output", "-o", help="Output PDF file path (optional)")
    args = parser.parse_args()
    
    result = export_pdf(args.input, args.output)
    if result:
        print(f"\nDone! PDF saved: {result}")
        # Open the PDF
        try:
            os.startfile(result)
        except:
            pass
    else:
        print("\nPDF export failed. See instructions above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
