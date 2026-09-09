import pandas as pd
import os

print("=" * 60)
print("STEP 5 - OVERCROWDING DETECTION")
print("=" * 60)

# ------------------------------------------------------------
# 1. LOAD PROCESSED OCCUPANCY DATA
# ------------------------------------------------------------

input_file = os.path.join(
    "data",
    "occupancy",
    "processed",
    "occupancy_processed.csv"
)

df = pd.read_csv(input_file)

print("\nProcessed occupancy data loaded.")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ------------------------------------------------------------
# 2. DETECT OVERCROWDING
# ------------------------------------------------------------

# Overcrowding occurs when occupancy is greater than room capacity

df["Overcrowding_Percent"] = (
    (df["Occupancy_Count"] - df["Room_Capacity"])
    / df["Room_Capacity"]
) * 100

df["Overcrowding_Percent"] = df["Overcrowding_Percent"].clip(lower=0)


# ------------------------------------------------------------
# 3. ASSIGN OVERCROWDING SEVERITY
# ------------------------------------------------------------

def assign_severity(row):

    utilization = row["Utilization_Percent"]

    if utilization > 120:
        return "Critical"

    elif utilization > 110:
        return "High"

    elif utilization > 100:
        return "Moderate"

    else:
        return "Normal"


df["Overcrowding_Severity"] = df.apply(assign_severity, axis=1)


# ------------------------------------------------------------
# 4. CREATE OVERCROWDING FLAG
# ------------------------------------------------------------

df["Overcrowding_Detected"] = (
    df["Occupancy_Count"] > df["Room_Capacity"]
)


overcrowded_df = df[df["Overcrowding_Detected"]].copy()


# ------------------------------------------------------------
# 5. OVERCROWDING SUMMARY
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("1. OVERCROWDING SUMMARY")
print("-" * 60)

total_records = len(df)
overcrowded_records = len(overcrowded_df)

print("Total occupancy records :", total_records)
print("Overcrowded records     :", overcrowded_records)

if total_records > 0:
    overcrowding_rate = (
        overcrowded_records / total_records
    ) * 100
else:
    overcrowding_rate = 0

print(
    "Overcrowding rate        : "
    f"{overcrowding_rate:.2f}%"
)


# ------------------------------------------------------------
# 6. SEVERITY DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("2. OVERCROWDING SEVERITY")
print("-" * 60)

if not overcrowded_df.empty:

    severity_counts = (
        overcrowded_df["Overcrowding_Severity"]
        .value_counts()
    )

    print(severity_counts)

else:

    print("No overcrowding detected.")


# ------------------------------------------------------------
# 7. BUILDING-WISE OVERCROWDING
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("3. BUILDING-WISE OVERCROWDING")
print("-" * 60)

building_overcrowding = (
    overcrowded_df
    .groupby("Building_ID")
    .agg(
        Overcrowded_Records=("Overcrowding_Detected", "sum"),
        Maximum_Utilization=("Utilization_Percent", "max"),
        Average_Overcrowding_Percent=(
            "Overcrowding_Percent",
            "mean"
        )
    )
    .sort_values(
        "Overcrowded_Records",
        ascending=False
    )
)

print(building_overcrowding)


# ------------------------------------------------------------
# 8. ROOM-WISE OVERCROWDING
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("4. ROOM-WISE OVERCROWDING")
print("-" * 60)

room_overcrowding = (
    overcrowded_df
    .groupby(
        [
            "Building_ID",
            "Room_ID",
            "Room_Type"
        ]
    )
    .agg(
        Room_Capacity=("Room_Capacity", "first"),
        Overcrowded_Records=(
            "Overcrowding_Detected",
            "sum"
        ),
        Maximum_Occupancy=(
            "Occupancy_Count",
            "max"
        ),
        Maximum_Utilization=(
            "Utilization_Percent",
            "max"
        ),
        Average_Overcrowding_Percent=(
            "Overcrowding_Percent",
            "mean"
        )
    )
    .sort_values(
        "Overcrowded_Records",
        ascending=False
    )
)

print(room_overcrowding)


# ------------------------------------------------------------
# 9. MOST SERIOUS OVERCROWDING EVENTS
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("5. MOST SERIOUS OVERCROWDING EVENTS")
print("-" * 60)

if not overcrowded_df.empty:

    serious_events = (
        overcrowded_df[
            [
                "Timestamp",
                "Building_ID",
                "Room_ID",
                "Room_Type",
                "Room_Capacity",
                "Occupancy_Count",
                "Utilization_Percent",
                "Overcrowding_Percent",
                "Overcrowding_Severity"
            ]
        ]
        .sort_values(
            "Utilization_Percent",
            ascending=False
        )
        .head(10)
    )

    print(serious_events.to_string(index=False))

else:

    print("No overcrowding events found.")


# ------------------------------------------------------------
# 10. SAVE OVERCROWDING EVENTS
# ------------------------------------------------------------

output_folder = os.path.join(
    "data",
    "occupancy",
    "processed"
)

os.makedirs(output_folder, exist_ok=True)


events_file = os.path.join(
    output_folder,
    "overcrowding_detection_results.csv"
)

overcrowded_df.to_csv(
    events_file,
    index=False
)


# ------------------------------------------------------------
# 11. SAVE BUILDING REPORT
# ------------------------------------------------------------

building_file = os.path.join(
    output_folder,
    "building_overcrowding_analysis.csv"
)

building_overcrowding.to_csv(
    building_file
)


# ------------------------------------------------------------
# 12. SAVE ROOM REPORT
# ------------------------------------------------------------

room_file = os.path.join(
    output_folder,
    "room_overcrowding_analysis.csv"
)

room_overcrowding.to_csv(
    room_file
)


# ------------------------------------------------------------
# 13. FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STEP 5 - OVERCROWDING DETECTION COMPLETED")
print("=" * 60)

print("\nFiles created:")

print(
    "1.",
    events_file
)

print(
    "2.",
    building_file
)

print(
    "3.",
    room_file
)

print("\nOvercrowding detection is ready.")
print("Ready for STEP 6 - Workspace Allocation.")