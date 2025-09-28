# Credible PDF Signature Scanner - Quick Reference

## Installation
```bash
pip install -r requirements.txt
python test_installation.py  # Verify installation
```

## Command Line Usage

### Single File
```bash
# Basic scan
python credible_scanner_cli.py single document.pdf

# Custom output
python credible_scanner_cli.py single document.pdf my_results.xlsx
```

### Batch Processing
```bash
# Scan all PDFs in directory
python credible_scanner_cli.py batch /path/to/pdfs/

# Custom output file
python credible_scanner_cli.py batch /path/to/pdfs/ batch_output.xlsx

# Custom file pattern
python credible_scanner_cli.py batch /path/to/pdfs/ --pattern "*.pdf"
```

## Python API

### Basic Usage
```python
from credible_scanner import credible_attachment_scanner

result = credible_attachment_scanner("document.pdf")
print(result['form_type'])        # Form type detected
print(result['signatures_found']) # Number of signatures
print(result['signature_locations']) # Signature coordinates
```

### Batch Processing
```python
from credible_scanner import batch_process_pdfs

output_path = batch_process_pdfs("/path/to/pdfs/", "results.xlsx")
```

### Individual Components
```python
from credible_scanner.form_detector import identify_form_type
from credible_scanner.signature_detector import find_signature_areas
from credible_scanner.output_handler import save_results

# Use individual functions as needed
```

## Supported Form Types
- **DLA-20**: Disability rating forms
- **Treatment Plan**: Individual treatment plans  
- **Progress Note**: Clinical progress notes
- **Assessment**: Clinical assessments
- **Intake Form**: Client intake forms
- **Unknown Form**: Generic signature detection

## Output Format
Excel file with two sheets:
1. **Signature Scan Results**: Detailed signature locations
2. **Summary**: Aggregate statistics

### Key Fields
- `File Name`, `Form Type`, `Total Pages`
- `Signatures Found`, `Page Number`
- `Signature Type` (box, line, form_specific)
- `X Coordinate`, `Y Coordinate`, `Width`, `Height`
- `Confidence`, `Error`, `Scan Date`

## Troubleshooting
```bash
# Test installation
python test_installation.py

# Run examples
python example_usage.py

# Check dependencies
pip list | grep -E "(pdf2image|pytesseract|opencv|pandas)"
```

## Dependencies
- **pdf2image**: PDF to image conversion
- **pytesseract**: OCR text recognition  
- **opencv-python**: Computer vision for signature detection
- **pandas**: Data processing and Excel output
- **Pillow**: Image processing support
- **openpyxl**: Excel file generation

## System Requirements
- **Poppler**: PDF processing (poppler-utils)
- **Tesseract**: OCR engine (tesseract-ocr)

See `CREDIBLE_SCANNER_INSTALL.md` for detailed installation instructions.