import pandas as pd
from pathlib import Path


# ============================================================
# CROSS-AGENT ORCHESTRATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# ACTUAL PROJECT FILE LOCATIONS
# ============================================================

# Energy Agent
ENERGY_FILE = (
    BASE_DIR
    / "data"
    / "energy"
    / "energy_anomaly_results.csv"
)

# Predictive Maintenance Agent
MAINTENANCE_FILE = (
    BASE_DIR
    / "data"
    / "maintenance"
    / "processed"
    / "maintenance_agent_results.csv"
)

# Occupancy Agent
OCCUPANCY_FILE = (
    BASE_DIR
    / "data"
    / "occupancy"
    / "processed"
    / "occupancy_agent_results.csv"
)

# Security Agent
# IMPORTANT:
# Your actual security processed file is inside data\energy
SECURITY_FILE = (
    BASE_DIR
    / "data"
    / "energy"
    / "security_processed.csv"
)

# Cost Optimization Agent
COST_FILE = (
    BASE_DIR
    / "data"
    / "cost_optimization"
    / "processed"
    / "cost_optimization_agent_results.csv"
)

# Final output
OUTPUT_FOLDER = (
    BASE_DIR
    / "data"
    / "cost_optimization"
    / "processed"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER
    / "cross_agent_cost_analysis.csv"
)


# ============================================================
# LOAD FILE
# ============================================================

def load_file(file_path, agent_name):

    print(f"\nLoading {agent_name} data...")

    if not file_path.exists():

        print(
            f"WARNING: {agent_name} file not found:"
        )

        print(file_path)

        return None

    try:

        df = pd.read_csv(file_path)

        print(
            f"{agent_name} data loaded successfully "
            f"({len(df)} records)"
        )

        return df

    except Exception as error:

        print(
            f"ERROR loading {agent_name} data: {error}"
        )

        return None


# ============================================================
# FIND BUILDING COLUMN
# ============================================================

def find_building_column(df):

    if df is None:
        return None

    possible_columns = [
        "Building_ID",
        "building_id",
        "BUILDING_ID"
    ]

    for column in possible_columns:

        if column in df.columns:
            return column

    return None


# ============================================================
# ENERGY AGENT ANALYSIS
# ============================================================

def analyze_energy(df):

    if df is None:
        return pd.DataFrame()

    building_column = find_building_column(df)

    if building_column is None:

        print(
            "WARNING: Building_ID not found "
            "in Energy data."
        )

        return pd.DataFrame()

    energy_column = None

    possible_energy_columns = [
        "Energy_Consumption_kWh",
        "Energy_Consumption",
        "Energy_Consumption_kwh",
        "Predicted_Energy_Consumption"
    ]

    for column in possible_energy_columns:

        if column in df.columns:

            energy_column = column
            break

    anomaly_column = None

    possible_anomaly_columns = [
        "Anomaly",
        "Anomaly_Flag",
        "Is_Anomaly",
        "Anomaly_Detected",
        "Prediction"
    ]

    for column in possible_anomaly_columns:

        if column in df.columns:

            anomaly_column = column
            break

    result = (
        df.groupby(building_column)
        .size()
        .reset_index(
            name="Energy_Records"
        )
    )

    result = result.rename(
        columns={
            building_column: "Building_ID"
        }
    )

    if energy_column is not None:

        energy_average = (
            df.groupby(building_column)[
                energy_column
            ]
            .mean()
            .reset_index()
        )

        energy_average = energy_average.rename(
            columns={
                building_column:
                    "Building_ID",
                energy_column:
                    "Average_Energy_Consumption"
            }
        )

        result = result.merge(
            energy_average,
            on="Building_ID",
            how="left"
        )

        overall_average = (
            df[energy_column].mean()
        )

        result[
            "Energy_Cost_Impact"
        ] = result[
            "Average_Energy_Consumption"
        ].apply(
            lambda value:
            "HIGH"
            if value > overall_average
            else "NORMAL"
        )

    else:

        result[
            "Average_Energy_Consumption"
        ] = 0

        result[
            "Energy_Cost_Impact"
        ] = "NORMAL"

    if anomaly_column is not None:

        anomaly_counts = []

        for building_id, group in df.groupby(
            building_column
        ):

            values = (
                group[anomaly_column]
                .astype(str)
                .str.upper()
            )

            anomaly_count = values.isin(
                [
                    "1",
                    "TRUE",
                    "YES",
                    "ABNORMAL",
                    "ANOMALY",
                    "HIGH"
                ]
            ).sum()

            anomaly_counts.append({
                "Building_ID": building_id,
                "Energy_Anomaly_Count":
                    anomaly_count
            })

        anomaly_df = pd.DataFrame(
            anomaly_counts
        )

        result = result.merge(
            anomaly_df,
            on="Building_ID",
            how="left"
        )

    else:

        result[
            "Energy_Anomaly_Count"
        ] = 0

    return result


# ============================================================
# MAINTENANCE AGENT ANALYSIS
# ============================================================

def analyze_maintenance(df):

    if df is None:
        return pd.DataFrame()

    building_column = find_building_column(df)

    if building_column is None:

        print(
            "WARNING: Building_ID not found "
            "in Maintenance data."
        )

        return pd.DataFrame()

    result_data = []

    for building_id, group in df.groupby(
        building_column
    ):

        high_count = 0
        medium_count = 0
        low_count = 0

        if "Priority" in group.columns:

            priority_values = (
                group["Priority"]
                .astype(str)
                .str.upper()
            )

            high_count = (
                priority_values == "HIGH"
            ).sum()

            medium_count = (
                priority_values == "MEDIUM"
            ).sum()

            low_count = (
                priority_values == "LOW"
            ).sum()

        elif "Maintenance_Decision" in group.columns:

            decision_values = (
                group["Maintenance_Decision"]
                .astype(str)
                .str.upper()
            )

            high_count = (
                decision_values
                .str.contains(
                    "URGENT|HIGH|CRITICAL",
                    regex=True
                )
                .sum()
            )

            medium_count = (
                decision_values
                .str.contains(
                    "MEDIUM|MAINTENANCE",
                    regex=True
                )
                .sum()
            )

            low_count = (
                len(group)
                - high_count
                - medium_count
            )

        if high_count > 0:

            risk_level = "HIGH"
            impact = "HIGH"

        elif medium_count > 0:

            risk_level = "MEDIUM"
            impact = "MEDIUM"

        else:

            risk_level = "LOW"
            impact = "LOW"

        result_data.append({

            "Building_ID":
                building_id,

            "Maintenance_High_Count":
                high_count,

            "Maintenance_Medium_Count":
                medium_count,

            "Maintenance_Low_Count":
                low_count,

            "Maintenance_Risk_Level":
                risk_level,

            "Maintenance_Impact":
                impact
        })

    return pd.DataFrame(
        result_data
    )


# ============================================================
# OCCUPANCY AGENT ANALYSIS
# ============================================================

def analyze_occupancy(df):

    if df is None:
        return pd.DataFrame()

    building_column = find_building_column(df)

    if building_column is None:

        print(
            "WARNING: Building_ID not found "
            "in Occupancy data."
        )

        return pd.DataFrame()

    result_data = []

    for building_id, group in df.groupby(
        building_column
    ):

        high_usage = 0
        overcrowding = 0
        low_usage = 0

        if "Occupancy_Decision" in group.columns:

            decision_text = (
                group["Occupancy_Decision"]
                .astype(str)
                .str.upper()
            )

            high_usage = (
                decision_text
                .str.contains(
                    "HIGH USAGE"
                )
                .sum()
            )

            overcrowding = (
                decision_text
                .str.contains(
                    "OVERCROWD"
                )
                .sum()
            )

            low_usage = (
                decision_text
                .str.contains(
                    "LOW USAGE"
                )
                .sum()
            )

        elif "Alert" in group.columns:

            alert_text = (
                group["Alert"]
                .astype(str)
                .str.upper()
            )

            high_usage = (
                alert_text
                .str.contains(
                    "HIGH"
                )
                .sum()
            )

            overcrowding = (
                alert_text
                .str.contains(
                    "OVERCROWD"
                )
                .sum()
            )

        elif "Priority" in group.columns:

            priority_text = (
                group["Priority"]
                .astype(str)
                .str.upper()
            )

            high_usage = (
                priority_text == "MEDIUM"
            ).sum()

        if overcrowding > 0:

            impact = "HIGH"

        elif high_usage > 0:

            impact = "MEDIUM"

        else:

            impact = "LOW"

        result_data.append({

            "Building_ID":
                building_id,

            "High_Usage_Records":
                high_usage,

            "Overcrowding_Records":
                overcrowding,

            "Low_Usage_Records":
                low_usage,

            "Occupancy_Cost_Impact":
                impact
        })

    return pd.DataFrame(
        result_data
    )


# ============================================================
# SECURITY AGENT ANALYSIS
# ============================================================

def analyze_security(df):

    if df is None:
        return pd.DataFrame()

    building_column = find_building_column(df)

    if building_column is None:

        print(
            "WARNING: Building_ID not found "
            "in Security data."
        )

        return pd.DataFrame()

    result_data = []

    for building_id, group in df.groupby(
        building_column
    ):

        unauthorized = 0
        security_alerts = 0
        incidents = 0
        cctv_issues = 0
        high_risk = 0
        critical_risk = 0

        # Unauthorized access
        if "Authorization_Status" in group.columns:

            authorization = (
                group["Authorization_Status"]
                .astype(str)
                .str.upper()
            )

            unauthorized = (
                authorization
                .str.contains(
                    "UNAUTHORIZED"
                )
            ).sum()

        # Security alerts
        if "Security_Alert" in group.columns:

            alert_values = (
                group["Security_Alert"]
                .astype(str)
                .str.upper()
            )

            security_alerts = (
                alert_values.isin(
                    [
                        "YES",
                        "TRUE",
                        "1",
                        "ALERT"
                    ]
                )
            ).sum()

        # Incidents
        if "Incident_Detected" in group.columns:

            incident_values = (
                group["Incident_Detected"]
                .astype(str)
                .str.upper()
            )

            incidents = (
                incident_values.isin(
                    [
                        "YES",
                        "TRUE",
                        "1"
                    ]
                )
            ).sum()

        # CCTV issues
        if "CCTV_Status" in group.columns:

            cctv_values = (
                group["CCTV_Status"]
                .astype(str)
                .str.upper()
            )

            cctv_issues = (
                ~cctv_values.isin(
                    [
                        "NORMAL",
                        "OK",
                        "ACTIVE"
                    ]
                )
            ).sum()

        # Risk level
        if "Risk_Level" in group.columns:

            risk_values = (
                group["Risk_Level"]
                .astype(str)
                .str.upper()
            )

            high_risk = (
                risk_values == "HIGH"
            ).sum()

            critical_risk = (
                risk_values == "CRITICAL"
            ).sum()

        # Security impact
        if (
            critical_risk > 0
            or incidents > 0
            or unauthorized > 0
        ):

            impact = "HIGH"

        elif (
            security_alerts > 0
            or cctv_issues > 0
            or high_risk > 0
        ):

            impact = "MEDIUM"

        else:

            impact = "LOW"

        result_data.append({

            "Building_ID":
                building_id,

            "Unauthorized_Access":
                unauthorized,

            "Security_Alerts":
                security_alerts,

            "Security_Incidents":
                incidents,

            "CCTV_Issues":
                cctv_issues,

            "High_Risk_Events":
                high_risk,

            "Critical_Risk_Events":
                critical_risk,

            "Security_Cost_Impact":
                impact
        })

    return pd.DataFrame(
        result_data
    )


# ============================================================
# COST OPTIMIZATION ANALYSIS
# ============================================================

def analyze_cost(df):

    if df is None:
        return pd.DataFrame()

    building_column = find_building_column(df)

    if building_column is None:

        print(
            "WARNING: Building_ID not found "
            "in Cost Optimization data."
        )

        return pd.DataFrame()

    result = (
        df.groupby(building_column)
        .agg(
            Total_Operational_Cost=(
                "Total_Operational_Cost",
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

            Total_Savings_Opportunity=(
                "Savings_Opportunity",
                "sum"
            ),

            Average_Facility_Health=(
                "Facility_Health_Score",
                "mean"
            ),

            Average_Resource_Utilization=(
                "Resource_Utilization_Percent",
                "mean"
            ),

            Optimization_Records=(
                "Record_ID",
                "count"
            )
        )
        .reset_index()
    )

    result = result.rename(
        columns={
            building_column:
                "Building_ID"
        }
    )

    return result


# ============================================================
# CROSS-AGENT IMPACT SCORE
# ============================================================

def calculate_impact_score(row):

    score = 0

    if row.get(
        "Energy_Cost_Impact",
        "NORMAL"
    ) == "HIGH":

        score += 2

    if row.get(
        "Maintenance_Impact",
        "LOW"
    ) == "HIGH":

        score += 2

    elif row.get(
        "Maintenance_Impact",
        "LOW"
    ) == "MEDIUM":

        score += 1

    if row.get(
        "Occupancy_Cost_Impact",
        "LOW"
    ) == "HIGH":

        score += 2

    elif row.get(
        "Occupancy_Cost_Impact",
        "LOW"
    ) == "MEDIUM":

        score += 1

    if row.get(
        "Security_Cost_Impact",
        "LOW"
    ) == "HIGH":

        score += 2

    elif row.get(
        "Security_Cost_Impact",
        "LOW"
    ) == "MEDIUM":

        score += 1

    if row.get(
        "Average_Cost_Reduction",
        0
    ) < 10:

        score += 1

    if row.get(
        "Average_ROI",
        0
    ) < 20:

        score += 1

    return score


# ============================================================
# CROSS-AGENT PRIORITY
# ============================================================

def determine_priority(score):

    if score >= 6:

        return "CRITICAL"

    elif score >= 4:

        return "HIGH"

    elif score >= 2:

        return "MEDIUM"

    else:

        return "LOW"


# ============================================================
# CROSS-AGENT RECOMMENDATION
# ============================================================

def generate_recommendation(row):

    recommendations = []

    if row.get(
        "Energy_Cost_Impact",
        "NORMAL"
    ) == "HIGH":

        recommendations.append(
            "Reduce energy consumption"
        )

    if row.get(
        "Maintenance_Impact",
        "LOW"
    ) in [
        "HIGH",
        "MEDIUM"
    ]:

        recommendations.append(
            "Optimize maintenance planning"
        )

    if row.get(
        "Occupancy_Cost_Impact",
        "LOW"
    ) in [
        "HIGH",
        "MEDIUM"
    ]:

        recommendations.append(
            "Optimize workspace and resource allocation"
        )

    if row.get(
        "Security_Cost_Impact",
        "LOW"
    ) in [
        "HIGH",
        "MEDIUM"
    ]:

        recommendations.append(
            "Optimize security resource allocation"
        )

    if row.get(
        "Average_Cost_Reduction",
        0
    ) < 10:

        recommendations.append(
            "Increase cost reduction initiatives"
        )

    if row.get(
        "Average_ROI",
        0
    ) < 20:

        recommendations.append(
            "Review low-return investments"
        )

    if row.get(
        "Total_Savings_Opportunity",
        0
    ) > 0:

        recommendations.append(
            "Implement identified savings opportunities"
        )

    if not recommendations:

        recommendations.append(
            "Continue monitoring and optimization"
        )

    return " | ".join(
        recommendations
    )


# ============================================================
# MAIN ORCHESTRATION
# ============================================================

def run_orchestration():

    print("=" * 70)
    print("CROSS-AGENT COST ORCHESTRATION")
    print("=" * 70)

    # Load all five agents
    energy_df = load_file(
        ENERGY_FILE,
        "Energy Agent"
    )

    maintenance_df = load_file(
        MAINTENANCE_FILE,
        "Maintenance Agent"
    )

    occupancy_df = load_file(
        OCCUPANCY_FILE,
        "Occupancy Agent"
    )

    security_df = load_file(
        SECURITY_FILE,
        "Security Agent"
    )

    cost_df = load_file(
        COST_FILE,
        "Cost Optimization Agent"
    )

    if cost_df is None:

        print(
            "\nERROR: Cost Optimization Agent "
            "data is required."
        )

        return

    print("\n" + "-" * 70)
    print("ANALYZING ALL AGENT IMPACTS")
    print("-" * 70)

    print("\nAnalyzing Energy Agent...")

    energy_analysis = analyze_energy(
        energy_df
    )

    print("Analyzing Maintenance Agent...")

    maintenance_analysis = analyze_maintenance(
        maintenance_df
    )

    print("Analyzing Occupancy Agent...")

    occupancy_analysis = analyze_occupancy(
        occupancy_df
    )

    print("Analyzing Security Agent...")

    security_analysis = analyze_security(
        security_df
    )

    print("Analyzing Cost Optimization Agent...")

    cost_analysis = analyze_cost(
        cost_df
    )

    # Start with cost data
    final_df = cost_analysis.copy()

    # Merge Energy
    if not energy_analysis.empty:

        final_df = final_df.merge(
            energy_analysis,
            on="Building_ID",
            how="left"
        )

    # Merge Maintenance
    if not maintenance_analysis.empty:

        final_df = final_df.merge(
            maintenance_analysis,
            on="Building_ID",
            how="left"
        )

    # Merge Occupancy
    if not occupancy_analysis.empty:

        final_df = final_df.merge(
            occupancy_analysis,
            on="Building_ID",
            how="left"
        )

    # Merge Security
    if not security_analysis.empty:

        final_df = final_df.merge(
            security_analysis,
            on="Building_ID",
            how="left"
        )

    # Fill missing values
    final_df = final_df.fillna(0)

    # Cross-agent impact score
    final_df[
        "Cross_Agent_Impact_Score"
    ] = final_df.apply(
        calculate_impact_score,
        axis=1
    )

    # Priority
    final_df[
        "Cross_Agent_Priority"
    ] = final_df[
        "Cross_Agent_Impact_Score"
    ].apply(
        determine_priority
    )

    # Recommendation
    final_df[
        "Cross_Agent_Recommendation"
    ] = final_df.apply(
        generate_recommendation,
        axis=1
    )

    # Round numbers
    numeric_columns = (
        final_df
        .select_dtypes(
            include="number"
        )
        .columns
    )

    final_df[numeric_columns] = (
        final_df[numeric_columns]
        .round(2)
    )

    # Create output directory
    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save
    final_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ========================================================
    # RESULTS
    # ========================================================

    print("\n" + "=" * 70)
    print("CROSS-AGENT ORCHESTRATION RESULTS")
    print("=" * 70)

    print(
        final_df.to_string(
            index=False
        )
    )

    print(
        "\nCross-Agent Priority Distribution:"
    )

    print(
        final_df[
            "Cross_Agent_Priority"
        ]
        .value_counts()
        .to_string()
    )

    # ========================================================
    # AGENT STATUS
    # ========================================================

    print("\nAgent Integration Status:")

    print(
        f"Energy Agent          : "
        f"{'CONNECTED' if energy_df is not None else 'NOT FOUND'}"
    )

    print(
        f"Maintenance Agent     : "
        f"{'CONNECTED' if maintenance_df is not None else 'NOT FOUND'}"
    )

    print(
        f"Occupancy Agent       : "
        f"{'CONNECTED' if occupancy_df is not None else 'NOT FOUND'}"
    )

    print(
        f"Security Agent        : "
        f"{'CONNECTED' if security_df is not None else 'NOT FOUND'}"
    )

    print(
        f"Cost Optimization     : "
        f"{'CONNECTED' if cost_df is not None else 'NOT FOUND'}"
    )

    print(
        "\nOutput saved successfully:"
    )

    print(OUTPUT_FILE)

    print(
        f"\nOutput rows    : "
        f"{len(final_df)}"
    )

    print(
        f"Output columns : "
        f"{len(final_df.columns)}"
    )

    print("\n" + "=" * 70)
    print(
        "CROSS-AGENT ORCHESTRATION COMPLETED SUCCESSFULLY"
    )
    print("=" * 70)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    run_orchestration()