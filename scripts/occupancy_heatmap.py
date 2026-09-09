import pandas as pd
import os

print("=" * 60)
print("STEP 7 - OCCUPANCY HEATMAP ANALYSIS")
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
# 2. CONVERT TIMESTAMP
# ------------------------------------------------------------

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"]
)

# Create readable day names
df["Day_Name"] = df["Timestamp"].dt.day_name()


# ------------------------------------------------------------
# 3. DEFINE DAY ORDER
# ------------------------------------------------------------

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]


# ------------------------------------------------------------
# 4. HOURLY OCCUPANCY HEATMAP DATA
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("1. HOURLY OCCUPANCY HEATMAP")
print("-" * 60)

hourly_heatmap = (
    df.groupby("Hour")
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
        )
    )
    .reset_index()
    .sort_values("Hour")
)

print(
    hourly_heatmap.to_string(index=False)
)


# ------------------------------------------------------------
# 5. DAY-WISE OCCUPANCY HEATMAP DATA
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("2. DAY-WISE OCCUPANCY HEATMAP")
print("-" * 60)

daily_heatmap = (
    df.groupby("Day_Name")
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
        )
    )
    .reindex(day_order)
    .reset_index()
)

print(
    daily_heatmap.to_string(index=False)
)


# ------------------------------------------------------------
# 6. DAY AND HOUR HEATMAP
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("3. DAY AND HOUR OCCUPANCY HEATMAP")
print("-" * 60)

day_hour_heatmap = (
    df.groupby(
        [
            "Day_Name",
            "Hour"
        ]
    )
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
    .reset_index()
)

day_hour_heatmap["Day_Name"] = pd.Categorical(
    day_hour_heatmap["Day_Name"],
    categories=day_order,
    ordered=True
)

day_hour_heatmap = (
    day_hour_heatmap
    .sort_values(
        [
            "Day_Name",
            "Hour"
        ]
    )
)

print(
    day_hour_heatmap.to_string(index=False)
)


# ------------------------------------------------------------
# 7. BUILDING AND HOUR HEATMAP
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("4. BUILDING AND HOUR OCCUPANCY HEATMAP")
print("-" * 60)

building_hour_heatmap = (
    df.groupby(
        [
            "Building_ID",
            "Hour"
        ]
    )
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
    .reset_index()
)

print(
    building_hour_heatmap.to_string(index=False)
)


# ------------------------------------------------------------
# 8. BUILDING AND DAY HEATMAP
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("5. BUILDING AND DAY OCCUPANCY HEATMAP")
print("-" * 60)

building_day_heatmap = (
    df.groupby(
        [
            "Building_ID",
            "Day_Name"
        ]
    )
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
    .reset_index()
)

building_day_heatmap["Day_Name"] = pd.Categorical(
    building_day_heatmap["Day_Name"],
    categories=day_order,
    ordered=True
)

building_day_heatmap = (
    building_day_heatmap
    .sort_values(
        [
            "Building_ID",
            "Day_Name"
        ]
    )
)

print(
    building_day_heatmap.to_string(index=False)
)


# ------------------------------------------------------------
# 9. FIND PEAK OCCUPANCY PERIOD
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("6. PEAK OCCUPANCY PERIOD")
print("-" * 60)

peak_period = (
    day_hour_heatmap
    .sort_values(
        "Average_Occupancy",
        ascending=False
    )
    .iloc[0]
)

print(
    "Peak day              :",
    peak_period["Day_Name"]
)

print(
    "Peak hour             :",
    f"{int(peak_period['Hour']):02d}:00"
)

print(
    "Average occupancy     :",
    f"{peak_period['Average_Occupancy']:.2f}"
)

print(
    "Average utilization   :",
    f"{peak_period['Average_Utilization']:.2f}%"
)


# ------------------------------------------------------------
# 10. BUILDING WITH HIGHEST OCCUPANCY
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("7. HIGHEST OCCUPANCY BUILDING")
print("-" * 60)

building_summary = (
    df.groupby("Building_ID")
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
        )
    )
    .reset_index()
)

highest_building = (
    building_summary
    .sort_values(
        "Average_Occupancy",
        ascending=False
    )
    .iloc[0]
)

print(
    "Building              :",
    highest_building["Building_ID"]
)

print(
    "Average occupancy     :",
    f"{highest_building['Average_Occupancy']:.2f}"
)

print(
    "Average utilization   :",
    f"{highest_building['Average_Utilization']:.2f}%"
)

print(
    "Maximum occupancy     :",
    int(highest_building["Maximum_Occupancy"])
)


# ------------------------------------------------------------
# 11. SAVE HOURLY HEATMAP DATA
# ------------------------------------------------------------

output_folder = os.path.join(
    "data",
    "occupancy",
    "processed"
)

os.makedirs(
    output_folder,
    exist_ok=True
)

hourly_file = os.path.join(
    output_folder,
    "occupancy_hourly_heatmap.csv"
)

hourly_heatmap.to_csv(
    hourly_file,
    index=False
)


# ------------------------------------------------------------
# 12. SAVE DAILY HEATMAP DATA
# ------------------------------------------------------------

daily_file = os.path.join(
    output_folder,
    "occupancy_daily_heatmap.csv"
)

daily_heatmap.to_csv(
    daily_file,
    index=False
)


# ------------------------------------------------------------
# 13. SAVE DAY-HOUR HEATMAP DATA
# ------------------------------------------------------------

day_hour_file = os.path.join(
    output_folder,
    "occupancy_day_hour_heatmap.csv"
)

day_hour_heatmap.to_csv(
    day_hour_file,
    index=False
)


# ------------------------------------------------------------
# 14. SAVE BUILDING-HOUR HEATMAP DATA
# ------------------------------------------------------------

building_hour_file = os.path.join(
    output_folder,
    "occupancy_building_hour_heatmap.csv"
)

building_hour_heatmap.to_csv(
    building_hour_file,
    index=False
)


# ------------------------------------------------------------
# 15. SAVE BUILDING-DAY HEATMAP DATA
# ------------------------------------------------------------

building_day_file = os.path.join(
    output_folder,
    "occupancy_building_day_heatmap.csv"
)

building_day_heatmap.to_csv(
    building_day_file,
    index=False
)


# ------------------------------------------------------------
# 16. FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STEP 7 - OCCUPANCY HEATMAP ANALYSIS COMPLETED")
print("=" * 60)

print("\nFiles created:")

print(
    "1.",
    hourly_file
)

print(
    "2.",
    daily_file
)

print(
    "3.",
    day_hour_file
)

print(
    "4.",
    building_hour_file
)

print(
    "5.",
    building_day_file
)

print("\nOccupancy heatmap analysis is ready.")
print("Ready for STEP 8 - Occupancy Forecast.")