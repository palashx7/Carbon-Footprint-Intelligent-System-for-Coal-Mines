from flask import Flask, request, jsonify, render_template, send_from_directory
import joblib
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Load the trained model
model = joblib.load('./model/carbon_emission_model1.pkl')

# Directory to store plots
PLOTS_DIR = 'static/plots'
os.makedirs(PLOTS_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')  # Load the HTML form

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the form
    coal_production = float(request.form['coal_production'])
    coal_type = int(request.form['coal_type'])
    energy_consumption = float(request.form['energy_consumption'])
    emission_factor = float(request.form['emission_factor'])
    
    # Create input array for prediction
    input_data = np.array([[coal_production, coal_type, energy_consumption, emission_factor]])
    
    
    # Make prediction
    prediction = model.predict(input_data)[0]
    
    # Generate and save histogram plot
    #generate_histogram([coal_production, energy_consumption, emission_factor])
    
    # Return prediction result and plot path to the frontend
    return jsonify({
        'prediction': prediction,
        #'histogram_image': '/static/plots/histogram.png'
    })

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

def generate_histogram(data):
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=5, color='blue', edgecolor='black')
    plt.title('Histogram of Input Data')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    
    # Save plot
    plot_path = os.path.join(PLOTS_DIR, 'histogram.png')
    plt.savefig(plot_path)
    plt.close()

if __name__ == '__main__':
    app.run(port=5004, debug=True)
