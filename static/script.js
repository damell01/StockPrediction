function predictStockPrices() {
    const startDate = document.getElementById('start-date').value;

    fetch(`/predict?start_date=${startDate}`)
        .then(response => response.json())
        .then(data => {
            const labels = data.labels;
            const actualPrices = data.actualPrices;
            const predictedPrices = data.predictedPrices;

            // Calculate Mean Absolute Error (MAE)
            let totalAbsoluteError = 0;
            for (let i = 0; i < actualPrices.length; i++) {
                totalAbsoluteError += Math.abs(predictedPrices[i] - actualPrices[i]);
            }
            const mae = totalAbsoluteError / actualPrices.length;

            // Display accuracy metric on the webpage
            if (!isNaN(mae)) {
                document.getElementById('accuracystat').innerText = `Mean Absolute Error (MAE): ${mae.toFixed(2)}`;
            } else {
                document.getElementById('accuracystat').innerText = 'Unable to calculate accuracy.';
            }

            // Create a chart using Chart.js
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
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
