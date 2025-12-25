from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import numpy as np

# -------------------------
# Load trained model files
# -------------------------
with open('model/model4.pkl', 'rb') as file:
    model = pickle.load(file)

with open('model/scaler4.pkl', 'rb') as file:
    scaler = pickle.load(file)

with open('model/label_encoder4.pkl', 'rb') as file:
    le = pickle.load(file)

# -------------------------
# Initialize Flask app
# -------------------------
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # -------------------------
        # Get input data from frontend
        # -------------------------
        data = request.get_json()
        emissions = float(data.get('emissions', 0))
        cost = float(data.get('cost', 0))

        if emissions <= 0 or cost <= 0:
            return jsonify({'error': 'Invalid input values. Both emissions and cost must be positive.'}), 400

        # -------------------------
        # Prepare all strategies for prediction
        # -------------------------
        strategies = le.classes_
        input_data = pd.DataFrame({
            'Emissions (tonnes)': [emissions] * len(strategies),
            'Cost (USD)': [cost] * len(strategies),
            'Strategy': le.transform(strategies),
            'Cost_per_Tonne': [cost / emissions] * len(strategies),
            'log_Cost': [np.log1p(cost)] * len(strategies),
            'log_Emission': [np.log1p(emissions)] * len(strategies)
        })

        # -------------------------
        # Scale numerical columns
        # -------------------------
        numeric_cols = ['Emissions (tonnes)', 'Cost (USD)', 'Cost_per_Tonne', 'log_Cost', 'log_Emission']
        input_data[numeric_cols] = scaler.transform(input_data[numeric_cols])

        # -------------------------
        # Model prediction
        # -------------------------
        predicted_effectiveness = model.predict(input_data)

        # -------------------------
        # Select the best strategy
        # -------------------------
        best_index = np.argmax(predicted_effectiveness)
        best_strategy = strategies[best_index]
        best_effectiveness = predicted_effectiveness[best_index]

        # Apply a realistic constraint (effectiveness ≤ emissions)
        best_effectiveness = float(min(best_effectiveness, emissions))

        # -------------------------
        # Return results
        # -------------------------
        return jsonify({
            'best_strategy': best_strategy,
            'best_effectiveness': round(best_effectiveness, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
