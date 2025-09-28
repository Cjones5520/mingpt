"""
Signature detection using computer vision techniques.

Uses OpenCV to detect signature boxes, lines, and potential signature areas
without relying on OCR for signature recognition.
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
from PIL import Image


def pil_to_cv2(pil_image: Image.Image) -> np.ndarray:
    """
    Convert PIL Image to OpenCV format.
    
    Args:
        pil_image (PIL.Image): PIL Image object
        
    Returns:
        np.ndarray: OpenCV image array
    """
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


def detect_signature_boxes(image: np.ndarray) -> List[Dict[str, int]]:
    """
    Detect rectangular signature boxes in the image.
    
    Args:
        image (np.ndarray): OpenCV image array
        
    Returns:
        List[Dict[str, int]]: List of detected boxes with coordinates
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    signature_boxes = []
    
    for contour in contours:
        # Approximate the contour
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Check if it's roughly rectangular (4 corners)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by size - typical signature boxes
            if 100 < w < 400 and 30 < h < 150:
                # Check aspect ratio (signature boxes are usually wider than tall)
                aspect_ratio = w / h
                if 1.5 < aspect_ratio < 8:
                    signature_boxes.append({
                        'x': int(x),
                        'y': int(y),
                        'width': int(w),
                        'height': int(h),
                        'type': 'box',
                        'confidence': 0.8
                    })
    
    return signature_boxes


def detect_signature_lines(image: np.ndarray) -> List[Dict[str, int]]:
    """
    Detect horizontal signature lines in the image.
    
    Args:
        image (np.ndarray): OpenCV image array
        
    Returns:
        List[Dict[str, int]]: List of detected signature lines with coordinates
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Use HoughLinesP to detect lines
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80, minLineLength=100, maxLineGap=10)
    
    signature_lines = []
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # Check if it's roughly horizontal
            angle = abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)
            if angle < 15 or angle > 165:  # Horizontal lines (allowing some tolerance)
                length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                
                # Filter by length - signature lines should be reasonably long
                if length > 100:
                    # Create bounding box around the line
                    x = min(x1, x2)
                    y = min(y1, y2) - 10  # Add some padding above the line
                    w = int(length)
                    h = 25  # Standard height for signature area
                    
                    signature_lines.append({
                        'x': int(x),
                        'y': int(y),
                        'width': int(w),
                        'height': int(h),
                        'type': 'line',
                        'confidence': 0.7
                    })
    
    return signature_lines


def detect_form_specific_areas(
    image: np.ndarray, 
    form_type: str
) -> List[Dict[str, int]]:
    """
    Detect signature areas based on form-specific patterns.
    
    Args:
        image (np.ndarray): OpenCV image array
        form_type (str): Type of form being processed
        
    Returns:
        List[Dict[str, int]]: List of detected signature areas
    """
    height, width = image.shape[:2]
    signature_areas = []
    
    # Form-specific signature location patterns
    if form_type == 'DLA-20':
        # DLA-20 forms typically have signatures at the bottom
        areas = [
            {'x': int(width * 0.1), 'y': int(height * 0.8), 
             'width': int(width * 0.35), 'height': 50},
            {'x': int(width * 0.55), 'y': int(height * 0.8), 
             'width': int(width * 0.35), 'height': 50}
        ]
    elif form_type == 'Treatment Plan':
        # Treatment plans often have multiple signature areas
        areas = [
            {'x': int(width * 0.1), 'y': int(height * 0.7), 
             'width': int(width * 0.4), 'height': 40},
            {'x': int(width * 0.1), 'y': int(height * 0.8), 
             'width': int(width * 0.4), 'height': 40},
            {'x': int(width * 0.55), 'y': int(height * 0.8), 
             'width': int(width * 0.4), 'height': 40}
        ]
    else:
        # Generic signature areas for unknown forms
        areas = [
            {'x': int(width * 0.1), 'y': int(height * 0.85), 
             'width': int(width * 0.35), 'height': 40},
            {'x': int(width * 0.55), 'y': int(height * 0.85), 
             'width': int(width * 0.35), 'height': 40}
        ]
    
    for area in areas:
        area.update({
            'type': 'form_specific',
            'confidence': 0.6
        })
        signature_areas.append(area)
    
    return signature_areas


def merge_overlapping_areas(areas: List[Dict[str, int]]) -> List[Dict[str, int]]:
    """
    Merge overlapping signature areas to avoid duplicates.
    
    Args:
        areas (List[Dict[str, int]]): List of signature areas
        
    Returns:
        List[Dict[str, int]]: Merged list of non-overlapping areas
    """
    if not areas:
        return []
    
    # Sort by y-coordinate then x-coordinate
    sorted_areas = sorted(areas, key=lambda a: (a['y'], a['x']))
    
    merged = [sorted_areas[0]]
    
    for current in sorted_areas[1:]:
        last_merged = merged[-1]
        
        # Check for overlap
        if (current['x'] < last_merged['x'] + last_merged['width'] and
            current['y'] < last_merged['y'] + last_merged['height'] and
            current['x'] + current['width'] > last_merged['x'] and
            current['y'] + current['height'] > last_merged['y']):
            
            # Merge overlapping areas
            new_x = min(last_merged['x'], current['x'])
            new_y = min(last_merged['y'], current['y'])
            new_width = max(last_merged['x'] + last_merged['width'], 
                           current['x'] + current['width']) - new_x
            new_height = max(last_merged['y'] + last_merged['height'], 
                            current['y'] + current['height']) - new_y
            
            merged[-1] = {
                'x': new_x,
                'y': new_y,
                'width': new_width,
                'height': new_height,
                'type': 'merged',
                'confidence': max(last_merged['confidence'], current['confidence'])
            }
        else:
            merged.append(current)
    
    return merged


def find_signature_areas(
    images: List[Image.Image], 
    form_type: Optional[str] = None
) -> List[Dict[str, any]]:
    """
    Find signature areas in all pages of a document.
    
    Args:
        images (List[PIL.Image]): List of page images
        form_type (Optional[str]): Type of form being processed
        
    Returns:
        List[Dict[str, any]]: List of detected signature areas with page info
    """
    all_signature_areas = []
    
    for page_num, pil_image in enumerate(images):
        # Convert PIL to OpenCV
        cv_image = pil_to_cv2(pil_image)
        
        # Detect different types of signature areas
        boxes = detect_signature_boxes(cv_image)
        lines = detect_signature_lines(cv_image)
        form_areas = detect_form_specific_areas(cv_image, form_type or "Unknown Form")
        
        # Combine all detected areas
        page_areas = boxes + lines + form_areas
        
        # Merge overlapping areas
        merged_areas = merge_overlapping_areas(page_areas)
        
        # Add page information
        for area in merged_areas:
            area.update({
                'page': page_num + 1,
                'page_width': pil_image.width,
                'page_height': pil_image.height
            })
            all_signature_areas.append(area)
    
    return all_signature_areas