#!/usr/bin/env python3
"""
Batch Compliance Scanner

A tool to quickly process PDF forms, identify them, and produce an Excel report with their details.

Requirements:
- pytesseract: pip install pytesseract
- pdf2image: pip install pdf2image
- pandas: pip install pandas
- openpyxl: pip install openpyxl

External dependencies:
- Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki (Windows)
- Poppler: https://blog.alivate.com.au/poppler-windows/ (Windows)

For Linux: sudo apt install tesseract-ocr poppler-utils
For macOS: brew install tesseract poppler
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

try:
    import pytesseract
    from pdf2image import convert_from_path
    import pandas as pd
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install required packages:")
    print("pip install pytesseract pdf2image pandas openpyxl")
    sys.exit(1)

# Default Tesseract path for Windows
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Form type detection patterns
FORM_PATTERNS = {
    'DLA-20': [r'DLA-20', r'DLA\s*20', r'DEFENSE\s*LOGISTICS\s*AGENCY'],
    'Credible Plan': [r'CREDIBLE\s*PLAN', r'CREDIBLE\s*PLAN\s*FORM'],
    'Consumer Choice': [r'CONSUMER\s*CHOICE', r'CONSUMER\s*CHOICE\s*FORM'],
    'Generic Form': [r'FORM\s*\d+', r'APPLICATION', r'REQUEST']
}

# Signature detection patterns
SIGNATURE_PATTERNS = [
    r'SIGNATURE\s*_+', r'SIGNED\s*BY', r'SIGN\s*HERE', r'SIGN\s*DATE',
    r'SIGNATURE\s*DATE', r'APPLICANT\s*SIGNATURE', r'AUTHORIZED\s*SIGNATURE',
    r'SIGNATURE\s*REQUIRED', r'SIGNATURE\s*BELOW', r'SIGNATURE\s*LINE'
]

# Negative patterns that suggest no signature is needed
NEGATIVE_SIGNATURE_PATTERNS = [
    r'NO\s*SIGNATURE', r'NOT?\s*REQUIRE[DS]?\s*SIGNATURE', r'SIGNATURE\s*NOT?\s*NEED',
    r'WITHOUT\s*SIGNATURE'
]


def configure_tesseract():
    """Configure Tesseract OCR path for Windows."""
    if os.name == 'nt':  # Windows
        if os.path.exists(TESSERACT_PATH):
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
        else:
            print(f"Warning: Tesseract not found at {TESSERACT_PATH}")
            print("Please install Tesseract OCR or update the TESSERACT_PATH variable")


def detect_form_type(text: str) -> Tuple[str, float]:
    """
    Detect form type based on text content.
    
    Args:
        text: Extracted text from PDF
        
    Returns:
        Tuple of (form_type, confidence_score)
    """
    text_upper = text.upper()
    best_match = "Unknown"
    best_confidence = 0.0
    
    for form_type, patterns in FORM_PATTERNS.items():
        matches = 0
        total_patterns = len(patterns)
        
        for pattern in patterns:
            if re.search(pattern, text_upper):
                matches += 1
        
        confidence = matches / total_patterns
        if confidence > best_confidence:
            best_confidence = confidence
            best_match = form_type
    
    return best_match, best_confidence


def detect_signature(text: str) -> bool:
    """
    Detect if document contains signature-related text.
    
    Args:
        text: Extracted text from PDF
        
    Returns:
        True if signature patterns are found and no negative patterns
    """
    text_upper = text.upper()
    
    # First check for negative patterns
    for pattern in NEGATIVE_SIGNATURE_PATTERNS:
        if re.search(pattern, text_upper):
            return False
    
    # Then check for positive patterns
    for pattern in SIGNATURE_PATTERNS:
        if re.search(pattern, text_upper):
            return True
    
    return False


def quick_scan_pdf(pdf_path: str) -> Dict:
    """
    Quick scan of PDF file - processes first page only for speed.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Dictionary containing scan results
    """
    result = {
        'filename': os.path.basename(pdf_path),
        'form_type': 'Unknown',
        'confidence_score': 0.0,
        'signature_present': False,
        'processing_status': 'Failed',
        'error_message': ''
    }
    
    try:
        # Convert first page only for quick processing
        pages = convert_from_path(pdf_path, first_page=1, last_page=1)
        
        if not pages:
            result['error_message'] = 'No pages found in PDF'
            return result
        
        # Extract text from first page using OCR
        first_page = pages[0]
        text = pytesseract.image_to_string(first_page)
        
        # Detect form type and confidence
        form_type, confidence = detect_form_type(text)
        result['form_type'] = form_type
        result['confidence_score'] = round(confidence, 2)
        
        # Detect signature presence
        result['signature_present'] = detect_signature(text)
        
        result['processing_status'] = 'Success'
        
    except Exception as e:
        result['error_message'] = str(e)
        result['processing_status'] = 'Failed'
    
    return result


def batch_scan_all_forms(folder_path: str) -> pd.DataFrame:
    """
    Batch process all PDF files in a folder.
    
    Args:
        folder_path: Path to folder containing PDF files
        
    Returns:
        pandas DataFrame with scan results
    """
    configure_tesseract()
    
    folder_path = Path(folder_path)
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    # Find all PDF files
    pdf_files = list(folder_path.glob("*.pdf")) + list(folder_path.glob("*.PDF"))
    
    if not pdf_files:
        print(f"No PDF files found in {folder_path}")
        return pd.DataFrame()
    
    print(f"Found {len(pdf_files)} PDF files to process...")
    
    results = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"Processing {i}/{len(pdf_files)}: {pdf_file.name}")
        
        result = quick_scan_pdf(str(pdf_file))
        results.append(result)
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Reorder columns for better readability
    columns_order = [
        'filename', 'form_type', 'confidence_score', 
        'signature_present', 'processing_status', 'error_message'
    ]
    df = df[columns_order]
    
    return df


def main():
    """Main function for command-line usage."""
    if len(sys.argv) != 2:
        print("Usage: python batch_compliance_scanner.py <pdf_folder_path>")
        print("Example: python batch_compliance_scanner.py ./pdf_forms/")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    try:
        # Process all PDFs
        results_df = batch_scan_all_forms(folder_path)
        
        if results_df.empty:
            print("No results to save.")
            return
        
        # Save to Excel
        output_file = "compliance_report.xlsx"
        results_df.to_excel(output_file, index=False)
        
        print(f"\nProcessing completed!")
        print(f"Results saved to: {output_file}")
        print(f"Total files processed: {len(results_df)}")
        print(f"Successful scans: {sum(results_df['processing_status'] == 'Success')}")
        print(f"Failed scans: {sum(results_df['processing_status'] == 'Failed')}")
        
        # Show form type summary
        form_counts = results_df['form_type'].value_counts()
        print("\nForm types detected:")
        for form_type, count in form_counts.items():
            print(f"  {form_type}: {count}")
        
        # Show signature summary
        signature_count = sum(results_df['signature_present'])
        print(f"\nSignatures detected: {signature_count}/{len(results_df)} files")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()