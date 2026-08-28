import pandas as pd

# Exact location of the dataset
file_path = r"D:\INFOSYS VIRTUAL INTERNSHIP 7.0\Agentic-AI-for-Smart-Facility-Operations-and-Optimization\data\energy_dataset.csv.xlsx"

# Read Excel file
df = pd.read_excel(file_path)

print("========== DATASET VALIDATION ==========")

# 1. Dataset size
print("\n1. Dataset Shape:")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 2. Column names
print("\n2. Column Names:")
for column in df.columns:
    print("-", column)

# 3. Missing values
print("\n3. Missing Values:")
print(df.isnull().sum())

# 4. Duplicate records
print("\n4. Duplicate Records:")
print("Total duplicates:", df.duplicated().sum())

# 5. Data types
print("\n5. Data Types:")
print(df.dtypes)

# 6. Negative values
print("\n6. Negative Values:")
numeric_columns = df.select_dtypes(include="number").columns

for column in numeric_columns:
    print(column, ":", (df[column] < 0).sum())

# 7. Basic statistics
print("\n7. Basic Statistics:")
print(df.describe())

# 8. Energy consumption check
print("\n8. Energy Consumption Check:")

if "Energy_Consumption_kWh" in df.columns:
    print("Minimum Energy:",
          df["Energy_Consumption_kWh"].min(), "kWh")
    print("Maximum Energy:",
          df["Energy_Consumption_kWh"].max(), "kWh")

# 9. Timestamp check
print("\n9. Timestamp Check:")

if "Timestamp" in df.columns:
    timestamp = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    print("Invalid timestamps:", timestamp.isnull().sum())

# 10. Final validation
print("\n10. Validation Summary:")

if (
    df.shape[0] == 1000
    and df.shape[1] == 10
    and df.isnull().sum().sum() == 0
    and df.duplicated().sum() == 0
):
    print("PASS: Dataset passed the basic validation checks.")
else:
    print("CHECK: Dataset needs further review.")

print("\n========== VALIDATION COMPLETE ==========")