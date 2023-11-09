# Import necessary libraries and modules
from flask import Flask, request, jsonify, render_template
from sklearn.linear_model import LinearRegression
import pandas as pd
import datetime

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
    try:
        selected_start_date_str = request.args.get('start_date')
        selected_start_date = datetime.datetime.strptime(selected_start_date_str, '%Y-%m-%d').date()

        # Calculate the end date (14 days from the start date)
        end_date = selected_start_date + datetime.timedelta(days=14)

        # Filter data based on start and end dates
        filtered_data = data[(data['Date'] >= selected_start_date_str) & (data['Date'] <= end_date.strftime('%Y-%m-%d'))]

        # Extract input features for prediction
        input_features = filtered_data[['Open', 'High', 'Low', 'Volume']]

        # Predict next 14 days
        predictions = model.predict(input_features)

        # Prepare response JSON
        response = {
            'labels': filtered_data['Date'].tolist(),
            'actualPrices': filtered_data['Close'].tolist(),
            'predictedPrices': predictions.tolist()
        }
        return jsonify(response)
    except Exception as e:
        # Handle any exceptions and return a JSON error response
        error_response = {
            'error': str(e)
        }
        return jsonify(error_response), 500  # HTTP status code 500 for internal server error

if __name__ == '__main__':
    app.run(debug=True)
