# Import necessary libraries and modules
from flask import Flask, request, jsonify, render_template
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import confusion_matrix
import pandas as pd
import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load your AAPL data (assuming it's in a CSV file named 'AAPL.csv')
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

        # Calculate Mean Absolute Error (MAE)
        mae = mean_absolute_error(filtered_data['Close'], predictions)

        # Generate histogram, scatter plot, and confusion matrix
        plt.hist(filtered_data['Close'], bins=10)
        plt.xlabel('Closing Prices')
        plt.ylabel('Frequency')
        plt.title('Closing Prices Histogram')
        plt.savefig('static/closing_prices_histogram.png')
        plt.close()

        plt.scatter(filtered_data['High'], filtered_data['Low'])
        plt.xlabel('High Prices')
        plt.ylabel('Low Prices')
        plt.title('High vs Low Scatter Plot')
        plt.savefig('static/high_vs_low_scatter.png')
        plt.close()

        actual_labels = filtered_data['Close'].apply(lambda x: 1 if x > filtered_data['Close'].mean() else 0)
        predicted_labels = predictions > predictions.mean()
        cm = confusion_matrix(actual_labels, predicted_labels)
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Confusion Matrix')
        plt.colorbar()
        plt.xlabel('Predicted Labels')
        plt.ylabel('True Labels')
        plt.xticks([0, 1], ['Low', 'High'])
        plt.yticks([0, 1], ['Low', 'High'])
        plt.savefig('static/confusion_matrix.png')
        plt.close()

        # Prepare response JSON
        response = {
            'labels': filtered_data['Date'].tolist(),
            'actualPrices': filtered_data['Close'].tolist(),
            'predictedPrices': predictions.tolist(),
            'mae': mae
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
