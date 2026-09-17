import pandas as pd
import os

print("=" * 60)
print("SECURITY AGENT - DATA VALIDATION")
print("=" * 60)

# Get project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Security dataset path
data_path = os.path.join(
    project_root,
    "data",
    "security",
    "security_agent_dataset.csv"
)

print("\nDataset path:")
print(data_path)

# Check whether dataset exists
if not os.path.exists(data_path):
    print("\nERROR: Security dataset not found.")
    exit()

# Load dataset
df = pd.read_csv(data_path)

print("\n1. DATASET INFORMATION")
print("-" * 60)
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nColumn Names:")
for column in df.columns:
    print("-", column)

# Missing values
print("\n2. MISSING VALUE CHECK")
print("-" * 60)

missing_values = df.isnull().sum()
total_missing = missing_values.sum()

print("Total missing values:", total_missing)

if total_missing == 0:
    print("No missing values found.")
else:
    print("\nColumns with missing values:")
    print(missing_values[missing_values > 0])

# Duplicate records
print("\n3. DUPLICATE RECORD CHECK")
print("-" * 60)

duplicates = df.duplicated().sum()

print("Duplicate records:", duplicates)

if duplicates == 0:
    print("No duplicate records found.")

# Display first records
print("\n4. SAMPLE RECORDS")
print("-" * 60)

print(df.head())

# Dataset statistics
print("\n5. DATASET SUMMARY")
print("-" * 60)

print(df.describe(include="all").transpose())

# Data types
print("\n6. DATA TYPES")
print("-" * 60)

print(df.dtypes)

print("\n" + "=" * 60)
print("VALIDATION COMPLETED")
print("=" * 60)

if total_missing == 0 and duplicates == 0:
    print("STATUS: DATASET IS VALID")
    print("Security dataset is ready for preprocessing.")
else:
    print("STATUS: DATASET NEEDS ATTENTION")

print("=" * 60)