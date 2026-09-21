import pandas as pd
from pathlib import Path


# ============================================================
# COST OPTIMIZATION DATA PREPROCESSING
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

COST_FOLDER = BASE_DIR / "data" / "cost_optimization"

INPUT_FILE = COST_FOLDER / "cost_optimization_dataset.xlsx"

PROCESSED_FOLDER = COST_FOLDER / "processed"

OUTPUT_FILE = PROCESSED_FOLDER / "cost_processed.csv"


def preprocess_cost_data():

    print("=" * 60)
    print("COST OPTIMIZATION DATA PREPROCESSING")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Check input file
    # --------------------------------------------------------

    if not INPUT_FILE.exists():

        print("\nERROR: Dataset not found!")
        print(f"Expected file: {INPUT_FILE}")
        return

    # --------------------------------------------------------
    # 2. Load dataset
    # --------------------------------------------------------

    df = pd.read_excel(INPUT_FILE)

    print("\n1. Dataset loaded successfully")
    print(f"Input rows    : {len(df)}")
    print(f"Input columns : {len(df.columns)}")

    # --------------------------------------------------------
    # 3. Create processed folder
    # --------------------------------------------------------

    PROCESSED_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\n2. Processed folder ready")
    print(f"Output folder: {PROCESSED_FOLDER}")

    # --------------------------------------------------------
    # 4. Convert Timestamp
    # --------------------------------------------------------

    print("\n3. Processing Timestamp")

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # 5. Create time-based features
    # --------------------------------------------------------

    print("\n4. Creating Time Features")

    df["Year"] = df["Timestamp"].dt.year

    df["Month"] = df["Timestamp"].dt.month

    df["Day"] = df["Timestamp"].dt.day

    df["Hour"] = df["Timestamp"].dt.hour

    df["Day_of_Week"] = df["Timestamp"].dt.day_name()

    df["Day_of_Week_Num"] = df["Timestamp"].dt.dayofweek

    df["Is_Weekend"] = (
        df["Day_of_Week_Num"] >= 5
    ).astype(int)

    # --------------------------------------------------------
    # 6. Cost percentage calculations
    # --------------------------------------------------------

    print("\n5. Creating Cost Analysis Features")

    df["Energy_Cost_Percent"] = (
        df["Energy_Cost"]
        / df["Total_Operational_Cost"]
        * 100
    )

    df["Maintenance_Cost_Percent"] = (
        df["Maintenance_Cost"]
        / df["Total_Operational_Cost"]
        * 100
    )

    df["Security_Cost_Percent"] = (
        df["Security_Cost"]
        / df["Total_Operational_Cost"]
        * 100
    )

    df["Administrative_Cost_Percent"] = (
        df["Administrative_Cost"]
        / df["Total_Operational_Cost"]
        * 100
    )

    # --------------------------------------------------------
    # 7. Budget status
    # --------------------------------------------------------

    print("\n6. Creating Budget Status")

    df["Budget_Status"] = df.apply(
        lambda row:
            "Within Budget"
            if row["Total_Operational_Cost"] <= row["Budget"]
            else "Over Budget",
        axis=1
    )

    # --------------------------------------------------------
    # 8. Savings opportunity category
    # --------------------------------------------------------

    print("\n7. Creating Savings Opportunity Category")

    df["Savings_Category"] = pd.cut(
        df["Savings_Opportunity"],
        bins=[
            -float("inf"),
            500,
            1000,
            2000,
            float("inf")
        ],
        labels=[
            "Low",
            "Moderate",
            "High",
            "Very High"
        ]
    )

    # --------------------------------------------------------
    # 9. Cost reduction category
    # --------------------------------------------------------

    print("\n8. Creating Cost Reduction Category")

    df["Cost_Reduction_Category"] = pd.cut(
        df["Cost_Reduction_Percent"],
        bins=[
            -float("inf"),
            5,
            10,
            15,
            float("inf")
        ],
        labels=[
            "Low",
            "Moderate",
            "High",
            "Very High"
        ]
    )

    # --------------------------------------------------------
    # 10. ROI category
    # --------------------------------------------------------

    print("\n9. Creating ROI Category")

    df["ROI_Category"] = pd.cut(
        df["ROI_Generated_Percent"],
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

    # --------------------------------------------------------
    # 11. Facility health category
    # --------------------------------------------------------

    print("\n10. Creating Facility Health Category")

    df["Facility_Health_Category"] = pd.cut(
        df["Facility_Health_Score"],
        bins=[
            -float("inf"),
            60,
            75,
            90,
            float("inf")
        ],
        labels=[
            "Poor",
            "Fair",
            "Good",
            "Excellent"
        ]
    )

    # --------------------------------------------------------
    # 12. Resource utilization category
    # --------------------------------------------------------

    print("\n11. Creating Resource Utilization Category")

    df["Resource_Utilization_Category"] = pd.cut(
        df["Resource_Utilization_Percent"],
        bins=[
            -float("inf"),
            50,
            70,
            85,
            float("inf")
        ],
        labels=[
            "Low",
            "Moderate",
            "High",
            "Very High"
        ]
    )

    # --------------------------------------------------------
    # 13. Vendor utilization category
    # --------------------------------------------------------

    print("\n12. Creating Vendor Utilization Category")

    df["Vendor_Utilization_Category"] = pd.cut(
        df["Vendor_Utilization_Percent"],
        bins=[
            -float("inf"),
            50,
            70,
            85,
            float("inf")
        ],
        labels=[
            "Low",
            "Moderate",
            "High",
            "Very High"
        ]
    )

    # --------------------------------------------------------
    # 14. Optimization category
    # --------------------------------------------------------

    print("\n13. Creating Optimization Category")

    df["Optimization_Category"] = pd.cut(
        df["Optimization_Count"],
        bins=[
            -float("inf"),
            3,
            7,
            12,
            float("inf")
        ],
        labels=[
            "Low",
            "Moderate",
            "High",
            "Very High"
        ]
    )

    # --------------------------------------------------------
    # 15. Potential savings percentage
    # --------------------------------------------------------

    print("\n14. Creating Potential Savings Percentage")

    df["Savings_Opportunity_Percent"] = (
        df["Savings_Opportunity"]
        / df["Total_Operational_Cost"]
        * 100
    )

    # --------------------------------------------------------
    # 16. Cost efficiency score
    # --------------------------------------------------------

    print("\n15. Creating Cost Efficiency Score")

    df["Cost_Efficiency_Score"] = (
        (
            df["Cost_Reduction_Percent"]
            + df["ROI_Generated_Percent"]
            + df["Facility_Health_Score"]
            + df["Resource_Utilization_Percent"]
        )
        / 4
    )

    df["Cost_Efficiency_Score"] = (
        df["Cost_Efficiency_Score"].round(2)
    )

    # --------------------------------------------------------
    # 17. Remove invalid rows
    # --------------------------------------------------------

    print("\n16. Cleaning Invalid Records")

    before_cleaning = len(df)

    df = df.dropna(
        subset=[
            "Timestamp",
            "Building_ID",
            "Total_Operational_Cost"
        ]
    )

    after_cleaning = len(df)

    removed_records = (
        before_cleaning - after_cleaning
    )

    print(f"Records before cleaning : {before_cleaning}")
    print(f"Records after cleaning  : {after_cleaning}")
    print(f"Records removed         : {removed_records}")

    # --------------------------------------------------------
    # 18. Save processed dataset
    # --------------------------------------------------------

    print("\n17. Saving Processed Dataset")

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Processed dataset saved:")
    print(OUTPUT_FILE)

    # --------------------------------------------------------
    # 19. Display final information
    # --------------------------------------------------------

    print("\n18. Final Dataset Information")

    print(f"Final rows    : {len(df)}")
    print(f"Final columns : {len(df.columns)}")

    print("\nNew Features Created:")

    new_features = [
        "Year",
        "Month",
        "Day",
        "Hour",
        "Day_of_Week",
        "Day_of_Week_Num",
        "Is_Weekend",
        "Energy_Cost_Percent",
        "Maintenance_Cost_Percent",
        "Security_Cost_Percent",
        "Administrative_Cost_Percent",
        "Budget_Status",
        "Savings_Category",
        "Cost_Reduction_Category",
        "ROI_Category",
        "Facility_Health_Category",
        "Resource_Utilization_Category",
        "Vendor_Utilization_Category",
        "Optimization_Category",
        "Savings_Opportunity_Percent",
        "Cost_Efficiency_Score"
    ]

    for feature in new_features:

        if feature in df.columns:
            print(f" - {feature}")

    # --------------------------------------------------------
    # 20. Summary
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("PREPROCESSING COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print("\nProcessed file:")
    print(OUTPUT_FILE)

    print("=" * 60)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    preprocess_cost_data()