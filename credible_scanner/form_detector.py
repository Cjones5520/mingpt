"""
Form type identification using OCR text recognition.

Uses pytesseract to identify form types based on keywords and patterns.
"""

import re
from typing import Dict, List, Optional
from PIL import Image
import pytesseract


# Form type keywords and patterns
FORM_PATTERNS = {
    'DLA-20': [
        r'DLA-20',
        r'DISABILITY\s+RATING',
        r'DEPARTMENT\s+OF\s+VETERANS\s+AFFAIRS',
        r'VA\s+FORM\s+21-0960'
    ],
    'Treatment Plan': [
        r'TREATMENT\s+PLAN',
        r'INDIVIDUAL\s+TREATMENT\s+PLAN',
        r'CARE\s+PLAN',
        r'THERAPEUTIC\s+GOALS',
        r'TREATMENT\s+GOALS'
    ],
    'Progress Note': [
        r'PROGRESS\s+NOTE',
        r'CLINICAL\s+NOTE',
        r'SESSION\s+NOTE',
        r'THERAPY\s+NOTE'
    ],
    'Assessment': [
        r'ASSESSMENT',
        r'CLINICAL\s+ASSESSMENT',
        r'PSYCHOLOGICAL\s+ASSESSMENT',
        r'MENTAL\s+HEALTH\s+ASSESSMENT'
    ],
    'Intake Form': [
        r'INTAKE\s+FORM',
        r'INITIAL\s+ASSESSMENT',
        r'CLIENT\s+INTAKE',
        r'ADMISSION\s+FORM'
    ]
}


def extract_text_from_image(image: Image.Image) -> str:
    """
    Extract text from an image using OCR.
    
    Args:
        image (PIL.Image): Image to extract text from
        
    Returns:
        str: Extracted text
    """
    try:
        # Use pytesseract to extract text
        # Configure for better text recognition
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)
        return text.upper()  # Convert to uppercase for consistent matching
    except Exception as e:
        print(f"Warning: OCR text extraction failed: {e}")
        return ""


def identify_form_type(image: Image.Image) -> Optional[str]:
    """
    Identify the form type based on OCR text analysis.
    
    Args:
        image (PIL.Image): First page image of the PDF
        
    Returns:
        Optional[str]: Identified form type or None if not recognized
    """
    # Extract text from the image
    text = extract_text_from_image(image)
    
    if not text.strip():
        return None
    
    # Check for form patterns
    form_scores = {}
    
    for form_type, patterns in FORM_PATTERNS.items():
        score = 0
        for pattern in patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches
        
        if score > 0:
            form_scores[form_type] = score
    
    # Return the form type with the highest score
    if form_scores:
        best_match = max(form_scores, key=form_scores.get)
        return best_match
    
    return "Unknown Form"


def get_form_specific_keywords(form_type: str) -> List[str]:
    """
    Get keywords specific to a form type for enhanced detection.
    
    Args:
        form_type (str): The identified form type
        
    Returns:
        List[str]: List of keywords specific to the form type
    """
    form_keywords = {
        'DLA-20': ['signature', 'veteran', 'examiner', 'date signed'],
        'Treatment Plan': ['therapist', 'client', 'provider', 'signature', 'date'],
        'Progress Note': ['clinician', 'signature', 'date', 'reviewed by'],
        'Assessment': ['assessor', 'signature', 'date completed', 'supervisor'],
        'Intake Form': ['client signature', 'staff signature', 'date', 'witness'],
        'Unknown Form': ['signature', 'signed', 'date']
    }
    
    return form_keywords.get(form_type, form_keywords['Unknown Form'])


def analyze_form_structure(image: Image.Image, form_type: str) -> Dict[str, any]:
    """
    Analyze the structure of the form to help with signature detection.
    
    Args:
        image (PIL.Image): Form image
        form_type (str): Identified form type
        
    Returns:
        Dict[str, any]: Structure analysis results
    """
    text = extract_text_from_image(image)
    keywords = get_form_specific_keywords(form_type)
    
    # Look for signature-related text positions
    signature_indicators = []
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        for keyword in keywords:
            if keyword.lower() in line.lower():
                signature_indicators.append({
                    'line_number': i,
                    'text': line.strip(),
                    'keyword': keyword
                })
    
    return {
        'form_type': form_type,
        'total_lines': len(lines),
        'signature_indicators': signature_indicators,
        'keywords_found': len(signature_indicators)
    }