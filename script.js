// This wrapper ensures the script waits for the HTML to load before running.
document.addEventListener('DOMContentLoaded', () => {

    const API_URL = '';

    const typeToIcon = {
        'personal': '🗓️', 'health': '💧', 'routine': '⏰',
        'meditation': '🧘', 'meal': '🍴', 'work': '💼', 'exercise': '🏃'
    };

    // --- Attach Event Listeners to Buttons ---
    document.getElementById('update-profile-btn').addEventListener('click', registerUser);
    document.getElementById('delete-profile-btn').addEventListener('click', deleteUser);
    document.getElementById('add-engagement-btn').addEventListener('click', addEngagement);

    // --- All Functions ---

    async function registerUser() {
        const username = document.getElementById('username').value;
        if (!username) {
            alert("Please enter a username.");
            return;
        }
        const payload = {
            username: username,
            height: document.getElementById('height').value,
            weight: document.getElementById('weight').value,
            job: document.getElementById('job').value,
            office_start: document.getElementById('office-start').value,
            office_end: document.getElementById('office-end').value,
        };
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        const data = await response.json();
        alert(data.message || data.error);
        if (response.ok) {
            generateSchedule();
        }
    }

    async function deleteUser() {
        const username = document.getElementById('username').value;
        if (!username) {
            alert("Please enter the username to delete.");
            return;
        }
        if (confirm(`Are you sure you want to delete the profile for "${username}"?`)) {
            const response = await fetch(`${API_URL}/delete_user/${username}`, {
                method: 'DELETE',
            });
            const data = await response.json();
            alert(data.message || data.error);
            if (response.ok) {
                document.getElementById('username').value = '';
                document.getElementById('height').value = '';
                document.getElementById('weight').value = '';
                document.getElementById('job').value = '';
                document.getElementById('office-start').value = '';
                document.getElementById('office-end').value = '';
                document.getElementById('schedule-list').innerHTML = '';
            }
        }
    }

    async function addEngagement() {
        const username = document.getElementById('username').value;
        const eventName = document.getElementById('engagement-name').value;
        const startTime = document.getElementById('engagement-start-time').value;
        const endTime = document.getElementById('engagement-end-time').value;
        if (!username || !eventName || !startTime || !endTime) {
            alert("Please provide username, event name, and both start and end times.");
            return;
        }
        if (endTime <= startTime) {
            alert("End time must be after start time.");
            return;
        }
        const response = await fetch(`${API_URL}/schedule_event`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: username,
                event_name: eventName,
                event_start_time: startTime,
                event_end_time: endTime
            }),
        });
        const data = await response.json();
        alert(data.message || data.error);
        if (response.ok) {
            document.getElementById('engagement-name').value = '';
            document.getElementById('engagement-start-time').value = '';
            document.getElementById('engagement-end-time').value = '';
            generateSchedule();
        }
    }

    async function generateSchedule() {
        const username = document.getElementById('username').value;
        if (!username) return;
        const response = await fetch(`${API_URL}/get_schedule/${username}`);
        const data = await response.json();
        const scheduleList = document.getElementById('schedule-list');
        scheduleList.innerHTML = '';
        if (data.schedule && data.schedule.length > 0) {
            data.schedule.forEach(item => {
                const li = document.createElement('li');
                li.classList.add(item.type);
                const icon = typeToIcon[item.type] || '⭐';
                li.innerHTML = `
                    <div class="schedule-icon" data-icon-type="${item.type}">${icon}</div>
                    <div class="schedule-content">
                        <div class="schedule-time">${item.time}</div>
                        <div class="schedule-name">${item.name}</div>
                    </div>
                `;
                scheduleList.appendChild(li);
            });
        } else if (data.error) {
            alert(`Could not get schedule: ${data.error}`);
        } else {
            const li = document.createElement('li');
            li.innerHTML = `<div class="schedule-content"><div class="schedule-name">No schedule items found. Update your profile and add engagements to get started.</div></div>`;
            scheduleList.appendChild(li);
        }
    }
});