import pandas as pd
import numpy as np

# Define columns
columns = [
    "CompanyID", "CompanyName", "Year", "Total_CO2_Emissions_Tons", "CarbonOffsets_Tons",
    "RenewableEnergyUsage_MWh", "Afforestation_Acres", "Investment_Green_Technologies",
    "CoalProduced_Tons", "Net_CO2_Emissions_Tons", "Emission_Intensity",
    "Green_Investment_Ratio", "RenewableEnergy_Intensity", "Emission_Intensity_Difference",
    "Green_Investment_Ratio_Difference", "RenewableEnergy_Intensity_Difference", "Score"
]

# Indian coal mining companies
indian_companies = [
    "Coal India Limited", "Adani Enterprises", "Singareni Collieries", "NLC India Limited",
    "South Eastern Coalfields", "Western Coalfields", "Central Coalfields",
    "Eastern Coalfields", "Mahanadi Coalfields", "Northern Coalfields",
    "Bharat Coking Coal", "Tata Steel Mining", "Hindalco Industries"
]

# Generate data for 500 companies over 10 years (2014–2023)
num_companies = 500
years = list(range(2014, 2024))
data = []

for i in range(num_companies):
    company_id = f"IND{i+1:03d}"
    company_name = indian_companies[i % len(indian_companies)]
    for year in years:
        total_co2 = np.random.randint(100000, 10000000)  # Random total emissions
        carbon_offsets = np.random.randint(0, total_co2 * 0.8)  # Up to 80% offset
        renewable_energy = np.random.randint(1000, 500000)  # MWh
        afforestation = np.random.randint(100, 5000)  # Acres
        green_investment = np.random.randint(1000000, 100000000)  # INR or similar
        coal_produced = np.random.randint(50000, 2000000)  # Tons
        net_co2 = total_co2 - carbon_offsets
        emission_intensity = round(net_co2 / coal_produced, 3) if coal_produced > 0 else 0
        green_investment_ratio = round(green_investment / (coal_produced * 1000), 3)  # Rough ratio
        renewable_intensity = round(renewable_energy / coal_produced, 3)
        emission_diff = np.random.uniform(-1, 1)  # Random difference
        green_investment_diff = np.random.uniform(-0.5, 0.5)
        renewable_diff = np.random.uniform(-0.5, 0.5)
        score = np.random.uniform(0, 250)  # Random score

        row = [
            company_id, company_name, year, total_co2, carbon_offsets, renewable_energy,
            afforestation, green_investment, coal_produced, net_co2, emission_intensity,
            green_investment_ratio, renewable_intensity, emission_diff,
            green_investment_diff, renewable_diff, score
        ]
        data.append(row)

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv('modified_indian_coal_companies.csv', index=False)
print("Generated 'modified_indian_coal_companies.csv' with 5000 rows.")