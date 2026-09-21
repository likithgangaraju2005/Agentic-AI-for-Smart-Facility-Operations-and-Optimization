import pandas as pd
from pathlib import Path


# ============================================================
# COST OPTIMIZATION - COST ANALYSIS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_FOLDER = (
    BASE_DIR
    / "data"
    / "cost_optimization"
    / "processed"
)

INPUT_FILE = PROCESSED_FOLDER / "cost_processed.csv"


def cost_analysis():

    print("=" * 65)
    print("COST OPTIMIZATION - COST ANALYSIS")
    print("=" * 65)

    # --------------------------------------------------------
    # 1. Check input file
    # --------------------------------------------------------

    if not INPUT_FILE.exists():
        print("\nERROR: Processed dataset not found!")
        print(f"Expected file: {INPUT_FILE}")
        return

    # --------------------------------------------------------
    # 2. Load dataset
    # --------------------------------------------------------

    df = pd.read_csv(INPUT_FILE)

    print("\n1. Processed dataset loaded successfully")
    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    # ========================================================
    # 3. BUILDING-WISE COST ANALYSIS
    # ========================================================

    print("\n2. Building-wise Cost Analysis")

    building_analysis = (
        df.groupby("Building_ID")
        .agg(
            Total_Operational_Cost=(
                "Total_Operational_Cost",
                "sum"
            ),
            Average_Operational_Cost=(
                "Total_Operational_Cost",
                "mean"
            ),
            Total_Energy_Cost=(
                "Energy_Cost",
                "sum"
            ),
            Total_Maintenance_Cost=(
                "Maintenance_Cost",
                "sum"
            ),
            Total_Security_Cost=(
                "Security_Cost",
                "sum"
            ),
            Total_Administrative_Cost=(
                "Administrative_Cost",
                "sum"
            ),
            Average_Cost_Reduction=(
                "Cost_Reduction_Percent",
                "mean"
            ),
            Average_ROI=(
                "ROI_Generated_Percent",
                "mean"
            ),
            Average_Facility_Health=(
                "Facility_Health_Score",
                "mean"
            ),
            Average_Resource_Utilization=(
                "Resource_Utilization_Percent",
                "mean"
            ),
            Total_Savings_Opportunity=(
                "Savings_Opportunity",
                "sum"
            ),
            Optimization_Count=(
                "Optimization_Count",
                "sum"
            )
        )
        .reset_index()
    )

    building_analysis = building_analysis.round(2)

    print(building_analysis.to_string(index=False))

    building_output = (
        PROCESSED_FOLDER
        / "building_cost_analysis.csv"
    )

    building_analysis.to_csv(
        building_output,
        index=False
    )

    # ========================================================
    # 4. COST COMPONENT ANALYSIS
    # ========================================================

    print("\n3. Cost Component Analysis")

    cost_components = {
        "Energy Cost": df["Energy_Cost"].sum(),
        "Maintenance Cost": df["Maintenance_Cost"].sum(),
        "Security Cost": df["Security_Cost"].sum(),
        "Administrative Cost": df["Administrative_Cost"].sum()
    }

    total_cost = sum(cost_components.values())

    cost_component_analysis = pd.DataFrame(
        [
            {
                "Cost_Component": name,
                "Total_Cost": value,
                "Cost_Percentage": (
                    value / total_cost * 100
                    if total_cost != 0
                    else 0
                )
            }
            for name, value in cost_components.items()
        ]
    )

    cost_component_analysis[
        "Total_Cost"
    ] = cost_component_analysis[
        "Total_Cost"
    ].round(2)

    cost_component_analysis[
        "Cost_Percentage"
    ] = cost_component_analysis[
        "Cost_Percentage"
    ].round(2)

    print(cost_component_analysis.to_string(index=False))

    cost_component_output = (
        PROCESSED_FOLDER
        / "cost_component_analysis.csv"
    )

    cost_component_analysis.to_csv(
        cost_component_output,
        index=False
    )

    # ========================================================
    # 5. BUDGET ANALYSIS
    # ========================================================

    print("\n4. Budget Analysis")

    budget_analysis = (
        df.groupby("Building_ID")
        .agg(
            Total_Budget=("Budget", "sum"),
            Total_Operational_Cost=(
                "Total_Operational_Cost",
                "sum"
            ),
            Average_Budget_Compliance=(
                "Budget_Compliance_Percent",
                "mean"
            ),
            Records=("Record_ID", "count")
        )
        .reset_index()
    )

    budget_analysis[
        "Budget_Variance"
    ] = (
        budget_analysis["Total_Budget"]
        - budget_analysis["Total_Operational_Cost"]
    )

    budget_analysis[
        "Budget_Usage_Percent"
    ] = (
        budget_analysis["Total_Operational_Cost"]
        / budget_analysis["Total_Budget"]
        * 100
    )

    budget_analysis[
        "Budget_Status"
    ] = budget_analysis.apply(
        lambda row:
        "Within Budget"
        if row["Total_Operational_Cost"]
        <= row["Total_Budget"]
        else "Over Budget",
        axis=1
    )

    budget_analysis = budget_analysis.round(2)

    print(budget_analysis.to_string(index=False))

    budget_output = (
        PROCESSED_FOLDER
        / "budget_analysis.csv"
    )

    budget_analysis.to_csv(
        budget_output,
        index=False
    )

    # ========================================================
    # 6. SAVINGS OPPORTUNITY ANALYSIS
    # ========================================================

    print("\n5. Savings Opportunity Analysis")

    savings_analysis = (
        df.groupby("Building_ID")
        .agg(
            Total_Savings_Opportunity=(
                "Savings_Opportunity",
                "sum"
            ),
            Average_Savings_Opportunity=(
                "Savings_Opportunity",
                "mean"
            ),
            Average_Savings_Percent=(
                "Savings_Opportunity_Percent",
                "mean"
            ),
            Average_Cost_Reduction=(
                "Cost_Reduction_Percent",
                "mean"
            ),
            Maximum_Cost_Reduction=(
                "Cost_Reduction_Percent",
                "max"
            )
        )
        .reset_index()
    )

    savings_analysis = savings_analysis.round(2)

    print(savings_analysis.to_string(index=False))

    savings_output = (
        PROCESSED_FOLDER
        / "savings_analysis.csv"
    )

    savings_analysis.to_csv(
        savings_output,
        index=False
    )

    # ========================================================
    # 7. ROI ANALYSIS
    # ========================================================

    print("\n6. ROI Analysis")

    roi_analysis = (
        df.groupby("Building_ID")
        .agg(
            Total_Investment=(
                "Investment_Amount",
                "sum"
            ),
            Average_Investment=(
                "Investment_Amount",
                "mean"
            ),
            Average_ROI=(
                "ROI_Generated_Percent",
                "mean"
            ),
            Maximum_ROI=(
                "ROI_Generated_Percent",
                "max"
            ),
            Minimum_ROI=(
                "ROI_Generated_Percent",
                "min"
            )
        )
        .reset_index()
    )

    roi_analysis["ROI_Category"] = pd.cut(
        roi_analysis["Average_ROI"],
        bins=[
            -float("inf"),
            15,
            30,
            50,
            float("inf")
        ],
        labels=[
            "Low",
            "Moderate",
            "High",
            "Very High"
        ]
    )

    roi_analysis = roi_analysis.round(2)

    print(roi_analysis.to_string(index=False))

    roi_output = (
        PROCESSED_FOLDER
        / "roi_analysis.csv"
    )

    roi_analysis.to_csv(
        roi_output,
        index=False
    )

    # ========================================================
    # 8. FACILITY HEALTH ANALYSIS
    # ========================================================

    print("\n7. Facility Health Analysis")

    health_analysis = (
        df.groupby("Building_ID")
        .agg(
            Average_Facility_Health=(
                "Facility_Health_Score",
                "mean"
            ),
            Minimum_Facility_Health=(
                "Facility_Health_Score",
                "min"
            ),
            Maximum_Facility_Health=(
                "Facility_Health_Score",
                "max"
            )
        )
        .reset_index()
    )

    def health_category(score):

        if score < 60:
            return "Poor"

        elif score < 75:
            return "Fair"

        elif score < 90:
            return "Good"

        else:
            return "Excellent"

    health_analysis[
        "Health_Category"
    ] = health_analysis[
        "Average_Facility_Health"
    ].apply(health_category)

    health_analysis = health_analysis.round(2)

    print(health_analysis.to_string(index=False))

    health_output = (
        PROCESSED_FOLDER
        / "facility_health_analysis.csv"
    )

    health_analysis.to_csv(
        health_output,
        index=False
    )

    # ========================================================
    # 9. RESOURCE UTILIZATION ANALYSIS
    # ========================================================

    print("\n8. Resource Utilization Analysis")

    resource_analysis = (
        df.groupby("Building_ID")
        .agg(
            Average_Resource_Utilization=(
                "Resource_Utilization_Percent",
                "mean"
            ),
            Minimum_Resource_Utilization=(
                "Resource_Utilization_Percent",
                "min"
            ),
            Maximum_Resource_Utilization=(
                "Resource_Utilization_Percent",
                "max"
            ),
            Average_Vendor_Utilization=(
                "Vendor_Utilization_Percent",
                "mean"
            )
        )
        .reset_index()
    )

    resource_analysis = resource_analysis.round(2)

    print(resource_analysis.to_string(index=False))

    resource_output = (
        PROCESSED_FOLDER
        / "resource_utilization_analysis.csv"
    )

    resource_analysis.to_csv(
        resource_output,
        index=False
    )

    # ========================================================
    # 10. OPTIMIZATION ANALYSIS
    # ========================================================

    print("\n9. Optimization Analysis")

    optimization_analysis = (
        df.groupby("Building_ID")
        .agg(
            Total_Optimizations=(
                "Optimization_Count",
                "sum"
            ),
            Average_Optimizations=(
                "Optimization_Count",
                "mean"
            ),
            Total_Savings_Opportunity=(
                "Savings_Opportunity",
                "sum"
            ),
            Average_Cost_Reduction=(
                "Cost_Reduction_Percent",
                "mean"
            )
        )
        .reset_index()
    )

    def optimization_category(value):

        if value < 3:
            return "Low"

        elif value < 7:
            return "Moderate"

        elif value < 12:
            return "High"

        else:
            return "Very High"

    optimization_analysis[
        "Optimization_Category"
    ] = optimization_analysis[
        "Average_Optimizations"
    ].apply(optimization_category)

    optimization_analysis = optimization_analysis.round(2)

    print(
        optimization_analysis.to_string(
            index=False
        )
    )

    optimization_output = (
        PROCESSED_FOLDER
        / "optimization_analysis.csv"
    )

    optimization_analysis.to_csv(
        optimization_output,
        index=False
    )

    # ========================================================
    # 11. OVERALL COST SUMMARY
    # ========================================================

    print("\n10. Overall Cost Summary")

    total_operational_cost = (
        df["Total_Operational_Cost"].sum()
    )

    total_budget = df["Budget"].sum()

    total_savings = (
        df["Savings_Opportunity"].sum()
    )

    total_investment = (
        df["Investment_Amount"].sum()
    )

    average_cost_reduction = (
        df["Cost_Reduction_Percent"].mean()
    )

    average_roi = (
        df["ROI_Generated_Percent"].mean()
    )

    average_health = (
        df["Facility_Health_Score"].mean()
    )

    average_resource_usage = (
        df["Resource_Utilization_Percent"].mean()
    )

    overall_summary = pd.DataFrame(
        [
            {
                "Metric": "Total Operational Cost",
                "Value": round(
                    total_operational_cost,
                    2
                )
            },
            {
                "Metric": "Total Budget",
                "Value": round(
                    total_budget,
                    2
                )
            },
            {
                "Metric": "Total Savings Opportunity",
                "Value": round(
                    total_savings,
                    2
                )
            },
            {
                "Metric": "Total Investment",
                "Value": round(
                    total_investment,
                    2
                )
            },
            {
                "Metric": "Average Cost Reduction",
                "Value": round(
                    average_cost_reduction,
                    2
                )
            },
            {
                "Metric": "Average ROI",
                "Value": round(
                    average_roi,
                    2
                )
            },
            {
                "Metric": "Average Facility Health",
                "Value": round(
                    average_health,
                    2
                )
            },
            {
                "Metric": "Average Resource Utilization",
                "Value": round(
                    average_resource_usage,
                    2
                )
            }
        ]
    )

    print(
        overall_summary.to_string(
            index=False
        )
    )

    summary_output = (
        PROCESSED_FOLDER
        / "cost_analysis_summary.csv"
    )

    overall_summary.to_csv(
        summary_output,
        index=False
    )

    # ========================================================
    # 12. FINAL MESSAGE
    # ========================================================

    print("\n" + "=" * 65)
    print("COST ANALYSIS COMPLETED SUCCESSFULLY")
    print("=" * 65)

    print("\nGenerated analysis files:")

    output_files = [
        building_output,
        cost_component_output,
        budget_output,
        savings_output,
        roi_output,
        health_output,
        resource_output,
        optimization_output,
        summary_output
    ]

    for file in output_files:
        print(f" - {file.name}")

    print("\nAll files saved in:")
    print(PROCESSED_FOLDER)

    print("=" * 65)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    cost_analysis()