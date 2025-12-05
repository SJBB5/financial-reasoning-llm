//Hudson


let graphChart = null;
let rawDataChart = null;

//create chart with formatted colors (this looked the best so dont fucking change it)
function initChart() {
    const ctx = document.getElementById('graphChart').getContext('2d');
    
    graphChart = new Chart(ctx,{
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Stock % Change',
                data: [],
                borderColor: '#4CAF50',
                backgroundColor: 'rgba(76, 175, 80, 0.2)',
                tension: 0.4,
                fill: true,
                pointRadius: [],
                pointHoverRadius: 8,
                pointBackgroundColor: [],
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio:false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color:'#fff',
                        font: {
                            size: 14,
                            family:'Raleway'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont:{
                        size: 14,
                        family:'Raleway'
                    },
                    bodyFont: {
                        size: 13,
                        family:'Raleway'
                    },
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.y;
                            const direction = value > 0 ? '↑' : '↓';
                            return `${direction} ${Math.abs(value).toFixed(2)}%`;
                        }
                    }
                }
            },
            scales:{
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff',
                        font: {
                            family: 'Raleway'
                        }
                    }
                },
                y: {
                    grid:{
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks:{
                        color: '#fff',
                        font:{
                            family: 'Raleway'
                        },
                        callback: function(value) {
                            return value.toFixed(1) + '%';
                        }
                    }
                }
            }
        }
    }); //literally just dont touch this
}

//create raw stock data chart
function initRawDataChart() {
    const ctx = document.getElementById('rawDataChart').getContext('2d');
    
    rawDataChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Stock Price',
                data: [],
                borderColor: '#2196F3',
                backgroundColor: 'rgba(33, 150, 243, 0.2)',
                tension: 0.4,
                fill: true,
                pointRadius: 2,
                pointHoverRadius: 6,
                pointBackgroundColor: '#2196F3',
                pointBorderColor: '#fff',
                pointBorderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#fff',
                        font: {
                            size: 14,
                            family: 'Raleway'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: {
                        size: 14,
                        family: 'Raleway'
                    },
                    bodyFont: {
                        size: 13,
                        family: 'Raleway'
                    },
                    callbacks: {
                        label: function(context) {
                            return `$${context.parsed.y.toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff',
                        font: {
                            family: 'Raleway'
                        }
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff',
                        font: {
                            family: 'Raleway'
                        },
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}

//tickers in dropdown
async function loadTickers(){
    try {
        const response = await fetch('/api/tickers'); //fetch and ticker reponse here for dropdown
        const tickers = await response.json();
        
        const select = document.getElementById('ticker-select');
        select.innerHTML = '<option value="">Select a ticker</option>'; //keep as innerHTML select option (llooks best)
        
        tickers.forEach(ticker =>{
            const option = document.createElement('option');
            option.value = ticker.symbol;
            option.textContent = `${ticker.symbol}-${ticker.name}`;
            select.appendChild(option);

            //check drop here
        });
        
        //default AAPL to follow Sam
        select.value = 'AAPL';
        
    } catch (error) { //just give up if this happens tbh
        console.error('Error loading tickers:', error);
        document.getElementById('ticker-select').innerHTML = '<option value="AAPL">AAPL - Apple Inc.</option>';
    }
}

//show or hide loading statea, currently set to disable loading for this
function setLoading(isLoading) {
    document.getElementById('loading').style.display = isLoading ? 'block' : 'none'; //i still dont know what tehse 
    const containers = document.querySelectorAll('.container');
    containers.forEach(container => {
        container.style.display = isLoading ? 'none' : 'flex';
    });
    document.getElementById('analyze-btn').disabled = isLoading;
    document.getElementById('ticker-select').disabled = isLoading;
    document.getElementById('threshold-input').disabled = isLoading;
}

//quick and easy formatting 
function formatExplanation(text) {
    text = text.replace(/^#\s*$/gm, '');
    text = text.replace(/^#\s+\d+\./gm, '');
                                            //removes # in some summaries issue NOT WORKING WTF
    //markdown style 
    text = text.replace(/### (.*)/g, '<h3>$1</h3>');
    text = text.replace(/## (.*)/g, '<h2>$1</h2>');
    
    //headers into bold for strong
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    //line breaks will be paragraphs
    const paragraphs = text.split('\n\n').map(para => {
        para = para.trim();
        if (para.startsWith('<h')) {
            return para;
        } else if (para.startsWith('---')) {
            return '<hr>';
        } else if (para.length > 0) {
            para = para.replace(/\n/g, '<br>');
            return `<p>${para}</p>`;
        }
        return '';
    }).filter(p => p.length > 0);
    
    return paragraphs.join('');
}

//analyze function using select and input threshold
async function analyzeStock() {
    const ticker = document.getElementById('ticker-select').value;
    const threshold = parseFloat(document.getElementById('threshold-input').value);
    
    if (!ticker) {
        alert('Please select a ticker');
        return;
    }

    //hudson check these tickers are working (done) to hudson from hudson
    
    if (isNaN(threshold) || threshold < 1 || threshold > 20) {
        alert('Please enter a valid threshold between 1 and 20');
        return;
    }


    
    
    setLoading(true);
    
    try {
        const response = await fetch('/api/analyze', { //post method with response.json
            method: 'POST',
            headers:{
                'Content-Type': 'application/json' //default application/json, dont change
            },
            body: JSON.stringify({
                ticker: ticker,
                threshold: threshold
            })
        });
        console.log('Response status:', response.status, 'OK?', response.ok);
        if (!response.ok){
            const errorData = await response.json();
            throw new Error(errorData.error || 'Analysis failed');
        }
        
        const data =await response.json();
        
        //if succusseful post, get data and move it to chart
        if (data.moves && data.moves.length > 0) {
            const labels = data.moves.map(m =>{

                //print
                const date = new Date(m.date);
                return date.toLocaleDateString('en-US', { 
                    month: 'short', 
                    day: 'numeric',
                    year: 'numeric'
                });

            });
            
            const values = data.moves.map(m => m.move);
            
            //Find max and min values
            const maxValue = Math.max(...values);
            const minValue = Math.min(...values);
            
            //et point sizes and colors - highlight max/min
            const pointRadii = values.map(v => {
                if (v === maxValue || v === minValue) return 10;
                return 6;
            });
            
            const pointColors = values.map(v => {
                if (v === maxValue) return '#FFD700'; // gold
                if (v === minValue) return '#FF6B6B'; // red
                return '#4CAF50';
            });
            
            graphChart.data.labels =labels;
            graphChart.data.datasets[0].data =values;
            graphChart.data.datasets[0].pointRadius = pointRadii;
            graphChart.data.datasets[0].pointBackgroundColor = pointColors;
            graphChart.data.datasets[0].label =`${data.ticker} - Big Moves (>${threshold}% threshold)`;
            //update chart here
            graphChart.update();
        } else {
            //if no moves are found, jsut clear the  data and update
            graphChart.data.labels =[];
            //keep as arrays for data row/col
            graphChart.data.datasets[0].data = [];
            graphChart.update();
        }
        
        //Update raw data chart hope work
        if (data.raw_data && data.raw_data.dates && data.raw_data.prices) {
            console.log('Raw data received:', data.raw_data.dates.length, 'dates,', data.raw_data.prices.length, 'prices');
            const rawLabels = data.raw_data.dates.map(d => {
                const date = new Date(d);
                return date.toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                });
            });
    
            rawDataChart.data.labels = rawLabels;
            rawDataChart.data.datasets[0].data = data.raw_data.prices;
            rawDataChart.data.datasets[0].label = `${data.ticker} - Stock Price`;
            rawDataChart.update();
            console.log('Updated raw chart, first price:', data.raw_data.prices[0]);
            console.log('Chart updated. Canvas exists?', document.getElementById('rawDataChart') !== null);
            console.log('Chart has data?', rawDataChart.data.datasets[0].data.length); //for anything see console f12
            
        }
        
        //resend data to explanation module
        const outputDiv = document.getElementById('llm-output'); //literally just html injection here, dont change a single space. 
        outputDiv.innerHTML = `
            <div class="explanation-header">
                <h2>Analysis for ${data.ticker}</h2>
                <p class="timestamp">Generated: ${new Date(data.timestamp).toLocaleString()}</p> 
            </div>
            <div class="explanation-content">
                ${formatExplanation(data.explanation)}
            </div>
        `;
        
    } catch (error){ //Same as here
        console.error('Error during analysis:', error);
        document.getElementById('llm-output').innerHTML = `
            <div class="error-message">
                <h3> Analysis Failed</h3>
                <p>${error.message}</p>
                <p>Please check the console for details.</p>
            </div>
        `;
    } finally { //once done remove loading and therefore makes page visible
        setLoading(false);
    }
}

//default values on page load
window.addEventListener('DOMContentLoaded', () => {
    initChart();
    initRawDataChart();
    loadTickers();
});


//check done
