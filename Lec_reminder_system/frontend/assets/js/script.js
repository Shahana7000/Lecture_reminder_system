document.addEventListener("DOMContentLoaded", function () {
    loadFaculty();
    loadTimetable();

    document.getElementById("facultyForm").addEventListener("submit", function (event) {
        event.preventDefault();
        addFaculty();
    });

    document.getElementById("timetableForm")?.addEventListener("submit", function (event) {
        event.preventDefault();
        addTimetable();
    });
});

async function addFaculty() {
    const name = document.getElementById("name").value;
    const phone = document.getElementById("phone").value;
    const whatsapp = document.getElementById("whatsapp").value;
    
    const response = await fetch('/api/faculty', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, phone, whatsapp })
    });
    if (response.ok) {
        document.getElementById("facultyForm").reset();
        loadFaculty();
    }
}

async function loadFaculty() {
    const response = await fetch('/api/faculty');
    const facultyList = await response.json();
    const tableBody = document.getElementById("facultyList");
    if (!tableBody) return;
    tableBody.innerHTML = "";
    
    facultyList.forEach(faculty => {
        const row = `<tr><td>${faculty.name}</td><td>${faculty.phone}</td><td>${faculty.whatsapp}</td></tr>`;
        tableBody.innerHTML += row;
    });
}

async function addTimetable() {
    const facultySelect = document.getElementById("faculty");
    const lectureTime = document.getElementById("lecture_time").value;
    
    if (!facultySelect.value || !lectureTime) return;
    
    const response = await fetch('/api/timetable', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ faculty: facultySelect.value, lectureTime })
    });
    if (response.ok) {
        document.getElementById("timetableForm").reset();
        loadTimetable();
    }
}

async function loadTimetable() {
    const response = await fetch('/api/timetable');
    const timetable = await response.json();
    const tableBody = document.getElementById("timetableList");
    if (!tableBody) return;
    tableBody.innerHTML = "";
    
    timetable.forEach(entry => {
        const row = `<tr><td>${entry.faculty}</td><td>${entry.lectureTime}</td></tr>`;
        tableBody.innerHTML += row;
    });
}
