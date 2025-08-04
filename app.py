from flask import Flask, request, jsonify
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyRegressor
import os

# Initialize the Flask app
app = Flask(__name__)

# Set up paths for models
base_dir = os.path.abspath(os.path.dirname(__file__))
model_dir = os.path.join(base_dir, '../models')
leak_model_path = os.path.join(model_dir, 'leak_model.pkl')
demand_model_path = os.path.join(model_dir, 'demand_model.pkl')

# Ensure the model directory exists
os.makedirs(model_dir, exist_ok=True)


# Function to create a dummy leak detection model
def create_leak_model():
    # Simulate some training data for binary classification
    X = np.random.rand(10, 3)  # 10 samples, 3 features
    y = np.random.randint(0, 2, 10)  # Random binary labels (0 or 1)
    model = LogisticRegression()
    model.fit(X, y)
    return model


# Function to create a dummy demand prediction model
def create_demand_model():
    # Simulate some training data for regression
    X = np.random.rand(10, 3)  # 10 samples, 3 features
    y = np.random.rand(10)  # Random continuous target values
    model = DummyRegressor(strategy="mean")  # For regression, always predicts the mean
    model.fit(X, y)
    return model


# Load or create the leak model
if not os.path.isfile(leak_model_path):
    print(f"[INFO] Leak model not found at {leak_model_path}. Creating a new dummy model...")
    leak_model = create_leak_model()  # Create the dummy leak detection model
    joblib.dump(leak_model, leak_model_path)  # Save it to the file path
    print(f"[INFO] Leak model saved at {leak_model_path}.")
else:
    leak_model = joblib.load(leak_model_path)  # Load the existing model
    print(f"[INFO] Leak model loaded from {leak_model_path}.")

# Load or create the demand model
if not os.path.isfile(demand_model_path):
    print(f"[INFO] Demand model not found at {demand_model_path}. Creating a new dummy model...")
    demand_model = create_demand_model()  # Create the dummy demand prediction model
    joblib.dump(demand_model, demand_model_path)  # Save it to the file path
    print(f"[INFO] Demand model saved at {demand_model_path}.")
else:
    demand_model = joblib.load(demand_model_path)  # Load the existing model
    print(f"[INFO] Demand model loaded from {demand_model_path}.")


# Flask route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse JSON input
        data = request.get_json()

        # Validate input
        required_keys = ['flow_rate_norm', 'pressure_norm', 'hour']
        if not all(key in data for key in required_keys):
            return jsonify({"error": f"Missing keys in input, required keys: {required_keys}"}), 400

        # Prepare input features
        features = np.array([
            data['flow_rate_norm'],
            data['pressure_norm'],
            data['hour']
        ]).reshape(1, -1)

        # Perform predictions
        leak_prob = leak_model.predict_proba(features)[0][1]  # Leak probability (binary classification)
        demand = demand_model.predict(features)[0]  # Demand forecast (regression)

        # Response payload
        return jsonify({
            "leak_probability": float(leak_prob),
            "forecast_demand": float(demand)
        })

    except Exception as e:
        # Error handling
        return jsonify({
            "error": str(e),
            "message": "An unexpected error occurred while processing the request."
        }), 500


# Entry point of the Flask application
if __name__ == "__main__":
    app.run(debug=True)  # Use debug=False for production environments

