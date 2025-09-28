#!/usr/bin/env python3
"""
Create sample PDF files for testing the batch compliance scanner.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


def create_test_pdf(filename: str, content: str):
    """Create a PDF with the given content."""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Add content as paragraphs
    lines = content.split('\n')
    for line in lines:
        if line.strip():
            p = Paragraph(line.strip(), styles['Normal'])
            story.append(p)
            story.append(Spacer(1, 0.2*inch))
    
    doc.build(story)


def main():
    """Create sample PDF files for testing."""
    test_folder = "test_pdfs"
    os.makedirs(test_folder, exist_ok=True)
    
    # Test PDF 1: DLA-20 form
    dla20_content = """
    DEFENSE LOGISTICS AGENCY
    DLA-20 FORM
    
    REQUEST FOR MILITARY SUPPLIES
    
    This is a DLA-20 defense logistics form for requesting military supplies.
    
    APPLICANT SIGNATURE: _________________________
    
    DATE: _______________
    """
    
    create_test_pdf(f"{test_folder}/dla20_form.pdf", dla20_content)
    print("Created: dla20_form.pdf")
    
    # Test PDF 2: Credible Plan form
    credible_content = """
    CREDIBLE PLAN FORM
    
    HEALTHCARE CREDIBLE PLAN APPLICATION
    
    This document contains information about the credible plan for healthcare services.
    
    Please complete all sections and return to the appropriate office.
    
    SIGNATURE REQUIRED: ________________________
    """
    
    create_test_pdf(f"{test_folder}/credible_plan.pdf", credible_content)
    print("Created: credible_plan.pdf")
    
    # Test PDF 3: Consumer Choice form
    consumer_content = """
    CONSUMER CHOICE FORM
    
    CONSUMER CHOICE PROGRAM APPLICATION
    
    This form is for enrolling in the consumer choice program.
    
    Complete and submit this form to participate.
    
    No signature needed for this document.
    """
    
    create_test_pdf(f"{test_folder}/consumer_choice.pdf", consumer_content)
    print("Created: consumer_choice.pdf")
    
    # Test PDF 4: Generic form
    generic_content = """
    FORM 456-A
    
    GENERAL APPLICATION FORM
    
    This is a general application form for various services.
    
    Please fill out all required fields.
    
    AUTHORIZED SIGNATURE: _____________________
    """
    
    create_test_pdf(f"{test_folder}/generic_form.pdf", generic_content)
    print("Created: generic_form.pdf")
    
    # Test PDF 5: Unknown form type
    unknown_content = """
    RANDOM DOCUMENT
    
    This is a random document that doesn't match any form patterns.
    
    It contains various information but no specific form indicators.
    
    Some random text here and there.
    """
    
    create_test_pdf(f"{test_folder}/unknown_doc.pdf", unknown_content)
    print("Created: unknown_doc.pdf")
    
    print(f"\nAll test PDFs created in '{test_folder}' folder")


if __name__ == "__main__":
    main()