import pandas as pd
import os


# ============================================================
# OCCUPANCY DATA VALIDATION
# Module 3 - Occupancy Agent
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "occupancy",
    "occupancy_dataset.xlsx"
)


# ============================================================
# 1. CHECK DATASET
# ============================================================

if not os.path.exists(DATA_PATH):
    print("ERROR: Occupancy dataset not found.")
    print(f"Expected location: {DATA_PATH}")
    exit()


# ============================================================
# 2. LOAD DATASET
# ============================================================

df = pd.read_excel(DATA_PATH)


print("=" * 60)
print("OCCUPANCY DATA VALIDATION")
print("=" * 60)


# ============================================================
# 3. DATASET INFORMATION
# ============================================================

print("\n1. DATASET INFORMATION")
print("-" * 60)

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")


# ============================================================
# 4. COLUMN NAMES
# ============================================================

print("\n2. COLUMN NAMES")
print("-" * 60)

for column in df.columns:
    print(f"- {column}")


# ============================================================
# 5. MISSING VALUES
# ============================================================

print("\n3. MISSING VALUES")
print("-" * 60)

missing_values = df.isnull().sum()

if missing_values.sum() == 0:
    print("No missing values found.")
else:
    for column, count in missing_values.items():
        if count > 0:
            print(f"{column}: {count} missing values")


# ============================================================
# 6. DUPLICATE RECORDS
# ============================================================

print("\n4. DUPLICATE RECORDS")
print("-" * 60)

duplicate_count = df.duplicated().sum()

print(f"Duplicate records: {duplicate_count}")


# ============================================================
# 7. BUILDING DISTRIBUTION
# ============================================================

print("\n5. BUILDING DISTRIBUTION")
print("-" * 60)

print(df["Building_ID"].value_counts().sort_index())


# ============================================================
# 8. ROOM TYPE DISTRIBUTION
# ============================================================

print("\n6. ROOM TYPE DISTRIBUTION")
print("-" * 60)

print(df["Room_Type"].value_counts())


# ============================================================
# 9. ROOM CAPACITY VALIDATION
# ============================================================

print("\n7. ROOM CAPACITY VALIDATION")
print("-" * 60)

invalid_capacity = (df["Room_Capacity"] <= 0).sum()

if invalid_capacity == 0:
    print("All room capacities are valid.")
else:
    print(f"Invalid room capacities: {invalid_capacity}")


# ============================================================
# 10. OCCUPANCY VALIDATION
# ============================================================

print("\n8. OCCUPANCY VALIDATION")
print("-" * 60)

negative_occupancy = (df["Occupancy_Count"] < 0).sum()

if negative_occupancy == 0:
    print("No negative occupancy values found.")
else:
    print(f"Negative occupancy records: {negative_occupancy}")


# ============================================================
# 11. CAPACITY CHECK
# ============================================================

print("\n9. CAPACITY CHECK")
print("-" * 60)

over_capacity = (
    df["Occupancy_Count"] > df["Room_Capacity"]
).sum()

print(f"Records exceeding room capacity: {over_capacity}")


# ============================================================
# 12. BUILDING ID VALIDATION
# ============================================================

print("\n10. BUILDING VALIDATION")
print("-" * 60)

expected_buildings = {
    "BLDG_A",
    "BLDG_B",
    "BLDG_C"
}

actual_buildings = set(df["Building_ID"].unique())

print(f"Buildings found: {sorted(actual_buildings)}")

if actual_buildings.issubset(expected_buildings):
    print("Building IDs are valid.")
else:
    print("WARNING: Unexpected Building ID found.")


# ============================================================
# 13. TIMESTAMP VALIDATION
# ============================================================

print("\n11. TIMESTAMP VALIDATION")
print("-" * 60)

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

invalid_timestamp = df["Timestamp"].isnull().sum()

if invalid_timestamp == 0:
    print("All timestamps are valid.")
else:
    print(f"Invalid timestamps: {invalid_timestamp}")


# ============================================================
# 14. REQUIRED COLUMN VALIDATION
# ============================================================

print("\n12. REQUIRED COLUMN VALIDATION")
print("-" * 60)

required_columns = [
    "Timestamp",
    "Building_ID",
    "Floor",
    "Room_ID",
    "Room_Type",
    "Room_Capacity",
    "Occupancy_Count",
    "Temperature_C",
    "Humidity_Percent",
    "Working_Hours",
    "Day_of_Week"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if len(missing_columns) == 0:
    print("All required columns are present.")
else:
    print("Missing columns:")
    for column in missing_columns:
        print(f"- {column}")


# ============================================================
# 15. FINAL VALIDATION SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("VALIDATION SUMMARY")
print("=" * 60)

print(f"Total records              : {len(df)}")
print(f"Total columns              : {len(df.columns)}")
print(f"Missing values             : {df.isnull().sum().sum()}")
print(f"Duplicate records          : {duplicate_count}")
print(f"Invalid capacities         : {invalid_capacity}")
print(f"Negative occupancy records : {negative_occupancy}")
print(f"Over-capacity records      : {over_capacity}")
print(f"Invalid timestamps         : {invalid_timestamp}")

print("\n" + "=" * 60)
print("DATA VALIDATION COMPLETED")
print("=" * 60)