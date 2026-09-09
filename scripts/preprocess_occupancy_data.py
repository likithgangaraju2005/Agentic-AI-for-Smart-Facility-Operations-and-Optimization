import pandas as pd
import os


# ============================================================
# OCCUPANCY DATA PREPROCESSING
# Module 3 - Occupancy Agent
# ============================================================

print("=" * 60)
print("OCCUPANCY DATA PREPROCESSING")
print("=" * 60)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

INPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "occupancy",
    "occupancy_dataset.xlsx"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "occupancy",
    "processed"
)

OUTPUT_PATH = os.path.join(
    OUTPUT_DIR,
    "occupancy_processed.csv"
)


# ============================================================
# 2. CHECK INPUT DATASET
# ============================================================

if not os.path.exists(INPUT_PATH):
    print("\nERROR: Occupancy dataset not found.")
    print(f"Expected location: {INPUT_PATH}")
    exit()


# ============================================================
# 3. CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 4. LOAD DATASET
# ============================================================

df = pd.read_excel(INPUT_PATH)

print("\n1. ORIGINAL DATASET")
print("-" * 60)

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")


# ============================================================
# 5. CONVERT TIMESTAMP
# ============================================================

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)


# ============================================================
# 6. TIME FEATURES
# ============================================================

df["Hour"] = df["Timestamp"].dt.hour

df["Minute"] = df["Timestamp"].dt.minute

df["Day"] = df["Timestamp"].dt.day

df["Month"] = df["Timestamp"].dt.month

df["Day_of_Week_Num"] = df["Timestamp"].dt.dayofweek

df["Is_Weekend"] = (
    df["Day_of_Week_Num"] >= 5
).astype(int)


# ============================================================
# 7. WORKING HOURS
# ============================================================

df["Working_Hours"] = (
    (df["Hour"] >= 8) &
    (df["Hour"] < 18) &
    (df["Day_of_Week_Num"] < 5)
).astype(int)


# ============================================================
# 8. AVAILABLE CAPACITY
# ============================================================

df["Available_Capacity"] = (
    df["Room_Capacity"] -
    df["Occupancy_Count"]
)


# ============================================================
# 9. OCCUPANCY UTILIZATION
# ============================================================

df["Utilization_Percent"] = (
    df["Occupancy_Count"] /
    df["Room_Capacity"]
) * 100

df["Utilization_Percent"] = (
    df["Utilization_Percent"]
    .round(2)
)


# ============================================================
# 10. OCCUPANCY RATIO
# ============================================================

df["Occupancy_Ratio"] = (
    df["Occupancy_Count"] /
    df["Room_Capacity"]
).round(3)


# ============================================================
# 11. OCCUPANCY STATUS
# ============================================================

def classify_occupancy(utilization):

    if utilization > 100:
        return "Overcrowded"

    elif utilization >= 90:
        return "Critical"

    elif utilization >= 75:
        return "High"

    elif utilization >= 50:
        return "Normal"

    else:
        return "Low"


df["Occupancy_Status"] = (
    df["Utilization_Percent"]
    .apply(classify_occupancy)
)


# ============================================================
# 12. OVERCROWDING FLAG
# ============================================================

df["Overcrowding_Flag"] = (
    df["Occupancy_Count"] >
    df["Room_Capacity"]
).astype(int)


# ============================================================
# 13. PEAK HOUR FLAG
# ============================================================

df["Peak_Hour"] = (
    (
        (df["Hour"] >= 9) &
        (df["Hour"] < 12)
    )
    |
    (
        (df["Hour"] >= 14) &
        (df["Hour"] < 17)
    )
).astype(int)


# ============================================================
# 14. OCCUPANCY LOAD CATEGORY
# ============================================================

def load_category(utilization):

    if utilization > 100:
        return "Overloaded"

    elif utilization >= 75:
        return "High Load"

    elif utilization >= 50:
        return "Moderate Load"

    else:
        return "Low Load"


df["Occupancy_Load_Category"] = (
    df["Utilization_Percent"]
    .apply(load_category)
)


# ============================================================
# 15. SORT DATA
# ============================================================

df = df.sort_values(
    by=["Timestamp", "Building_ID", "Room_ID"]
).reset_index(drop=True)


# ============================================================
# 16. SAVE PROCESSED DATA
# ============================================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# 17. DISPLAY RESULTS
# ============================================================

print("\n2. PREPROCESSING COMPLETED")
print("-" * 60)

print(f"Processed rows    : {df.shape[0]}")
print(f"Processed columns : {df.shape[1]}")


# ============================================================
# 18. NEW FEATURES
# ============================================================

print("\n3. NEW FEATURES CREATED")
print("-" * 60)

new_features = [
    "Hour",
    "Minute",
    "Day",
    "Month",
    "Day_of_Week_Num",
    "Is_Weekend",
    "Working_Hours",
    "Available_Capacity",
    "Utilization_Percent",
    "Occupancy_Ratio",
    "Occupancy_Status",
    "Overcrowding_Flag",
    "Peak_Hour",
    "Occupancy_Load_Category"
]

for feature in new_features:
    print(f"- {feature}")


# ============================================================
# 19. OCCUPANCY STATUS DISTRIBUTION
# ============================================================

print("\n4. OCCUPANCY STATUS DISTRIBUTION")
print("-" * 60)

print(
    df["Occupancy_Status"]
    .value_counts()
)


# ============================================================
# 20. OVERCROWDING SUMMARY
# ============================================================

print("\n5. OVERCROWDING SUMMARY")
print("-" * 60)

overcrowded_count = (
    df["Overcrowding_Flag"]
    .sum()
)

print(
    f"Overcrowded records : {overcrowded_count}"
)

print(
    f"Normal/acceptable records : "
    f"{len(df) - overcrowded_count}"
)


# ============================================================
# 21. BUILDING UTILIZATION
# ============================================================

print("\n6. BUILDING UTILIZATION")
print("-" * 60)

building_utilization = (
    df.groupby("Building_ID")[
        "Utilization_Percent"
    ]
    .mean()
    .round(2)
)

print(building_utilization)


# ============================================================
# 22. FINAL SAMPLE
# ============================================================

print("\n7. PROCESSED DATA SAMPLE")
print("-" * 60)

print(
    df[
        [
            "Timestamp",
            "Building_ID",
            "Room_ID",
            "Room_Capacity",
            "Occupancy_Count",
            "Available_Capacity",
            "Utilization_Percent",
            "Occupancy_Status",
            "Overcrowding_Flag"
        ]
    ].head(10).to_string(index=False)
)


# ============================================================
# 23. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("STEP 3 - DATA PREPROCESSING COMPLETED")
print("=" * 60)

print(f"\nProcessed dataset saved to:")
print(OUTPUT_PATH)

print("\nReady for STEP 4 - Occupancy Analysis.")