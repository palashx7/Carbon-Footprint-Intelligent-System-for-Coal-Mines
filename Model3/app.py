from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np


app = Flask(__name__)

# Load CSV data
df = pd.read_csv('./static/rankings.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    # Select specific columns
    columns = ['CompanyID', 'CompanyName', 'Emission_Intensity', 'Green_Investment_Ratio', 'RenewableEnergyUsage_MWh', 'CoalProduced_Tons']
    
    # Replace NaN with None for JSON compatibility
    df_cleaned = df[columns].replace({np.nan: None})
    
    # Convert to JSON-friendly format
    data = df_cleaned.to_dict(orient='records')
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5002, debug=True)
