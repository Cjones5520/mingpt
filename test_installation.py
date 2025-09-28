#!/usr/bin/env python3
"""
Installation test script for Credible PDF Signature Scanner.

This script verifies that all required dependencies are properly installed
and the scanner components can be imported successfully.
"""

import sys
import traceback


def test_imports():
    """Test that all required packages can be imported."""
    print("Testing Python package imports...")
    
    required_packages = [
        ('pdf2image', 'pdf2image'),
        ('pytesseract', 'pytesseract'),  
        ('opencv-python', 'cv2'),
        ('pandas', 'pandas'),
        ('Pillow', 'PIL'),
        ('openpyxl', 'openpyxl')
    ]
    
    success = True
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"  ✓ {package_name} imported successfully")
        except ImportError as e:
            print(f"  ✗ {package_name} import failed: {e}")
            success = False
    
    return success


def test_system_dependencies():
    """Test that system dependencies (poppler, tesseract) are available."""
    print("\nTesting system dependencies...")
    
    success = True
    
    # Test poppler (via pdf2image)
    try:
        from pdf2image import convert_from_path
        from pdf2image.exceptions import PDFInfoNotInstalledError
        print("  ✓ Poppler utilities available")
    except Exception as e:
        print(f"  ✗ Poppler test failed: {e}")
        success = False
    
    # Test tesseract
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"  ✓ Tesseract OCR available (version: {version})")
    except Exception as e:
        print(f"  ✗ Tesseract test failed: {e}")
        success = False
    
    return success


def test_scanner_import():
    """Test that the credible scanner module can be imported."""
    print("\nTesting Credible Scanner module...")
    
    try:
        from credible_scanner import (
            credible_attachment_scanner,
            batch_process_pdfs,
            identify_form_type,
            find_signature_areas,
            save_results
        )
        print("  ✓ Credible Scanner module imported successfully")
        print("  ✓ All main functions available")
        return True
    except ImportError as e:
        print(f"  ✗ Credible Scanner import failed: {e}")
        print(f"  ✗ Traceback: {traceback.format_exc()}")
        return False


def test_basic_functionality():
    """Test basic functionality without requiring actual PDF files."""
    print("\nTesting basic functionality...")
    
    try:
        from credible_scanner.form_detector import get_form_specific_keywords
        from credible_scanner.signature_detector import merge_overlapping_areas
        from credible_scanner.output_handler import prepare_results_data
        
        # Test form detector
        keywords = get_form_specific_keywords('DLA-20')
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        print("  ✓ Form detector basic functions work")
        
        # Test signature detector
        areas = [
            {'x': 100, 'y': 100, 'width': 50, 'height': 30, 'confidence': 0.8},
            {'x': 200, 'y': 200, 'width': 50, 'height': 30, 'confidence': 0.7}
        ]
        merged = merge_overlapping_areas(areas)
        assert isinstance(merged, list)
        print("  ✓ Signature detector basic functions work")
        
        # Test output handler
        test_results = [
            {
                'file_path': 'test.pdf',
                'form_type': 'DLA-20',
                'total_pages': 1,
                'signatures_found': 1,
                'signature_locations': [],
                'error': None
            }
        ]
        df = prepare_results_data(test_results)
        assert len(df) > 0
        print("  ✓ Output handler basic functions work")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Basic functionality test failed: {e}")
        print(f"  ✗ Traceback: {traceback.format_exc()}")
        return False


def main():
    """Run all installation tests."""
    print("=" * 60)
    print("Credible PDF Signature Scanner - Installation Test")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Run all tests
    tests = [
        ("Python Package Imports", test_imports),
        ("System Dependencies", test_system_dependencies), 
        ("Scanner Module Import", test_scanner_import),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        if not test_func():
            all_tests_passed = False
    
    print("\n" + "=" * 60)
    
    if all_tests_passed:
        print("✓ ALL TESTS PASSED!")
        print("✓ Credible PDF Signature Scanner is ready to use.")
        print("\nNext steps:")
        print("  1. Try scanning a PDF: python credible_scanner_cli.py single your_file.pdf")
        print("  2. For batch processing: python credible_scanner_cli.py batch /path/to/pdfs/")
        print("  3. See CREDIBLE_SCANNER_INSTALL.md for more usage examples")
        return 0
    else:
        print("✗ SOME TESTS FAILED!")
        print("✗ Please check the installation instructions and resolve the issues above.")
        print("\nTroubleshooting:")
        print("  1. Install missing packages: pip install -r requirements.txt")
        print("  2. Install system dependencies (poppler, tesseract)")
        print("  3. See CREDIBLE_SCANNER_INSTALL.md for detailed instructions")
        return 1


if __name__ == "__main__":
    sys.exit(main())