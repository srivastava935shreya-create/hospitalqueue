<img width="1920" height="1020" alt="Screenshot 2025-10-11 104518" src="https://github.com/user-attachments/assets/c33ba0e7-770a-410f-b9f3-c70dd5ab78ad" />
<img width="1920" height="1020" alt="Screenshot 2025-10-11 104536" src="https://github.com/user-attachments/assets/e802fc2b-c1d5-4b55-8edf-44dad3cc55bd" />
<img width="1920" height="1020" alt="Screenshot 2025-10-11 120331" src="https://github.com/user-attachments/assets/3ecb5fb5-a160-4643-b999-3dd688202e0d" />
<img width="1920" height="1020" alt="Screenshot 2025-10-11 120542" src="https://github.com/user-attachments/assets/e8fb9ca7-4938-42a0-bc94-bb8b27f02ca2" />
# 📸 Hospital Queue Management System - Screenshots & UI Guide

## Overview

This document provides a visual guide to all features and interfaces of the Hospital Queue Management System. The application features two main views: **Public Patient View** and **Staff Dashboard**

---

## 🏥 Public Patient View

### 1. Main Dashboard & Registration Form

**Description:** The main landing page where patients register and view the hospital queue.

**Key Features:**
- 🎨 **Header Section**
  - Hospital Queue Management title
  - "AI-Powered Triage System" subtitle
  - Help button (?) for user guidance
  - Staff Login button for switching to staff view

- 📊 **Statistics Cards**
  - Waiting Count (patients in queue)
  - In Consultation Count (currently being treated)
  - Completed Count (finished consultations)
  - Total Count (all patients today)

- 📋 **Patient Registration Form**
  - Patient Name field
  - Age field
  - Contact Number field
  - Symptoms (detailed description)
  - Vital Signs Grid:
    - Temperature (°F)
    - Blood Pressure (mmHg)
    - Heart Rate (bpm)
  - Submit Button: "Get Token & AI Assessment"

**Form Layout:**
```
┌─────────────────────────────────────────┐
│  🏥 Hospital Queue Management          │
│     AI-Powered Triage System            │
│  [?]              [Staff Login]         │
├─────────────────────────────────────────┤
│  ┌─────────┬──────────┬──────────────┐  │
│  │Waiting: │Consult: │Completed: │  │  │
│  │    5    │    2    │    12     │  │  │
│  └─────────┴──────────┴──────────────┘  │
├─────────────────────────────────────────┤
│ PATIENT REGISTRATION                    │
│ ┌─────────────────────────────────────┐ │
│ │ Patient Name: [________________]   │ │
│ │ Age: [___]  Contact: [__________]  │ │
│ │ Symptoms: [__________________]     │ │
│ │ ┌──────────┬──────────┬──────────┐ │ │
│ │ │Temp: ___│BP: ___/___│HR: ____  │ │ │
│ │ └──────────┴──────────┴──────────┘ │ │
│ │ [Get Token & AI Assessment]        │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

### 2. Token Display (After Registration)

**Description:** Displayed after successful patient registration with AI assessment.

**Output Information:**
```
╔════════════════════════════════════════╗
║          YOUR TOKEN: T-4532           ║
║                                        ║
║ Priority Level: 🔴 CRITICAL           ║
║ Color Code: Red (#dc2626)             ║
║                                        ║
║ Estimated Wait Time: 0-5 minutes      ║
║ AI Assessment:                         ║
║ • Temperature: Abnormally High         ║
║ • Heart Rate: Elevated                 ║
║ • Blood Pressure: High                 ║
║ • Symptoms: Chest pain detected        ║
║                                        ║
║ Recommendation: URGENT ATTENTION      ║
║ Please wait at the reception!          ║
╚════════════════════════════════════════╝
```

**Token Color Codes:**
- 🔴 **Red (#dc2626)** - Critical (Score ≥80, Wait: 0-5 min)
- 🟠 **Orange (#ea580c)** - Emergency (Score ≥50, Wait: 5-15 min)
- 🟡 **Amber (#f59e0b)** - Urgent (Score ≥30, Wait: 15-30 min)
- 🟢 **Green (#16a34a)** - Non-urgent (Score <30, Wait: 30-60 min)

---

### 3. Current Queue Display

**Description:** Real-time list of all patients in the queue with their status and priority.

**Queue Table Layout:**
```
CURRENT QUEUE
┌──────┬─────────────┬─────┬──────────┬────────────┬─────────────[...]
│Token │   Name      │Age  │Symptoms  │ Priority   │ Wait Time (min)  │
├──────┼─────────────┼─────┼──────────┼────────────┼─────────────[...]
│T-4532│ John Doe    │ 35  │Chest pain│🔴 Critical │      3          │
│T-4531│ Jane Smith  │ 28  │Fever     │🟠 Emergency│      8          │
│T-4530│ Mike Brown  │ 45  │Headache  │🟡 Urgent  │     22          │
│T-4529│ Sarah Jones │ 55  │Cough     │🟢 Non-urg │     42          │
│T-4528│ Tom Wilson  │ 62  │Back pain │🟢 Non-urg │     51          │
└──────┴─────────────┴─────┴──────────┴────────────┴─────────────[...]
```

**Features:**
- Real-time updates from Firebase
- Color-coded priority indicators
- Remaining wait time countdown
- Patient symptoms at a glance
- Automatic refresh every 5 seconds

---

### 4. Help Modal

**Description:** Interactive help section for patient guidance.

**Help Content:**
```
┌────────────────────────────────────────────┐
│          🏥 PATIENT GUIDE                  │
│                                            │
│ HOW TO REGISTER:                           │
│ • Fill all required fields in the form    │
│ • Describe your symptoms clearly          │
│ • Provide vital signs if available        │
│ • Click "Get Token & AI Assessment"       │
│ • Note your token number and wait         │
│                                            │
│ UNDERSTANDING YOUR PRIORITY:               │
│ 🔴 Critical (0-5 min) - Severe conditions │
│ 🟠 Emergency (5-15 min) - High priority   │
│ 🟡 Urgent (15-30 min) - Moderate need    │
│ 🟢 Non-urgent (30-60 min) - Routine      │
│                                            │
│ WHAT TO BRING:                             │
│ • Valid ID                                 │
│ • Insurance card                           │
│ • Medical history (if available)           │
│                                            │
│            [Close Help]                    │
└────────────────────────────────────────────┘
```

---

## 👨‍⚕️ Staff Dashboard

### 1. Staff Login

**Description:** Password-protected access for hospital staff.

**Authentication Flow:**
```
Public View Button: [Staff Login]
    ↓
Modal Prompt: "Enter Staff Password"
    ↓
Input Field: [_______________]
    ↓
[Authenticate] [Cancel]
    ↓
Access granted → Staff Dashboard
```

**Default Password:** `staff123` (change in production)

---

### 2. Staff Dashboard Main View

**Description:** Comprehensive dashboard for managing patient consultations.

**Layout:**
```
┌─────────────────────────────────────────────────┐
│  Staff Dashboard                                │
│  Patient Management System              [?]     │
│  [Public View]                                  │
├─────────────────────────────────────────────────┤
│ [Waiting Patients] [In Consultation] [Completed]│
├─────────────────────────────────────────────────┤
│ WAITING PATIENTS                                │
│ ┌───────────────────────────────────────┐   │
│ │ Token: T-4532 | Name: John Doe | Age: 35│   │
│ │ Symptoms: Chest pain, difficulty breathe│   │
│ │ Priority: 🔴 CRITICAL | Waiting: 3 min  │   │
│ │ [START] [CANCEL]                         │   │
│ ├──────────────────────────────────────┤   │
│ │ Token: T-4531 | Name: Jane Smith | Age:28│   │
│ │ Symptoms: High fever, body ache          │   │
│ │ Priority: 🟠 EMERGENCY | Waiting: 8 min │   │
│ │ [START] [CANCEL]                         │   │
│ └──────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

### 3. Waiting Patients Tab

**Description:** Shows all patients currently waiting in the queue.

**Patient Card Layout:**
```
┌────────────────────────────────────────┐
│ 🔴 CRITICAL PRIORITY                   │
│                                        │
│ Token: T-4532                          │
│ Name: John Doe                         │
│ Age: 35 years                          │
│ Contact: 555-1234                      │
│ Symptoms: Chest pain, shortness breath│
│ Temperature: 103.5°F                   │
│ Heart Rate: 125 bpm                    │
│ Blood Pressure: 180/120 mmHg           │
│ Waiting Since: 3 minutes ago           │
│                                        │
│ [START CONSULTATION] [CANCEL PATIENT] │
└────────────────────────────────────────┘
```

**Staff Actions:**
- **[START CONSULTATION]** - Move patient to in-consultation status
- **[CANCEL PATIENT]** - Remove patient from queue

---

### 4. In Consultation Tab

**Description:** Patients currently being treated by doctors.

**Patient Card Layout:**
```
┌────────────────────────────────────────┐
│ 🟠 EMERGENCY PRIORITY                  │
│                                        │
│ Token: T-4531                          │
│ Name: Jane Smith                       │
│ Age: 28 years                          │
│ Consulting Since: 8 minutes ago        │
│ Doctor: Dr. Smith                      │
│ Symptoms: High fever (102.5°F)         │
│ Heart Rate: 95 bpm                     │
│                                        │
│ [COMPLETE CONSULTATION] [CANCEL]       │
└────────────────────────────────────────┘
```

**Staff Actions:**
- **[COMPLETE CONSULTATION]** - Mark consultation as done, move to completed
- **[CANCEL]** - Reschedule or remove patient

---

### 5. Completed Tab

**Description:** Archive of all completed consultations for the day.

**Completed Patient Card Layout:**
```
┌────────────────────────────────────────┐
│ ✅ COMPLETED                           │
│                                        │
│ Token: T-4520                          │
│ Name: Robert Brown                     │
│ Age: 52 years                          │
│ Symptoms: Fractured arm                │
│ Consultation Duration: 22 minutes      │
│ Doctor: Dr. Johnson                    │
│ Completed At: 12:45 PM                 │
│                                        │
│ [VIEW FULL RECORD]                     │
└────────────────────────────────────────┘
```

---

## 🎨 UI Design Elements

### Color Scheme
- **Primary:** Medical Blue (#1e40af)
- **Success:** Green (#16a34a)
- **Warning:** Amber (#f59e0b)
- **Danger:** Red (#dc2626)
- **Background:** Light Gray (#f3f4f6)
- **Text:** Dark Gray (#111827)

### Typography
- **Headers:** Bold, 24-32px
- **Subheaders:** Bold, 18-20px
- **Body Text:** Regular, 14-16px
- **Labels:** Medium, 12-14px

### Responsive Design
- **Desktop:** Full layout with side-by-side columns
- **Tablet:** Stacked layout with responsive cards
- **Mobile:** Single column, touch-optimized buttons

---

## 📊 AI Priority Algorithm Visualization

### Input Form with Real-time Scoring

```
PATIENT REGISTRATION
┌─────────────────────────────────────┐
│ Name: John Doe              [Input]  │
│ Age: 45 years               [Input]  │
│ Symptoms: Chest pain        [Input]  │
│ Temperature: 103.5°F        [Input]  │
│ Heart Rate: 125 bpm         [Input]  │
│ Blood Pressure: 180/120     [Input]  │
└─────────────────────────────────────┘

SCORING BREAKDOWN:
┌───────────────────────────────────────┐
│ Vital Signs Analysis:                 │
│  • Temperature (103.5°F) ........40pts│
│  • Heart Rate (125 bpm) .........40pts│
│  • Blood Pressure (180/120) .....40pts│
│                         Subtotal: 120 │
│                                       │
│ Symptom Analysis:                     │
│  • Chest pain (Critical) .........50pts│
│                         Subtotal: 50  │
│                                       │
│ Age Risk Factor (45 years) ......10pts│
│                                       │
│          TOTAL SCORE: 180 / 145 ❌    │
│                                       │
│ But capped at 145 = CRITICAL LEVEL   │
│ ➜ Priority: 🔴 CRITICAL              │
│ ➜ Wait Time: 0-5 minutes              │
│ ➜ Color: Red (#dc2626)                │
└───────────────────────────────────────┘
```

---

## 🔄 Data Flow Visualization

### Patient Registration Flow
```
┌─────────────────────────┐
│  Patient Fills Form     │
│  (Name, Age, Symptoms) │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  Submit Registration    │
│  POST /api/register     │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  Backend Processing:    │
│  • Validate Input       │
│  • Calculate Priority   │
│  • Generate Token       │
│  • Create Record        │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  Save to Firebase       │
│  Database               │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  Display Token & Info   │
│  Show Priority Level    │
│  Estimated Wait Time    │
└─────────────────────────┘
```

### Staff Consultation Flow
```
┌────────────────────────────┐
│  Staff Login               │
│  (Password Protected)      │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────┐
│  View Waiting Patients     │
│  Sorted by Priority        │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────┐
│  Select & Start            │
│  Consultation              │
│  POST /staff/start-consult │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────┐
│  Status → In Consultation  │
│  Patient Moved to Tab      │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────┐
│  Treatment in Progress     │
│  Staff Reviews Details     │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────┐
│  Complete Consultation     │
│  POST /staff/complete      │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────┐
│  Status → Completed        │
│  Archived Automatically    │
│  Record Stored             │
└────────────────────────────┘
```

---

## 📱 Mobile View (Responsive Design)

### Mobile Patient Registration
```
┌─────────────────────────┐
│ 🏥 Hospital Queue       │
│    Management           │
│ [?] [Staff Login]       │
├─────────────────────────┤
│ Waiting: 5              │
│ Consult: 2              │
│ Completed: 12           │
│ Total: 19               │
├─────────────────────────┤
│ PATIENT REGISTRATION    │
│ ┌──────────────────────┐│
│ │Name [___________]   ││
│ │Age [__] Contact[__]││
│ │Symptoms [______]   ││
│ │Temp [_] BP [_] HR[]││
│ │[Get Token]         ││
│ └──────────────────────┘│
├─────────────────────────┤
│ QUEUE (Scrollable)      │
│ ┌──────────────────────┐│
│ │T-4532: John Doe    ││
│ │🔴 Critical | 3 min ││
│ ├──────────────────────┤│
│ │T-4531: Jane Smith  ││
│ │🟠 Emergency | 8min ││
│ └──────────────────────┘│
└─────────────────────────┘
```

---

## 🔔 Notifications & Status Updates

### Real-time Firebase Updates
- **Queue Changes** - Instant queue updates when patients register/complete
- **Priority Changes** - Dynamic priority adjustments
- **Status Updates** - Live status transitions (waiting → consultation → completed)
- **Patient Expiration** - Automatic removal after 30 minutes inactivity

### Visual Indicators
```
✅ Success: Green checkmark
⚠️  Warning: Amber triangle
❌ Error: Red X mark
🔄 Loading: Spinner animation
🔴 Critical: Red indicator
🟠 Emergency: Orange indicator
🟡 Urgent: Amber indicator
🟢 Non-urgent: Green indicator
```

---

## 🎯 Key UI Features Summary

| Feature | Location | Purpose |
|---------|----------|---------|
| **Header** | Top | Branding and main navigation |
| **Stats Cards** | Below header | Quick queue overview |
| **Registration Form** | Main section | Patient data entry |
| **Token Display** | Modal popup | Shows AI assessment result |
| **Patient Queue** | Bottom | Real-time patient list |
| **Help Button** | Top right | User guidance |
| **Staff Login** | Top right | Staff access |
| **Dashboard Tabs** | Staff view | Organize patients by status |
| **Action Buttons** | Patient cards | Manage consultations |
| **Footer** | Bottom | Contact info (optional) |

---

## 🌐 Accessibility Features

✅ **Color Contrast** - High contrast for readability
✅ **Responsive Text** - Scales with device size
✅ **Button Labels** - Clear, descriptive text
✅ **Form Labels** - Associated with input fields
✅ **Error Messages** - Clear validation feedback
✅ **Keyboard Navigation** - All features keyboard accessible
✅ **Mobile Optimized** - Touch-friendly interface
✅ **ARIA Labels** - Screen reader support

---

## 📝 Notes for Users

1. **Patient View:**
   - Fill all required fields for accurate AI assessment
   - Vitals are important for priority calculation
   - Save your token number for check-in

2. **Staff View:**
   - Default password: `staff123` (change immediately in production)
   - Prioritize critical/emergency patients
   - Complete consultations to free up staff time
   - Archive regularly for performance

3. **System Maintenance:**
   - Tokens expire after 30 minutes of inactivity
   - Completed records auto-archive daily
   - Database cleanup runs automatically

---

## 🚀 Future UI Enhancements

- [ ] Dark mode toggle
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Patient notifications (SMS/Email)
- [ ] Doctor appointment calendar
- [ ] Payment integration interface
- [ ] Advanced filtering and search
- [ ] Customizable branding
- [ ] Export reports functionality
- [ ] Video consultation interface

---

**Last Updated:** May 5, 2026
**Version:** 1.0
**Status:** Production Ready
