import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "cost_optimization"
    / "processed"
    / "cross_agent_cost_analysis.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "cost_optimization"
    / "processed"
    / "facility_intelligence_report.csv"
)


# ============================================================
# LOAD CROSS-AGENT DATA
# ============================================================

print("=" * 70)
print("FACILITY INTELLIGENCE REPORT")
print("=" * 70)

print("\nLoading cross-agent analysis...")

if not INPUT_FILE.exists():
    print("\nERROR: Cross-agent analysis file not found:")
    print(INPUT_FILE)
    raise FileNotFoundError(INPUT_FILE)

df = pd.read_csv(INPUT_FILE)

print(f"Input records : {len(df)}")
print(f"Input columns : {len(df.columns)}")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_value(row, column, default=0):
    """Safely get a value from a row."""
    if column in row.index:
        value = row[column]

        if pd.isna(value):
            return default

        return value

    return default


def calculate_budget_compliance(row):
    """
    Calculate budget compliance percentage.

    Budget compliance is based on:
    Operational Cost / Budget
    """

    operational_cost = get_value(
        row,
        "Total_Operational_Cost",
        0
    )

    budget = get_value(
        row,
        "Total_Budget",
        0
    )

    if budget > 0:
        return (operational_cost / budget) * 100

    return 0


def determine_facility_status(health):
    """Determine facility health status."""

    if health >= 85:
        return "Excellent"
    elif health >= 70:
        return "Good"
    elif health >= 50:
        return "Moderate"
    else:
        return "Needs Attention"


def determine_executive_priority(row):
    """Determine overall executive priority."""

    priority = str(
        get_value(
            row,
            "Cross_Agent_Priority",
            "MEDIUM"
        )
    ).upper()

    if priority == "HIGH":
        return "HIGH"
    elif priority == "MEDIUM":
        return "MEDIUM"

    return "LOW"


# ============================================================
# CREATE FACILITY INTELLIGENCE REPORT
# ============================================================

report = []

for _, row in df.iterrows():

    building_id = get_value(
        row,
        "Building_ID",
        "UNKNOWN"
    )

    # --------------------------------------------------------
    # COST KPIs
    # --------------------------------------------------------

    operational_cost = float(
        get_value(
            row,
            "Total_Operational_Cost",
            0
        )
    )

    cost_reduction = float(
        get_value(
            row,
            "Average_Cost_Reduction",
            0
        )
    )

    roi = float(
        get_value(
            row,
            "Average_ROI",
            0
        )
    )

    savings = float(
        get_value(
            row,
            "Total_Savings_Opportunity",
            0
        )
    )

    # --------------------------------------------------------
    # FACILITY KPIs
    # --------------------------------------------------------

    facility_health = float(
        get_value(
            row,
            "Average_Facility_Health",
            0
        )
    )

    resource_utilization = float(
        get_value(
            row,
            "Average_Resource_Utilization",
            0
        )
    )

    optimizations = int(
        get_value(
            row,
            "Optimization_Records",
            0
        )
    )

    # --------------------------------------------------------
    # BUDGET
    # --------------------------------------------------------

    budget = float(
        get_value(
            row,
            "Total_Budget",
            0
        )
    )

    budget_compliance = calculate_budget_compliance(row)

    # --------------------------------------------------------
    # AGENT INFORMATION
    # --------------------------------------------------------

    energy_impact = str(
        get_value(
            row,
            "Energy_Cost_Impact",
            "NORMAL"
        )
    )

    maintenance_impact = str(
        get_value(
            row,
            "Maintenance_Impact",
            "LOW"
        )
    )

    occupancy_impact = str(
        get_value(
            row,
            "Occupancy_Cost_Impact",
            "LOW"
        )
    )

    security_impact = str(
        get_value(
            row,
            "Security_Cost_Impact",
            "LOW"
        )
    )

    cross_agent_score = float(
        get_value(
            row,
            "Cross_Agent_Impact_Score",
            0
        )
    )

    cross_agent_priority = determine_executive_priority(row)

    # --------------------------------------------------------
    # FACILITY STATUS
    # --------------------------------------------------------

    facility_status = determine_facility_status(
        facility_health
    )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    recommendation = str(
        get_value(
            row,
            "Cross_Agent_Recommendation",
            "Maintain current facility operations"
        )
    )

    # --------------------------------------------------------
    # REPORT RECORD
    # --------------------------------------------------------

    report.append({

        "Building_ID": building_id,

        # Cost KPIs
        "Total_Operational_Cost": round(
            operational_cost,
            2
        ),

        "Total_Budget": round(
            budget,
            2
        ),

        "Budget_Compliance_Percent": round(
            budget_compliance,
            2
        ),

        "Cost_Reduction_Percent": round(
            cost_reduction,
            2
        ),

        "ROI_Generated_Percent": round(
            roi,
            2
        ),

        "Total_Savings_Opportunity": round(
            savings,
            2
        ),

        # Facility KPIs
        "Facility_Health_Score": round(
            facility_health,
            2
        ),

        "Facility_Health_Status": facility_status,

        "Optimization_Count": optimizations,

        "Resource_Utilization_Percent": round(
            resource_utilization,
            2
        ),

        # Agent impacts
        "Energy_Cost_Impact": energy_impact,

        "Maintenance_Impact": maintenance_impact,

        "Occupancy_Cost_Impact": occupancy_impact,

        "Security_Cost_Impact": security_impact,

        # Cross-agent intelligence
        "Cross_Agent_Impact_Score": round(
            cross_agent_score,
            2
        ),

        "Executive_Priority": cross_agent_priority,

        "Executive_Recommendation": recommendation
    })


# ============================================================
# CREATE DATAFRAME
# ============================================================

report_df = pd.DataFrame(report)


# ============================================================
# SAVE REPORT
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

report_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# DISPLAY REPORT
# ============================================================

print("\n" + "=" * 70)
print("FACILITY INTELLIGENCE REPORT GENERATED")
print("=" * 70)

print(f"\nOutput file:")
print(OUTPUT_FILE)

print(f"\nReport records : {len(report_df)}")
print(f"Report columns : {len(report_df.columns)}")


print("\n" + "-" * 70)
print("FACILITY INTELLIGENCE SUMMARY")
print("-" * 70)

for _, row in report_df.iterrows():

    print(f"\nBuilding: {row['Building_ID']}")

    print(
        f"  Operational Cost     : "
        f"{row['Total_Operational_Cost']:,.2f}"
    )

    print(
        f"  Cost Reduction       : "
        f"{row['Cost_Reduction_Percent']:.2f}%"
    )

    print(
        f"  ROI Generated        : "
        f"{row['ROI_Generated_Percent']:.2f}%"
    )

    print(
        f"  Facility Health      : "
        f"{row['Facility_Health_Score']:.2f}/100"
    )

    print(
        f"  Optimizations        : "
        f"{row['Optimization_Count']}"
    )

    print(
        f"  Resource Utilization : "
        f"{row['Resource_Utilization_Percent']:.2f}%"
    )

    print(
        f"  Savings Opportunity  : "
        f"{row['Total_Savings_Opportunity']:,.2f}"
    )

    print(
        f"  Executive Priority   : "
        f"{row['Executive_Priority']}"
    )

    print(
        f"  Recommendation       : "
        f"{row['Executive_Recommendation']}"
    )


print("\n" + "=" * 70)
print("SUCCESS: Facility Intelligence Report completed.")
print("=" * 70)