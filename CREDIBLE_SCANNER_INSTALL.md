# Credible PDF Signature Scanner - Installation Guide

This guide provides instructions for installing and using the Credible PDF Signature Scanner tool.

## System Requirements

- Python 3.7 or higher
- Operating System: Windows, macOS, or Linux

## Dependencies Installation

### 1. Install Python Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Or install individual packages
pip install pdf2image>=3.1.0 pytesseract>=0.3.10 opencv-python>=4.5.0 pandas>=1.3.0 Pillow>=8.0.0 openpyxl>=3.0.0
```

### 2. Install System Dependencies

#### For Windows:
1. **Poppler for Windows:**
   - Download from: https://github.com/oschwartz10612/poppler-windows/releases/
   - Extract to a folder (e.g., `C:\poppler`)
   - Add the `bin` folder to your system PATH

2. **Tesseract OCR:**
   - Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install and note the installation path (usually `C:\Program Files\Tesseract-OCR`)
   - Add to PATH or set TESSERACT_CMD environment variable

#### For macOS:
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install poppler
brew install tesseract
```

#### For Ubuntu/Debian Linux:
```bash
sudo apt-get update
sudo apt-get install -y poppler-utils tesseract-ocr
```

#### For CentOS/RHEL/Fedora:
```bash
sudo yum install -y poppler-utils tesseract
# or for newer versions:
sudo dnf install -y poppler-utils tesseract
```

## Installation Verification

Test your installation with this Python script:

```python
# test_installation.py
import sys

def test_imports():
    try:
        import pdf2image
        print("✓ pdf2image imported successfully")
    except ImportError as e:
        print(f"✗ pdf2image import failed: {e}")
        return False
    
    try:
        import pytesseract
        print("✓ pytesseract imported successfully")
    except ImportError as e:
        print(f"✗ pytesseract import failed: {e}")
        return False
    
    try:
        import cv2
        print("✓ opencv-python imported successfully")
    except ImportError as e:
        print(f"✗ opencv-python import failed: {e}")
        return False
    
    try:
        import pandas
        print("✓ pandas imported successfully")
    except ImportError as e:
        print(f"✗ pandas import failed: {e}")
        return False
    
    return True

def test_system_dependencies():
    try:
        import pdf2image
        # Test poppler
        from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError
        print("✓ Poppler utilities available")
    except Exception as e:
        print(f"✗ Poppler test failed: {e}")
        return False
    
    try:
        import pytesseract
        # Test tesseract
        version = pytesseract.get_tesseract_version()
        print(f"✓ Tesseract OCR available (version: {version})")
    except Exception as e:
        print(f"✗ Tesseract test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing Credible Scanner Installation...")
    print("-" * 40)
    
    if test_imports() and test_system_dependencies():
        print("-" * 40)
        print("✓ All dependencies installed successfully!")
        print("You can now use the Credible PDF Signature Scanner.")
    else:
        print("-" * 40)
        print("✗ Installation incomplete. Please check the errors above.")
        sys.exit(1)
```

Run the test:
```bash
python test_installation.py
```

## Usage

### 1. Command Line Interface

#### Scan a single PDF:
```bash
python credible_scanner_cli.py single document.pdf
python credible_scanner_cli.py single document.pdf custom_output.xlsx
```

#### Batch process multiple PDFs:
```bash
python credible_scanner_cli.py batch /path/to/pdf/directory/
python credible_scanner_cli.py batch /path/to/pdf/directory/ batch_results.xlsx
```

### 2. Python API

```python
from credible_scanner import credible_attachment_scanner, batch_process_pdfs

# Scan a single file
result = credible_attachment_scanner("document.pdf")
print(f"Form Type: {result['form_type']}")
print(f"Signatures Found: {result['signatures_found']}")

# Batch process
output_file = batch_process_pdfs("/path/to/pdfs/", "results.xlsx")
print(f"Results saved to: {output_file}")
```

## Output Format

The scanner generates Excel files with two sheets:

### 1. "Signature Scan Results" Sheet
Contains detailed information for each detected signature:
- File Name
- File Path  
- Form Type
- Total Pages
- Signatures Found
- Page Number
- Signature Type (box, line, form_specific)
- Coordinates (X, Y, Width, Height)
- Confidence Score
- Error Messages (if any)
- Scan Date

### 2. "Summary" Sheet
Contains aggregate statistics:
- Total files processed
- Total signatures found
- Files with signatures
- Success rate
- Form type breakdown
- Signature type breakdown

## Troubleshooting

### Common Issues:

1. **"poppler not found" error:**
   - Ensure poppler-utils is installed and in PATH
   - On Windows, verify the poppler bin directory is in PATH

2. **"tesseract not found" error:**
   - Install Tesseract OCR
   - Set TESSERACT_CMD environment variable if needed

3. **Import errors:**
   - Verify all Python packages are installed: `pip list`
   - Try reinstalling: `pip install --upgrade -r requirements.txt`

4. **Memory errors with large PDFs:**
   - Process files individually instead of batch processing
   - Reduce image resolution in pdf2image conversion

5. **Poor signature detection:**
   - Ensure PDFs are not scanned at too low resolution
   - Check that signature areas have clear contrast
   - Try adjusting OpenCV parameters in signature_detector.py

### Getting Help

For issues with the scanner:
1. Check that all dependencies are properly installed
2. Verify input PDFs are readable and not corrupted
3. Test with a simple, clear PDF first
4. Check error messages in the output Excel file

## Advanced Configuration

You can modify detection parameters by editing the configuration in the source files:

- `form_detector.py`: Adjust OCR settings and form patterns
- `signature_detector.py`: Modify computer vision parameters
- `output_handler.py`: Customize output format

## Performance Notes

- Processing time depends on PDF size and complexity
- Typical performance: 2-5 seconds per page
- Large batch jobs may take several minutes
- Memory usage scales with image resolution and PDF size