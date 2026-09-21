import pandas as pd
import json
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

COST_FILE = (
    BASE_DIR
    / "data"
    / "cost_optimization"
    / "processed"
    / "cost_processed.csv"
)

FACILITY_FILE = (
    BASE_DIR
    / "data"
    / "cost_optimization"
    / "processed"
    / "facility_intelligence_report.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "scripts"
    / "cost_dashboard_data.js"
)


# ============================================================
# START
# ============================================================

print("=" * 70)
print("EXECUTIVE DASHBOARD DATA GENERATOR")
print("=" * 70)


# ============================================================
# CHECK FILES
# ============================================================

if not COST_FILE.exists():
    raise FileNotFoundError(
        f"Cost processed file not found:\n{COST_FILE}"
    )

if not FACILITY_FILE.exists():
    raise FileNotFoundError(
        f"Facility intelligence report not found:\n{FACILITY_FILE}"
    )


# ============================================================
# LOAD DATA
# ============================================================

cost_df = pd.read_csv(COST_FILE)
facility_df = pd.read_csv(FACILITY_FILE)

print(f"\nCost records     : {len(cost_df)}")
print(f"Facility records : {len(facility_df)}")


# ============================================================
# BUILDING DATA
# ============================================================

buildings = {}

for building_id in sorted(cost_df["Building_ID"].dropna().unique()):

    building_data = cost_df[
        cost_df["Building_ID"] == building_id
    ].copy()

    facility_row = facility_df[
        facility_df["Building_ID"] == building_id
    ]

    # --------------------------------------------------------
    # COST VALUES
    # --------------------------------------------------------

    operational_cost = building_data[
        "Total_Operational_Cost"
    ].sum()

    budget = building_data[
        "Budget"
    ].sum()

    savings = building_data[
        "Savings_Opportunity"
    ].sum()

    # --------------------------------------------------------
    # KPI VALUES
    # --------------------------------------------------------

    cost_reduction = building_data[
        "Cost_Reduction_Percent"
    ].mean()

    roi = building_data[
        "ROI_Generated_Percent"
    ].mean()

    facility_health = building_data[
        "Facility_Health_Score"
    ].mean()

    resource_utilization = building_data[
        "Resource_Utilization_Percent"
    ].mean()

    optimization_count = building_data[
        "Optimization_Count"
    ].sum()

    # --------------------------------------------------------
    # BUDGET COMPLIANCE
    # --------------------------------------------------------

    if budget > 0:
        budget_compliance = (
            operational_cost / budget
        ) * 100
    else:
        budget_compliance = 0

    # --------------------------------------------------------
    # FACILITY REPORT INFORMATION
    # --------------------------------------------------------

    priority = "MEDIUM"
    recommendation = "Maintain current operations"

    if len(facility_row) > 0:

        priority_value = facility_row.iloc[0].get(
            "Executive_Priority",
            "MEDIUM"
        )

        recommendation_value = facility_row.iloc[0].get(
            "Executive_Recommendation",
            "Maintain current operations"
        )

        if pd.notna(priority_value):
            priority = str(priority_value)

        if pd.notna(recommendation_value):
            recommendation = str(
                recommendation_value
            )

    # --------------------------------------------------------
    # COST COMPONENTS
    # --------------------------------------------------------

    energy_cost = building_data[
        "Energy_Cost"
    ].sum()

    maintenance_cost = building_data[
        "Maintenance_Cost"
    ].sum()

    security_cost = building_data[
        "Security_Cost"
    ].sum()

    administrative_cost = building_data[
        "Administrative_Cost"
    ].sum()

    total_components = (
        energy_cost
        + maintenance_cost
        + security_cost
        + administrative_cost
    )

    if total_components > 0:

        energy_percent = (
            energy_cost / total_components
        ) * 100

        maintenance_percent = (
            maintenance_cost / total_components
        ) * 100

        security_percent = (
            security_cost / total_components
        ) * 100

        administrative_percent = (
            administrative_cost / total_components
        ) * 100

    else:

        energy_percent = 0
        maintenance_percent = 0
        security_percent = 0
        administrative_percent = 0

    # --------------------------------------------------------
    # STORE BUILDING
    # --------------------------------------------------------

    buildings[building_id] = {

        "operationalCost": round(
            operational_cost,
            2
        ),

        "budget": round(
            budget,
            2
        ),

        "budgetCompliance": round(
            budget_compliance,
            2
        ),

        "costReduction": round(
            cost_reduction,
            2
        ),

        "roi": round(
            roi,
            2
        ),

        "facilityHealth": round(
            facility_health,
            2
        ),

        "optimizations": int(
            optimization_count
        ),

        "resourceUtilization": round(
            resource_utilization,
            2
        ),

        "savingsOpportunity": round(
            savings,
            2
        ),

        "priority": priority,

        "recommendation": recommendation,

        "costDistribution": {

            "energy": round(
                energy_percent,
                2
            ),

            "maintenance": round(
                maintenance_percent,
                2
            ),

            "security": round(
                security_percent,
                2
            ),

            "administrative": round(
                administrative_percent,
                2
            )
        }
    }


# ============================================================
# OVERALL FACILITY DATA
# ============================================================

total_operational_cost = cost_df[
    "Total_Operational_Cost"
].sum()

total_budget = cost_df[
    "Budget"
].sum()

total_savings = cost_df[
    "Savings_Opportunity"
].sum()

if total_budget > 0:
    overall_budget_compliance = (
        total_operational_cost
        / total_budget
    ) * 100
else:
    overall_budget_compliance = 0


overall = {

    "operationalCost": round(
        total_operational_cost,
        2
    ),

    "budget": round(
        total_budget,
        2
    ),

    "budgetCompliance": round(
        overall_budget_compliance,
        2
    ),

    "costReduction": round(
        cost_df[
            "Cost_Reduction_Percent"
        ].mean(),
        2
    ),

    "roi": round(
        cost_df[
            "ROI_Generated_Percent"
        ].mean(),
        2
    ),

    "facilityHealth": round(
        cost_df[
            "Facility_Health_Score"
        ].mean(),
        2
    ),

    "optimizations": int(
        cost_df[
            "Optimization_Count"
        ].sum()
    ),

    "resourceUtilization": round(
        cost_df[
            "Resource_Utilization_Percent"
        ].mean(),
        2
    ),

    "savingsOpportunity": round(
        total_savings,
        2
    )
}


# ============================================================
# FINAL DASHBOARD DATA
# ============================================================

dashboard_data = {

    "overall": overall,

    "buildings": buildings
}


# ============================================================
# WRITE JAVASCRIPT DATA FILE
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

json_data = json.dumps(
    dashboard_data,
    indent=4
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "window.COST_DASHBOARD_DATA = "
        + json_data
        + ";"
    )


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 70)
print("DASHBOARD DATA GENERATED")
print("=" * 70)

print(f"\nOutput file:")
print(OUTPUT_FILE)

print("\nOverall Facility KPIs:")

print(
    f"  Cost Reduction       : "
    f"{overall['costReduction']:.2f}%"
)

print(
    f"  ROI Generated        : "
    f"{overall['roi']:.2f}%"
)

print(
    f"  Facility Health      : "
    f"{overall['facilityHealth']:.2f}/100"
)

print(
    f"  Optimizations        : "
    f"{overall['optimizations']:,}"
)

print(
    f"  Operational Cost     : "
    f"{overall['operationalCost']:,.2f}"
)

print(
    f"  Budget Compliance    : "
    f"{overall['budgetCompliance']:.2f}%"
)

print(
    f"  Resource Utilization : "
    f"{overall['resourceUtilization']:.2f}%"
)

print(
    f"  Savings Opportunity  : "
    f"{overall['savingsOpportunity']:,.2f}"
)

print("\nBuildings processed:")

for building in buildings:
    print(f"  {building}")

print("\n" + "=" * 70)
print("SUCCESS: Executive dashboard data is ready.")
print("=" * 70)