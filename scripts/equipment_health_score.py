import pandas as pd
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output paths
INPUT_PATH = (
    BASE_DIR
    / "data"
    / "maintenance"
    / "processed"
    / "maintenance_processed.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "maintenance"
    / "processed"
    / "maintenance_health_scores.csv"
)

print("=" * 60)
print("EQUIPMENT HEALTH SCORE CALCULATION")
print("=" * 60)

# Load processed dataset
df = pd.read_csv(INPUT_PATH)

print(f"\nRecords loaded: {len(df)}")

# ---------------------------------------------------------
# Calculate individual risk components
# ---------------------------------------------------------

# Temperature risk
temperature_risk = (
    (df["Equipment_Temperature_C"] - 50) / 30 * 100
).clip(0, 100)

# Vibration risk
vibration_risk = (
    (df["Vibration_mm_s"] - 2) / 6 * 100
).clip(0, 100)

# Pressure risk
pressure_risk = (
    (6 - df["Pressure_bar"]).abs() / 4 * 100
).clip(0, 100)

# Load risk
load_risk = (
    (df["Load_Percent"] - 70).abs() / 30 * 100
).clip(0, 100)

# Maintenance risk
maintenance_risk = (
    df["Days_Since_Maintenance"] / 180 * 100
).clip(0, 100)

# Age risk
age_risk = (
    df["Age_Years"] / 15 * 100
).clip(0, 100)

# ---------------------------------------------------------
# Overall risk score
# ---------------------------------------------------------

risk_score = (
    temperature_risk * 0.25
    + vibration_risk * 0.25
    + pressure_risk * 0.10
    + load_risk * 0.10
    + maintenance_risk * 0.20
    + age_risk * 0.10
)

# Convert risk into health score
df["Equipment_Health_Score"] = (
    100 - risk_score
).clip(0, 100).round(2)

# ---------------------------------------------------------
# Health status
# ---------------------------------------------------------

def get_health_status(score):

    if score >= 80:
        return "Healthy"

    elif score >= 60:
        return "Normal"

    elif score >= 40:
        return "Warning"

    else:
        return "Critical"


df["Health_Status"] = df["Equipment_Health_Score"].apply(
    get_health_status
)

# ---------------------------------------------------------
# Maintenance recommendation
# ---------------------------------------------------------

def get_recommendation(status):

    if status == "Healthy":
        return "Continue normal monitoring"

    elif status == "Normal":
        return "Schedule routine inspection"

    elif status == "Warning":
        return "Schedule maintenance soon"

    else:
        return "Immediate maintenance required"


df["Maintenance_Recommendation"] = (
    df["Health_Status"].apply(get_recommendation)
)

# Save results
df.to_csv(OUTPUT_PATH, index=False)

# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("\nHealth Score Summary:")
print(
    df["Equipment_Health_Score"].describe()
)

print("\nHealth Status Distribution:")
print(
    df["Health_Status"].value_counts()
)

print("\nSample results:")
print(
    df[
        [
            "Asset_ID",
            "Equipment_Type",
            "Equipment_Health_Score",
            "Health_Status",
            "Maintenance_Recommendation"
        ]
    ].head(10).to_string(index=False)
)

print(f"\nSaved to:")
print(OUTPUT_PATH)

print("\n" + "=" * 60)
print("EQUIPMENT HEALTH SCORING COMPLETED ✓")
print("=" * 60)