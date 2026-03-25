// gui/onboarding.js

const form = document.getElementById('onboarding-form');

// Fetch stations from backend
async function fetchStations(query) {
    if (!query) return [];
    try {
        const res = await fetch(`http://127.0.0.1:8000/stations/search?q=${encodeURIComponent(query)}`);
        if (!res.ok) return [];
        const data = await res.json();
        return (data.results || []).map(name => ({ name }));
    } catch (err) {
        console.error("Error fetching stations:", err);
        return [];
    }
}

// Auto-suggest setup
function setupAutoSuggest(inputId, containerId) {
    const input = document.getElementById(inputId);
    const container = document.getElementById(containerId);

    input.addEventListener('input', async () => {
        const query = input.value.trim();
        const stations = await fetchStations(query);
        container.innerHTML = '';
        if (stations.length > 0) {
            container.style.display = 'block';
            stations.forEach(station => {
                const div = document.createElement('div');
                div.className = 'suggestion-item';
                div.textContent = station.name;
                div.addEventListener('click', () => {
                    input.value = station.name;
                    container.style.display = 'none';
                });
                container.appendChild(div);
            });
        } else {
            container.style.display = 'none';
        }
    });

    document.addEventListener('click', e => {
        if (!container.contains(e.target) && e.target !== input) container.style.display = 'none';
    });
}

// Initialize dropdowns
setupAutoSuggest('from_station', 'from_suggestions');
setupAutoSuggest('destination_station', 'to_suggestions');

// Form submission to MongoDB
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
        username: document.getElementById('username').value,
        pincode: document.getElementById('pincode').value,
        passenger_type: document.getElementById('passenger_type').value,
        ticket_type: document.getElementById('ticket_type').value,
        journey_time: document.getElementById('journey_time').value,
        source_station: document.getElementById('from_station').value,
        destination_station: document.getElementById('destination_station').value
    };

    try {
        const res = await fetch('http://127.0.0.1:8000/users/details', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const data = await res.json();
        console.log("User saved:", data);

        // Save locally too (optional)
        localStorage.setItem('user_info', JSON.stringify(payload));

        // Redirect to dashboard
        window.location.href = 'dashboard.html';
    } catch (err) {
        alert("Failed to save details: " + err.message);
        console.error(err);
    }
});