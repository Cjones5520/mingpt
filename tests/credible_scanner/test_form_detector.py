"""
Tests for form detection functionality.
"""

import unittest
from unittest.mock import Mock, patch
from PIL import Image
import numpy as np

# Import the modules to test
from credible_scanner.form_detector import (
    identify_form_type, 
    get_form_specific_keywords,
    analyze_form_structure,
    extract_text_from_image
)


class TestFormDetector(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock image
        self.mock_image = Mock(spec=Image.Image)
        self.mock_image.width = 800
        self.mock_image.height = 1100
    
    def test_get_form_specific_keywords(self):
        """Test that form-specific keywords are returned correctly."""
        # Test known form types
        dla_keywords = get_form_specific_keywords('DLA-20')
        self.assertIn('signature', dla_keywords)
        self.assertIn('veteran', dla_keywords)
        
        treatment_keywords = get_form_specific_keywords('Treatment Plan')
        self.assertIn('therapist', treatment_keywords)
        self.assertIn('client', treatment_keywords)
        
        # Test unknown form type
        unknown_keywords = get_form_specific_keywords('Unknown Form Type')
        self.assertIn('signature', unknown_keywords)
    
    @patch('credible_scanner.form_detector.pytesseract.image_to_string')
    def test_extract_text_from_image(self, mock_tesseract):
        """Test text extraction from image."""
        # Mock pytesseract response
        mock_tesseract.return_value = "Sample text from PDF"
        
        result = extract_text_from_image(self.mock_image)
        
        self.assertEqual(result, "SAMPLE TEXT FROM PDF")
        mock_tesseract.assert_called_once()
    
    @patch('credible_scanner.form_detector.extract_text_from_image')
    def test_identify_form_type_dla20(self, mock_extract):
        """Test identification of DLA-20 form."""
        # Mock text that would identify a DLA-20 form
        mock_extract.return_value = "DLA-20 DISABILITY RATING DEPARTMENT OF VETERANS AFFAIRS"
        
        result = identify_form_type(self.mock_image)
        
        self.assertEqual(result, "DLA-20")
    
    @patch('credible_scanner.form_detector.extract_text_from_image')
    def test_identify_form_type_treatment_plan(self, mock_extract):
        """Test identification of Treatment Plan form."""
        mock_extract.return_value = "INDIVIDUAL TREATMENT PLAN THERAPEUTIC GOALS"
        
        result = identify_form_type(self.mock_image)
        
        self.assertEqual(result, "Treatment Plan")
    
    @patch('credible_scanner.form_detector.extract_text_from_image')
    def test_identify_form_type_unknown(self, mock_extract):
        """Test handling of unknown form type."""
        mock_extract.return_value = "Some random text that doesn't match any patterns"
        
        result = identify_form_type(self.mock_image)
        
        self.assertEqual(result, "Unknown Form")
    
    @patch('credible_scanner.form_detector.extract_text_from_image')
    def test_identify_form_type_empty_text(self, mock_extract):
        """Test handling of empty text extraction."""
        mock_extract.return_value = ""
        
        result = identify_form_type(self.mock_image)
        
        self.assertIsNone(result)
    
    @patch('credible_scanner.form_detector.extract_text_from_image')
    def test_analyze_form_structure(self, mock_extract):
        """Test form structure analysis."""
        mock_extract.return_value = "Line 1\nClient signature required\nLine 3\nTherapist signature\nLine 5"
        
        result = analyze_form_structure(self.mock_image, "Treatment Plan")
        
        self.assertEqual(result['form_type'], "Treatment Plan")
        self.assertEqual(result['total_lines'], 5)
        self.assertGreater(result['keywords_found'], 0)
        self.assertIsInstance(result['signature_indicators'], list)


if __name__ == '__main__':
    unittest.main()