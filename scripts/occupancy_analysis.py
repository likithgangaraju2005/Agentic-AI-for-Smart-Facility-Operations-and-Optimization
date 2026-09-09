import pandas as pd
import os


# ============================================================
# OCCUPANCY ANALYSIS
# Module 3 - Occupancy Agent
# ============================================================

print("=" * 60)
print("OCCUPANCY ANALYSIS")
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
    "processed",
    "occupancy_processed.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "occupancy",
    "processed"
)


# ============================================================
# 2. CHECK DATASET
# ============================================================

if not os.path.exists(INPUT_PATH):
    print("\nERROR: Processed occupancy dataset not found.")
    print(f"Expected location: {INPUT_PATH}")
    exit()


# ============================================================
# 3. LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_PATH)

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"]
)


# ============================================================
# 4. BASIC OCCUPANCY SUMMARY
# ============================================================

print("\n1. OVERALL OCCUPANCY SUMMARY")
print("-" * 60)

total_occupancy = df["Occupancy_Count"].sum()

average_occupancy = (
    df["Occupancy_Count"].mean()
)

maximum_occupancy = (
    df["Occupancy_Count"].max()
)

total_capacity = df["Room_Capacity"].sum()

average_utilization = (
    df["Utilization_Percent"].mean()
)

print(f"Total occupancy records : {len(df)}")
print(f"Total occupancy count   : {total_occupancy}")
print(f"Average occupancy       : {average_occupancy:.2f}")
print(f"Maximum occupancy       : {maximum_occupancy}")
print(f"Average utilization     : {average_utilization:.2f}%")
print(f"Total capacity records  : {total_capacity}")


# ============================================================
# 5. BUILDING ANALYSIS
# ============================================================

print("\n2. BUILDING OCCUPANCY ANALYSIS")
print("-" * 60)

building_analysis = (
    df.groupby("Building_ID")
    .agg(
        Average_Occupancy=(
            "Occupancy_Count",
            "mean"
        ),
        Maximum_Occupancy=(
            "Occupancy_Count",
            "max"
        ),
        Average_Utilization=(
            "Utilization_Percent",
            "mean"
        ),
        Average_Available_Capacity=(
            "Available_Capacity",
            "mean"
        ),
        Overcrowded_Records=(
            "Overcrowding_Flag",
            "sum"
        )
    )
    .round(2)
)

print(building_analysis)


# ============================================================
# 6. ROOM ANALYSIS
# ============================================================

print("\n3. ROOM UTILIZATION ANALYSIS")
print("-" * 60)

room_analysis = (
    df.groupby(
        [
            "Building_ID",
            "Room_ID",
            "Room_Type"
        ]
    )
    .agg(
        Room_Capacity=(
            "Room_Capacity",
            "first"
        ),
        Average_Occupancy=(
            "Occupancy_Count",
            "mean"
        ),
        Maximum_Occupancy=(
            "Occupancy_Count",
            "max"
        ),
        Average_Utilization=(
            "Utilization_Percent",
            "mean"
        ),
        Overcrowded_Records=(
            "Overcrowding_Flag",
            "sum"
        )
    )
    .reset_index()
    .round(2)
)


# ============================================================
# 7. MOST UTILIZED ROOMS
# ============================================================

print("\n4. TOP 10 MOST UTILIZED ROOMS")
print("-" * 60)

top_rooms = (
    room_analysis
    .sort_values(
        "Average_Utilization",
        ascending=False
    )
    .head(10)
)

print(top_rooms.to_string(index=False))


# ============================================================
# 8. LEAST UTILIZED ROOMS
# ============================================================

print("\n5. TOP 10 LEAST UTILIZED ROOMS")
print("-" * 60)

least_rooms = (
    room_analysis
    .sort_values(
        "Average_Utilization",
        ascending=True
    )
    .head(10)
)

print(least_rooms.to_string(index=False))


# ============================================================
# 9. ROOM TYPE ANALYSIS
# ============================================================

print("\n6. ROOM TYPE UTILIZATION")
print("-" * 60)

room_type_analysis = (
    df.groupby("Room_Type")
    .agg(
        Average_Occupancy=(
            "Occupancy_Count",
            "mean"
        ),
        Average_Utilization=(
            "Utilization_Percent",
            "mean"
        ),
        Maximum_Occupancy=(
            "Occupancy_Count",
            "max"
        ),
        Overcrowded_Records=(
            "Overcrowding_Flag",
            "sum"
        )
    )
    .round(2)
)

print(room_type_analysis)


# ============================================================
# 10. HOURLY OCCUPANCY ANALYSIS
# ============================================================

print("\n7. HOURLY OCCUPANCY ANALYSIS")
print("-" * 60)

hourly_analysis = (
    df.groupby("Hour")
    .agg(
        Average_Occupancy=(
            "Occupancy_Count",
            "mean"
        ),
        Average_Utilization=(
            "Utilization_Percent",
            "mean"
        )
    )
    .round(2)
)

print(hourly_analysis)


# ============================================================
# 11. FIND PEAK OCCUPANCY HOUR
# ============================================================

peak_hour = (
    hourly_analysis[
        "Average_Occupancy"
    ]
    .idxmax()
)

peak_occupancy = (
    hourly_analysis.loc[
        peak_hour,
        "Average_Occupancy"
    ]
)

print("\n8. PEAK OCCUPANCY")
print("-" * 60)

print(f"Peak hour              : {peak_hour}:00")
print(
    f"Average occupancy      : "
    f"{peak_occupancy:.2f}"
)


# ============================================================
# 12. WORKING HOURS ANALYSIS
# ============================================================

print("\n9. WORKING HOURS ANALYSIS")
print("-" * 60)

working_analysis = (
    df.groupby("Working_Hours")
    .agg(
        Average_Occupancy=(
            "Occupancy_Count",
            "mean"
        ),
        Average_Utilization=(
            "Utilization_Percent",
            "mean"
        )
    )
    .round(2)
)

print(working_analysis)


# ============================================================
# 13. OVERCROWDING SUMMARY
# ============================================================

print("\n10. OVERCROWDING SUMMARY")
print("-" * 60)

overcrowded_records = (
    df[
        df["Overcrowding_Flag"] == 1
    ]
)

print(
    f"Overcrowded records : "
    f"{len(overcrowded_records)}"
)

if len(overcrowded_records) > 0:

    print("\nOvercrowded rooms:")

    overcrowded_rooms = (
        overcrowded_records[
            [
                "Timestamp",
                "Building_ID",
                "Room_ID",
                "Room_Capacity",
                "Occupancy_Count",
                "Utilization_Percent"
            ]
        ]
        .sort_values(
            "Utilization_Percent",
            ascending=False
        )
    )

    print(
        overcrowded_rooms
        .head(20)
        .to_string(index=False)
    )


# ============================================================
# 14. SAVE BUILDING ANALYSIS
# ============================================================

building_output = os.path.join(
    OUTPUT_DIR,
    "building_occupancy_analysis.csv"
)

building_analysis.to_csv(
    building_output
)


# ============================================================
# 15. SAVE ROOM ANALYSIS
# ============================================================

room_output = os.path.join(
    OUTPUT_DIR,
    "room_utilization_analysis.csv"
)

room_analysis.to_csv(
    room_output,
    index=False
)


# ============================================================
# 16. SAVE HOURLY ANALYSIS
# ============================================================

hourly_output = os.path.join(
    OUTPUT_DIR,
    "hourly_occupancy_analysis.csv"
)

hourly_analysis.to_csv(
    hourly_output
)


# ============================================================
# 17. SAVE ROOM TYPE ANALYSIS
# ============================================================

room_type_output = os.path.join(
    OUTPUT_DIR,
    "room_type_occupancy_analysis.csv"
)

room_type_analysis.to_csv(
    room_type_output
)


# ============================================================
# 18. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("STEP 4 - OCCUPANCY ANALYSIS COMPLETED")
print("=" * 60)

print("\nAnalysis files created:")

print(
    "1. building_occupancy_analysis.csv"
)

print(
    "2. room_utilization_analysis.csv"
)

print(
    "3. hourly_occupancy_analysis.csv"
)

print(
    "4. room_type_occupancy_analysis.csv"
)

print("\nReady for STEP 5 - Overcrowding Detection.")