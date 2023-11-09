# app.py
from flask import Flask, request, jsonify, render_template
from sklearn.linear_model import LinearRegression
import pandas as pd
import datetime
import numpy as np

app = Flask(__name__)

# Load your AAPL data (assuming it's in a CSV file named 'aapl_data.csv')
data = pd.read_csv('AAPL.csv')
X = data[['Open', 'High', 'Low', 'Volume']]
y = data['Close']

# Train the model
model = LinearRegression()
model.fit(X, y)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict():
    selected_date_str = request.args.get('start_date')

    if not selected_date_str:
        return jsonify(error="Invalid or missing start date"), 400  # Bad request status code

    # Parse selected date
    selected_date = datetime.datetime.strptime(selected_date_str, '%Y-%m-%d').date()

    # Fetch the data for the selected date and next N days (N = number of predicted days)
    num_predicted_days = 15  # You can change this number based on your requirement
    selected_data = data[data['Date'] >= selected_date_str].head(num_predicted_days * 2)  # Fetch 10 days data
    input_features = selected_data[['Open', 'High', 'Low', 'Volume']]

    # Predict next N days
    predictions = model.predict(input_features.tail(num_predicted_days))

    # Calculate accuracy
    actual_prices = selected_data['Close'][:num_predicted_days].values
    accuracy = calculate_accuracy(actual_prices, predictions)

    # Prepare response JSON
    response = {
        'labels': selected_data['Date'].tolist(),
        'actualPrices': actual_prices.tolist(),
        'predictedPrices': predictions.tolist(),
        'accuracy': accuracy
    }
    return jsonify(response)

def calculate_accuracy(actual_prices, predicted_prices):
    # Calculate mean absolute percentage error (MAPE) for accuracy
    mape = np.mean(np.abs((actual_prices - predicted_prices) / actual_prices)) * 100
    accuracy = 100 - mape
    return round(accuracy, 2)

if __name__ == '__main__':
    app.run(debug=True)
