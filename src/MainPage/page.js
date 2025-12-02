//placeholder for graph, labels and data will be supplied here
const data = {
    labels: ["2025-11-01", "2025-11-02", "2025-11-03", "2025-11-04", "2025-11-05"],
    datasets: [{
        label: 'Stock % Change',
        data: [1.2, -0.5, 2.3, -1.1, 0.8], //preset data that im keeping
        borderColor: '#4CAF50',
        backgroundColor: 'rgba(76, 175, 80, 0.2)',
        tension: 0.4,
        fill: true,
        pointRadius: 3
    }]
};

//just a simple config for the graph
const config ={
    type: 'line',
    data: data,
    options: {
        responsive: true,
        plugins: {legend: {display: false} },
        scales: {
            x: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#fff' } },
            y: {grid: { color: 'rgba(255,255,255,0.1)'}, ticks: {color: '#fff' } }
        }
    }
};

const ctx = document.getElementById('graphChart').getContext('2d');
const graphChart = new Chart(ctx, config);

//llm output here
function updateOutput(text) {
    const outputDiv = document.getElementById("llm-output"); //assuming that is the elementID
    outputDiv.textContent = text;
}


// backend here

const ticker = "AAPL"; //placeholder here

// fetch big moves from backend
async function fetchMoves() {
    try {
        const res = await fetch(`/data/${ticker}`);
        const data = await res.json();

        const moves = data.moves || [];
        const labels = moves.map(m => m.time);
        const values = moves.map(m => m.move);

        //update the existing chart with new data
        graphChart.data.labels = labels;
        graphChart.data.datasets[0].data = values;
        graphChart.update();

        return moves;
    } catch (err) {
        console.error("Error fetching moves:", err);
        return [];
    }
}

//fetch LLM explanation from sam backend
async function fetchExplanation(moves) {
    try {
        const res = await fetch("/explain", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ticker: ticker })
        });
        const data = await res.json();
        updateOutput(data.explanation);
    } catch (err) {
        console.error("Error fetching explanation:", err);
        updateOutput("Error fetching explanation");
    }
}

//main loader function
async function loadData() {
    const moves = await fetchMoves();
    if (moves.length === 0) {
        updateOutput("No big moves found for this ticker.");
        return;
    }
    await fetchExplanation(moves);
}

//load
loadData();

//Refresh 30 sec
setInterval(loadData, 30000);
