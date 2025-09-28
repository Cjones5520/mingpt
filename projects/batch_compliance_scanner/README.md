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

### Command Line Usage
```bash
python batch_compliance_scanner.py /path/to/pdf/folder
```

### Python API Usage
```python
from batch_compliance_scanner import batch_scan_all_forms, quick_scan_pdf

# Scan all PDFs in a folder and generate report
results_df = batch_scan_all_forms("/path/to/pdf/folder")
results_df.to_excel("compliance_report.xlsx", index=False)

# Scan a single PDF
result = quick_scan_pdf("form.pdf")
print(result)
```

### Example Output
The scanner generates an Excel report with the following columns:
- `filename`: Name of the PDF file
- `form_type`: Detected form type (DLA-20, Credible Plan, Consumer Choice, Generic Form, or Unknown)
- `confidence_score`: Confidence in the form type detection (0.0-1.0)
- `signature_present`: Whether signature patterns were detected (True/False)
- `processing_status`: Success or Failed
- `error_message`: Error details if processing failed

## Testing

Run the included tests:
```bash
python test_scanner.py
```

Run the example usage:
```bash
python example_usage.py
```

Create test PDFs for demonstration:
```bash
python create_test_pdfs.py
```