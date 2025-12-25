🌱 CarbonSathi – Carbon Footprint Quantification & Credit Management Platform

CarbonSathi is a full-stack, multi-model web platform designed to quantify carbon emissions, analyze neutrality pathways, calculate carbon credits, and enable government–industry interaction for Indian coal mining companies.

The system integrates machine learning models, IPCC-based calculations, and interactive dashboards to simulate how coal companies can measure, reduce, offset, and manage carbon emissions in compliance with regulatory frameworks.

🚀 Key Features

📊 Carbon Emission Prediction using operational parameters

🌍 Carbon Neutrality Pathway Recommendation based on emissions and budget

💰 Carbon Credit Price Prediction using project characteristics

♻️ Carbon Offset & Credit Calculator using IPCC GWP factors

🏆 Company Leaderboard based on emission intensity & sustainability metrics

🏛️ BCCL Government Dashboard for compliance, approvals, notices, auctions, and reports

Each model works independently and is also integrated through a unified sidebar dashboard.

🧠 Project Architecture
CarbonFootPrintTool/
│
├── Main-Dashboard/          # Unified sidebar & navigation
│
├── Model1/                  # Carbon Neutrality Predictor
├── Model2/                  # Carbon Credit Price Predictor
├── Model3/                  # Sustainability Leaderboard
├── Model4/                  # Carbon Offset & Credit Calculator
├── Model5/                  # Carbon Emission Predictor
├── Model6/                  # BCCL Government Dashboard
│
├── model/                   # Trained ML pickle files
├── static/                  # CSS, JS, charts
├── templates/               # HTML files
├── datasets/                # CSV datasets
│
├── requirements.txt
└── README.md

🧪 Models Overview
🔹 Model 1 – Carbon Neutrality Predictor

Inputs:

Emissions (tonnes CO₂)

Budget (USD)

Outputs:

Best neutralization strategy

Emissions neutralized (tonnes)

ML Used: Random Forest Regressor

Purpose: Suggests how much carbon can realistically be neutralized within a budget.

🔹 Model 2 – Carbon Credit Price Predictor

Inputs:

Offset Method

Project Location

Verification Status

Technology Used

Emission Reduction

Project Size

Output:

Price per carbon credit (₹ / credit)

ML Used: Regression model trained on synthetic + domain-based data.

🔹 Model 3 – Sustainability Leaderboard

Metrics Used:

Emission Intensity

Renewable Energy Usage

Green Investment Ratio

Output:

Ranked list of companies

Purpose: Encourages competitive sustainability compliance.

🔹 Model 4 – Carbon Offset & Credit Calculator

Input: CSV file containing activity data and emission factors

Standards Used: IPCC Global Warming Potentials (GWP)

Output:

CO₂ equivalent emissions

Carbon offsets

Carbon credits (1 credit = 1 tonne CO₂)

🔹 Model 5 – Carbon Emission Predictor

Inputs:

Coal production

Coal type

Energy consumption

Emission factor

Output:

Predicted CO₂ emissions (tonnes)

Purpose: Quick estimation of emissions from mining activity.

🔹 Model 6 – BCCL Government Dashboard (Core Module)

This is the central regulatory interface.

Features:

Company-wise production & emission data

Compliance approval / rejection (persistent storage)

Government notices

Auctions management

Report generation (production, emissions, compliance)

Two-way communication channel

Data Persistence:

Compliance decisions are saved using JSON-based storage, ensuring data is retained after page reloads or server restarts.

📚 Standards & References Used

IPCC 2006 & 2019 Guidelines – Emission factors & GWP values

Carbon Credit Principle:

1 Carbon Credit = 1 tonne of CO₂ equivalent

Bureau of Energy Efficiency (BEE) – Energy efficiency concepts

UNFCCC & Voluntary Carbon Markets – Offset methodologies

🛠️ Tech Stack
Layer	Technologies
Frontend	HTML, CSS, JavaScript, FontAwesome
Backend	Python, Flask, Flask-CORS
ML	Scikit-learn, Pandas, NumPy
Storage	CSV, JSON
Visualization	Matplotlib
Standards	IPCC Guidelines
▶️ How to Run the Project
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Run models individually
python app.py


Each model runs on its own port (5000–5005).

3️⃣ Open the Main Dashboard

Navigate using the sidebar to access all models.

🎯 Project Objective

This project demonstrates how AI, data analytics, and policy-driven standards can be combined to:

Help coal companies measure and reduce emissions

Support government compliance and regulation

Simulate real-world carbon credit mechanisms

Encourage sustainable industrial practices

👨‍💻 Author

Palash Bhivgade
Final Year – Electronics & Telecommunication Engineering
VIT Pune

⚠️ Disclaimer

This project is an academic and research prototype.
Emission factors, prices, and datasets are representative and may not reflect real-time regulatory values.
