import pandas as pd
from pathlib import Path

print("========== DATA PREPROCESSING ==========\n")

# Get the project folder automatically
BASE_DIR = Path(__file__).resolve().parent.parent

# File paths
INPUT_FILE = BASE_DIR / "data" / "energy_dataset.csv.xlsx"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "energy_processed.csv"

# Create processed folder if it does not exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_excel(INPUT_FILE)

# Missing values
print("Missing values:")
print(df.isnull().sum().sum())

# Duplicate records
print("\nDuplicate records:")
print(df.duplicated().sum())

# Convert Timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Create time-based features
df["Hour"] = df["Timestamp"].dt.hour
df["Day"] = df["Timestamp"].dt.day
df["Day_of_Week"] = df["Timestamp"].dt.dayofweek

# Working hours: 9 AM to 6 PM
df["Working_Hours"] = (
    (df["Hour"] >= 9) &
    (df["Hour"] <= 18)
).astype(int)

# Save processed dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nProcessed dataset shape:")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nNew features added:")
print("- Hour")
print("- Day")
print("- Day_of_Week")
print("- Working_Hours")

print("\nProcessed dataset saved to:")
print(OUTPUT_FILE)

print("\n========== PREPROCESSING COMPLETE ==========")