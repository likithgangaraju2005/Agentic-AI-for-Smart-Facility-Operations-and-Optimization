import pandas as pd
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output paths
INPUT_PATH = BASE_DIR / "data" / "maintenance" / "maintenance_dataset.xlsx"
OUTPUT_DIR = BASE_DIR / "data" / "maintenance" / "processed"
OUTPUT_PATH = OUTPUT_DIR / "maintenance_processed.csv"

print("=" * 60)
print("MAINTENANCE DATA PREPROCESSING")
print("=" * 60)

# Create output folder
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_excel(INPUT_PATH)

print(f"\nOriginal dataset:")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# Convert date columns
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df["Last_Maintenance_Date"] = pd.to_datetime(
    df["Last_Maintenance_Date"]
)
# Time-based features
df["Hour"] = df["Timestamp"].dt.hour
df["Day"] = df["Timestamp"].dt.day
df["Day_of_Week"] = df["Timestamp"].dt.dayofweek

# Working hours
df["Working_Hours"] = (
    (df["Hour"] >= 9) &
    (df["Hour"] < 18)
).astype(int)

# Equipment temperature difference
df["Temperature_Difference_C"] = (
    df["Equipment_Temperature_C"] -
    df["Ambient_Temperature_C"]
)

# Equipment stress indicator
df["Equipment_Stress"] = (
    df["Vibration_mm_s"] * 0.4 +
    df["Load_Percent"] * 0.01 +
    df["Days_Since_Maintenance"] * 0.02
)

# Maintenance urgency indicator
df["Maintenance_Urgency"] = (
    df["Days_Since_Maintenance"] > 90
).astype(int)

# High temperature indicator
df["High_Temperature"] = (
    df["Equipment_Temperature_C"] > 70
).astype(int)

# High vibration indicator
df["High_Vibration"] = (
    df["Vibration_mm_s"] > 6
).astype(int)

# Save processed dataset
df.to_csv(OUTPUT_PATH, index=False)

print("\nNew features created:")
print("- Hour")
print("- Day")
print("- Day_of_Week")
print("- Working_Hours")
print("- Temperature_Difference_C")
print("- Equipment_Stress")
print("- Maintenance_Urgency")
print("- High_Temperature")
print("- High_Vibration")

print(f"\nProcessed dataset:")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print(f"\nSaved to:")
print(OUTPUT_PATH)

print("\n" + "=" * 60)
print("PREPROCESSING COMPLETED ✓")
print("=" * 60)