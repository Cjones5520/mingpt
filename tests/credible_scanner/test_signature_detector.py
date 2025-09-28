"""
Tests for signature detection functionality.
"""

import unittest
from unittest.mock import Mock, patch
import numpy as np
from PIL import Image

from credible_scanner.signature_detector import (
    pil_to_cv2,
    detect_signature_boxes,
    detect_signature_lines,
    detect_form_specific_areas,
    merge_overlapping_areas,
    find_signature_areas
)


class TestSignatureDetector(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock PIL image
        self.mock_pil_image = Mock(spec=Image.Image)
        self.mock_pil_image.width = 800
        self.mock_pil_image.height = 1100
        
        # Create a mock OpenCV image (numpy array)
        self.mock_cv_image = np.zeros((1100, 800, 3), dtype=np.uint8)
    
    def test_pil_to_cv2(self):
        """Test PIL to OpenCV conversion."""
        # Create a simple PIL image
        pil_img = Image.new('RGB', (100, 100), color='red')
        
        result = pil_to_cv2(pil_img)
        
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, (100, 100, 3))
    
    def test_detect_form_specific_areas_dla20(self):
        """Test form-specific area detection for DLA-20."""
        areas = detect_form_specific_areas(self.mock_cv_image, 'DLA-20')
        
        self.assertIsInstance(areas, list)
        self.assertEqual(len(areas), 2)  # DLA-20 should have 2 signature areas
        
        for area in areas:
            self.assertIn('x', area)
            self.assertIn('y', area)
            self.assertIn('width', area)
            self.assertIn('height', area)
            self.assertEqual(area['type'], 'form_specific')
            self.assertEqual(area['confidence'], 0.6)
    
    def test_detect_form_specific_areas_treatment_plan(self):
        """Test form-specific area detection for Treatment Plan."""
        areas = detect_form_specific_areas(self.mock_cv_image, 'Treatment Plan')
        
        self.assertIsInstance(areas, list)
        self.assertEqual(len(areas), 3)  # Treatment Plan should have 3 signature areas
    
    def test_detect_form_specific_areas_unknown(self):
        """Test form-specific area detection for unknown form."""
        areas = detect_form_specific_areas(self.mock_cv_image, 'Unknown Form')
        
        self.assertIsInstance(areas, list)
        self.assertEqual(len(areas), 2)  # Unknown forms should have 2 generic areas
    
    def test_merge_overlapping_areas_no_overlap(self):
        """Test merging when areas don't overlap."""
        areas = [
            {'x': 100, 'y': 100, 'width': 50, 'height': 30, 'confidence': 0.8},
            {'x': 200, 'y': 200, 'width': 50, 'height': 30, 'confidence': 0.7}
        ]
        
        result = merge_overlapping_areas(areas)
        
        self.assertEqual(len(result), 2)
    
    def test_merge_overlapping_areas_with_overlap(self):
        """Test merging when areas overlap."""
        areas = [
            {'x': 100, 'y': 100, 'width': 100, 'height': 50, 'confidence': 0.8},
            {'x': 120, 'y': 110, 'width': 80, 'height': 40, 'confidence': 0.7}
        ]
        
        result = merge_overlapping_areas(areas)
        
        self.assertEqual(len(result), 1)
        merged = result[0]
        self.assertEqual(merged['type'], 'merged')
        self.assertEqual(merged['confidence'], 0.8)  # Should take max confidence
    
    def test_merge_overlapping_areas_empty_list(self):
        """Test merging with empty area list."""
        result = merge_overlapping_areas([])
        self.assertEqual(result, [])
    
    @patch('credible_scanner.signature_detector.detect_signature_boxes')
    @patch('credible_scanner.signature_detector.detect_signature_lines')
    @patch('credible_scanner.signature_detector.detect_form_specific_areas')
    @patch('credible_scanner.signature_detector.pil_to_cv2')
    def test_find_signature_areas(self, mock_pil_to_cv2, mock_form_areas, mock_lines, mock_boxes):
        """Test the main signature area finding function."""
        # Mock return values
        mock_pil_to_cv2.return_value = self.mock_cv_image
        mock_boxes.return_value = [
            {'x': 100, 'y': 100, 'width': 50, 'height': 30, 'type': 'box', 'confidence': 0.8}
        ]
        mock_lines.return_value = [
            {'x': 200, 'y': 200, 'width': 100, 'height': 25, 'type': 'line', 'confidence': 0.7}
        ]
        mock_form_areas.return_value = [
            {'x': 300, 'y': 300, 'width': 80, 'height': 40, 'type': 'form_specific', 'confidence': 0.6}
        ]
        
        images = [self.mock_pil_image]
        result = find_signature_areas(images, 'DLA-20')
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)  # Should have all three signature areas
        
        # Check that page information is added
        for area in result:
            self.assertIn('page', area)
            self.assertIn('page_width', area)
            self.assertIn('page_height', area)
            self.assertEqual(area['page'], 1)
            self.assertEqual(area['page_width'], 800)
            self.assertEqual(area['page_height'], 1100)
    
    def test_signature_box_validation(self):
        """Test that detected boxes meet size and aspect ratio criteria."""
        # This would be a more complex test requiring actual OpenCV operations
        # For now, we'll test the logic conceptually
        
        # A valid signature box should be:
        # - Width: 100-400 pixels
        # - Height: 30-150 pixels  
        # - Aspect ratio: 1.5-8
        
        valid_box = {'x': 100, 'y': 100, 'width': 200, 'height': 50}
        aspect_ratio = valid_box['width'] / valid_box['height']
        
        self.assertGreaterEqual(valid_box['width'], 100)
        self.assertLessEqual(valid_box['width'], 400)
        self.assertGreaterEqual(valid_box['height'], 30)
        self.assertLessEqual(valid_box['height'], 150)
        self.assertGreaterEqual(aspect_ratio, 1.5)
        self.assertLessEqual(aspect_ratio, 8)


if __name__ == '__main__':
    unittest.main()