# 🏥 Hospital Queue Management System

A **professional-grade hospital queue management system** with AI-based patient prioritization, real-time tracking, and staff management interface.

---

## ✨ Key Features

- 🔢 **Smart Token Generation** - Unique tokens with automatic reuse of expired slots
- 🧠 **AI Priority Calculation** - Intelligent prioritization based on vitals, symptoms, and age
- ⚡ **Real-time Queue Dashboard** - Live patient queue with priority levels and wait times
- 👨‍⚕️ **Staff Management Interface** - Doctors can manage consultations efficiently
- 📱 **Responsive Design** - Mobile-friendly interface for all devices
- 🔄 **Automatic Expiration** - Tokens expire after 30 minutes of inactivity
- 📦 **Auto-Archive** - Completed consultations stored automatically
- 🔐 **Staff Authentication** - Secure password-protected staff access

---

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, JavaScript
- Firebase Realtime Database
- Real-time event listeners

### Backend (Python)
- **Flask** - REST API framework
- **Firebase Admin SDK** - Database management
- **Flask-CORS** - Cross-origin requests
- **Python 3.8+**

### Database
- **Firebase Realtime Database** - NoSQL data storage
- Real-time synchronization

---

## 📁 Project Structure

```
hospitalqueue/
├── main.py                 # Flask REST API server (15+ endpoints)
├── queue_logic.py          # Core business logic & AI priority calculation
├── firebase_config.py      # Firebase initialization & setup
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── index.html             # Frontend HTML interface
├── script.js              # Frontend JavaScript (Firebase integration)
├── style.css              # Frontend styling (responsive design)
└── README.md              # Complete documentation
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Firebase project with Realtime Database
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/srivastava935shreya-create/hospitalqueue.git
cd hospitalqueue
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
# Edit .env with your Firebase credentials and settings
```

### Step 5: Setup Firebase
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Create/select your project
3. Download Service Account Key:
   - Project Settings → Service Accounts → Generate Private Key
4. Update `firebase_config.py` with your credentials

### Step 6: Run Backend Server
```bash
python main.py
```

Server will start on `http://localhost:5000`

### Step 7: Run Frontend (in another terminal)
```bash
python -m http.server 8000
# Open http://localhost:8000 in browser
```

---

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Response Format
All endpoints return JSON:
```json
{
  "success": true,
  "message": "Description",
  "data": { }
}
```

### Public Endpoints

#### 1. Health Check
```
GET /health
Description: Verify API is running

Response:
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2026-05-05T12:37:00Z"
  }
}
```

#### 2. Register Patient
```
POST /register
Content-Type: application/json

Request:
{
  "name": "John Doe",
  "age": 30,
  "contact": "555-1234",
  "symptoms": "chest pain",
  "temperature": 102.5,
  "bloodPressure": "140/90",
  "heartRate": 95
}

Response:
{
  "success": true,
  "data": {
    "token": "T-4532",
    "priority": "Critical",
    "color": "#dc2626",
    "waitTime": "0-5 minutes",
    "registeredAt": "2026-05-05T12:37:00Z"
  }
}
```

#### 3. Get All Patients
```
GET /patients
Description: Get current queue list with statistics

Response:
{
  "success": true,
  "data": {
    "patients": [
      {
        "id": "key1",
        "name": "John Doe",
        "age": 30,
        "token": "T-4532",
        "priority": "Critical",
        "status": "waiting",
        "waitTimeRemaining": 15
      }
    ],
    "stats": {
      "waiting": 5,
      "in_consultation": 2,
      "completed": 12,
      "total": 19
    }
  }
}
```

#### 4. Get Patient Details
```
GET /patients/<patient_id>
Description: Get specific patient information

Response:
{
  "success": true,
  "data": {
    "id": "key1",
    "name": "John Doe",
    "age": 30,
    "contact": "555-1234",
    "token": "T-4532",
    "symptoms": "chest pain",
    "vitals": {
      "temperature": 102.5,
      "heartRate": 95,
      "bloodPressure": "140/90"
    },
    "priority": "Critical",
    "status": "waiting",
    "waitTimeRemaining": 15
  }
}
```

### Staff Endpoints

#### 1. Staff Authentication
```
POST /staff/authenticate
Request: { "password": "staff123" }

Response: { "success": true, "data": { "authenticated": true } }
```

#### 2. Get Staff Dashboard
```
GET /staff/patients
Description: Get patients grouped by status

Response:
{
  "success": true,
  "data": {
    "waiting": [ {...}, {...} ],
    "inConsultation": [ {...}, {...} ],
    "completed": [ {...} ],
    "stats": {
      "waiting": 5,
      "in_consultation": 2,
      "completed": 12,
      "total": 19
    }
  }
}
```

#### 3. Start Consultation
```
POST /staff/start-consultation/<patient_id>
Description: Mark patient as in-consultation

Response:
{
  "success": true,
  "data": { "status": "in-consultation" }
}
```

#### 4. Complete Consultation
```
POST /staff/complete-consultation/<patient_id>
Description: Mark patient as completed

Response:
{
  "success": true,
  "data": { "status": "completed" }
}
```

#### 5. Cancel Patient
```
DELETE /staff/cancel-patient/<patient_id>
Description: Remove patient from queue

Response:
{
  "success": true,
  "data": { "status": "cancelled" }
}
```

### Admin/Maintenance Endpoints

#### 1. Expire Old Tokens
```
POST /maintenance/expire-tokens
Description: Remove patients waiting >30 minutes

Response:
{
  "success": true,
  "message": "Token expiration check completed"
}
```

#### 2. Archive Completed
```
POST /maintenance/archive-completed
Description: Move completed consultations to archive

Response:
{
  "success": true,
  "message": "Archiving completed"
}
```

---

## 🧠 Priority Algorithm

The system uses an **intelligent AI-based scoring algorithm** that considers multiple factors:

### Scoring Components

#### 1. Vital Signs (0-80 points)
- **Temperature**: Extreme values = 40pts
  - >103°F or <95°F = 40pts
  - >101°F or <96°F = 20pts
  
- **Heart Rate**: Extreme values = 40pts
  - >120 or <50 = 40pts
  - >100 or <60 = 20pts
  
- **Blood Pressure**: Out of normal range = 40pts
  - Systolic >180 or <90, Diastolic >120 or <60 = 40pts
  - Systolic >140 or <100 = 20pts

#### 2. Symptoms (0-50 points)
- **Critical Symptoms** (50pts):
  - Chest pain, severe bleeding, unconscious, seizure, stroke, heart attack, difficulty breathing, severe head injury
  
- **Urgent Symptoms** (30pts):
  - Fracture, severe pain, high fever, vomiting, dizziness, confusion

#### 3. Age (0-15 points)
- **Vulnerable Groups** (15pts): Age <2 or >70
- **At-Risk Groups** (10pts): Age <12 or >60

### Priority Levels

| Level | Score | Color | Wait Time |
|-------|-------|-------|-----------|
| **Critical** | ≥80 | 🔴 Red (#dc2626) | 0-5 min |
| **Emergency** | ≥50 | 🟠 Orange (#ea580c) | 5-15 min |
| **Urgent** | ≥30 | 🟡 Amber (#f59e0b) | 15-30 min |
| **Non-urgent** | <30 | 🟢 Green (#16a34a) | 30-60 min |

---

## 💻 Usage Examples

### Example 1: Register Critical Patient
```javascript
const response = await fetch('http://localhost:5000/api/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Jane Smith',
    age: 45,
    contact: '555-5678',
    symptoms: 'chest pain, difficulty breathing',
    temperature: 103.5,
    bloodPressure: '180/120',
    heartRate: 125
  })
});

const result = await response.json();
console.log('Token:', result.data.token);
console.log('Priority:', result.data.priority); // Critical
console.log('Wait Time:', result.data.waitTime); // 0-5 minutes
```

### Example 2: Staff Workflow
```javascript
// 1. Authenticate staff
const auth = await fetch('http://localhost:5000/api/staff/authenticate', {
  method: 'POST',
  body: JSON.stringify({ password: 'staff123' })
}).then(r => r.json());

// 2. Get waiting patients
const patients = await fetch('http://localhost:5000/api/staff/patients')
  .then(r => r.json());
console.log('Waiting:', patients.data.waiting);

// 3. Start consultation
await fetch(`http://localhost:5000/api/staff/start-consultation/${patientId}`, {
  method: 'POST'
});

// 4. Complete consultation
await fetch(`http://localhost:5000/api/staff/complete-consultation/${patientId}`, {
  method: 'POST'
});
```

### Example 3: Monitor Queue
```javascript
// Poll every 5 seconds
setInterval(async () => {
  const response = await fetch('http://localhost:5000/api/patients');
  const result = await response.json();
  
  console.log('Queue Stats:');
  console.log('Waiting:', result.data.stats.waiting);
  console.log('In Consultation:', result.data.stats.in_consultation);
  console.log('Completed:', result.data.stats.completed);
}, 5000);
```

---

## 🔐 Environment Configuration

Create `.env` file from `.env.example`:

```bash
# Flask Configuration
FLASK_ENV=development
PORT=5000

# Staff Authentication
STAFF_PASSWORD=your_secure_password_here

# Firebase Configuration
FIREBASE_API_KEY=your_api_key
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
# ... other Firebase settings
```

---

## 🔒 Security Considerations

1. **Change Staff Password** - Default is `staff123`, change in production
2. **Environment Variables** - Never commit `.env` file (add to `.gitignore`)
3. **Firebase Rules** - Implement proper security rules
4. **HTTPS** - Use HTTPS in production
5. **Input Validation** - All inputs validated on backend
6. **Rate Limiting** - Implement rate limiting for endpoints
7. **Authentication** - Consider JWT tokens for staff

---

## 📊 Database Schema

### Patients Collection
```json
{
  "patients": {
    "uniqueId": {
      "name": "John Doe",
      "age": 30,
      "contact": "555-1234",
      "symptoms": "chest pain",
      "vitals": {
        "temperature": 102.5,
        "heartRate": 95,
        "bloodPressure": "140/90"
      },
      "token": "T-4532",
      "status": "waiting|in-consultation|completed",
      "priorityLevel": "Critical|Emergency|Urgent|Non-urgent",
      "registeredAt": "2026-05-05T12:37:00Z",
      "consultationStart": "2026-05-05T12:40:00Z",
      "consultationEnd": "2026-05-05T12:50:00Z",
      "doctor": "Dr. Smith"
    }
  }
}
```

---

## 🚀 Deployment

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

### Using Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
```

### Deploy to Heroku
```bash
heroku create your-app-name
git push heroku main
heroku config:set STAFF_PASSWORD=your_password
```

---

## 🔄 System Flow

```
Patient Registration
    ↓
Input Vitals & Symptoms
    ↓
AI Priority Calculation
    ↓
Token Generation
    ↓
Real-time Queue Update
    ↓
Display Wait Time
    ↓
Staff Calls Patient
    ↓
Start Consultation
    ↓
Complete Consultation
    ↓
Archive Record
```

---

## 🔄 System Flow

1. Patient registers → gets token  
2. System assigns priority (normal/emergency)  
3. Queue updates in real-time  
4. Staff processes next patient  

## 📈 Future Enhancements

- [ ] Doctor/Staff user accounts with authentication
- [ ] SMS/Email notifications for patients
- [ ] Patient history and records tracking
- [ ] Analytics dashboard for hospital management
- [ ] Multi-location hospital support
- [ ] Appointment scheduling system
- [ ] Doctor availability calendar
- [ ] Patient feedback/rating system
- [ ] Integration with hospital management system
- [ ] Mobile app (iOS/Android)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📞 Support & Contact

- **GitHub Issues**: Report bugs and feature requests
- **Email**: srivastava935shreya@gmail.com
- **GitHub Profile**: https://github.com/srivastava935shreya-create

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## ⭐ Show Your Support

If you find this project helpful, please consider:
- ⭐ Starring this repository
- 🐛 Reporting bugs or issues
- 💡 Suggesting improvements
- 🤝 Contributing code

---

**Made with ❤️ by Shreya Srivastava**

**Last Updated:** May 5, 2026
