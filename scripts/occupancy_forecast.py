import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# OCCUPANCY FORECAST
# ============================================================

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "occupancy"
    / "processed"
    / "occupancy_processed.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "occupancy"
    / "processed"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# STEP 1: LOAD DATA
# ============================================================

print("=" * 60)
print("OCCUPANCY FORECAST")
print("=" * 60)

df = pd.read_csv(INPUT_FILE)

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

print(f"Input records: {len(df)}")


# ============================================================
# STEP 2: PREPARE TIME FEATURES
# ============================================================

df["Hour"] = df["Timestamp"].dt.hour
df["Day_of_Week_Num"] = df["Timestamp"].dt.dayofweek
df["Day_Name"] = df["Timestamp"].dt.day_name()

print("\nTime features prepared.")


# ============================================================
# STEP 3: HOURLY OCCUPANCY
# ============================================================

hourly = (
    df.groupby(
        ["Building_ID", "Day_of_Week_Num", "Hour"],
        as_index=False
    )
    .agg(
        Average_Occupancy=("Occupancy_Count", "mean"),
        Average_Utilization=("Utilization_Percent", "mean"),
        Average_Capacity=("Room_Capacity", "mean")
    )
)

print(f"Hourly patterns created: {len(hourly)}")


# ============================================================
# STEP 4: FORECAST NEXT 24 HOURS
# ============================================================

# Use the latest timestamp in the dataset as the forecast starting point.
latest_timestamp = df["Timestamp"].max()

future_times = pd.date_range(
    start=latest_timestamp + pd.Timedelta(hours=1),
    periods=24,
    freq="h"
)

buildings = sorted(df["Building_ID"].unique())

forecast_records = []


for building in buildings:

    building_data = hourly[
        hourly["Building_ID"] == building
    ].copy()

    for timestamp in future_times:

        hour = timestamp.hour
        day_of_week = timestamp.dayofweek

        # First preference:
        # Same building + same weekday + same hour
        match = building_data[
            (building_data["Day_of_Week_Num"] == day_of_week)
            & (building_data["Hour"] == hour)
        ]

        # If not enough historical data,
        # use same building + same hour.
        if len(match) == 0:

            match = building_data[
                building_data["Hour"] == hour
            ]

        # Final fallback:
        # Use complete building average.
        if len(match) == 0:

            predicted_occupancy = (
                df[df["Building_ID"] == building]["Occupancy_Count"].mean()
            )

            predicted_utilization = (
                df[df["Building_ID"] == building]["Utilization_Percent"].mean()
            )

            predicted_capacity = (
                df[df["Building_ID"] == building]["Room_Capacity"].mean()
            )

        else:

            predicted_occupancy = match["Average_Occupancy"].mean()
            predicted_utilization = match["Average_Utilization"].mean()
            predicted_capacity = match["Average_Capacity"].mean()

        # Calculate forecast utilization
        if predicted_capacity > 0:
            forecast_utilization = (
                predicted_occupancy / predicted_capacity
            ) * 100
        else:
            forecast_utilization = predicted_utilization

        # Forecast status
        if forecast_utilization > 120:
            status = "Critical"
        elif forecast_utilization > 110:
            status = "High"
        elif forecast_utilization > 100:
            status = "Moderate"
        elif forecast_utilization >= 50:
            status = "Normal"
        else:
            status = "Low"

        # Usage category
        if forecast_utilization >= 80:
            usage_category = "High Usage"
        elif forecast_utilization >= 50:
            usage_category = "Medium Usage"
        else:
            usage_category = "Low Usage"

        forecast_records.append(
            {
                "Forecast_Timestamp": timestamp,
                "Building_ID": building,
                "Forecast_Hour": hour,
                "Day_of_Week": timestamp.day_name(),
                "Predicted_Occupancy": round(
                    predicted_occupancy, 2
                ),
                "Forecast_Utilization_Percent": round(
                    forecast_utilization, 2
                ),
                "Forecast_Status": status,
                "Usage_Category": usage_category
            }
        )


forecast_df = pd.DataFrame(forecast_records)


# ============================================================
# STEP 5: OVERALL FACILITY FORECAST
# ============================================================

overall_forecast = (
    forecast_df.groupby(
        [
            "Forecast_Timestamp",
            "Forecast_Hour",
            "Day_of_Week"
        ],
        as_index=False
    )
    .agg(
        Predicted_Occupancy=(
            "Predicted_Occupancy",
            "sum"
        ),
        Average_Utilization=(
            "Forecast_Utilization_Percent",
            "mean"
        )
    )
)

overall_forecast["Forecast_Status"] = np.select(
    [
        overall_forecast["Average_Utilization"] > 120,
        overall_forecast["Average_Utilization"] > 110,
        overall_forecast["Average_Utilization"] > 100,
        overall_forecast["Average_Utilization"] >= 50
    ],
    [
        "Critical",
        "High",
        "Moderate",
        "Normal"
    ],
    default="Low"
)

overall_forecast["Predicted_Occupancy"] = (
    overall_forecast["Predicted_Occupancy"]
    .round(2)
)

overall_forecast["Average_Utilization"] = (
    overall_forecast["Average_Utilization"]
    .round(2)
)


# ============================================================
# STEP 6: PEAK FORECAST
# ============================================================

peak_row = overall_forecast.loc[
    overall_forecast["Predicted_Occupancy"].idxmax()
]

print("\n" + "=" * 60)
print("FORECAST SUMMARY")
print("=" * 60)

print(f"Latest dataset timestamp: {latest_timestamp}")
print(f"Forecast periods: {len(overall_forecast)}")

print(
    f"Peak forecast hour: "
    f"{int(peak_row['Forecast_Hour']):02d}:00"
)

print(
    f"Peak predicted occupancy: "
    f"{peak_row['Predicted_Occupancy']:.2f}"
)

print(
    f"Peak forecast utilization: "
    f"{peak_row['Average_Utilization']:.2f}%"
)


# ============================================================
# STEP 7: BUILDING FORECAST SUMMARY
# ============================================================

building_forecast_summary = (
    forecast_df.groupby(
        "Building_ID",
        as_index=False
    )
    .agg(
        Average_Predicted_Occupancy=(
            "Predicted_Occupancy",
            "mean"
        ),
        Maximum_Predicted_Occupancy=(
            "Predicted_Occupancy",
            "max"
        ),
        Average_Forecast_Utilization=(
            "Forecast_Utilization_Percent",
            "mean"
        ),
        Maximum_Forecast_Utilization=(
            "Forecast_Utilization_Percent",
            "max"
        )
    )
)

building_forecast_summary[
    "Average_Predicted_Occupancy"
] = building_forecast_summary[
    "Average_Predicted_Occupancy"
].round(2)

building_forecast_summary[
    "Maximum_Predicted_Occupancy"
] = building_forecast_summary[
    "Maximum_Predicted_Occupancy"
].round(2)

building_forecast_summary[
    "Average_Forecast_Utilization"
] = building_forecast_summary[
    "Average_Forecast_Utilization"
].round(2)

building_forecast_summary[
    "Maximum_Forecast_Utilization"
] = building_forecast_summary[
    "Maximum_Forecast_Utilization"
].round(2)


# ============================================================
# STEP 8: HIGH USAGE PERIODS
# ============================================================

high_usage_periods = forecast_df[
    forecast_df["Forecast_Utilization_Percent"] >= 80
].copy()

high_usage_periods = high_usage_periods.sort_values(
    "Forecast_Utilization_Percent",
    ascending=False
)


# ============================================================
# STEP 9: SAVE RESULTS
# ============================================================

forecast_file = (
    OUTPUT_DIR
    / "occupancy_forecast_results.csv"
)

overall_file = (
    OUTPUT_DIR
    / "overall_occupancy_forecast.csv"
)

building_file = (
    OUTPUT_DIR
    / "building_occupancy_forecast.csv"
)

high_usage_file = (
    OUTPUT_DIR
    / "high_usage_forecast_periods.csv"
)


forecast_df.to_csv(
    forecast_file,
    index=False
)

overall_forecast.to_csv(
    overall_file,
    index=False
)

building_forecast_summary.to_csv(
    building_file,
    index=False
)

high_usage_periods.to_csv(
    high_usage_file,
    index=False
)


# ============================================================
# STEP 10: DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("BUILDING FORECAST SUMMARY")
print("=" * 60)

print(
    building_forecast_summary.to_string(
        index=False
    )
)

print("\n" + "=" * 60)
print("HIGH USAGE FORECAST PERIODS")
print("=" * 60)

print(
    f"High usage periods: "
    f"{len(high_usage_periods)}"
)

if len(high_usage_periods) > 0:

    print(
        high_usage_periods[
            [
                "Forecast_Timestamp",
                "Building_ID",
                "Predicted_Occupancy",
                "Forecast_Utilization_Percent",
                "Forecast_Status"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 60)
print("OCCUPANCY FORECAST COMPLETED")
print("=" * 60)

print("\nFiles created:")

print(f"1. {forecast_file}")
print(f"2. {overall_file}")
print(f"3. {building_file}")
print(f"4. {high_usage_file}")