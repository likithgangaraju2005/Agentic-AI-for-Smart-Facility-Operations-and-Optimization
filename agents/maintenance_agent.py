import os
import pandas as pd


print("=" * 60)
print("MAINTENANCE AGENT")
print("=" * 60)


# ---------------------------------------------------------
# 1. Load maintenance prediction results
# ---------------------------------------------------------

input_file = "data/maintenance/processed/maintenance_predictions.csv"

if not os.path.exists(input_file):
    print(f"ERROR: File not found:")
    print(input_file)
    exit()

df = pd.read_csv(input_file)

print(f"\nRecords loaded: {len(df)}")


# ---------------------------------------------------------
# 2. Maintenance Agent decision logic
# ---------------------------------------------------------

def maintenance_decision(row):

    failure_probability = row["Failure_Probability"]
    health_score = row["Equipment_Health_Score"]

    # Highest priority condition
    if failure_probability >= 0.70 or health_score < 30:
        return "Immediate Maintenance"

    # High-risk condition
    elif failure_probability >= 0.40 or health_score < 50:
        return "Schedule Maintenance Soon"

    # Moderate-risk condition
    elif failure_probability >= 0.25 or health_score < 65:
        return "Monitor Equipment"

    # Low-risk condition
    else:
        return "No Immediate Action"


df["Agent_Decision"] = df.apply(
    maintenance_decision,
    axis=1
)


# ---------------------------------------------------------
# 3. Generate maintenance priority
# ---------------------------------------------------------

def maintenance_priority(row):

    failure_probability = row["Failure_Probability"]
    health_score = row["Equipment_Health_Score"]

    if failure_probability >= 0.70 or health_score < 30:
        return "HIGH"

    elif failure_probability >= 0.40 or health_score < 50:
        return "MEDIUM"

    else:
        return "LOW"


df["Maintenance_Priority"] = df.apply(
    maintenance_priority,
    axis=1
)


# ---------------------------------------------------------
# 4. Generate agent recommendation
# ---------------------------------------------------------

def agent_recommendation(row):

    decision = row["Agent_Decision"]

    if decision == "Immediate Maintenance":
        return (
            "Stop or inspect equipment immediately. "
            "Maintenance team should investigate the asset."
        )

    elif decision == "Schedule Maintenance Soon":
        return (
            "Schedule preventive maintenance soon "
            "and inspect equipment condition."
        )

    elif decision == "Monitor Equipment":
        return (
            "Continue monitoring equipment health, "
            "temperature, vibration and operating conditions."
        )

    else:
        return (
            "Equipment condition is acceptable. "
            "Continue normal operation and routine inspection."
        )


df["Agent_Recommendation"] = df.apply(
    agent_recommendation,
    axis=1
)


# ---------------------------------------------------------
# 5. Generate final alert
# ---------------------------------------------------------

def generate_alert(row):

    priority = row["Maintenance_Priority"]

    if priority == "HIGH":
        return "URGENT ALERT"

    elif priority == "MEDIUM":
        return "MAINTENANCE WARNING"

    else:
        return "NORMAL"


df["Agent_Alert"] = df.apply(
    generate_alert,
    axis=1
)


# ---------------------------------------------------------
# 6. Generate maintenance schedule
# ---------------------------------------------------------

def maintenance_schedule(row):

    decision = row["Agent_Decision"]

    if decision == "Immediate Maintenance":
        return "Within 24 hours"

    elif decision == "Schedule Maintenance Soon":
        return "Within 7 days"

    elif decision == "Monitor Equipment":
        return "Within 30 days"

    else:
        return "Next routine maintenance cycle"


df["Recommended_Maintenance_Schedule"] = df.apply(
    maintenance_schedule,
    axis=1
)


# ---------------------------------------------------------
# 7. Display agent results
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("MAINTENANCE AGENT DECISIONS")
print("=" * 60)

print("\nAgent Decisions:")
print(df["Agent_Decision"].value_counts())

print("\nMaintenance Priority:")
print(df["Maintenance_Priority"].value_counts())

print("\nAgent Alerts:")
print(df["Agent_Alert"].value_counts())


# ---------------------------------------------------------
# 8. Display sample recommendations
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("SAMPLE AGENT RECOMMENDATIONS")
print("=" * 60)

columns_to_show = [
    "Asset_ID",
    "Equipment_Type",
    "Equipment_Health_Score",
    "Failure_Risk_Percent",
    "Failure_Risk_Level",
    "Maintenance_Priority",
    "Agent_Decision",
    "Agent_Recommendation",
    "Recommended_Maintenance_Schedule"
]

print(
    df[columns_to_show]
    .head(10)
    .to_string(index=False)
)


# ---------------------------------------------------------
# 9. Save Maintenance Agent results
# ---------------------------------------------------------

output_file = (
    "data/maintenance/processed/maintenance_agent_results.csv"
)

df.to_csv(output_file, index=False)

print("\n" + "=" * 60)
print("MAINTENANCE AGENT RESULTS SAVED")
print("=" * 60)

print(f"\nSaved to:")
print(os.path.abspath(output_file))

print("\n" + "=" * 60)
print("MAINTENANCE AGENT COMPLETED ✓")
print("=" * 60)