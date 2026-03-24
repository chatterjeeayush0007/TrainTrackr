document.addEventListener("DOMContentLoaded", () => {
    const pincodeInput = document.getElementById("pincodeInput");
    const fetchTrainsBtn = document.getElementById("fetchTrains");
    const nearestStationsList = document.getElementById("nearestStations");
    const crowdTableBody = document.querySelector("#crowdTable tbody");

    fetchTrainsBtn.addEventListener("click", async () => {
        const pincode = pincodeInput.value;
        if (!pincode) return alert("Enter a pincode");

        try {
            // 1️⃣ Fetch nearest stations
            const nearestRes = await fetch("http://127.0.0.1:8000/users/details", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username: "demo_user", pincode, passenger_type: "daily", ticket_type: "single", journey_time: "08:00", source_station: "Station A", destination_station: "Station B" })
            });
            const nearestData = await nearestRes.json();
            nearestStationsList.innerHTML = "";
            nearestData.nearest_stations.forEach(station => {
                const li = document.createElement("li");
                li.textContent = station;
                nearestStationsList.appendChild(li);
            });

            // 2️⃣ Fetch predictions
            const predictionsRes = await fetch(`http://127.0.0.1:8000/predictions?stations=${nearestData.nearest_stations.join(",")}`);
            const predictionsData = await predictionsRes.json();

            // Populate table
            crowdTableBody.innerHTML = "";
            predictionsData.predictions.forEach(train => {
                const tr = document.createElement("tr");
                tr.innerHTML = `<td>${train.name}</td><td>${train.departure}</td><td>${train.passengers}</td>`;
                crowdTableBody.appendChild(tr);
            });

        } catch (err) {
            alert("Error fetching data: " + err.message);
        }
    });
});