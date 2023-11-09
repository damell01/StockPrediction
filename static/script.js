function predictStockPrices() {
    const startDate = document.getElementById('start-date').value;

    fetch(`/predict?start_date=${startDate}`)
        .then(response => response.json())
        .then(data => {
            const labels = data.labels;
            const actualPrices = data.actualPrices;
            const predictedPrices = data.predictedPrices;

            // Calculate the height of the chart based on 15vh (15% of the viewport height)
            const chartHeight = window.innerHeight * 0.95; // 15% of the viewport height

            // Set the new canvas size (width of the page and fixed height of 15vh)
            const canvas = document.getElementById('stockChart');
            canvas.width = window.innerWidth;
            canvas.height = chartHeight;

            // Create a chart using Chart.js with the updated canvas size
            const ctx = canvas.getContext('2d');
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
                    responsive: false, // Disable automatic resizing of the chart
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
