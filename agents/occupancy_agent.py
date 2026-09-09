import pandas as pd
from pathlib import Path


# ============================================================
# OCCUPANCY AGENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = (
    BASE_DIR
    / "data"
    / "occupancy"
    / "processed"
)

FORECAST_FILE = (
    PROCESSED_DIR
    / "occupancy_forecast_results.csv"
)

OVERCROWDING_FILE = (
    PROCESSED_DIR
    / "overcrowding_detection_results.csv"
)

WORKSPACE_FILE = (
    PROCESSED_DIR
    / "workspace_allocation_results.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("OCCUPANCY AGENT")
print("=" * 60)

forecast_df = pd.read_csv(FORECAST_FILE)

overcrowding_df = pd.read_csv(OVERCROWDING_FILE)

workspace_df = pd.read_csv(WORKSPACE_FILE)

print("\nOccupancy forecast data loaded.")
print(f"Forecast records: {len(forecast_df)}")

print("\nOvercrowding data loaded.")
print(f"Overcrowding records: {len(overcrowding_df)}")

print("\nWorkspace allocation data loaded.")
print(f"Workspace records: {len(workspace_df)}")


# ============================================================
# OCCUPANCY AGENT DECISION FUNCTION
# ============================================================

def occupancy_decision(
    forecast_utilization,
    overcrowded,
    workspace_status
):
    """
    Generate an operational decision based on
    occupancy, overcrowding and workspace availability.
    """

    # Critical overcrowding
    if overcrowded and forecast_utilization > 120:
        return (
            "Immediate Occupancy Action",
            "HIGH",
            "Immediately redirect occupants and activate alternate workspace."
        )

    # High overcrowding
    elif overcrowded and forecast_utilization > 110:
        return (
            "Overcrowding Alert",
            "HIGH",
            "Redirect occupants to available rooms and monitor the affected area."
        )

    # Moderate overcrowding
    elif overcrowded:
        return (
            "Manage Overcrowding",
            "MEDIUM",
            "Redistribute occupants to available workspace."
        )

    # High predicted utilization
    elif forecast_utilization >= 80:
        return (
            "High Usage Monitoring",
            "MEDIUM",
            "Monitor occupancy and prepare alternate workspace."
        )

    # Good workspace availability
    elif workspace_status == "Underutilized":
        return (
            "Workspace Available",
            "LOW",
            "Prefer this workspace for future allocation."
        )

    # Normal condition
    else:
        return (
            "Normal Occupancy",
            "LOW",
            "Continue normal occupancy monitoring."
        )


# ============================================================
# PREPARE OVERCROWDING DATA
# ============================================================

overcrowding_df["Overcrowded_Detected"] = (
    overcrowding_df["Overcrowding_Detected"]
    .astype(str)
    .str.lower()
    .isin(["true", "1", "yes"])
)

overcrowding_lookup = (
    overcrowding_df
    .groupby("Building_ID")["Overcrowded_Detected"]
    .sum()
    .to_dict()
)


# ============================================================
# PREPARE WORKSPACE DATA
# ============================================================

workspace_lookup = (
    workspace_df
    .set_index("Room_ID")["Workspace_Status"]
    .to_dict()
)


# ============================================================
# GENERATE AGENT DECISIONS
# ============================================================

agent_results = []

for _, row in forecast_df.iterrows():

    building_id = row["Building_ID"]

    forecast_utilization = float(
        row["Forecast_Utilization_Percent"]
    )

    predicted_occupancy = float(
        row["Predicted_Occupancy"]
    )

    # Determine whether building has overcrowding
    overcrowded_count = overcrowding_lookup.get(
        building_id,
        0
    )

    overcrowded = overcrowded_count > 0

    # Find a representative workspace status
    building_workspace = workspace_df[
        workspace_df["Building_ID"] == building_id
    ]

    if len(building_workspace) > 0:

        workspace_status = (
            building_workspace["Workspace_Status"]
            .mode()
            .iloc[0]
        )

    else:
        workspace_status = "Unknown"

    # Generate decision
    decision, priority, recommendation = occupancy_decision(
        forecast_utilization,
        overcrowded,
        workspace_status
    )

    # Alert type
    if priority == "HIGH":
        alert_type = "URGENT ALERT"

    elif priority == "MEDIUM":
        alert_type = "OCCUPANCY WARNING"

    else:
        alert_type = "NORMAL"

    agent_results.append(
        {
            "Forecast_Timestamp": row[
                "Forecast_Timestamp"
            ],
            "Building_ID": building_id,
            "Predicted_Occupancy": round(
                predicted_occupancy,
                2
            ),
            "Forecast_Utilization_Percent": round(
                forecast_utilization,
                2
            ),
            "Overcrowded_Records": int(
                overcrowded_count
            ),
            "Workspace_Status": workspace_status,
            "Agent_Decision": decision,
            "Priority": priority,
            "Alert_Type": alert_type,
            "Agent_Recommendation": recommendation
        }
    )


agent_df = pd.DataFrame(agent_results)


# ============================================================
# BUILDING-LEVEL AGENT SUMMARY
# ============================================================

building_summary = (
    agent_df
    .groupby("Building_ID", as_index=False)
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
        ),
        Overcrowded_Records=(
            "Overcrowded_Records",
            "max"
        )
    )
)


# ============================================================
# OVERALL FACILITY DECISION
# ============================================================

maximum_utilization = agent_df[
    "Forecast_Utilization_Percent"
].max()

total_overcrowded_records = overcrowding_df[
    "Overcrowding_Detected"
].sum()

if total_overcrowded_records > 0 and maximum_utilization > 110:

    overall_decision = "Immediate Occupancy Action"
    overall_priority = "HIGH"
    overall_recommendation = (
        "Overcrowding risk detected. "
        "Redirect occupants and activate alternate workspace."
    )

elif total_overcrowded_records > 0:

    overall_decision = "Overcrowding Monitoring"
    overall_priority = "MEDIUM"
    overall_recommendation = (
        "Monitor affected buildings and redistribute occupants "
        "to available workspace."
    )

elif maximum_utilization >= 80:

    overall_decision = "High Usage Monitoring"
    overall_priority = "MEDIUM"
    overall_recommendation = (
        "Occupancy is expected to increase. "
        "Prepare alternate workspace."
    )

else:

    overall_decision = "Normal Occupancy"
    overall_priority = "LOW"
    overall_recommendation = (
        "Facility occupancy is within manageable levels. "
        "Continue normal monitoring."
    )


# ============================================================
# SAVE RESULTS
# ============================================================

AGENT_OUTPUT = (
    PROCESSED_DIR
    / "occupancy_agent_results.csv"
)

BUILDING_OUTPUT = (
    PROCESSED_DIR
    / "occupancy_agent_building_summary.csv"
)


agent_df.to_csv(
    AGENT_OUTPUT,
    index=False
)

building_summary.to_csv(
    BUILDING_OUTPUT,
    index=False
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("OCCUPANCY AGENT DECISION SUMMARY")
print("=" * 60)

print(
    agent_df[
        [
            "Forecast_Timestamp",
            "Building_ID",
            "Predicted_Occupancy",
            "Forecast_Utilization_Percent",
            "Agent_Decision",
            "Priority",
            "Alert_Type"
        ]
    ]
    .head(15)
    .to_string(index=False)
)


print("\n" + "-" * 60)
print("AGENT DECISION DISTRIBUTION")
print("-" * 60)

print(
    agent_df["Agent_Decision"]
    .value_counts()
)


print("\n" + "-" * 60)
print("PRIORITY DISTRIBUTION")
print("-" * 60)

print(
    agent_df["Priority"]
    .value_counts()
)


print("\n" + "-" * 60)
print("ALERT DISTRIBUTION")
print("-" * 60)

print(
    agent_df["Alert_Type"]
    .value_counts()
)


print("\n" + "-" * 60)
print("BUILDING SUMMARY")
print("-" * 60)

print(
    building_summary.to_string(
        index=False
    )
)


print("\n" + "=" * 60)
print("OVERALL FACILITY DECISION")
print("=" * 60)

print(
    f"Decision       : {overall_decision}"
)

print(
    f"Priority       : {overall_priority}"
)

print(
    f"Maximum usage  : {maximum_utilization:.2f}%"
)

print(
    f"Overcrowded records: "
    f"{int(total_overcrowded_records)}"
)

print(
    f"Recommendation : {overall_recommendation}"
)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 60)
print("STEP 9 - OCCUPANCY AGENT COMPLETED")
print("=" * 60)

print("\nFiles created:")

print(
    f"1. {AGENT_OUTPUT}"
)

print(
    f"2. {BUILDING_OUTPUT}"
)

print("\nOccupancy Agent is ready.")