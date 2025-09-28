#!/usr/bin/env python3
"""
Example usage of the Credible PDF Signature Scanner.

This script demonstrates how to use the scanner programmatically.
"""

import os
import tempfile
from pathlib import Path

# Import the credible scanner
from credible_scanner import (
    credible_attachment_scanner,
    batch_process_pdfs,
    scan_single_file
)


def create_sample_pdf():
    """
    Create a simple text file that simulates a PDF for testing.
    In real usage, you would use actual PDF files.
    """
    temp_dir = tempfile.mkdtemp()
    sample_file = os.path.join(temp_dir, "sample_dla_20.pdf")
    
    # Create a mock file (in real usage, this would be a PDF)
    with open(sample_file, 'w') as f:
        f.write("Mock PDF content - this would be a real PDF file in practice")
    
    print(f"Created sample file: {sample_file}")
    return sample_file, temp_dir


def example_single_file_scan():
    """Example of scanning a single PDF file."""
    print("\n" + "="*50)
    print("EXAMPLE 1: Single File Scan")
    print("="*50)
    
    # Create a sample file for testing
    sample_file, temp_dir = create_sample_pdf()
    
    try:
        # Method 1: Direct function call
        print("Method 1: Using credible_attachment_scanner() directly")
        result = credible_attachment_scanner(sample_file)
        
        print(f"File: {result['file_path']}")
        print(f"Form Type: {result['form_type']}")
        print(f"Pages: {result['total_pages']}")
        print(f"Signatures Found: {result['signatures_found']}")
        if result['error']:
            print(f"Error: {result['error']}")
        
        # Method 2: Scan and save to Excel
        print("\nMethod 2: Using scan_single_file() with Excel output")
        output_file = scan_single_file(sample_file, "example_output.xlsx")
        print(f"Results saved to: {output_file}")
        
    except Exception as e:
        print(f"Error during single file scan: {e}")
    
    finally:
        # Clean up
        if os.path.exists(sample_file):
            os.remove(sample_file)
        os.rmdir(temp_dir)


def example_batch_processing():
    """Example of batch processing multiple PDF files."""
    print("\n" + "="*50)
    print("EXAMPLE 2: Batch Processing")
    print("="*50)
    
    # Create a temporary directory with multiple sample files
    temp_dir = tempfile.mkdtemp()
    sample_files = []
    
    try:
        # Create multiple sample PDF files
        for i in range(3):
            sample_file = os.path.join(temp_dir, f"sample_{i+1}.pdf")
            with open(sample_file, 'w') as f:
                f.write(f"Mock PDF content {i+1} - this would be a real PDF file")
            sample_files.append(sample_file)
            print(f"Created: {sample_file}")
        
        # Batch process all files
        print(f"\nProcessing all PDF files in: {temp_dir}")
        output_file = batch_process_pdfs(temp_dir, "batch_results.xlsx")
        print(f"Batch processing complete. Results saved to: {output_file}")
        
    except Exception as e:
        print(f"Error during batch processing: {e}")
    
    finally:
        # Clean up
        for sample_file in sample_files:
            if os.path.exists(sample_file):
                os.remove(sample_file)
        os.rmdir(temp_dir)


def example_api_usage():
    """Example of using individual API components."""
    print("\n" + "="*50)
    print("EXAMPLE 3: Individual API Components")
    print("="*50)
    
    from credible_scanner.form_detector import get_form_specific_keywords
    from credible_scanner.signature_detector import merge_overlapping_areas
    from credible_scanner.output_handler import save_results
    
    # Example 1: Get form-specific keywords
    print("Form-specific keywords:")
    dla_keywords = get_form_specific_keywords('DLA-20')
    print(f"  DLA-20: {dla_keywords}")
    
    treatment_keywords = get_form_specific_keywords('Treatment Plan')
    print(f"  Treatment Plan: {treatment_keywords}")
    
    # Example 2: Merge overlapping signature areas
    print("\nMerging overlapping signature areas:")
    test_areas = [
        {'x': 100, 'y': 100, 'width': 100, 'height': 50, 'confidence': 0.8},
        {'x': 120, 'y': 110, 'width': 80, 'height': 40, 'confidence': 0.7},
        {'x': 300, 'y': 200, 'width': 100, 'height': 50, 'confidence': 0.9}
    ]
    
    merged_areas = merge_overlapping_areas(test_areas)
    print(f"  Original areas: {len(test_areas)}")
    print(f"  After merging: {len(merged_areas)}")
    
    # Example 3: Save results to Excel
    print("\nSaving sample results:")
    sample_results = [
        {
            'file_path': 'sample1.pdf',
            'form_type': 'DLA-20',
            'total_pages': 2,
            'signatures_found': 1,
            'signature_locations': [
                {'x': 100, 'y': 200, 'width': 150, 'height': 40, 'type': 'box', 'confidence': 0.8, 'page': 2}
            ],
            'error': None
        },
        {
            'file_path': 'sample2.pdf',
            'form_type': 'Treatment Plan', 
            'total_pages': 1,
            'signatures_found': 2,
            'signature_locations': [
                {'x': 100, 'y': 300, 'width': 120, 'height': 35, 'type': 'line', 'confidence': 0.7, 'page': 1},
                {'x': 300, 'y': 400, 'width': 140, 'height': 45, 'type': 'box', 'confidence': 0.9, 'page': 1}
            ],
            'error': None
        }
    ]
    
    output_path = save_results(sample_results, "api_example_results.xlsx")
    print(f"  Results saved to: {output_path}")


def main():
    """Run all examples."""
    print("Credible PDF Signature Scanner - Usage Examples")
    print("Note: These examples use mock files. In real usage, provide actual PDF files.")
    
    try:
        example_single_file_scan()
        example_batch_processing() 
        example_api_usage()
        
        print("\n" + "="*50)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*50)
        print("\nFor real usage:")
        print("1. Replace mock files with actual PDF files")
        print("2. Use the command line interface: python credible_scanner_cli.py")
        print("3. See CREDIBLE_SCANNER_INSTALL.md for more details")
        
    except ImportError as e:
        print(f"\nError importing credible_scanner: {e}")
        print("Make sure to install all dependencies first:")
        print("  pip install -r requirements.txt")
        print("  python test_installation.py")
    
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please check your installation and try again.")


if __name__ == "__main__":
    main()