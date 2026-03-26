// -----------------------------
// Backend base URL (Render deployment)
// -----------------------------
const BASE_URL = "https://traintrackr.onrender.com";

// -----------------------------
// Fetch all trains with crowd (for dashboard)
// -----------------------------
async function fetchTrains() {
    try {
        const res = await fetch(`${BASE_URL}/predictions/all`);
        const data = await res.json();

        const tbody = document.querySelector("#trains-table tbody");
        if (!tbody) return; // Only for dashboard page
        tbody.innerHTML = ""; // clear old rows

        data.trains.forEach(train => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${train.train_no}</td>
                <td>${train.train_name}</td>
                <td>${train.current_station}</td>
                <td>${train.expected_arrival}</td>
                <td>${train.expected_departure}</td>
                <td>${train.predicted_delay_minutes}</td>
                <td>${train.status}</td>
                <td>${train.predicted_crowd ?? "N/A"}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error("Error fetching trains:", err);
    }
}

// -----------------------------
// Save user journey details (details page)
// -----------------------------
async function saveJourneyDetails(event) {
    event.preventDefault();

    const payload = {
        username: document.getElementById("username").value,
        pincode: document.getElementById("pincode").value,
        passenger_type: document.getElementById("passenger_type").value,
        ticket_type: document.getElementById("ticket_type").value,
        from_date: document.getElementById("from_date").value || null,
        to_date: document.getElementById("to_date").value || null,
        journey_time: document.getElementById("journey_time").value,
        source_station: document.getElementById("source_station").value || null,
        destination_station: document.getElementById("destination_station").value
    };

    const output = document.getElementById("output");
    const nearestUl = document.getElementById("nearest-stations");

    try {
        const res = await fetch(`${BASE_URL}/users/details`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (!res.ok) {
            output.innerHTML = `<p style="color:red;">Error: ${data.detail}</p>`;
            return;
        }

        output.innerHTML = `
            <p style="color:green;">${data.message}</p>
            <p>Predicted Crowd: ${data.predicted_crowd ?? "N/A"}</p>
        `;

        nearestUl.innerHTML = "";
        (data.nearest_stations || []).forEach(s => {
            const li = document.createElement("li");
            li.textContent = `${s.name} (${s.distance_km.toFixed(2)} km)`;
            nearestUl.appendChild(li);
        });

    } catch (err) {
        console.error(err);
        output.innerHTML = `<p style="color:red;">Request failed. Check console.</p>`;
    }
}

// -----------------------------
// Find nearest stations (details page)
// -----------------------------
async function findNearestStations() {
    const pincode = document.getElementById("pincode").value;
    if (!pincode) return alert("Enter pincode!");

    try {
        const res = await fetch(`${BASE_URL}/users/nearest_stations?pincode=${pincode}`);
        const stations = await res.json();

        const ul = document.getElementById("nearest-stations");
        if (!ul) return;
        ul.innerHTML = "";

        stations.forEach(s => {
            const li = document.createElement("li");
            li.textContent = `${s.name} (${s.distance_km.toFixed(2)} km)`;
            ul.appendChild(li);
        });
    } catch (err) {
        console.error("Error fetching nearest stations:", err);
    }
}

// -----------------------------
// Event listeners
// -----------------------------
document.addEventListener("DOMContentLoaded", () => {
    const journeyForm = document.getElementById("journey-form");
    if (journeyForm) journeyForm.addEventListener("submit", saveJourneyDetails);

    const findStationsBtn = document.getElementById("find-stations");
    if (findStationsBtn) findStationsBtn.addEventListener("click", findNearestStations);

    // Initial load for dashboard table
    fetchTrains();
    // Auto-refresh every minute
    setInterval(fetchTrains, 60000);
});