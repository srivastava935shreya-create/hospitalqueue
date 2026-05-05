"""
Firebase Configuration Module
Handles Firebase initialization and database setup
"""

import firebase_admin
from firebase_admin import credentials, db

# Firebase Configuration
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyCxNXnhhJe90YA2J-7TahSakZ582-NjQLA",
    "authDomain": "hospital-queue-managemen-10527.firebaseapp.com",
    "databaseURL": "https://hospital-queue-managemen-10527-default-rtdb.firebaseio.com",
    "projectId": "hospital-queue-managemen-10527",
    "storageBucket": "hospital-queue-managemen-10527.appspot.com",
    "messagingSenderId": "666283597659",
    "appId": "1:666283597659:web:4af8ecb32fdedeb5ab447e"
}

def initialize_firebase():
    """
    Initialize Firebase Admin SDK
    Note: You need to add your serviceAccountKey.json file
    Download it from Firebase Console -> Project Settings -> Service Accounts
    """
    try:
        # Uncomment and update path when you have the service account key
        # cred = credentials.Certificate('path/to/serviceAccountKey.json')
        # firebase_admin.initialize_app(cred, {
        #     'databaseURL': FIREBASE_CONFIG['databaseURL']
        # })
        pass
    except Exception as e:
        print(f"Firebase initialization error: {e}")
        raise

def get_database():
    """Get Firebase Realtime Database reference"""
    try:
        return db.reference()
    except Exception as e:
        print(f"Error getting database reference: {e}")
        return None
