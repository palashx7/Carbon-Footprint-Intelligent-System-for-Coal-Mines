from flask import Flask, request, render_template, jsonify
import pandas as pd
import os
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Calculate emissions for each gas
        df['Emissions_CO2'] = df['Activity'] * df['Emission_Factor_CO2']
        df['Emissions_CH4'] = df['Activity'] * df['Emission_Factor_CH4']
        df['Emissions_N2O'] = df['Activity'] * df['Emission_Factor_N2O']
        df['Emissions_HFCs'] = df['Activity'] * df['Emission_Factor_HFCs']
        df['Emissions_PFCs'] = df['Activity'] * df['Emission_Factor_PFCs']
        df['Emissions_SF6'] = df['Activity'] * df['Emission_Factor_SF6']

        # Convert to CO2 equivalents
        df['CO2_eq_CO2'] = df['Emissions_CO2'] * df['GWP_CO2']
        df['CO2_eq_CH4'] = df['Emissions_CH4'] * df['GWP_CH4']
        df['CO2_eq_N2O'] = df['Emissions_N2O'] * df['GWP_N2O']
        df['CO2_eq_HFCs'] = df['Emissions_HFCs'] * df['GWP_HFCs']
        df['CO2_eq_PFCs'] = df['Emissions_PFCs'] * df['GWP_PFCs']
        df['CO2_eq_SF6'] = df['Emissions_SF6'] * df['GWP_SF6']

        # Calculate total CO2 equivalent emissions (carbon offset)
        df['Carbon Offset'] = (df['CO2_eq_CO2'] + df['CO2_eq_CH4'] + df['CO2_eq_N2O'] +
                               df['CO2_eq_HFCs'] + df['CO2_eq_PFCs'] + df['CO2_eq_SF6'])  # Convert to tons

        # Assuming 1 carbon credit equals 1 ton of CO2
        df['Carbon_Credits'] = df['Carbon Offset'] / 1000 

        # Generate the plot
        plt.figure(figsize=(12, 6))

        # Emissions Breakdown
        plt.subplot(1, 2, 1)
        plt.bar(df.index, df[['CO2_eq_CO2', 'CO2_eq_CH4', 'CO2_eq_N2O', 'CO2_eq_HFCs', 'CO2_eq_PFCs', 'CO2_eq_SF6']].sum(axis=1), color='c')
        plt.xlabel('Index')
        plt.ylabel('Carbon Offset Generated (tons)')
        plt.title('Emissions Breakdown by Source')

        # Carbon Credits
        plt.subplot(1, 2, 2)
        plt.bar(df.index, df['Carbon_Credits'], color='g')
        plt.xlabel('Index')
        plt.ylabel('Carbon Credits')
        plt.title('Carbon Credits Earned')

        plt.tight_layout()

        # Save the plot to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        # Encode the plot to display on the frontend
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

        # Convert dataframe to HTML table
        result_table = df.to_html(index=False, classes="table table-bordered")

        return render_template('index.html', table=result_table, plot_url=plot_url)

    return jsonify({'error': 'File upload failed'})

if __name__ == '__main__':
    app.run(port=5003, debug=True)
