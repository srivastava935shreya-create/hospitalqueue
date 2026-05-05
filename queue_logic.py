"""
Queue Logic Module
Core business logic for hospital queue management system
Handles priority calculation, token generation, and queue operations
"""

from datetime import datetime
import random

MIN_TOKEN = 1000
MAX_TOKEN = 9999

# ============================================================================
# TOKEN MANAGEMENT
# ============================================================================

def generate_token():
    """Generate a new unique token for patient"""
    return f'T-{random.randint(MIN_TOKEN, MAX_TOKEN)}'

def get_available_token(patients_dict):
    """
    Get an available token - reuse expired tokens or generate new one
    
    Args:
        patients_dict: Dictionary of all patients from database
        
    Returns:
        str: Available token number
    """
    if patients_dict:
        for key, patient in patients_dict.items():
            if patient.get('status') == 'expired':
                return patient['token']
    return generate_token()

# ============================================================================
# PRIORITY CALCULATION - AI Algorithm
# ============================================================================

def calculate_vitals_score(vitals):
    """Calculate priority score based on vital signs"""
    score = 0
    
    # Temperature scoring
    temp = vitals.get('temperature', 98.6)
    if temp > 103 or temp < 95:
        score += 40
    elif temp > 101 or temp < 96:
        score += 20
    
    # Heart rate scoring
    hr = vitals.get('heartRate', 72)
    if hr > 120 or hr < 50:
        score += 40
    elif hr > 100 or hr < 60:
        score += 20
    
    # Blood pressure scoring
    bp = vitals.get('bloodPressure', '120/80')
    try:
        systolic, diastolic = map(int, bp.split('/'))
        if systolic > 180 or systolic < 90 or diastolic > 120 or diastolic < 60:
            score += 40
        elif systolic > 140 or systolic < 100:
            score += 20
    except:
        pass
    
    return score

def calculate_symptoms_score(symptoms):
    """Calculate priority score based on reported symptoms"""
    score = 0
    symptoms_lower = symptoms.lower()
    
    critical_symptoms = [
        'chest pain', 'severe bleeding', 'unconscious', 'seizure',
        'stroke', 'heart attack', 'difficulty breathing', 'severe head injury'
    ]
    
    urgent_symptoms = [
        'fracture', 'severe pain', 'high fever', 'vomiting',
        'dizziness', 'confusion'
    ]
    
    if any(s in symptoms_lower for s in critical_symptoms):
        score += 50
    elif any(s in symptoms_lower for s in urgent_symptoms):
        score += 30
    
    return score

def calculate_age_score(age):
    """Calculate priority score based on age"""
    score = 0
    
    # Vulnerable age groups
    if age < 2 or age > 70:
        score += 15
    elif age < 12 or age > 60:
        score += 10
    
    return score

def calculate_priority(patient):
    """
    Calculate priority level and color based on patient data
    Uses AI-based scoring system combining vitals, symptoms, and age
    
    Args:
        patient: Dictionary containing patient data
        
    Returns:
        dict: {'level': 'Critical|Emergency|Urgent|Non-urgent', 'color': '#hex_color'}
    """
    total_score = 0
    
    # Calculate individual scores
    total_score += calculate_vitals_score(patient.get('vitals', {}))
    total_score += calculate_symptoms_score(patient.get('symptoms', ''))
    total_score += calculate_age_score(patient.get('age', 30))
    
    # Determine priority level and color
    if total_score >= 80:
        return {'level': 'Critical', 'color': '#dc2626'}
    elif total_score >= 50:
        return {'level': 'Emergency', 'color': '#ea580c'}
    elif total_score >= 30:
        return {'level': 'Urgent', 'color': '#f59e0b'}
    else:
        return {'level': 'Non-urgent', 'color': '#16a34a'}

# ============================================================================
# WAIT TIME ESTIMATION
# ============================================================================

def get_wait_time(priority_level):
    """
    Get estimated wait time based on priority level
    
    Args:
        priority_level: str - 'Critical', 'Emergency', 'Urgent', or 'Non-urgent'
        
    Returns:
        str: Estimated wait time range (e.g., '0-5 minutes')
    """
    wait_times = {
        'Critical': '0-5',
        'Emergency': '5-15',
        'Urgent': '15-30',
        'Non-urgent': '30-60'
    }
    return f"{wait_times.get(priority_level, '30-60')} minutes"

# ============================================================================
# PATIENT RECORD CREATION
# ============================================================================

def create_patient_record(form_data):
    """
    Create a complete patient record from form data
    
    Args:
        form_data: Dictionary with keys: name, age, contact, symptoms, 
                   temperature, bloodPressure, heartRate
        
    Returns:
        dict: Complete patient record ready for database
    """
    patient = {
        'name': form_data.get('name', ''),
        'age': int(form_data.get('age', 30)),
        'contact': form_data.get('contact', ''),
        'symptoms': form_data.get('symptoms', ''),
        'vitals': {
            'temperature': float(form_data.get('temperature', 98.6)),
            'bloodPressure': form_data.get('bloodPressure', '120/80'),
            'heartRate': int(form_data.get('heartRate', 72))
        },
        'token': generate_token(),
        'status': 'waiting',
        'registeredAt': datetime.now().isoformat(),
        'priority': calculate_priority({
            'age': int(form_data.get('age', 30)),
            'symptoms': form_data.get('symptoms', ''),
            'vitals': {
                'temperature': float(form_data.get('temperature', 98.6)),
                'bloodPressure': form_data.get('bloodPressure', '120/80'),
                'heartRate': int(form_data.get('heartRate', 72))
            }
        })
    }
    
    patient['priorityLevel'] = patient['priority']['level']
    patient['priorityColor'] = patient['priority']['color']
    
    return patient

# ============================================================================
# QUEUE OPERATIONS
# ============================================================================

def get_queue_stats(patients_dict):
    """
    Calculate queue statistics
    
    Args:
        patients_dict: Dictionary of all patients
        
    Returns:
        dict: Statistics containing counts by status
    """
    if not patients_dict:
        return {
            'waiting': 0,
            'in_consultation': 0,
            'completed': 0,
            'total': 0
        }
    
    patients = list(patients_dict.values())
    return {
        'waiting': len([p for p in patients if p.get('status') == 'waiting']),
        'in_consultation': len([p for p in patients if p.get('status') == 'in-consultation']),
        'completed': len([p for p in patients if p.get('status') == 'completed']),
        'total': len(patients)
    }

def get_priority_color(priority_level):
    """Get color code for priority level"""
    colors = {
        'Critical': '#dc2626',
        'Emergency': '#ea580c',
        'Urgent': '#f59e0b',
        'Non-urgent': '#16a34a'
    }
    return colors.get(priority_level, '#666')

def calculate_wait_time_remaining(registered_at, max_wait_minutes=30):
    """
    Calculate remaining wait time for a patient
    
    Args:
        registered_at: ISO format timestamp of registration
        max_wait_minutes: Maximum wait time in minutes
        
    Returns:
        int: Minutes remaining (minimum 0)
    """
    try:
        reg_time = datetime.fromisoformat(registered_at)
        now = datetime.now()
        elapsed = (now - reg_time).total_seconds() / 60
        return max(0, int(max_wait_minutes - elapsed))
    except:
        return max_wait_minutes
