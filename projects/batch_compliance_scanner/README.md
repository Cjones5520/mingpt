# Batch Compliance Scanner

A tool to quickly process PDF forms, identify them, and produce an Excel report with their details.

## Features

- Process all PDFs in a specified folder using Tesseract OCR
- Detect form types based on keywords (e.g., "DLA-20", "Credible Plan", "Consumer Choice")
- Perform basic signature detection by looking for keywords like "SIGNATURE" or "SIGNED"
- Generate an Excel report containing filename, form type, confidence score, signature presence, and processing status

## Requirements

- Python libraries: pytesseract, pdf2image, pandas, openpyxl
- External dependencies: Tesseract OCR and Poppler for Windows

## Installation

1. Install Tesseract OCR:
   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt install tesseract-ocr`
   - macOS: `brew install tesseract`

2. Install Poppler:
   - Windows: Download from https://blog.alivate.com.au/poppler-windows/
   - Linux: `sudo apt install poppler-utils`
   - macOS: `brew install poppler`

3. Install Python dependencies:
   ```bash
   pip install pytesseract pdf2image pandas openpyxl
   ```

## Usage

```python
from batch_compliance_scanner import batch_scan_all_forms

# Scan all PDFs in a folder and generate report
results_df = batch_scan_all_forms("/path/to/pdf/folder")
results_df.to_excel("compliance_report.xlsx", index=False)
```