"""
Tests for the main scanner functionality.
"""

import unittest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from credible_scanner.scanner import (
    credible_attachment_scanner,
    batch_process_pdfs,
    scan_single_file
)


class TestScanner(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_pdf_path = os.path.join(self.temp_dir, "test.pdf")
        
        # Create a mock PDF file
        with open(self.test_pdf_path, 'w') as f:
            f.write("mock pdf content")
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temp files
        if os.path.exists(self.test_pdf_path):
            os.remove(self.test_pdf_path)
        os.rmdir(self.temp_dir)
    
    def test_credible_attachment_scanner_file_not_found(self):
        """Test scanner behavior when PDF file doesn't exist."""
        result = credible_attachment_scanner("nonexistent.pdf")
        
        self.assertIn('error', result)
        self.assertIsNotNone(result['error'])
        self.assertIsNone(result['form_type'])
        self.assertEqual(result['signature_locations'], [])
    
    @patch('credible_scanner.scanner.save_results')
    @patch('credible_scanner.scanner.find_signature_areas')  
    @patch('credible_scanner.scanner.identify_form_type')
    @patch('credible_scanner.scanner.convert_from_path')
    def test_credible_attachment_scanner_success(
        self, mock_convert, mock_identify, mock_find_sigs, mock_save
    ):
        """Test successful scanning of a PDF file."""
        # Mock the dependencies
        mock_image = Mock()
        mock_convert.return_value = [mock_image]
        mock_identify.return_value = "DLA-20"
        mock_find_sigs.return_value = [
            {'x': 100, 'y': 200, 'width': 150, 'height': 40, 'type': 'box', 'confidence': 0.8}
        ]
        
        result = credible_attachment_scanner(self.test_pdf_path)
        
        self.assertEqual(result['file_path'], self.test_pdf_path)
        self.assertEqual(result['form_type'], "DLA-20")
        self.assertEqual(result['total_pages'], 1)
        self.assertEqual(result['signatures_found'], 1)
        self.assertIsNone(result['error'])
        self.assertEqual(len(result['signature_locations']), 1)
    
    @patch('credible_scanner.scanner.convert_from_path')
    def test_credible_attachment_scanner_pdf_conversion_failure(self, mock_convert):
        """Test scanner behavior when PDF conversion fails."""
        mock_convert.return_value = []  # Empty list indicates conversion failure
        
        result = credible_attachment_scanner(self.test_pdf_path)
        
        self.assertEqual(result['file_path'], self.test_pdf_path)
        self.assertIn('Failed to convert PDF to images', result['error'])
        self.assertIsNone(result['form_type'])
        self.assertEqual(result['signature_locations'], [])
    
    @patch('credible_scanner.scanner.convert_from_path')
    def test_credible_attachment_scanner_exception_handling(self, mock_convert):
        """Test scanner behavior when an exception occurs."""
        mock_convert.side_effect = Exception("Test exception")
        
        result = credible_attachment_scanner(self.test_pdf_path)
        
        self.assertEqual(result['file_path'], self.test_pdf_path)
        self.assertEqual(result['error'], "Test exception")
        self.assertIsNone(result['form_type'])
        self.assertEqual(result['signature_locations'], [])
    
    def test_batch_process_pdfs_directory_not_found(self):
        """Test batch processing when directory doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            batch_process_pdfs("nonexistent_directory")
    
    @patch('credible_scanner.scanner.save_results')
    @patch('credible_scanner.scanner.credible_attachment_scanner')
    def test_batch_process_pdfs_no_files(self, mock_scanner, mock_save):
        """Test batch processing when no PDF files are found."""
        # Create empty directory
        empty_dir = tempfile.mkdtemp()
        
        try:
            with self.assertRaises(ValueError):
                batch_process_pdfs(empty_dir)
        finally:
            os.rmdir(empty_dir)
    
    @patch('credible_scanner.scanner.save_results')
    @patch('credible_scanner.scanner.credible_attachment_scanner')
    def test_batch_process_pdfs_success(self, mock_scanner, mock_save):
        """Test successful batch processing."""
        # Create multiple test PDF files
        pdf1 = os.path.join(self.temp_dir, "test1.pdf")
        pdf2 = os.path.join(self.temp_dir, "test2.pdf")
        
        with open(pdf1, 'w') as f:
            f.write("mock pdf 1")
        with open(pdf2, 'w') as f:
            f.write("mock pdf 2")
        
        # Mock scanner results
        mock_scanner.side_effect = [
            {'file_path': pdf1, 'form_type': 'DLA-20', 'signatures_found': 1},
            {'file_path': pdf2, 'form_type': 'Treatment Plan', 'signatures_found': 2}
        ]
        mock_save.return_value = "output.xlsx"
        
        result = batch_process_pdfs(self.temp_dir, "batch_output.xlsx")
        
        self.assertEqual(result, "output.xlsx")
        self.assertEqual(mock_scanner.call_count, 2)
        mock_save.assert_called_once()
        
        # Clean up
        os.remove(pdf1)
        os.remove(pdf2)
    
    @patch('credible_scanner.scanner.save_results')
    @patch('credible_scanner.scanner.credible_attachment_scanner')
    def test_scan_single_file_default_output(self, mock_scanner, mock_save):
        """Test scanning single file with default output name."""
        mock_scanner.return_value = {
            'file_path': self.test_pdf_path,
            'form_type': 'DLA-20',
            'signatures_found': 1
        }
        mock_save.return_value = "test_signature_scan.xlsx"
        
        result = scan_single_file(self.test_pdf_path)
        
        self.assertEqual(result, "test_signature_scan.xlsx")
        mock_scanner.assert_called_once_with(self.test_pdf_path)
        
        # Check that save_results was called with correct default filename
        call_args = mock_save.call_args
        self.assertEqual(call_args[0][1], "test_signature_scan.xlsx")
    
    @patch('credible_scanner.scanner.save_results')
    @patch('credible_scanner.scanner.credible_attachment_scanner')
    def test_scan_single_file_custom_output(self, mock_scanner, mock_save):
        """Test scanning single file with custom output name."""
        mock_scanner.return_value = {
            'file_path': self.test_pdf_path,
            'form_type': 'Treatment Plan',
            'signatures_found': 2
        }
        mock_save.return_value = "custom_output.xlsx"
        
        result = scan_single_file(self.test_pdf_path, "custom_output.xlsx")
        
        self.assertEqual(result, "custom_output.xlsx")
        mock_scanner.assert_called_once_with(self.test_pdf_path)
        
        # Check that save_results was called with custom filename
        call_args = mock_save.call_args
        self.assertEqual(call_args[0][1], "custom_output.xlsx")


if __name__ == '__main__':
    unittest.main()