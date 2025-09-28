#!/usr/bin/env python3
"""
Command-line interface for the Credible PDF Signature Scanner.

Usage:
    python credible_scanner_cli.py single input.pdf [output.xlsx]
    python credible_scanner_cli.py batch /path/to/pdfs/ [output.xlsx]
"""

import sys
import argparse
from pathlib import Path
from credible_scanner import credible_attachment_scanner, batch_process_pdfs, scan_single_file


def main():
    parser = argparse.ArgumentParser(
        description="Credible PDF Signature Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan a single PDF file
  python credible_scanner_cli.py single document.pdf
  
  # Scan a single PDF with custom output
  python credible_scanner_cli.py single document.pdf custom_output.xlsx
  
  # Batch process all PDFs in a directory
  python credible_scanner_cli.py batch /path/to/pdfs/
  
  # Batch process with custom output
  python credible_scanner_cli.py batch /path/to/pdfs/ batch_results.xlsx
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Single file command
    single_parser = subparsers.add_parser('single', help='Scan a single PDF file')
    single_parser.add_argument('pdf_file', help='Path to the PDF file')
    single_parser.add_argument('output_file', nargs='?', help='Output Excel file (optional)')
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch process PDF files')
    batch_parser.add_argument('pdf_directory', help='Directory containing PDF files')
    batch_parser.add_argument('output_file', nargs='?', 
                            default='signature_scan_results.xlsx',
                            help='Output Excel file (default: signature_scan_results.xlsx)')
    batch_parser.add_argument('--pattern', default='*.pdf', 
                            help='File pattern to match (default: *.pdf)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'single':
            if not Path(args.pdf_file).exists():
                print(f"Error: File not found: {args.pdf_file}")
                return 1
            
            print(f"Scanning single file: {args.pdf_file}")
            output_path = scan_single_file(args.pdf_file, args.output_file)
            print(f"Results saved to: {output_path}")
            
        elif args.command == 'batch':
            if not Path(args.pdf_directory).exists():
                print(f"Error: Directory not found: {args.pdf_directory}")
                return 1
            
            print(f"Batch processing directory: {args.pdf_directory}")
            print(f"File pattern: {args.pattern}")
            
            output_path = batch_process_pdfs(
                args.pdf_directory, 
                args.output_file, 
                args.pattern
            )
            print(f"Batch processing complete. Results saved to: {output_path}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())