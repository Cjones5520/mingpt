"""
Main scanner module for Credible PDF signature detection.

Implements the core workflow: PDF → Images → Form Type → Signature Detection → Output
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from pdf2image import convert_from_path
from .form_detector import identify_form_type
from .signature_detector import find_signature_areas
from .output_handler import save_results


def credible_attachment_scanner(pdf_path: str) -> Dict[str, Any]:
    """
    Main function to scan a single PDF for signatures.
    
    Args:
        pdf_path (str): Path to the PDF file to scan
        
    Returns:
        Dict[str, Any]: Results containing form type and signature locations
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    try:
        # 1. PDF → Images
        images = convert_from_path(pdf_path)
        
        if not images:
            return {
                'file_path': pdf_path,
                'error': 'Failed to convert PDF to images',
                'form_type': None,
                'signature_locations': []
            }

        # 2. Identify Form Type (OCR text search)
        form_type = identify_form_type(images[0])

        # 3. Signature Detection (Computer Vision)
        signature_locations = find_signature_areas(images, form_type)

        # 4. Prepare results
        results = {
            'file_path': pdf_path,
            'form_type': form_type,
            'signature_locations': signature_locations,
            'total_pages': len(images),
            'signatures_found': len(signature_locations),
            'error': None
        }
        
        return results
        
    except Exception as e:
        return {
            'file_path': pdf_path,
            'error': str(e),
            'form_type': None,
            'signature_locations': []
        }


def batch_process_pdfs(
    pdf_directory: str, 
    output_file: str = "signature_scan_results.xlsx",
    file_pattern: str = "*.pdf"
) -> str:
    """
    Process multiple PDF files in a directory and generate a consolidated report.
    
    Args:
        pdf_directory (str): Directory containing PDF files
        output_file (str): Output Excel file name
        file_pattern (str): File pattern to match (default: "*.pdf")
        
    Returns:
        str: Path to the generated output file
    """
    pdf_dir = Path(pdf_directory)
    
    if not pdf_dir.exists():
        raise FileNotFoundError(f"Directory not found: {pdf_directory}")
    
    # Find all PDF files
    pdf_files = list(pdf_dir.glob(file_pattern))
    
    if not pdf_files:
        raise ValueError(f"No PDF files found in {pdf_directory} matching pattern {file_pattern}")
    
    # Process each PDF
    all_results = []
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")
        result = credible_attachment_scanner(str(pdf_file))
        all_results.append(result)
    
    # Save consolidated results
    output_path = save_results(all_results, output_file)
    
    print(f"Batch processing complete. Results saved to: {output_path}")
    return output_path


def scan_single_file(pdf_path: str, output_file: Optional[str] = None) -> str:
    """
    Convenience function to scan a single file and save results.
    
    Args:
        pdf_path (str): Path to PDF file
        output_file (str, optional): Output file name. If None, generates based on input filename.
        
    Returns:
        str: Path to the generated output file
    """
    result = credible_attachment_scanner(pdf_path)
    
    if output_file is None:
        pdf_name = Path(pdf_path).stem
        output_file = f"{pdf_name}_signature_scan.xlsx"
    
    output_path = save_results([result], output_file)
    return output_path