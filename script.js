// ✅ Firebase Config
const firebaseConfig = {
  apiKey: "AIzaSyCxNXnhhJe90YA2J-7TahSakZ582-NjQLA",
  authDomain: "hospital-queue-managemen-10527.firebaseapp.com",
  databaseURL: "https://hospital-queue-managemen-10527-default-rtdb.firebaseio.com",
  projectId: "hospital-queue-managemen-10527",
  storageBucket: "hospital-queue-managemen-10527.appspot.com",
  messagingSenderId: "666283597659",
  appId: "1:666283597659:web:4af8ecb32fdedeb5ab447e"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
const db = firebase.database();

const MIN_TOKEN = 1000;
const MAX_TOKEN = 9999;

// Generate or reuse token
async function getAvailableToken() {
  const snapshot = await db.ref('patients').once('value');
  const patients = snapshot.val() || {};
  for (const [key, patient] of Object.entries(patients)) {
    if (patient.status === 'expired') {
      await db.ref('patients/' + key).remove();
      return patient.token;
    }
  }
  return 'T-' + Math.floor(MIN_TOKEN + Math.random() * (MAX_TOKEN - MIN_TOKEN + 1));
}

// AI priority calculation
function calculatePriority(patient) {
  let score = 0;
  const vitals = patient.vitals;
  const symptoms = patient.symptoms.toLowerCase();
  const age = patient.age;

  if (vitals.temperature > 103 || vitals.temperature < 95) score += 40;
  else if (vitals.temperature > 101 || vitals.temperature < 96) score += 20;

  if (vitals.heartRate > 120 || vitals.heartRate < 50) score += 40;
  else if (vitals.heartRate > 100 || vitals.heartRate < 60) score += 20;

  const [systolic, diastolic] = vitals.bloodPressure.split('/').map(Number);
  if (systolic > 180 || systolic < 90 || diastolic > 120 || diastolic < 60) score += 40;
  else if (systolic > 140 || systolic < 100) score += 20;

  const critical = ['chest pain','severe bleeding','unconscious','seizure','stroke','heart attack','difficulty breathing','severe head injury'];
  const urgent = ['fracture','severe pain','high fever','vomiting','dizziness','confusion'];

  if (critical.some(s => symptoms.includes(s))) score += 50;
  else if (urgent.some(s => symptoms.includes(s))) score += 30;

  if (age < 2 || age > 70) score += 15;
  else if (age < 12 || age > 60) score += 10;

  if (score >= 80) return { level: 'Critical', color: '#dc2626' };
  if (score >= 50) return { level: 'Emergency', color: '#ea580c' };
  if (score >= 30) return { level: 'Urgent', color: '#f59e0b' };
  return { level: 'Non-urgent', color: '#16a34a' };
}

// ---------------- Form Submission ----------------
document.getElementById('patientForm').addEventListener('submit', async e => {
  e.preventDefault();
  const f = e.target;

  const token = await getAvailableToken();

  const patient = {
    name: f.name.value,
    age: parseInt(f.age.value),
    contact: f.contact.value,
    symptoms: f.symptoms.value,
    vitals: {
      temperature: parseFloat(f.temperature.value) || 98.6,
      bloodPressure: f.bloodPressure.value || "120/80",
      heartRate: parseInt(f.heartRate.value) || 72
    },
    token: token,
    status: 'waiting',
    registeredAt: Date.now()
  };

  const priority = calculatePriority(patient);
  patient.priorityLevel = priority.level;

  db.ref('patients').push(patient)
    .then(() => {
      document.getElementById('tokenDisplay').innerHTML = `
        <h3>Registration Successful!</h3>
        <div class="token-number">${patient.token}</div>
        <p>Priority Level: <span style="color:${priority.color}; font-weight: bold;">${priority.level}</span></p>
        <p>Registered At: ${new Date(patient.registeredAt).toLocaleTimeString()}</p>
        <p>Estimated Wait Time: <strong>${getWaitTime(priority.level)} minutes</strong></p>
      `;
      document.getElementById('tokenDisplay').style.display = 'block';
      f.reset();
    })
    .catch(err => alert("Error saving to Firebase: " + err));
});

function getWaitTime(priority) {
  const times = {
    'Critical': '0-5',
    'Emergency': '5-15', 
    'Urgent': '15-30',
    'Non-urgent': '30-60'
  };
  return times[priority] || '30-60';
}

// ---------------- Load Dashboard ----------------
function loadPatients() {
  const list = document.getElementById('patientList');
  list.innerHTML = '';
  db.ref('patients').once('value', snap => {
    const patients = snap.val();
    
    // Update stats
    updateStats(patients);
    
    if (!patients) { 
      list.innerHTML = "<p style='text-align: center; color: #666;'>No patients in queue</p>"; 
      return; 
    }
    
    Object.values(patients).forEach(p => {
      const timePassed = Math.floor((Date.now() - p.registeredAt)/60000);
      const timeLeft = Math.max(0, 30 - timePassed);
      const div = document.createElement('div');
      div.className = `patient-item priority-${p.priorityLevel.toLowerCase().replace(' ', '-')}`;
      div.innerHTML = `
        <div>
          <strong>${p.name}</strong> (${p.age})<br>
          <small>${p.symptoms}</small>
        </div>
        <div>${p.token}</div>
        <div style="color: ${getPriorityColor(p.priorityLevel)}">${p.priorityLevel}</div>
        <div>${p.status}</div>
        <div>${timeLeft} min left</div>
      `;
      
      // ✅ ADD THIS LINE HERE
      div.classList.add('fade-in');
      
      list.appendChild(div);
    });
  });
}

function getPriorityColor(priority) {
  const colors = {
    'Critical': '#dc2626',
    'Emergency': '#ea580c',
    'Urgent': '#f59e0b',
    'Non-urgent': '#16a34a'
  };
  return colors[priority] || '#666';
}

function updateStats(patients) {
  if (!patients) {
    document.getElementById('waitingCount').textContent = '0';
    document.getElementById('consultationCount').textContent = '0';
    document.getElementById('completedCount').textContent = '0';
    document.getElementById('totalCount').textContent = '0';
    return;
  }
  
  const patientArray = Object.values(patients);
  const waiting = patientArray.filter(p => p.status === 'waiting').length;
  const inConsultation = patientArray.filter(p => p.status === 'in-consultation').length;
  const completed = patientArray.filter(p => p.status === 'completed').length;
  
  document.getElementById('waitingCount').textContent = waiting;
  document.getElementById('consultationCount').textContent = inConsultation;
  document.getElementById('completedCount').textContent = completed;
  document.getElementById('totalCount').textContent = patientArray.length;
}

// ---------------- Staff Functions ----------------
function toggleStaffView() {
  const publicView = document.getElementById('publicView');
  const staffView = document.getElementById('staffView');
  const isStaff = staffView.style.display === 'none';
  
  if (isStaff) {
    const password = prompt('Enter staff password:');
    if (password === 'staff123') {
      publicView.style.display = 'none';
      staffView.style.display = 'block';
      loadStaffPatients();
    }
  } else {
    publicView.style.display = 'block';
    staffView.style.display = 'none';
  }
}

function showStaffTab(tabName) {
  // Update tab buttons
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');
  
  // Hide all tab contents
  document.getElementById('staffWaitingList').style.display = 'none';
  document.getElementById('staffInProgressList').style.display = 'none'; 
  document.getElementById('staffCompletedList').style.display = 'none';
  
  // Show selected tab
  let tabToShow;
  if (tabName === 'waiting') tabToShow = 'staffWaitingList';
  else if (tabName === 'in-progress') tabToShow = 'staffInProgressList';
  else if (tabName === 'completed') tabToShow = 'staffCompletedList';
  
  document.getElementById(tabToShow).style.display = 'block';
  
  // Refresh the data for this tab
  loadStaffPatients();
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).replace('-', '');
}

function loadStaffPatients() {
  db.ref('patients').on('value', snap => {
    const patients = snap.val();
    const waitingDiv = document.getElementById('staffWaitingPatients');
    const inProgressDiv = document.getElementById('staffInProgressPatients');
    const completedDiv = document.getElementById('staffCompletedPatients');
    
    waitingDiv.innerHTML = '';
    inProgressDiv.innerHTML = '';
    completedDiv.innerHTML = '';
    
    if (!patients) {
      waitingDiv.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">No patients waiting</p>';
      inProgressDiv.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">No patients in consultation</p>';
      completedDiv.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">No completed consultations</p>';
      return;
    }
    
    Object.entries(patients).forEach(([key, patient]) => {
      const patientDiv = createStaffPatientCard(patient, key);
      
      if (patient.status === 'waiting') {
        waitingDiv.appendChild(patientDiv);
      } else if (patient.status === 'in-consultation') {
        inProgressDiv.appendChild(patientDiv);
      } else if (patient.status === 'completed') {
        completedDiv.appendChild(patientDiv);
      }
    });

    // Add empty state messages if no patients in any tab
    if (waitingDiv.innerHTML === '') {
      waitingDiv.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">No patients waiting</p>';
    }
    if (inProgressDiv.innerHTML === '') {
      inProgressDiv.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">No patients in consultation</p>';
    }
    if (completedDiv.innerHTML === '') {
      completedDiv.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">No completed consultations</p>';
    }
  });
}

function createStaffPatientCard(patient, key) {
  const div = document.createElement('div');
  div.className = `patient-item priority-${patient.priorityLevel.toLowerCase().replace(' ', '-')}`;
  
  const waitTime = Math.floor((Date.now() - patient.registeredAt) / 60000);
  
  div.innerHTML = `
    <div>
      <strong>${patient.name}</strong> (${patient.age})<br>
      <small>${patient.symptoms}</small><br>
      <small>Token: ${patient.token}</small>
    </div>
    <div>${patient.priorityLevel}</div>
    <div>${waitTime} min</div>
    <div>${patient.vitals.temperature}°F</div>
    <div class="staff-actions">
      ${patient.status === 'waiting' ? 
        `<button class="action-btn btn-start" onclick="startConsultation('${key}')">Start</button>
         <button class="action-btn btn-cancel" onclick="cancelPatient('${key}')">Cancel</button>` : 
      patient.status === 'in-consultation' ? 
        `<button class="action-btn btn-complete" onclick="completeConsultation('${key}')">Complete</button>` :
        `<span style="color: green;">✓ Done</span>`
      }
    </div>
  `;
  
  // ✅ ADD THIS LINE HERE
  div.classList.add('fade-in');
  
  return div;
}

function startConsultation(patientKey) {
  db.ref('patients/' + patientKey).update({
    status: 'in-consultation',
    doctor: 'Dr. Smith',
    consultationStart: Date.now()
  }).then(() => {
    // Force refresh staff view after status change
    loadStaffPatients();
    // Auto-switch to In Consultation tab
    showStaffTab('in-progress');
  });
}

function completeConsultation(patientKey) {
  db.ref('patients/' + patientKey).update({
    status: 'completed',
    consultationEnd: Date.now()
  }).then(() => {
    // Force refresh after completion
    loadStaffPatients();
    // Auto-switch to Completed tab  
    showStaffTab('completed');
  });
}

function cancelPatient(patientKey) {
  if (confirm('Are you sure you want to cancel this patient?')) {
    db.ref('patients/' + patientKey).remove()
    .then(() => {
      loadStaffPatients(); // Refresh the view
    });
  }
}

// ---------------- Expire Tokens ----------------
function checkForExpiredTokens() {
  const now = Date.now();
  db.ref('patients').once('value', snapshot => {
    const patients = snapshot.val();
    if (!patients) return;
    Object.entries(patients).forEach(([key, patient]) => {
      if (patient.status === 'waiting') {
        const timePassed = now - patient.registeredAt;
        if (timePassed > 30 * 60 * 1000) {
          db.ref('archived/patients/' + key).set({
            ...patient,
            status: 'expired',
            expiredAt: now
          });
          db.ref('patients/' + key).remove();
        }
      }
    });
  });
}

// ---------------- Archive Completed Patients ----------------
function archiveCompletedPatients() {
  db.ref('patients').once('value', snapshot => {
    const patients = snapshot.val();
    if (!patients) return;
    Object.entries(patients).forEach(([key, patient]) => {
      if (patient.status === 'completed') {
        db.ref('archived/patients/' + key).set({
          ...patient,
          completedAt: Date.now()
        });
        db.ref('patients/' + key).remove();
      }
    });
  });
}

// Initialize
loadPatients();
setInterval(loadPatients, 5000);
setInterval(checkForExpiredTokens, 30000);
setInterval(archiveCompletedPatients, 10000);

function toggleHelp() {
  const modal = document.getElementById('helpModal');
  const publicHelp = document.getElementById('publicHelp');
  const staffHelp = document.getElementById('staffHelp');
  
  // Check which view is active
  const isStaffView = document.getElementById('staffView').style.display !== 'none';
  
  if (isStaffView) {
    publicHelp.style.display = 'none';
    staffHelp.style.display = 'block';
  } else {
    publicHelp.style.display = 'block';
    staffHelp.style.display = 'none';
  }
  
  // Toggle modal visibility
  modal.style.display = modal.style.display === 'flex' ? 'none' : 'flex';
}