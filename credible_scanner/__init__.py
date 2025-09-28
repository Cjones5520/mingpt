"""
Credible PDF Signature Scanner

A tool for detecting signatures on service forms (e.g., DLA-20, Treatment Plans)
and standardizing the form processing workflow.
"""

from .scanner import credible_attachment_scanner, batch_process_pdfs
from .form_detector import identify_form_type
from .signature_detector import find_signature_areas
from .output_handler import save_results

__version__ = "1.0.0"
__all__ = [
    "credible_attachment_scanner",
    "batch_process_pdfs", 
    "identify_form_type",
    "find_signature_areas",
    "save_results"
]