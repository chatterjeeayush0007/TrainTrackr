document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById('trains-list');

    // Get user info from localStorage (onboarded data)
    const userInfo = JSON.parse(localStorage.getItem('user_info'));
    if (!userInfo) {
        container.innerHTML = '<p class="no-trains">No user info found! Please onboard first.</p>';
        return;
    }

    try {
        // 1️⃣ Fetch nearest stations from backend
        const nearestRes = await fetch("http://127.0.0.1:8000/users/details", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userInfo)
        });
        const nearestData = await nearestRes.json();
        const stations = nearestData.nearest_stations || [];

        if (!stations.length) {
            container.innerHTML = '<p class="no-trains">No nearby stations found!</p>';
            return;
        }

        // 2️⃣ Fetch predictions for nearest stations
        const predictionsRes = await fetch(`http://127.0.0.1:8000/predictions?stations=${stations.join(",")}`);
        const predictionsData = await predictionsRes.json();
        const trains = predictionsData.predictions || [];

        // 3️⃣ Render trains
        container.innerHTML = '';
        if (!trains.length) {
            container.innerHTML = '<p class="no-trains">No trains available!</p>';
            return;
        }

        trains.forEach(train => {
            const div = document.createElement('div');
            div.className = "train-card";
            div.innerHTML = `
                <h3>${train.name}</h3>
                <p>ETA: ${train.expected_arrival} | ETD: ${train.expected_departure}</p>
                <p>Crowd Level: <span class="crowd-${train.crowd.toLowerCase()}">${train.crowd.toUpperCase()}</span></p>
            `;
            container.appendChild(div);
        });

    } catch (err) {
        console.error("Error fetching trains:", err);
        container.innerHTML = '<p class="no-trains">Error fetching train data!</p>';
    }
});