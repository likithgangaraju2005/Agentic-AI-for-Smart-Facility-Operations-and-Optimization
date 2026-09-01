import pandas as pd

# Load processed dataset
file_path = "../data/processed/energy_processed.csv"
df = pd.read_csv(file_path)

print("========== ENERGY DATA ANALYSIS ==========")

# Basic information
print("\n1. Dataset Information")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# Energy statistics
print("\n2. Energy Consumption Statistics")
print("Average:", round(df["Energy_Consumption_kWh"].mean(), 2), "kWh")
print("Minimum:", round(df["Energy_Consumption_kWh"].min(), 2), "kWh")
print("Maximum:", round(df["Energy_Consumption_kWh"].max(), 2), "kWh")

# Power demand
print("\n3. Power Demand Statistics")
print("Average:", round(df["Power_Demand_kW"].mean(), 2), "kW")
print("Maximum:", round(df["Power_Demand_kW"].max(), 2), "kW")

# HVAC
print("\n4. HVAC Usage")
print("Average:", round(df["HVAC_Usage_kWh"].mean(), 2), "kWh")
print("Maximum:", round(df["HVAC_Usage_kWh"].max(), 2), "kWh")

# Lighting
print("\n5. Lighting Usage")
print("Average:", round(df["Lighting_Usage_kWh"].mean(), 2), "kWh")
print("Maximum:", round(df["Lighting_Usage_kWh"].max(), 2), "kWh")

# Water
print("\n6. Water Consumption")
print("Average:", round(df["Water_Consumption_L"].mean(), 2), "L")
print("Maximum:", round(df["Water_Consumption_L"].max(), 2), "L")

# Working vs non-working hours
print("\n7. Working Hours Analysis")

working = df[df["Working_Hours"] == 1]
non_working = df[df["Working_Hours"] == 0]

print(
    "Average energy during working hours:",
    round(working["Energy_Consumption_kWh"].mean(), 2),
    "kWh"
)

print(
    "Average energy during non-working hours:",
    round(non_working["Energy_Consumption_kWh"].mean(), 2),
    "kWh"
)

# Hourly energy consumption
print("\n8. Energy Consumption by Hour")

hourly_energy = (
    df.groupby("Hour")["Energy_Consumption_kWh"]
    .mean()
    .round(2)
)

print(hourly_energy)

# Building comparison
print("\n9. Energy Consumption by Building")

building_energy = (
    df.groupby("Building_ID")["Energy_Consumption_kWh"]
    .mean()
    .round(2)
)

print(building_energy)

print("\n========== ANALYSIS COMPLETE ==========")