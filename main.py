"""
Hospital Queue Management System - Flask Backend
RESTful API for patient registration, queue management, and staff operations
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

# Import custom modules
from queue_logic import (
    create_patient_record, calculate_priority, get_wait_time,
    get_queue_stats, get_priority_color, calculate_wait_time_remaining,
    get_available_token
)
from firebase_config import get_database

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
STAFF_PASSWORD = os.getenv('STAFF_PASSWORD', 'staff123')
PORT = int(os.getenv('PORT', 5000))

# Get Firebase database reference
db = get_database()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def error_response(message, status_code=400):
    """Return standardized error response"""
    return jsonify({'error': message, 'success': False}), status_code

def success_response(data=None, message='Success', status_code=200):
    """Return standardized success response"""
    response = {'success': True, 'message': message}
    if data:
        response['data'] = data
    return jsonify(response), status_code

# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return success_response({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# ============================================================================
# PATIENT REGISTRATION
# ============================================================================

@app.route('/api/register', methods=['POST'])
def register_patient():
    """
    Register a new patient
    
    Expected JSON:
    {
        "name": "John Doe",
        "age": 30,
        "contact": "555-1234",
        "symptoms": "chest pain",
        "temperature": 102.5,
        "bloodPressure": "140/90",
        "heartRate": 95
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'age', 'contact', 'symptoms']
        if not all(field in data for field in required_fields):
            return error_response('Missing required fields')
        
        # Create patient record
        patient = create_patient_record(data)
        
        if db:
            # Save to Firebase
            db.child('patients').push(patient)
        
        return success_response(
            {
                'token': patient['token'],
                'priority': patient['priorityLevel'],
                'color': patient['priorityColor'],
                'waitTime': get_wait_time(patient['priorityLevel']),
                'registeredAt': patient['registeredAt']
            },
            'Patient registered successfully',
            201
        )
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return error_response(f'Registration failed: {str(e)}', 500)

# ============================================================================
# QUEUE MANAGEMENT - PUBLIC VIEW
# ============================================================================

@app.route('/api/patients', methods=['GET'])
def get_patients():
    """Get all patients in queue"""
    try:
        if db:
            patients_data = db.child('patients').get().val()
        else:
            patients_data = {}
        
        if not patients_data:
            return success_response({'patients': [], 'stats': get_queue_stats(None)})
        
        # Format patient data
        formatted_patients = []
        for key, patient in patients_data.items():
            wait_remaining = calculate_wait_time_remaining(patient.get('registeredAt'))
            formatted_patients.append({
                'id': key,
                'name': patient.get('name'),
                'age': patient.get('age'),
                'token': patient.get('token'),
                'symptoms': patient.get('symptoms'),
                'priority': patient.get('priorityLevel'),
                'status': patient.get('status'),
                'waitTimeRemaining': wait_remaining
            })
        
        return success_response({
            'patients': formatted_patients,
            'stats': get_queue_stats(patients_data)
        })
        
    except Exception as e:
        logger.error(f"Get patients error: {str(e)}")
        return error_response(f'Failed to fetch patients: {str(e)}', 500)

@app.route('/api/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get specific patient details"""
    try:
        if db:
            patient = db.child('patients').child(patient_id).get().val()
        else:
            patient = None
        
        if not patient:
            return error_response('Patient not found', 404)
        
        wait_remaining = calculate_wait_time_remaining(patient.get('registeredAt'))
        
        return success_response({
            'id': patient_id,
            'name': patient.get('name'),
            'age': patient.get('age'),
            'contact': patient.get('contact'),
            'token': patient.get('token'),
            'symptoms': patient.get('symptoms'),
            'vitals': patient.get('vitals'),
            'priority': patient.get('priorityLevel'),
            'status': patient.get('status'),
            'waitTimeRemaining': wait_remaining,
            'registeredAt': patient.get('registeredAt')
        })
        
    except Exception as e:
        logger.error(f"Get patient error: {str(e)}")
        return error_response(f'Failed to fetch patient: {str(e)}', 500)

# ============================================================================
# STAFF OPERATIONS
# ============================================================================

@app.route('/api/staff/authenticate', methods=['POST'])
def staff_auth():
    """Authenticate staff member"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        if password == STAFF_PASSWORD:
            return success_response({'authenticated': True}, 'Staff authenticated')
        else:
            return error_response('Invalid password', 401)
            
    except Exception as e:
        logger.error(f"Staff auth error: {str(e)}")
        return error_response(f'Authentication failed: {str(e)}', 500)

@app.route('/api/staff/patients', methods=['GET'])
def staff_get_patients():
    """Get all patients for staff view"""
    try:
        if db:
            patients_data = db.child('patients').get().val()
        else:
            patients_data = {}
        
        if not patients_data:
            return success_response({
                'waiting': [],
                'inConsultation': [],
                'completed': [],
                'stats': get_queue_stats(None)
            })
        
        waiting = []
        in_consultation = []
        completed = []
        
        for key, patient in patients_data.items():
            wait_time = calculate_wait_time_remaining(patient.get('registeredAt'))
            patient_data = {
                'id': key,
                'name': patient.get('name'),
                'age': patient.get('age'),
                'token': patient.get('token'),
                'symptoms': patient.get('symptoms'),
                'priority': patient.get('priorityLevel'),
                'temperature': patient.get('vitals', {}).get('temperature'),
                'waitTime': wait_time,
                'registeredAt': patient.get('registeredAt')
            }
            
            status = patient.get('status')
            if status == 'waiting':
                waiting.append(patient_data)
            elif status == 'in-consultation':
                in_consultation.append(patient_data)
            elif status == 'completed':
                completed.append(patient_data)
        
        return success_response({
            'waiting': waiting,
            'inConsultation': in_consultation,
            'completed': completed,
            'stats': get_queue_stats(patients_data)
        })
        
    except Exception as e:
        logger.error(f"Staff get patients error: {str(e)}")
        return error_response(f'Failed to fetch patients: {str(e)}', 500)

@app.route('/api/staff/start-consultation/<patient_id>', methods=['POST'])
def start_consultation(patient_id):
    """Start consultation for a patient"""
    try:
        if db:
            db.child('patients').child(patient_id).update({
                'status': 'in-consultation',
                'doctor': 'Dr. Available',
                'consultationStart': datetime.now().isoformat()
            })
        
        return success_response({'status': 'in-consultation'}, 'Consultation started')
        
    except Exception as e:
        logger.error(f"Start consultation error: {str(e)}")
        return error_response(f'Failed to start consultation: {str(e)}', 500)

@app.route('/api/staff/complete-consultation/<patient_id>', methods=['POST'])
def complete_consultation(patient_id):
    """Complete consultation for a patient"""
    try:
        if db:
            db.child('patients').child(patient_id).update({
                'status': 'completed',
                'consultationEnd': datetime.now().isoformat()
            })
        
        return success_response({'status': 'completed'}, 'Consultation completed')
        
    except Exception as e:
        logger.error(f"Complete consultation error: {str(e)}")
        return error_response(f'Failed to complete consultation: {str(e)}', 500)

@app.route('/api/staff/cancel-patient/<patient_id>', methods=['DELETE'])
def cancel_patient(patient_id):
    """Cancel/remove a patient from queue"""
    try:
        if db:
            db.child('patients').child(patient_id).remove()
        
        return success_response({'status': 'cancelled'}, 'Patient cancelled')
        
    except Exception as e:
        logger.error(f"Cancel patient error: {str(e)}")
        return error_response(f'Failed to cancel patient: {str(e)}', 500)

# ============================================================================
# MAINTENANCE ENDPOINTS
# ============================================================================

@app.route('/api/maintenance/expire-tokens', methods=['POST'])
def expire_tokens():
    """Check and expire old tokens (30+ minutes)"""
    try:
        if db:
            patients_data = db.child('patients').get().val()
            
            if patients_data:
                now = datetime.now()
                for key, patient in patients_data.items():
                    if patient.get('status') == 'waiting':
                        reg_time = datetime.fromisoformat(patient.get('registeredAt'))
                        elapsed_minutes = (now - reg_time).total_seconds() / 60
                        
                        if elapsed_minutes > 30:
                            # Archive to expired
                            db.child('archived').child('patients').child(key).set({
                                **patient,
                                'status': 'expired',
                                'expiredAt': now.isoformat()
                            })
                            # Remove from active queue
                            db.child('patients').child(key).remove()
        
        return success_response({'message': 'Token expiration check completed'})
        
    except Exception as e:
        logger.error(f"Expire tokens error: {str(e)}")
        return error_response(f'Failed to expire tokens: {str(e)}', 500)

@app.route('/api/maintenance/archive-completed', methods=['POST'])
def archive_completed():
    """Archive completed consultations"""
    try:
        if db:
            patients_data = db.child('patients').get().val()
            
            if patients_data:
                for key, patient in patients_data.items():
                    if patient.get('status') == 'completed':
                        # Archive patient
                        db.child('archived').child('patients').child(key).set({
                            **patient,
                            'archivedAt': datetime.now().isoformat()
                        })
                        # Remove from active queue
                        db.child('patients').child(key).remove()
        
        return success_response({'message': 'Archiving completed'})
        
    except Exception as e:
        logger.error(f"Archive completed error: {str(e)}")
        return error_response(f'Failed to archive: {str(e)}', 500)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return error_response('Endpoint not found', 404)

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return error_response('Internal server error', 500)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    logger.info(f"Starting Hospital Queue Management API on port {PORT}")
    app.run(debug=True, host='0.0.0.0', port=PORT)
