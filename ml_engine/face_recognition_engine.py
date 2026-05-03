"""
Face Recognition Engine
Uses OpenCV and face_recognition library to detect and match faces
"""
import os
import json

try:
    import cv2
    import face_recognition
    import numpy as np
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    print("face_recognition or opencv-python not installed. Face recognition disabled.")


def detect_faces(image_path):
    """
    Detect faces in an image and extract encodings
    
    Args:
        image_path (str): Path to image file
    
    Returns:
        tuple: (number_of_faces, list_of_encodings)
    """
    if not FACE_RECOGNITION_AVAILABLE:
        return 0, []
    
    try:
        # Load image
        image = face_recognition.load_image_file(image_path)
        
        # Detect face locations
        face_locations = face_recognition.face_locations(image)
        
        # Get face encodings
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        # Convert numpy arrays to lists for JSON storage
        encodings_list = [encoding.tolist() for encoding in face_encodings]
        
        return len(face_locations), encodings_list
    
    except Exception as e:
        print(f"Face detection error: {e}")
        return 0, []


def compare_faces(known_encoding, unknown_encoding, tolerance=0.6):
    """
    Compare two face encodings
    
    Args:
        known_encoding (list): Known face encoding
        unknown_encoding (list): Unknown face encoding
        tolerance (float): Matching tolerance (lower is stricter)
    
    Returns:
        tuple: (is_match, distance)
    """
    if not FACE_RECOGNITION_AVAILABLE:
        return False, 1.0
    
    try:
        # Convert lists back to numpy arrays
        known = np.array(known_encoding)
        unknown = np.array(unknown_encoding)
        
        # Calculate face distance
        face_distance = face_recognition.face_distance([known], unknown)[0]
        
        # Check if match
        is_match = face_distance < tolerance
        
        return is_match, float(face_distance)
    
    except Exception as e:
        print(f"Face comparison error: {e}")
        return False, 1.0


def find_matching_suspects(suspect_encodings, evidence_encodings, tolerance=0.6):
    """
    Find matching faces between suspects and evidence
    
    Args:
        suspect_encodings (list): List of suspect face encodings
        evidence_encodings (list): List of evidence face encodings
        tolerance (float): Matching tolerance
    
    Returns:
        list: List of matches with indices and distances
    """
    if not FACE_RECOGNITION_AVAILABLE:
        return []
    
    matches = []
    
    try:
        for i, suspect_enc in enumerate(suspect_encodings):
            for j, evidence_enc in enumerate(evidence_encodings):
                is_match, distance = compare_faces(suspect_enc, evidence_enc, tolerance)
                
                if is_match:
                    matches.append({
                        'suspect_index': i,
                        'evidence_index': j,
                        'distance': distance,
                        'confidence': 1.0 - distance  # Convert distance to confidence
                    })
    
    except Exception as e:
        print(f"Error finding matches: {e}")
    
    return matches


def extract_face_image(image_path, output_path):
    """
    Extract and save detected faces from an image
    
    Args:
        image_path (str): Input image path
        output_path (str): Output directory for face images
    
    Returns:
        list: Paths to saved face images
    """
    if not FACE_RECOGNITION_AVAILABLE:
        return []
    
    try:
        # Load image
        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_image)
        
        saved_faces = []
        
        for i, (top, right, bottom, left) in enumerate(face_locations):
            # Extract face
            face_image = image[top:bottom, left:right]
            
            # Save face
            face_filename = f"face_{i}.jpg"
            face_path = os.path.join(output_path, face_filename)
            cv2.imwrite(face_path, face_image)
            
            saved_faces.append(face_path)
        
        return saved_faces
    
    except Exception as e:
        print(f"Error extracting faces: {e}")
        return []


def analyze_image(image_path):
    """
    Comprehensive image analysis
    
    Args:
        image_path (str): Path to image
    
    Returns:
        dict: Analysis results
    """
    result = {
        'faces_detected': 0,
        'face_locations': [],
        'face_encodings': [],
        'image_size': None,
        'error': None
    }
    
    if not FACE_RECOGNITION_AVAILABLE:
        result['error'] = 'Face recognition not available'
        return result
    
    try:
        # Load image
        image = face_recognition.load_image_file(image_path)
        result['image_size'] = image.shape
        
        # Detect faces
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        result['faces_detected'] = len(face_locations)
        result['face_locations'] = face_locations
        result['face_encodings'] = [enc.tolist() for enc in face_encodings]
    
    except Exception as e:
        result['error'] = str(e)
    
    return result
