

//placeholder for graph, labels and data will be supplied here
const data = {
    labels: ["2025-11-01", "2025-11-02", "2025-11-03", "2025-11-04", "2025-11-05"],
    datasets: [{
        label: 'Stock % Change',
        data: [1.2, -0.5, 2.3, -1.1, 0.8],
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

// failsafe timeout (literally a placeholder for now)
setTimeout(() => {
    updateOutput("The stock showed a large jump on Nov 3 likely due to positive earnings. Other small fluctuations seem normal.");
}, 2000);
