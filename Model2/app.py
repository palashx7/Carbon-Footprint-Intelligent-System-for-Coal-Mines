from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('./model/carbonCreditPrice1.pkl')

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from the request
    data = request.get_json()
    offset_method = data.get('offset_method')
    project_location = data.get('project_location')
    verification_status = data.get('verification_status')
    technology_used = data.get('technology_used')
    emission_reduction = data.get('emission_reduction')
    project_size = data.get('project_size')
    
    if not all([offset_method, project_location, verification_status, technology_used, emission_reduction, project_size]):
        return jsonify({'error': 'Missing input data'}), 400

    # Prepare the data for prediction
    input_data = {
        'OffsetMethod': [offset_method],
        'ProjectLocation': [project_location],
        'VerificationStatus': [verification_status],
        'TechnologyUsed': [technology_used],
        'EmissionReduction': [emission_reduction],
        'ProjectSize': [project_size]
    }
    df = pd.DataFrame(input_data)

    # Predict the carbon credit price
    predicted_price = model.predict(df)
    predicted_price = predicted_price[0] * 8.1  # Convert to INR

    return jsonify({'predicted_price': round(predicted_price, 2)})

if __name__ == '__main__':
    app.run(port=5001,debug=True)
