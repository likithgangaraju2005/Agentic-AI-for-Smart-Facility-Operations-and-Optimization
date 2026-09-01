import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load processed dataset
data_path = "../data/processed/energy_processed.csv"
df = pd.read_csv(data_path)

# Load trained model
model_path = "../models/energy_anomaly_model.pkl"
model = joblib.load(model_path)

# Features used during training
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

# Model prediction
predictions = model.predict(X)

# Convert predictions
# Isolation Forest: 1 = Normal, -1 = Abnormal
predicted_labels = (predictions == -1).astype(int)

# Create expected labels using the strongest energy-consumption outliers
# Top 2.5% of energy consumption is treated as abnormal
threshold = df["Energy_Consumption_kWh"].quantile(0.975)

actual_labels = (
    df["Energy_Consumption_kWh"] >= threshold
).astype(int)

# Calculate evaluation metrics
accuracy = accuracy_score(actual_labels, predicted_labels)
precision = precision_score(actual_labels, predicted_labels, zero_division=0)
recall = recall_score(actual_labels, predicted_labels, zero_division=0)
f1 = f1_score(actual_labels, predicted_labels, zero_division=0)

print("========== MODEL EVALUATION ==========")

print("\nAbnormal energy threshold:")
print(round(threshold, 2), "kWh")

print("\nEvaluation Results:")
print("Accuracy :", round(accuracy * 100, 2), "%")
print("Precision:", round(precision * 100, 2), "%")
print("Recall   :", round(recall * 100, 2), "%")
print("F1 Score :", round(f1 * 100, 2), "%")

print("\nActual abnormal records:", actual_labels.sum())
print("Predicted abnormal records:", predicted_labels.sum())

print("\n========== EVALUATION COMPLETE ==========")