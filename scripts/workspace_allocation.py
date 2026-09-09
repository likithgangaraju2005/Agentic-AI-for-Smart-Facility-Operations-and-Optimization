import pandas as pd
import os

print("=" * 60)
print("STEP 6 - WORKSPACE ALLOCATION")
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
# 2. CALCULATE ROOM UTILIZATION
# ------------------------------------------------------------

room_allocation = (
    df.groupby(
        [
            "Building_ID",
            "Room_ID",
            "Room_Type"
        ]
    )
    .agg(
        Room_Capacity=("Room_Capacity", "first"),
        Average_Occupancy=("Occupancy_Count", "mean"),
        Maximum_Occupancy=("Occupancy_Count", "max"),
        Average_Utilization=("Utilization_Percent", "mean"),
        Maximum_Utilization=("Utilization_Percent", "max"),
        Overcrowded_Records=("Overcrowding_Flag", "sum")
    )
    .reset_index()
)


# ------------------------------------------------------------
# 3. CALCULATE AVAILABLE CAPACITY
# ------------------------------------------------------------

room_allocation["Average_Available_Spaces"] = (
    room_allocation["Room_Capacity"]
    - room_allocation["Average_Occupancy"]
)

room_allocation["Average_Available_Spaces"] = (
    room_allocation["Average_Available_Spaces"]
    .clip(lower=0)
)


# ------------------------------------------------------------
# 4. ASSIGN WORKSPACE STATUS
# ------------------------------------------------------------

def assign_workspace_status(row):

    utilization = row["Average_Utilization"]

    if row["Overcrowded_Records"] > 0:
        return "Overcrowded"

    elif utilization >= 80:
        return "Highly Utilized"

    elif utilization >= 50:
        return "Moderately Utilized"

    elif utilization >= 25:
        return "Available"

    else:
        return "Underutilized"


room_allocation["Workspace_Status"] = (
    room_allocation.apply(
        assign_workspace_status,
        axis=1
    )
)


# ------------------------------------------------------------
# 5. ALLOCATION RECOMMENDATION
# ------------------------------------------------------------

def allocation_recommendation(row):

    status = row["Workspace_Status"]

    if status == "Overcrowded":
        return "Avoid allocation - redirect users to another room"

    elif status == "Highly Utilized":
        return "Limited availability - allocate only if necessary"

    elif status == "Moderately Utilized":
        return "Suitable for workspace allocation"

    elif status == "Available":
        return "Recommended for workspace allocation"

    else:
        return "High availability - preferred for allocation"


room_allocation["Allocation_Recommendation"] = (
    room_allocation.apply(
        allocation_recommendation,
        axis=1
    )
)


# ------------------------------------------------------------
# 6. DISPLAY ROOM ALLOCATION ANALYSIS
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("1. ROOM WORKSPACE ALLOCATION")
print("-" * 60)

display_columns = [
    "Building_ID",
    "Room_ID",
    "Room_Type",
    "Room_Capacity",
    "Average_Occupancy",
    "Average_Available_Spaces",
    "Average_Utilization",
    "Workspace_Status",
    "Allocation_Recommendation"
]

print(
    room_allocation[
        display_columns
    ]
    .sort_values(
        "Average_Available_Spaces",
        ascending=False
    )
    .to_string(index=False)
)


# ------------------------------------------------------------
# 7. BEST ROOMS FOR ALLOCATION
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("2. TOP ROOMS RECOMMENDED FOR ALLOCATION")
print("-" * 60)

recommended_rooms = (
    room_allocation[
        room_allocation["Workspace_Status"].isin(
            [
                "Available",
                "Underutilized",
                "Moderately Utilized"
            ]
        )
    ]
    .sort_values(
        [
            "Average_Available_Spaces",
            "Average_Utilization"
        ],
        ascending=[
            False,
            True
        ]
    )
    .head(10)
)

print(
    recommended_rooms[
        display_columns
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 8. ROOMS WITH LIMITED AVAILABILITY
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("3. ROOMS WITH LIMITED AVAILABILITY")
print("-" * 60)

limited_rooms = (
    room_allocation[
        room_allocation["Workspace_Status"].isin(
            [
                "Highly Utilized",
                "Overcrowded"
            ]
        )
    ]
    .sort_values(
        "Average_Utilization",
        ascending=False
    )
)

if not limited_rooms.empty:

    print(
        limited_rooms[
            display_columns
        ].to_string(index=False)
    )

else:

    print("No rooms with limited availability.")


# ------------------------------------------------------------
# 9. BUILDING-WISE WORKSPACE AVAILABILITY
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("4. BUILDING-WISE WORKSPACE AVAILABILITY")
print("-" * 60)

building_allocation = (
    room_allocation
    .groupby("Building_ID")
    .agg(
        Total_Rooms=("Room_ID", "count"),
        Total_Capacity=("Room_Capacity", "sum"),
        Average_Occupancy=("Average_Occupancy", "sum"),
        Average_Available_Spaces=(
            "Average_Available_Spaces",
            "sum"
        ),
        Average_Utilization=(
            "Average_Utilization",
            "mean"
        ),
        Overcrowded_Rooms=(
            "Overcrowded_Records",
            lambda x: (x > 0).sum()
        )
    )
    .reset_index()
)

print(
    building_allocation.to_string(index=False)
)


# ------------------------------------------------------------
# 10. WORKSPACE STATUS DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("5. WORKSPACE STATUS DISTRIBUTION")
print("-" * 60)

status_distribution = (
    room_allocation["Workspace_Status"]
    .value_counts()
)

print(status_distribution)


# ------------------------------------------------------------
# 11. ROOM TYPE ALLOCATION ANALYSIS
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("6. ROOM TYPE WORKSPACE AVAILABILITY")
print("-" * 60)

room_type_allocation = (
    room_allocation
    .groupby("Room_Type")
    .agg(
        Number_of_Rooms=("Room_ID", "count"),
        Total_Capacity=("Room_Capacity", "sum"),
        Average_Occupancy=("Average_Occupancy", "mean"),
        Average_Available_Spaces=(
            "Average_Available_Spaces",
            "mean"
        ),
        Average_Utilization=(
            "Average_Utilization",
            "mean"
        )
    )
    .sort_values(
        "Average_Available_Spaces",
        ascending=False
    )
)

print(
    room_type_allocation.to_string()
)


# ------------------------------------------------------------
# 12. SAVE ROOM ALLOCATION REPORT
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

room_file = os.path.join(
    output_folder,
    "workspace_allocation_results.csv"
)

room_allocation.to_csv(
    room_file,
    index=False
)


# ------------------------------------------------------------
# 13. SAVE BUILDING ALLOCATION REPORT
# ------------------------------------------------------------

building_file = os.path.join(
    output_folder,
    "building_workspace_allocation.csv"
)

building_allocation.to_csv(
    building_file,
    index=False
)


# ------------------------------------------------------------
# 14. SAVE ROOM TYPE REPORT
# ------------------------------------------------------------

room_type_file = os.path.join(
    output_folder,
    "room_type_workspace_allocation.csv"
)

room_type_allocation.to_csv(
    room_type_file
)


# ------------------------------------------------------------
# 15. FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STEP 6 - WORKSPACE ALLOCATION COMPLETED")
print("=" * 60)

print("\nFiles created:")

print(
    "1.",
    room_file
)

print(
    "2.",
    building_file
)

print(
    "3.",
    room_type_file
)

print("\nWorkspace allocation analysis is ready.")
print("Ready for STEP 7 - Occupancy Heatmap.")