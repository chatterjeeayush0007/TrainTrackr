const BASE_URL = "http://127.0.0.1:8000";

async function getTrains() {
    const res = await fetch(`${BASE_URL}/trains/`);
    return await res.json();
}

async function getTrainRoute(train_no) {
    const res = await fetch(`${BASE_URL}/trains/${train_no}/route`);
    return await res.json();
}

async function getDelay(train_no) {
    const res = await fetch(`${BASE_URL}/predictions/delay/${train_no}`);
    const data = await res.json();
    return data.predicted_delay_minutes;
}

async function getCrowdLevel(station) {
    const res = await fetch(`${BASE_URL}/crowd/${station}`);
    const data = await res.json();
    return data.crowd_level;
}

// Core function: find best train
async function findBestTrain(startStation, destStation, arrivalTime) {
    const trainData = await getTrains();
    const arrivalDt = new Date();
    const [hours, minutes] = arrivalTime.split(":");
    arrivalDt.setHours(hours, minutes);

    let candidates = [];

    const crowd = await getCrowdLevel(startStation);
    const CROWD_SCORE = { Low: 0, Medium: 1, High: 2 };
    const crowdPenalty = CROWD_SCORE[crowd] || 1;

    for (let train of trainData.trains) {
        const route = await getTrainRoute(train.train_no);
        const stops = route.stops;

        const startIndex = stops.findIndex(s => s.station.toLowerCase() === startStation.toLowerCase());
        const destIndex = stops.findIndex(s => s.station.toLowerCase() === destStation.toLowerCase());

        if (startIndex === -1 || destIndex === -1 || startIndex >= destIndex) continue;

        const delay = await getDelay(train.train_no);
        const destArrival = new Date();
        const [destHours, destMinutes] = stops[destIndex].arrival.split(":");
        destArrival.setHours(destHours, destMinutes);
        destArrival.setMinutes(destArrival.getMinutes() + delay);

        const timeDiff = Math.round((destArrival - arrivalDt) / 60000);

        candidates.push({
            train_no: train.train_no,
            train_name: train.train_name,
            expected_arrival: destArrival,
            delay,
            time_diff: timeDiff,
            crowd,
            crowd_penalty: crowdPenalty
        });
    }

    if (!candidates.length) return null;

    const onTime = candidates.filter(c => c.time_diff <= 0);
    let best;
    if (onTime.length) {
        best = onTime.reduce((a, b) => (a.crowd_penalty < b.crowd_penalty ? a : b));
    } else {
        best = candidates.reduce((a, b) => (a.crowd_penalty < b.crowd_penalty ? a : b));
    }
    return best;
}
