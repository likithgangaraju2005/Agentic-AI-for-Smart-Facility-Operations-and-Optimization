import pandas as pd
from pathlib import Path


# ============================================================
# COST OPTIMIZATION DATA VALIDATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

COST_FOLDER = BASE_DIR / "data" / "cost_optimization"


def find_dataset():

    # Possible filenames
    possible_files = [
        COST_FOLDER / "cost_optimization_dataset.xlsx",
        COST_FOLDER / "cost_optimization_dataset.csv.xlsx",
        COST_FOLDER / "cost_optimization_dataset.xls",
    ]

    for file in possible_files:
        if file.exists():
            return file

    # Automatically search for Excel files if exact name is different
    excel_files = list(COST_FOLDER.glob("*.xlsx"))

    if len(excel_files) > 0:
        return excel_files[0]

    return None


def validate_cost_data():

    print("=" * 60)
    print("COST OPTIMIZATION DATA VALIDATION")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Find dataset
    # --------------------------------------------------------

    DATA_FILE = find_dataset()

    if DATA_FILE is None:
        print("\nERROR: Dataset not found!")
        print(f"Expected folder: {COST_FOLDER}")
        print("\nPlease make sure the Excel dataset is inside:")
        print(COST_FOLDER)
        return

    print("\nDataset found successfully!")
    print(f"File: {DATA_FILE}")

    # --------------------------------------------------------
    # 2. Load dataset
    # --------------------------------------------------------

    try:
        df = pd.read_excel(DATA_FILE)

    except Exception as e:
        print("\nERROR: Unable to read the Excel file.")
        print(f"Details: {e}")
        return

    print("\n1. Dataset loaded successfully")

    # --------------------------------------------------------
    # 3. Dataset shape
    # --------------------------------------------------------

    print("\n2. Dataset Shape")
    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    # --------------------------------------------------------
    # 4. Columns
    # --------------------------------------------------------

    print("\n3. Columns")

    for column in df.columns:
        print(f" - {column}")

    # --------------------------------------------------------
    # 5. Missing values
    # --------------------------------------------------------

    print("\n4. Missing Value Check")

    missing_values = df.isnull().sum()
    total_missing = missing_values.sum()

    if total_missing == 0:
        print("No missing values found.")
    else:
        print(f"Total missing values: {total_missing}")

        for column, count in missing_values.items():

            if count > 0:
                print(f" - {column}: {count}")

    # --------------------------------------------------------
    # 6. Duplicate records
    # --------------------------------------------------------

    print("\n5. Duplicate Record Check")

    duplicates = df.duplicated().sum()

    if duplicates == 0:
        print("No duplicate records found.")
    else:
        print(f"Duplicate records: {duplicates}")

    # --------------------------------------------------------
    # 7. Record ID
    # --------------------------------------------------------

    print("\n6. Record ID Validation")

    if "Record_ID" in df.columns:

        duplicate_ids = df["Record_ID"].duplicated().sum()

        if duplicate_ids == 0:
            print("Record IDs are unique.")
        else:
            print(f"Duplicate Record IDs: {duplicate_ids}")

    # --------------------------------------------------------
    # 8. Cost validation
    # --------------------------------------------------------

    print("\n7. Cost Value Validation")

    cost_columns = [
        "Energy_Cost",
        "Maintenance_Cost",
        "Security_Cost",
        "Administrative_Cost",
        "Total_Operational_Cost",
        "Budget",
        "Savings_Opportunity",
        "Investment_Amount"
    ]

    for column in cost_columns:

        if column not in df.columns:
            print(f"{column}: Column not found")
            continue

        negative_count = (df[column] < 0).sum()

        if negative_count == 0:
            print(f"{column}: Valid")
        else:
            print(
                f"{column}: "
                f"{negative_count} negative values found"
            )

    # --------------------------------------------------------
    # 9. Percentage validation
    # --------------------------------------------------------

    print("\n8. Percentage Validation")

    percentage_columns = [
        "Budget_Compliance_Percent",
        "Cost_Reduction_Percent",
        "ROI_Generated_Percent",
        "Resource_Utilization_Percent",
        "Vendor_Utilization_Percent"
    ]

    for column in percentage_columns:

        if column not in df.columns:
            print(f"{column}: Column not found")
            continue

        invalid_count = (
            (df[column] < 0) |
            (df[column] > 100)
        ).sum()

        if invalid_count == 0:
            print(f"{column}: Valid")
        else:
            print(
                f"{column}: "
                f"{invalid_count} invalid values"
            )

    # --------------------------------------------------------
    # 10. Facility health
    # --------------------------------------------------------

    print("\n9. Facility Health Validation")

    if "Facility_Health_Score" in df.columns:

        invalid_health = (
            (df["Facility_Health_Score"] < 0) |
            (df["Facility_Health_Score"] > 100)
        ).sum()

        if invalid_health == 0:
            print("Facility Health Score: Valid")
        else:
            print(
                f"Invalid Facility Health values: "
                f"{invalid_health}"
            )

    # --------------------------------------------------------
    # 11. Optimization count
    # --------------------------------------------------------

    print("\n10. Optimization Count Validation")

    if "Optimization_Count" in df.columns:

        invalid_optimization = (
            df["Optimization_Count"] < 0
        ).sum()

        if invalid_optimization == 0:
            print("Optimization Count: Valid")
        else:
            print(
                f"Invalid Optimization Count: "
                f"{invalid_optimization}"
            )

    # --------------------------------------------------------
    # 12. Building validation
    # --------------------------------------------------------

    print("\n11. Building Validation")

    if "Building_ID" in df.columns:

        valid_buildings = [
            "BLDG_A",
            "BLDG_B",
            "BLDG_C"
        ]

        invalid_buildings = (
            ~df["Building_ID"].isin(valid_buildings)
        ).sum()

        if invalid_buildings == 0:
            print("Building IDs: Valid")
        else:
            print(
                f"Invalid Building IDs: "
                f"{invalid_buildings}"
            )

        print("\nBuilding Distribution:")

        building_counts = df["Building_ID"].value_counts()

        for building, count in building_counts.items():
            print(f" - {building}: {count}")

    # --------------------------------------------------------
    # 13. Timestamp validation
    # --------------------------------------------------------

    print("\n12. Timestamp Validation")

    if "Timestamp" in df.columns:

        timestamp_data = pd.to_datetime(
            df["Timestamp"],
            errors="coerce"
        )

        invalid_timestamps = timestamp_data.isnull().sum()

        if invalid_timestamps == 0:
            print("Timestamps: Valid")
        else:
            print(
                f"Invalid timestamps: "
                f"{invalid_timestamps}"
            )

    # --------------------------------------------------------
    # 14. Total operational cost
    # --------------------------------------------------------

    print("\n13. Total Operational Cost Validation")

    required_columns = [
        "Energy_Cost",
        "Maintenance_Cost",
        "Security_Cost",
        "Administrative_Cost",
        "Total_Operational_Cost"
    ]

    if all(column in df.columns for column in required_columns):

        calculated_total = (
            df["Energy_Cost"]
            + df["Maintenance_Cost"]
            + df["Security_Cost"]
            + df["Administrative_Cost"]
        )

        difference = (
            calculated_total
            - df["Total_Operational_Cost"]
        ).abs()

        incorrect_total = (difference > 0.01).sum()

        if incorrect_total == 0:
            print("Total Operational Cost: Valid")
        else:
            print(
                f"Incorrect Total Operational Cost records: "
                f"{incorrect_total}"
            )

    # --------------------------------------------------------
    # 15. Dataset summary
    # --------------------------------------------------------

    print("\n14. Dataset Summary")

    print(f"Total Records  : {len(df)}")
    print(f"Total Columns  : {len(df.columns)}")

    if "Total_Operational_Cost" in df.columns:
        print(
            f"Average Operational Cost : "
            f"{df['Total_Operational_Cost'].mean():.2f}"
        )

    if "Cost_Reduction_Percent" in df.columns:
        print(
            f"Average Cost Reduction   : "
            f"{df['Cost_Reduction_Percent'].mean():.2f}%"
        )

    if "ROI_Generated_Percent" in df.columns:
        print(
            f"Average ROI              : "
            f"{df['ROI_Generated_Percent'].mean():.2f}%"
        )

    if "Facility_Health_Score" in df.columns:
        print(
            f"Average Facility Health  : "
            f"{df['Facility_Health_Score'].mean():.2f}"
        )

    if "Resource_Utilization_Percent" in df.columns:
        print(
            f"Average Resource Usage   : "
            f"{df['Resource_Utilization_Percent'].mean():.2f}%"
        )

    # --------------------------------------------------------
    # 16. Final validation
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    validation_passed = True

    if total_missing != 0:
        validation_passed = False

    if duplicates != 0:
        validation_passed = False

    if "Building_ID" in df.columns:

        if invalid_buildings != 0:
            validation_passed = False

    if "Timestamp" in df.columns:

        if invalid_timestamps != 0:
            validation_passed = False

    # Check percentage columns
    for column in percentage_columns:

        if column in df.columns:

            invalid_count = (
                (df[column] < 0) |
                (df[column] > 100)
            ).sum()

            if invalid_count != 0:
                validation_passed = False

    if validation_passed:

        print("SUCCESS: Cost Optimization dataset is valid.")

    else:

        print(
            "WARNING: Dataset contains validation issues."
        )

    print("=" * 60)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    validate_cost_data()