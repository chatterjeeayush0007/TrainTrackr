const BASE_URL = "http://127.0.0.1:8000";

// ----------------- AUTH MODAL -----------------
function openAuthModal() {
    document.getElementById("auth-modal").classList.remove("hidden");
}
function closeAuthModal() {
    document.getElementById("auth-modal").classList.add("hidden");
}
function toggleAuthMode(e) {
    e.preventDefault();
    const title = document.getElementById("auth-title");
    const button = document.getElementById("main-auth-button");
    if (title.innerText.includes("Sign Up")) {
        title.innerText = "Sign In to Your Account";
        button.innerText = "Sign In";
        document.getElementById("signup-fields").style.display = "none";
    } else {
        title.innerText = "Sign Up to Start Tracking";
        button.innerText = "Sign Up";
        document.getElementById("signup-fields").style.display = "block";
    }
}
function simulateGoogleSignIn() {
    alert("Simulated Google Sign In successful!");
    window.location.href = "dashboard.html";
}

// ----------------- DASHBOARD / TRAIN SEARCH -----------------
async function fetchStations() {
    const resp = await fetch(`${BASE_URL}/stations/`);
    if (!resp.ok) throw new Error("Could not fetch stations");
    const data = await resp.json();
    return data.stations;
}

async function fetchTrains() {
    const resp = await fetch(`${BASE_URL}/trains/`);
    if (!resp.ok) throw new Error("Could not fetch trains");
    const data = await resp.json();
    return data.trains;
}

async function getTrainRoute(train_no) {
    const resp = await fetch(`${BASE_URL}/trains/${train_no}/route`);
    if (!resp.ok) throw new Error("Could not fetch route");
    return await resp.json();
}

async function getDelay(train_no) {
    const resp = await fetch(`${BASE_URL}/predictions/delay/${train_no}`);
    if (!resp.ok) throw new Error("Could not get delay");
    const data = await resp.json();
    return data.predicted_delay_minutes;
}

async function getCrowd(station) {
    const resp = await fetch(`${BASE_URL}/crowd/${station}`);
    if (!resp.ok) throw new Error("Could not get crowd");
    const data = await resp.json();
    return data.crowd_level;
}

const CROWD_SCORE = { "Low": 0, "Medium": 1, "High": 2 };

async function findBestTrain(start, dest, time) {
    const arrivalDt = new Date();
    const [hours, minutes] = time.split(":");
    arrivalDt.setHours(parseInt(hours), parseInt(minutes));

    const trains = await fetchTrains();
    const crowd = await getCrowd(start);
    const crowdPenalty = CROWD_SCORE[crowd] ?? 1;
    let candidates = [];

    for (let train of trains) {
        const route = await getTrainRoute(train.train_no);
        const stops = route.stops;

        const startIndex = stops.findIndex(s => s.station.toLowerCase() === start.toLowerCase());
        const destIndex = stops.findIndex(s => s.station.toLowerCase() === dest.toLowerCase());
        if (startIndex === -1 || destIndex === -1 || startIndex >= destIndex) continue;

        const delay = await getDelay(train.train_no);
        const scheduledArrival = new Date();
        const [sh, sm] = stops[destIndex].arrival.split(":");
        scheduledArrival.setHours(sh, sm);

        const expectedArrival = new Date(scheduledArrival.getTime() + delay * 60000);
        const timeDiff = Math.floor((expectedArrival - arrivalDt)/60000);

        candidates.push({
            train_no: train.train_no,
            train_name: train.train_name,
            expected_arrival: expectedArrival,
            delay,
            time_diff: timeDiff,
            crowd,
            crowd_penalty: crowdPenalty
        });
    }

    if (candidates.length === 0) return null;
    const onTime = candidates.filter(c => c.time_diff <= 0);
    if (onTime.length > 0) return onTime.reduce((a,b) => (a.crowd_penalty < b.crowd_penalty ? a : b));
    return candidates.reduce((a,b) => (a.crowd_penalty < b.crowd_penalty ? a : b));
}

// ----------------- Populate select inputs -----------------
document.addEventListener("DOMContentLoaded", async () => {
    const stations = await fetchStations();
    const fromSelect = document.getElementById("from-station");
    const toSelect = document.getElementById("to-station");
    stations.forEach(s => {
        const opt1 = document.createElement("option");
        opt1.value = s; opt1.text = s;
        fromSelect.appendChild(opt1);
        const opt2 = document.createElement("option");
        opt2.value = s; opt2.text = s;
        toSelect.appendChild(opt2);
    });
});

// ----------------- Search form submit -----------------
document.getElementById("search-form").addEventListener("submit", async e => {
    e.preventDefault();
    const start = document.getElementById("from-station").value;
    const dest = document.getElementById("to-station").value;
    const time = document.getElementById("desired-time-input").value;

    const resultsDiv = document.getElementById("results-container");
    resultsDiv.innerHTML = "Searching...";

    try {
        const best = await findBestTrain(start, dest, time);
        if (!best) {
            resultsDiv.innerHTML = "<p class='error'>No trains found for this route</p>";
            return;
        }
        resultsDiv.innerHTML = `
            <h3>📌 Recommended Train</h3>
            <p>Train No: ${best.train_no}</p>
            <p>Train Name: ${best.train_name}</p>
            <p>Expected Arrival: ${best.expected_arrival.getHours().toString().padStart(2,'0')}:${best.expected_arrival.getMinutes().toString().padStart(2,'0')}</p>
            <p>Delay: ${best.delay} min</p>
            <p>Crowd Level: ${best.crowd}</p>
        `;
    } catch(err) {
        resultsDiv.innerHTML = "<p class='error'>Error fetching train data</p>";
        console.error(err);
    }
});
