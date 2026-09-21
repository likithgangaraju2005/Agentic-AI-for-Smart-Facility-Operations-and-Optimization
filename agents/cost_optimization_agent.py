import pandas as pd
from pathlib import Path


# ============================================================
# COST OPTIMIZATION AGENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_FOLDER = (
    BASE_DIR
    / "data"
    / "cost_optimization"
    / "processed"
)

INPUT_FILE = PROCESSED_FOLDER / "cost_processed.csv"

OUTPUT_FILE = (
    PROCESSED_FOLDER
    / "cost_optimization_agent_results.csv"
)


# ============================================================
# COST OPTIMIZATION AGENT CLASS
# ============================================================

class CostOptimizationAgent:

    def __init__(self):

        self.data = None
        self.results = None

    # --------------------------------------------------------
    # Load processed data
    # --------------------------------------------------------

    def load_data(self):

        print("\n1. Loading processed cost data")

        if not INPUT_FILE.exists():

            print("ERROR: Processed cost dataset not found!")
            print(f"Expected file: {INPUT_FILE}")

            return False

        self.data = pd.read_csv(INPUT_FILE)

        print("Processed cost data loaded successfully")
        print(f"Records : {len(self.data)}")

        return True

    # --------------------------------------------------------
    # Generate optimization decision
    # --------------------------------------------------------

    def generate_decision(self, row):

        recommendations = []
        actions = []

        priority = "LOW"
        decision = "Maintain Current Operations"

        # ----------------------------------------------------
        # Energy cost optimization
        # ----------------------------------------------------

        if row["Energy_Cost_Percent"] >= 45:

            recommendations.append(
                "Optimize energy consumption"
            )

            actions.append(
                "Review HVAC and lighting usage"
            )

            priority = "HIGH"
            decision = "Energy Cost Optimization Required"

        # ----------------------------------------------------
        # Maintenance cost optimization
        # ----------------------------------------------------

        if row["Maintenance_Cost_Percent"] >= 25:

            recommendations.append(
                "Optimize maintenance expenditure"
            )

            actions.append(
                "Review preventive maintenance schedules"
            )

            if priority != "HIGH":
                priority = "MEDIUM"

            decision = (
                "Maintenance Cost Optimization Required"
            )

        # ----------------------------------------------------
        # Security cost optimization
        # ----------------------------------------------------

        if row["Security_Cost_Percent"] >= 18:

            recommendations.append(
                "Review security operating costs"
            )

            actions.append(
                "Optimize security resource allocation"
            )

            if priority == "LOW":
                priority = "MEDIUM"

            decision = (
                "Security Cost Optimization Required"
            )

        # ----------------------------------------------------
        # Administrative cost optimization
        # ----------------------------------------------------

        if row["Administrative_Cost_Percent"] >= 18:

            recommendations.append(
                "Reduce administrative overhead"
            )

            actions.append(
                "Review administrative resource usage"
            )

            if priority == "LOW":
                priority = "MEDIUM"

            decision = (
                "Administrative Cost Optimization Required"
            )

        # ----------------------------------------------------
        # Savings opportunity
        # ----------------------------------------------------

        if row["Savings_Opportunity_Percent"] >= 10:

            recommendations.append(
                "Implement identified savings opportunities"
            )

            actions.append(
                "Prioritize high-value cost-saving activities"
            )

            if priority == "LOW":
                priority = "MEDIUM"

        # ----------------------------------------------------
        # Cost reduction
        # ----------------------------------------------------

        if row["Cost_Reduction_Percent"] < 10:

            recommendations.append(
                "Increase cost reduction initiatives"
            )

            actions.append(
                "Identify additional cost-saving opportunities"
            )

            if priority == "LOW":
                priority = "MEDIUM"

        # ----------------------------------------------------
        # ROI
        # ----------------------------------------------------

        if row["ROI_Generated_Percent"] < 20:

            recommendations.append(
                "Review low-return investments"
            )

            actions.append(
                "Evaluate investment effectiveness"
            )

            priority = "MEDIUM"

        # ----------------------------------------------------
        # Facility health
        # ----------------------------------------------------

        if row["Facility_Health_Score"] < 70:

            recommendations.append(
                "Improve facility health"
            )

            actions.append(
                "Prioritize facility maintenance activities"
            )

            priority = "HIGH"

        # ----------------------------------------------------
        # Resource utilization
        # ----------------------------------------------------

        if row["Resource_Utilization_Percent"] < 50:

            recommendations.append(
                "Improve resource utilization"
            )

            actions.append(
                "Reallocate underutilized resources"
            )

            if priority == "LOW":
                priority = "MEDIUM"

        elif row["Resource_Utilization_Percent"] > 85:

            recommendations.append(
                "Monitor high resource utilization"
            )

            actions.append(
                "Balance resource allocation"
            )

            if priority == "LOW":
                priority = "MEDIUM"

        # ----------------------------------------------------
        # Vendor utilization
        # ----------------------------------------------------

        if row["Vendor_Utilization_Percent"] < 50:

            recommendations.append(
                "Optimize vendor utilization"
            )

            actions.append(
                "Review vendor resource allocation"
            )

            if priority == "LOW":
                priority = "MEDIUM"

        # ----------------------------------------------------
        # Optimization count
        # ----------------------------------------------------

        if row["Optimization_Count"] >= 10:

            recommendations.append(
                "Prioritize multiple optimization opportunities"
            )

            actions.append(
                "Create a structured optimization plan"
            )

            if priority == "LOW":
                priority = "MEDIUM"

        # ----------------------------------------------------
        # Budget
        # ----------------------------------------------------

        if row["Budget_Status"] == "Over Budget":

            recommendations.append(
                "Reduce operational expenditure"
            )

            actions.append(
                "Review spending against allocated budget"
            )

            priority = "HIGH"

            decision = "Budget Optimization Required"

        # ----------------------------------------------------
        # Default recommendation
        # ----------------------------------------------------

        if len(recommendations) == 0:

            recommendations.append(
                "Continue monitoring facility performance"
            )

            actions.append(
                "Maintain current optimization strategy"
            )

        return (
            decision,
            priority,
            " | ".join(recommendations),
            " | ".join(actions)
        )

    # --------------------------------------------------------
    # Run agent
    # --------------------------------------------------------

    def run_agent(self):

        print("\n2. Running Cost Optimization Agent")

        results = []

        for _, row in self.data.iterrows():

            (
                decision,
                priority,
                recommendation,
                action
            ) = self.generate_decision(row)

            results.append({

                "Record_ID":
                    row["Record_ID"],

                "Timestamp":
                    row["Timestamp"],

                "Building_ID":
                    row["Building_ID"],

                "Total_Operational_Cost":
                    row["Total_Operational_Cost"],

                "Budget":
                    row["Budget"],

                "Savings_Opportunity":
                    row["Savings_Opportunity"],

                "Cost_Reduction_Percent":
                    row["Cost_Reduction_Percent"],

                "ROI_Generated_Percent":
                    row["ROI_Generated_Percent"],

                "Facility_Health_Score":
                    row["Facility_Health_Score"],

                "Resource_Utilization_Percent":
                    row["Resource_Utilization_Percent"],

                "Optimization_Count":
                    row["Optimization_Count"],

                "Optimization_Decision":
                    decision,

                "Priority":
                    priority,

                "Recommendation":
                    recommendation,

                "Recommended_Action":
                    action
            })

        self.results = pd.DataFrame(results)

        print("Cost Optimization Agent completed")

    # --------------------------------------------------------
    # Display summary
    # --------------------------------------------------------

    def display_summary(self):

        print("\n3. Cost Optimization Agent Summary")

        print(
            "\nOptimization Decision Distribution:"
        )

        print(
            self.results[
                "Optimization_Decision"
            ].value_counts().to_string()
        )

        print(
            "\nPriority Distribution:"
        )

        print(
            self.results[
                "Priority"
            ].value_counts().to_string()
        )

        print(
            "\nBuilding-wise Optimization Summary:"
        )

        building_summary = (
            self.results
            .groupby("Building_ID")
            .agg(
                Records=(
                    "Record_ID",
                    "count"
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
                )
            )
            .reset_index()
        )

        building_summary = (
            building_summary.round(2)
        )

        print(
            building_summary.to_string(
                index=False
            )
        )

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    def save_results(self):

        print("\n4. Saving Agent Results")

        self.results.to_csv(
            OUTPUT_FILE,
            index=False
        )

        print(
            "Agent results saved successfully:"
        )

        print(OUTPUT_FILE)

        print(
            f"\nOutput records : {len(self.results)}"
        )

        print(
            f"Output columns : {len(self.results.columns)}"
        )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 65)
    print("COST OPTIMIZATION AGENT")
    print("=" * 65)

    agent = CostOptimizationAgent()

    if not agent.load_data():
        return

    agent.run_agent()

    agent.display_summary()

    agent.save_results()

    print("\n" + "=" * 65)
    print("COST OPTIMIZATION AGENT COMPLETED SUCCESSFULLY")
    print("=" * 65)


if __name__ == "__main__":
    main()