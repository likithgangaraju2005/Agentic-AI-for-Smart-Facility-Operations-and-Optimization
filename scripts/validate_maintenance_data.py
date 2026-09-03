import pandas as pd
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset path
DATA_PATH = BASE_DIR / "data" / "maintenance" / "maintenance_dataset.xlsx"

print("=" * 60)
print("MAINTENANCE DATA VALIDATION")
print("=" * 60)

# Check if dataset exists
if not DATA_PATH.exists():
    print("ERROR: Maintenance dataset not found!")
    print(f"Expected location: {DATA_PATH}")
    exit()

# Load dataset
df = pd.read_excel(DATA_PATH)

print(f"\nDataset loaded successfully.")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# Display column names
print("\nColumns:")
for column in df.columns:
    print(f"- {column}")

# Check missing values
missing_values = df.isnull().sum().sum()

print(f"\nMissing values: {missing_values}")

if missing_values == 0:
    print("✓ No missing values found.")
else:
    print("⚠ Missing values found.")

# Check duplicate records
duplicates = df.duplicated().sum()

print(f"\nDuplicate records: {duplicates}")

if duplicates == 0:
    print("✓ No duplicate records found.")
else:
    print("⚠ Duplicate records found.")

# Check target column
target_column = "Failure_Within_7_Days"

print(f"\nTarget column: {target_column}")

if target_column in df.columns:
    print("✓ Target column found.")

    print("\nTarget distribution:")
    print(df[target_column].value_counts())

else:
    print("✗ Target column not found!")

# Check important maintenance columns
required_columns = [
    "Asset_ID",
    "Building_ID",
    "Equipment_Type",
    "Equipment_Temperature_C",
    "Vibration_mm_s",
    "Pressure_bar",
    "Power_Consumption_kW",
    "Load_Percent",
    "Operating_Hours",
    "Age_Years",
    "Maintenance_Count",
    "Days_Since_Maintenance",
    "Historical_Failure_Count",
    "Failure_Within_7_Days"
]

print("\nRequired column check:")

missing_columns = []

for column in required_columns:
    if column in df.columns:
        print(f"✓ {column}")
    else:
        print(f"✗ {column}")
        missing_columns.append(column)

# Final result
print("\n" + "=" * 60)

if (
    missing_values == 0
    and duplicates == 0
    and len(missing_columns) == 0
):
    print("VALIDATION PASSED ✓")
    print("Maintenance dataset is ready for preprocessing.")
else:
    print("VALIDATION NEEDS ATTENTION ⚠")

print("=" * 60)