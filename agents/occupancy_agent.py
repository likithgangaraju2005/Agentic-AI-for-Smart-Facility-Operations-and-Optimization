import pandas as pd
import os


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORECAST_FILE = os.path.join(
    BASE_DIR,
    "data",
    "occupancy",
    "processed",
    "occupancy_forecast_results.csv"
)

OVERCROWDING_FILE = os.path.join(
    BASE_DIR,
    "data",
    "occupancy",
    "processed",
    "overcrowding_detection_results.csv"
)

WORKSPACE_FILE = os.path.join(
    BASE_DIR,
    "data",
    "occupancy",
    "processed",
    "workspace_allocation_results.csv"
)

MODEL_PREDICTIONS_FILE = os.path.join(
    BASE_DIR,
    "data",
    "occupancy",
    "processed",
    "occupancy_model_predictions.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "occupancy",
    "processed",
    "occupancy_agent_results.csv"
)

BUILDING_SUMMARY_FILE = os.path.join(
    BASE_DIR,
    "data",
    "occupancy",
    "processed",
    "occupancy_agent_building_summary.csv"
)


# ============================================================
# 2. LOAD DATA
# ============================================================

print("=" * 60)
print("OCCUPANCY AGENT")
print("=" * 60)


print("\nLoading ML model predictions...")

ml_predictions = pd.read_csv(MODEL_PREDICTIONS_FILE)

print("ML prediction records:", len(ml_predictions))


print("\nLoading occupancy forecast data...")

forecast = pd.read_csv(FORECAST_FILE)

forecast["Forecast_Timestamp"] = pd.to_datetime(
    forecast["Forecast_Timestamp"]
)

print("Forecast records:", len(forecast))


print("\nLoading overcrowding data...")

overcrowding = pd.read_csv(OVERCROWDING_FILE)

print("Overcrowding records:", len(overcrowding))


print("\nLoading workspace allocation data...")

workspace = pd.read_csv(WORKSPACE_FILE)

print("Workspace records:", len(workspace))


# ============================================================
# 3. PREPARE ML PREDICTIONS
# ============================================================

print("\nPreparing ML occupancy predictions...")

ml_predictions["Timestamp"] = pd.to_datetime(
    ml_predictions["Timestamp"]
)

ml_predictions["Predicted_Utilization_Percent"] = pd.to_numeric(
    ml_predictions["Predicted_Utilization_Percent"],
    errors="coerce"
)

ml_predictions["Predicted_Occupancy"] = pd.to_numeric(
    ml_predictions["Predicted_Occupancy"],
    errors="coerce"
)


# ============================================================
# 4. BUILD AGENT DECISION FUNCTION
# ============================================================

def occupancy_decision(utilization):

    if utilization > 120:
        return (
            "Immediate Occupancy Action",
            "HIGH",
            "CRITICAL OCCUPANCY ALERT",
            "Immediately redirect occupants to available workspace."
        )

    elif utilization > 100:
        return (
            "Overcrowding Alert",
            "HIGH",
            "OVERCROWDING ALERT",
            "Redistribute occupants to available workspace."
        )

    elif utilization >= 80:
        return (
            "High Usage Monitoring",
            "MEDIUM",
            "HIGH USAGE WARNING",
            "Monitor occupancy and prepare alternate workspace."
        )

    elif utilization >= 40:
        return (
            "Normal Occupancy",
            "LOW",
            "NORMAL",
            "Continue normal occupancy monitoring."
        )

    else:
        return (
            "Low Occupancy",
            "LOW",
            "LOW USAGE",
            "Workspace is available for allocation."
        )


# ============================================================
# 5. APPLY ML-BASED AGENT DECISIONS
# ============================================================

print("\nGenerating ML-based occupancy agent decisions...")

results = ml_predictions.copy()

decisions = results[
    "Predicted_Utilization_Percent"
].apply(occupancy_decision)

results["Agent_Decision"] = decisions.apply(
    lambda x: x[0]
)

results["Priority"] = decisions.apply(
    lambda x: x[1]
)

results["Alert_Type"] = decisions.apply(
    lambda x: x[2]
)

results["Agent_Recommendation"] = decisions.apply(
    lambda x: x[3]
)


# ============================================================
# 6. ADD HISTORICAL OVERCROWDING INFORMATION
# ============================================================

historical_overcrowding = (
    overcrowding
    .groupby("Building_ID")
    .size()
    .reset_index(name="Historical_Overcrowding_Records")
)

results = results.merge(
    historical_overcrowding,
    on="Building_ID",
    how="left"
)

results["Historical_Overcrowding_Records"] = (
    results["Historical_Overcrowding_Records"]
    .fillna(0)
    .astype(int)
)


# ============================================================
# 7. ADD WORKSPACE INFORMATION
# ============================================================

if "Workspace_Status" in workspace.columns:

    workspace_info = workspace[
        ["Building_ID", "Room_ID", "Workspace_Status"]
    ].drop_duplicates()

else:

    workspace_info = workspace[
        ["Building_ID", "Room_ID"]
    ].drop_duplicates()

    workspace_info["Workspace_Status"] = "Available"


# ============================================================
# 8. SAVE AGENT RESULTS
# ============================================================

results.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 9. DECISION DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("OCCUPANCY AGENT DECISION SUMMARY")
print("=" * 60)

display_columns = [
    "Timestamp",
    "Building_ID",
    "Room_ID",
    "Predicted_Occupancy",
    "Predicted_Utilization_Percent",
    "Predicted_Occupancy_Status",
    "Agent_Decision",
    "Priority",
    "Alert_Type",
    "Agent_Recommendation"
]

available_columns = [
    column
    for column in display_columns
    if column in results.columns
]

print(
    results[available_columns].head(20).to_string(
        index=False
    )
)


# ============================================================
# 10. DECISION DISTRIBUTION
# ============================================================

print("\n" + "-" * 60)
print("AGENT DECISION DISTRIBUTION")
print("-" * 60)

print(
    results["Agent_Decision"]
    .value_counts()
)


# ============================================================
# 11. PRIORITY DISTRIBUTION
# ============================================================

print("\n" + "-" * 60)
print("PRIORITY DISTRIBUTION")
print("-" * 60)

print(
    results["Priority"]
    .value_counts()
)


# ============================================================
# 12. ALERT DISTRIBUTION
# ============================================================

print("\n" + "-" * 60)
print("ALERT DISTRIBUTION")
print("-" * 60)

print(
    results["Alert_Type"]
    .value_counts()
)


# ============================================================
# 13. BUILDING SUMMARY
# ============================================================

building_summary = (
    results
    .groupby("Building_ID")
    .agg(
        Average_Predicted_Occupancy=(
            "Predicted_Occupancy",
            "mean"
        ),

        Maximum_Predicted_Occupancy=(
            "Predicted_Occupancy",
            "max"
        ),

        Average_Predicted_Utilization=(
            "Predicted_Utilization_Percent",
            "mean"
        ),

        Maximum_Predicted_Utilization=(
            "Predicted_Utilization_Percent",
            "max"
        ),

        Historical_Overcrowding_Records=(
            "Historical_Overcrowding_Records",
            "max"
        )
    )
    .reset_index()
)


building_summary[
    "Average_Predicted_Occupancy"
] = building_summary[
    "Average_Predicted_Occupancy"
].round(2)


building_summary[
    "Maximum_Predicted_Occupancy"
] = building_summary[
    "Maximum_Predicted_Occupancy"
].round(2)


building_summary[
    "Average_Predicted_Utilization"
] = building_summary[
    "Average_Predicted_Utilization"
].round(2)


building_summary[
    "Maximum_Predicted_Utilization"
] = building_summary[
    "Maximum_Predicted_Utilization"
].round(2)


building_summary.to_csv(
    BUILDING_SUMMARY_FILE,
    index=False
)


# ============================================================
# 14. BUILDING SUMMARY DISPLAY
# ============================================================

print("\n" + "-" * 60)
print("BUILDING SUMMARY")
print("-" * 60)

print(
    building_summary.to_string(
        index=False
    )
)


# ============================================================
# 15. OVERALL FACILITY DECISION
# ============================================================

maximum_usage = results[
    "Predicted_Utilization_Percent"
].max()

high_usage_count = (
    results["Predicted_Utilization_Percent"] >= 80
).sum()

overcrowding_count = (
    results["Predicted_Utilization_Percent"] > 100
).sum()


print("\n" + "=" * 60)
print("OVERALL FACILITY DECISION")
print("=" * 60)


if maximum_usage > 120:

    overall_decision = "Immediate Occupancy Action"
    overall_priority = "HIGH"
    overall_recommendation = (
        "Critical overcrowding predicted. "
        "Immediately redistribute occupants."
    )

elif maximum_usage > 100:

    overall_decision = "Overcrowding Alert"
    overall_priority = "HIGH"
    overall_recommendation = (
        "Overcrowding predicted. "
        "Redistribute occupants to available workspace."
    )

elif maximum_usage >= 80:

    overall_decision = "High Usage Monitoring"
    overall_priority = "MEDIUM"
    overall_recommendation = (
        "High occupancy predicted. "
        "Monitor facility usage and prepare alternate workspace."
    )

else:

    overall_decision = "Normal Occupancy"
    overall_priority = "LOW"
    overall_recommendation = (
        "Occupancy is within acceptable levels. "
        "Continue normal monitoring."
    )


print(f"Decision            : {overall_decision}")
print(f"Priority            : {overall_priority}")
print(f"Maximum usage       : {maximum_usage:.2f}%")
print(f"High usage records  : {high_usage_count}")
print(f"Overcrowded records : {overcrowding_count}")
print(f"Recommendation      : {overall_recommendation}")


# ============================================================
# 16. FINAL OUTPUT
# ============================================================

print("\n" + "=" * 60)
print("STEP 9 - ML-BASED OCCUPANCY AGENT COMPLETED")
print("=" * 60)

print("\nFiles created:")
print("1.", OUTPUT_FILE)
print("2.", BUILDING_SUMMARY_FILE)

print("\nOccupancy Agent is now using ML predictions.")
print("=" * 60)