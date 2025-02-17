const API_BASE_URL = "http://127.0.0.1:5000";

// Function to fetch courses and populate dropdown
async function fetchCourses() {
    try {
        const response = await fetch(`${API_BASE_URL}/courses`);
        if (!response.ok) throw new Error("Failed to fetch courses");
        
        const courses = await response.json();
        const courseSelect = document.getElementById("courseSelect");

        courseSelect.innerHTML = ""; // Clear existing options
        courses.forEach(course => {
            const option = document.createElement("option");
            option.value = course.id;
            option.textContent = course.name;
            courseSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Error fetching courses:", error);
    }
}

// Function to fetch faculties and populate dropdown
async function fetchFaculties() {
    try {
        const response = await fetch(`${API_BASE_URL}/faculties`);
        if (!response.ok) throw new Error("Failed to fetch faculties");
        
        const faculties = await response.json();
        const facultySelect = document.getElementById("facultySelect");

        facultySelect.innerHTML = ""; // Clear existing options
        faculties.forEach(faculty => {
            const option = document.createElement("option");
            option.value = faculty.id;
            option.textContent = faculty.name;
            facultySelect.appendChild(option);
        });
    } catch (error) {
        console.error("Error fetching faculties:", error);
    }
}

// Function to fetch timetable entries and display them
async function fetchTimetable() {
    try {
        const response = await fetch(`${API_BASE_URL}/timetable`);
        if (!response.ok) throw new Error("Failed to fetch timetable");
        
        const timetable = await response.json();
        const timetableBody = document.getElementById("timetableBody");
        timetableBody.innerHTML = ""; // Clear existing data

        timetable.forEach(entry => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${entry.course_name}</td>
                <td>${entry.faculty_name}</td>
                <td>${entry.classroom}</td>
                <td>${entry.start_time}</td>
                <td>${entry.end_time}</td>
            `;
            timetableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching timetable:", error);
    }
}

// Function to submit timetable form
document.getElementById("timetableForm")?.addEventListener("submit", async function (event) {
    event.preventDefault();

    const courseId = document.getElementById("courseSelect").value;
    const facultyId = document.getElementById("facultySelect").value;
    const classroom = document.getElementById("classroomInput").value;
    const startTime = document.getElementById("startTime").value;
    const endTime = document.getElementById("endTime").value;

    const lectureData = {
        course_id: courseId,
        faculty_id: facultyId,
        classroom: classroom,
        start_time: startTime,
        end_time: endTime
    };

    try {
        const response = await fetch(`${API_BASE_URL}/timetable/add`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(lectureData)
        });

        const result = await response.json();
        if (response.ok) {
            alert("Timetable added successfully!");
            document.getElementById("timetableForm").reset();
            fetchTimetable(); // Refresh timetable data
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        console.error("Error adding timetable:", error);
    }
});

// Function to send notification to faculty
async function sendNotification(facultyId) {
    try {
        const response = await fetch(`${API_BASE_URL}/notify/${facultyId}`, { method: "POST" });
        const result = await response.json();
        if (response.ok) {
            console.log("Notification sent:", result.message);
        } else {
            console.error("Failed to send notification:", result.error);
        }
    } catch (error) {
        console.error("Error in sending notification:", error);
    }
}

// Initialize page data
document.addEventListener("DOMContentLoaded", function () {
    fetchCourses();
    fetchFaculties();
    fetchTimetable();
});
