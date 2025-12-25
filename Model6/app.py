from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from datetime import datetime
import pandas as pd
import os
import logging
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)
CORS(app)

# Directory to save reports
REPORTS_DIR = 'reports'
os.makedirs(REPORTS_DIR, exist_ok=True)

# Load the CSV file (replace with your actual file path)
CSV_FILE = 'modified_indian_coal_companies.csv'
df = pd.read_csv(CSV_FILE)

# Mock data for notices, auctions, reports, and messages
notices = [{"date": "15/11/2025", "text": "New emission norms effective November 2025"}]
auctions = [{"name": "Coal Block A", "reserve": 1000000, "status": "Open", "created": "03/03/2025"}]  # Added created date
reports = [{"date": "15/11/2025", "type": "Production Report", "url": "http://example.com/production.pdf"}]
messages = []  # Store all messages here

# In-memory store for compliance status (to persist government approvals/rejections)
compliance_status = {company: "pending" for company in df['CompanyName'].unique()}  # Default all to "pending"

def get_industry_overview():
    total_production = df['CoalProduced_Tons'].sum()
    total_emissions = df['Total_CO2_Emissions_Tons'].sum()
    active_companies = df['CompanyName'].nunique()
    return {
        "total_production": int(total_production),
        "total_emissions": int(total_emissions),
        "active_companies": active_companies
    }

@app.route('/')
def index():
    return render_template('index.html')

# Company Endpoints
@app.route('/api/production/<company>', methods=['GET'])
def get_production(company):
    if company == "BCCL": company = "Bharat Coking Coal"  # Map BCCL to Bharat Coking Coal
    company_data = df[df['CompanyName'] == company]
    if company_data.empty:
        return jsonify({"error": "Company not found"}), 404
    production = {
        "daily": int(company_data['CoalProduced_Tons'].mean() / 365),  # Rough estimate
        "monthly": int(company_data['CoalProduced_Tons'].mean() / 12),
        "yearly": int(company_data['CoalProduced_Tons'].sum())
    }
    return jsonify(production)

@app.route('/api/compliance/<company>', methods=['GET'])
def get_compliance(company):
    if company == "BCCL": company = "Bharat Coking Coal"  # Map BCCL to Bharat Coking Coal
    company_data = df[df['CompanyName'] == company]
    if company_data.empty:
        return jsonify({"error": "Company not found"}), 404
    # Default all to "pending" initially
    compliance = {
        "environmental": "pending",
        "safety": "pending",
        "report": "pending"
    }
    # Override with government decision
    if compliance_status.get(company) == "approved":
        compliance = {key: "approved" for key in compliance}
    elif compliance_status.get(company) == "rejected":
        compliance = {key: "rejected" for key in compliance}
    return jsonify(compliance)

@app.route('/predict', methods=['POST'])
def predict_emission():
    data = request.form
    try:
        coal_production = float(data.get('coal_production', 0))
        coal_type = float(data.get('coal_type', 0))
        energy_consumption = float(data.get('energy_consumption', 0))
        emission_factor = float(data.get('emission_factor', 0))
        prediction = coal_production * emission_factor * (1 + coal_type / 10) * energy_consumption / 1000
        histogram_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="
        return jsonify({"prediction": round(prediction, 2), "histogram_image": histogram_image})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Government Endpoints
@app.route('/api/industry-overview', methods=['GET'])
def industry_overview():
    return jsonify(get_industry_overview())

@app.route('/api/companies', methods=['GET'])
def get_all_companies():
    summary = []
    for company in df['CompanyName'].unique():
        company_data = df[df['CompanyName'] == company]
        current_status = compliance_status.get(company, "pending")  # Default to "pending"
        # Map "Bharat Coking Coal" to "BCCL" for display
        display_name = "BCCL" if company == "Bharat Coking Coal" else company
        summary.append({
            "name": display_name,
            "production": int(company_data['CoalProduced_Tons'].sum()),
            "emissions": int(company_data['Total_CO2_Emissions_Tons'].sum()),
            "compliance_status": current_status
        })
    return jsonify(summary)

@app.route('/api/approve/<company>', methods=['POST'])
def approve_company(company):
    if company == "BCCL": company = "Bharat Coking Coal"  # Map BCCL to Bharat Coking Coal
    if company not in df['CompanyName'].unique():
        return jsonify({"error": "Company not found"}), 404
    compliance_status[company] = "approved"
    return jsonify({"message": f"{company} approved successfully"})

@app.route('/api/reject/<company>', methods=['POST'])
def reject_company(company):
    if company == "BCCL": company = "Bharat Coking Coal"  # Map BCCL to Bharat Coking Coal
    if company not in df['CompanyName'].unique():
        return jsonify({"error": "Company not found"}), 404
    compliance_status[company] = "rejected"
    return jsonify({"message": f"{company} rejected successfully"})

@app.route('/api/send-notice', methods=['POST'])
def send_notice():
    data = request.json
    notice_text = data.get('notice', '')
    if not notice_text:
        return jsonify({"error": "Notice text required"}), 400
    notice = {"date": datetime.now().strftime("%d/%m/%Y"), "text": notice_text}
    notices.append(notice)
    return jsonify({"message": "Notice sent successfully", "notice": notice})

@app.route('/api/notices', methods=['GET'])
def get_notices():
    return jsonify(notices)

@app.route('/api/auctions', methods=['GET'])
def get_auctions():
    return jsonify(auctions)

@app.route('/api/start-auction', methods=['POST'])
def start_auction():
    data = request.json
    name = data.get('name', '')
    reserve = data.get('reserve', 0)
    if not name or reserve <= 0:
        return jsonify({"error": "Valid auction name and reserve price required"}), 400
    auction = {
        "name": name,
        "reserve": reserve,
        "status": "Open",
        "created": datetime.now().strftime("%d/%m/%Y")  # Add creation date
    }
    auctions.append(auction)
    return jsonify({"message": "Auction started successfully", "auction": auction})

@app.route('/api/reports', methods=['GET'])
def get_reports():
    return jsonify(reports)

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    data = request.json
    report_type = data.get('type', '')
    if report_type not in ['production', 'emissions', 'compliance']:
        return jsonify({"error": "Invalid report type"}), 400

    report_date = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{report_type}_report_{report_date}.csv"
    report_path = os.path.join(REPORTS_DIR, filename)

    if report_type == 'production':
        report_df = df.groupby('CompanyName').agg({
            'CoalProduced_Tons': 'sum',
            'Year': 'count'
        }).rename(columns={'CoalProduced_Tons': 'Total_Production_Tons', 'Year': 'Years_Covered'})
        report_df.to_csv(report_path)
    elif report_type == 'emissions':
        report_df = df.groupby('CompanyName').agg({
            'Total_CO2_Emissions_Tons': 'sum',
            'Net_CO2_Emissions_Tons': 'sum',
            'Emission_Intensity': 'mean'
        })
        report_df.to_csv(report_path)
    elif report_type == 'compliance':
        report_df = df.groupby('CompanyName').agg({
            'Score': 'mean',
            'Green_Investment_Ratio': 'mean',
            'RenewableEnergyUsage_MWh': 'sum',
            'Afforestation_Acres': 'sum'
        })
        report_df.to_csv(report_path)

    report = {
        "date": datetime.now().strftime("%d/%m/%Y"),
        "type": report_type.capitalize() + " Report",
        "url": f"http://localhost:5005/{REPORTS_DIR}/{filename}"
    }
    reports.append(report)
    return jsonify({"message": "Report generated successfully", "report": report})

@app.route(f'/{REPORTS_DIR}/<filename>')
def serve_report(filename):
    return send_from_directory(REPORTS_DIR, filename)

# Communication Channel Endpoints
@app.route('/api/messages/<company>', methods=['GET'])
def get_company_messages(company):
    if company == "BCCL": company = "Bharat Coking Coal"  # Map BCCL to Bharat Coking Coal
    if company not in df['CompanyName'].unique():
        return jsonify({"error": "Company not found"}), 404
    company_messages = [msg for msg in messages if msg["company"] == company]
    return jsonify(company_messages)

@app.route('/api/messages/all', methods=['GET'])
def get_all_messages():
    return jsonify(messages)

@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.json
    company = data.get('company', '')
    if company == "BCCL": company = "Bharat Coking Coal"  # Map BCCL to Bharat Coking Coal
    text = data.get('text', '')
    sender = data.get('sender', company)
    if not company or not text or company not in df['CompanyName'].unique():
        return jsonify({"error": "Valid company and message text required"}), 404
    message = {
        "company": company,
        "text": text,
        "sender": sender,
        "date": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    messages.append(message)
    return jsonify({"message": "Message sent successfully", "message": message})

@app.route('/api/company-summary', methods=['GET'])
def get_company_summary():
    summary_list = []
    for company in df['CompanyName'].unique():
        company_data = df[df['CompanyName'] == company]
        total_prod = int(company_data['CoalProduced_Tons'].sum())
        total_emi = int(company_data['Total_CO2_Emissions_Tons'].sum())
        avg_intensity = round(company_data['Emission_Intensity'].mean(), 3) if 'Emission_Intensity' in df.columns else None
        avg_score = round(company_data['Score'].mean(), 2) if 'Score' in df.columns else None
        green_ratio = round(company_data['Green_Investment_Ratio'].mean(), 2) if 'Green_Investment_Ratio' in df.columns else None
        status = compliance_status.get(company, 'pending')
        summary_list.append({
            'company': "BCCL" if company=="Bharat Coking Coal" else company,
            'production': total_prod,
            'emissions': total_emi,
            'intensity': avg_intensity,
            'score': avg_score,
            'green_investment_ratio': green_ratio,
            'status': status
        })
    return jsonify(summary_list)




@app.route('/api/predict-future', methods=['GET'])
def predict_future():
    """
    Simple linear projection of next month's production and emissions
    based on yearly averages and growth trend.
    """
    try:
        # Compute yearly totals for each company
        df['Year'] = pd.to_datetime(df['Year'], errors='coerce')
        yearly = df.groupby(df['Year'].dt.year).agg({
            'CoalProduced_Tons': 'sum',
            'Total_CO2_Emissions_Tons': 'sum'
        }).reset_index()

        # Simple trend prediction (linear extrapolation)
        if len(yearly) > 1:
            yearly = yearly.sort_values('Year')
            prod_growth = yearly['CoalProduced_Tons'].pct_change().mean()
            emi_growth = yearly['Total_CO2_Emissions_Tons'].pct_change().mean()

            next_year = int(yearly['Year'].max() + 1)
            next_prod = yearly['CoalProduced_Tons'].iloc[-1] * (1 + prod_growth)
            next_emi = yearly['Total_CO2_Emissions_Tons'].iloc[-1] * (1 + emi_growth)
        else:
            next_year = datetime.now().year + 1
            next_prod = df['CoalProduced_Tons'].mean()
            next_emi = df['Total_CO2_Emissions_Tons'].mean()

        return jsonify({
            "year": next_year,
            "predicted_production": round(next_prod, 2),
            "predicted_emissions": round(next_emi, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)