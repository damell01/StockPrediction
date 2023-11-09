document.addEventListener("DOMContentLoaded", function () {
    // Fetch initial data when the page loads
    predictStockPrices();
});

function predictStockPrices() {
    const startDate = document.getElementById('start-date').value;

    fetch(`/predict?start_date=${startDate}`)
        .then(response => response.json())
        .then(data => {
            const labels = data.labels;
            const actualPrices = data.actualPrices;
            const predictedPrices = data.predictedPrices;

            const ctx = document.getElementById('stockChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Actual Prices',
                        data: actualPrices,
                        borderColor: 'blue',
                        borderWidth: 1,
                        fill: false
                    }, {
                        label: 'Predicted Prices',
                        data: predictedPrices,
                        borderColor: 'orange',
                        borderWidth: 1,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day'
                            }
                        },
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });
}
