#!/usr/bin/env python3
"""
Example usage of the Batch Compliance Scanner

This script demonstrates how to use the batch compliance scanner
to process PDF forms and generate Excel reports.
"""

import os
from batch_compliance_scanner import batch_scan_all_forms, quick_scan_pdf


def demo_single_pdf():
    """Demonstrate scanning a single PDF file."""
    print("=== Single PDF Scan Demo ===")
    
    # This would scan a single PDF file
    # result = quick_scan_pdf("sample_form.pdf")
    # print(f"Result: {result}")
    
    print("To scan a single PDF, use:")
    print("result = quick_scan_pdf('path/to/your/file.pdf')")
    print("This returns a dictionary with scan results")


def demo_batch_scan():
    """Demonstrate batch scanning of PDFs."""
    print("\n=== Batch Scan Demo ===")
    
    # Example of how to use batch scanning
    print("To scan all PDFs in a folder:")
    print("results_df = batch_scan_all_forms('/path/to/pdf/folder')")
    print("results_df.to_excel('compliance_report.xlsx', index=False)")
    
    # If you have a test folder with PDFs, uncomment below:
    # folder_path = "test_pdfs"
    # if os.path.exists(folder_path):
    #     results_df = batch_scan_all_forms(folder_path)
    #     print(f"Processed {len(results_df)} files")
    #     print(results_df.head())
    # else:
    #     print(f"Test folder '{folder_path}' not found")


def create_sample_report():
    """Create a sample report structure for demonstration."""
    print("\n=== Sample Report Structure ===")
    
    import pandas as pd
    
    # Sample data structure that would be generated
    sample_data = [
        {
            'filename': 'form_dla20.pdf',
            'form_type': 'DLA-20',
            'confidence_score': 0.8,
            'signature_present': True,
            'processing_status': 'Success',
            'error_message': ''
        },
        {
            'filename': 'credible_plan.pdf',
            'form_type': 'Credible Plan',
            'confidence_score': 0.9,
            'signature_present': False,
            'processing_status': 'Success',
            'error_message': ''
        },
        {
            'filename': 'unknown_form.pdf',
            'form_type': 'Unknown',
            'confidence_score': 0.0,
            'signature_present': True,
            'processing_status': 'Success',
            'error_message': ''
        }
    ]
    
    df = pd.DataFrame(sample_data)
    print("Sample report structure:")
    print(df.to_string(index=False))
    
    # Save sample report
    df.to_excel("sample_compliance_report.xlsx", index=False)
    print("\nSample report saved as 'sample_compliance_report.xlsx'")


def main():
    """Main demo function."""
    print("Batch Compliance Scanner - Example Usage")
    print("=" * 50)
    
    demo_single_pdf()
    demo_batch_scan()
    create_sample_report()
    
    print("\n" + "=" * 50)
    print("For actual usage:")
    print("1. Place PDF files in a folder")
    print("2. Run: python batch_compliance_scanner.py <folder_path>")
    print("3. Check the generated compliance_report.xlsx file")


if __name__ == "__main__":
    main()