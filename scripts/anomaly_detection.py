import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import IsolationForest

print("========== ENERGY ANOMALY DETECTION ==========\n")

# Get project folder automatically
BASE_DIR = Path(__file__).resolve().parent.parent

# File paths
INPUT_FILE = BASE_DIR / "data" / "processed" / "energy_processed.csv"
MODEL_DIR = BASE_DIR / "models"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "energy_anomaly_results.csv"

# Create folders if needed
MODEL_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Load processed dataset
df = pd.read_csv(INPUT_FILE)

# Features for anomaly detection
features = [
    "Energy_Consumption_kWh",
    "Power_Demand_kW",
    "HVAC_Usage_kWh",
    "Lighting_Usage_kWh",
    "Temperature_C",
    "Humidity_Percent",
    "Occupancy_Count",
    "Hour",
    "Working_Hours"
]

X = df[features]

# Create Isolation Forest model
model = IsolationForest(
    contamination=0.025,
    random_state=42
)

# Train model
model.fit(X)

# Predict anomalies
predictions = model.predict(X)

# Convert predictions
df["Status"] = predictions

df["Status"] = df["Status"].map({
    1: "Normal",
    -1: "Abnormal"
})

# Count results
normal_count = (df["Status"] == "Normal").sum()
abnormal_count = (df["Status"] == "Abnormal").sum()

print("Model Results:")
print("Normal records:", normal_count)
print("Abnormal records:", abnormal_count)

# Show abnormal records
print("\nAbnormal Energy Records:")

abnormal_records = df[df["Status"] == "Abnormal"]

print(
    abnormal_records[
        [
            "Timestamp",
            "Building_ID",
            "Energy_Consumption_kWh",
            "Power_Demand_kW",
            "HVAC_Usage_kWh",
            "Occupancy_Count",
            "Status"
        ]
    ].head(20)
)

# Save model
model_path = MODEL_DIR / "energy_anomaly_model.pkl"
joblib.dump(model, model_path)

# Save anomaly results
df.to_csv(OUTPUT_FILE, index=False)

print("\nModel saved to:")
print(model_path)

print("\nAnomaly results saved to:")
print(OUTPUT_FILE)

print("\n========== ANOMALY DETECTION COMPLETE ==========")