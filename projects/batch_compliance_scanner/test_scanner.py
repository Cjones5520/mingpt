#!/usr/bin/env python3
"""
Simple test script for the batch compliance scanner functions.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from batch_compliance_scanner import detect_form_type, detect_signature, configure_tesseract


def test_form_type_detection():
    """Test form type detection with sample text."""
    print("=== Testing Form Type Detection ===")
    
    test_cases = [
        ("This is a DLA-20 defense logistics form", "DLA-20"),
        ("CREDIBLE PLAN FORM APPLICATION", "Credible Plan"),
        ("CONSUMER CHOICE FORM REQUEST", "Consumer Choice"),
        ("This is a FORM 123 application", "Generic Form"),
        ("Random text with no form indicators", "Unknown")
    ]
    
    for text, expected in test_cases:
        form_type, confidence = detect_form_type(text)
        print(f"Text: '{text[:50]}...'")
        print(f"  Detected: {form_type} (confidence: {confidence})")
        print(f"  Expected: {expected}")
        print(f"  Result: {'✓' if form_type == expected else '✗'}")
        print()


def test_signature_detection():
    """Test signature detection with sample text."""
    print("=== Testing Signature Detection ===")
    
    test_cases = [
        ("Please sign here: SIGNATURE _____________", True),
        ("Document has been SIGNED by applicant", True),
        ("APPLICANT SIGNATURE required", True),
        ("No signature needed for this document", False),
        ("Random text without signature indicators", False)
    ]
    
    for text, expected in test_cases:
        has_signature = detect_signature(text)
        print(f"Text: '{text}'")
        print(f"  Detected: {has_signature}")
        print(f"  Expected: {expected}")
        print(f"  Result: {'✓' if has_signature == expected else '✗'}")
        print()


def test_tesseract_configuration():
    """Test Tesseract configuration."""
    print("=== Testing Tesseract Configuration ===")
    
    try:
        configure_tesseract()
        print("✓ Tesseract configuration completed successfully")
        
        # Try to import pytesseract and check if it works
        import pytesseract
        print("✓ pytesseract imported successfully")
        
        # Test if tesseract is accessible (this might fail in some environments)
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✓ Tesseract version: {version}")
        except Exception as e:
            print(f"⚠ Tesseract version check failed: {e}")
            print("  This might be normal in some environments")
        
    except Exception as e:
        print(f"✗ Tesseract configuration failed: {e}")


def main():
    """Run all tests."""
    print("Batch Compliance Scanner - Function Tests")
    print("=" * 50)
    
    test_form_type_detection()
    test_signature_detection()
    test_tesseract_configuration()
    
    print("=" * 50)
    print("Tests completed!")


if __name__ == "__main__":
    main()