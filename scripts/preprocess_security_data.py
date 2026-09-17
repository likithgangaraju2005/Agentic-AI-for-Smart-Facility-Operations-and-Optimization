# ============================================================
# SECURITY AGENT - DATA PREPROCESSING
# Smart Facility Operations and Optimization
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 1. FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "security"
    / "security_agent_dataset.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "security_processed.csv"
)


# ============================================================
# 2. CREATE OUTPUT DIRECTORY
# ============================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 3. LOAD DATASET
# ============================================================

print("=" * 60)
print("SECURITY AGENT - DATA PREPROCESSING")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Original rows    : {len(df)}")
print(f"Original columns : {len(df.columns)}")


# ============================================================
# 4. CONVERT TIMESTAMP
# ============================================================

print("\nConverting Timestamp...")

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)


# ============================================================
# 5. CREATE TIME FEATURES
# ============================================================

print("Creating time-based features...")

df["Hour"] = df["Timestamp"].dt.hour

df["Day"] = df["Timestamp"].dt.day

df["Day_of_Week"] = df["Timestamp"].dt.day_name()

df["Month"] = df["Timestamp"].dt.month

df["Date"] = df["Timestamp"].dt.date


# ============================================================
# 6. WORKING HOURS
# ============================================================

print("Creating Working_Hours feature...")

df["Working_Hours"] = df["Hour"].apply(
    lambda hour:
        "Yes"
        if 9 <= hour < 18
        else "No"
)


# ============================================================
# 7. UNAUTHORIZED ACCESS FLAG
# ============================================================

print("Creating Unauthorized_Access flag...")

df["Unauthorized_Access"] = (
    df["Authorization_Status"]
    .str.lower()
    .eq("unauthorized")
    .astype(int)
)


# ============================================================
# 8. SECURITY ALERT FLAG
# ============================================================

print("Creating Security_Alert_Flag...")

df["Security_Alert_Flag"] = (
    df["Security_Alert"]
    .str.lower()
    .eq("yes")
    .astype(int)
)


# ============================================================
# 9. INCIDENT FLAG
# ============================================================

print("Creating Incident_Flag...")

df["Incident_Flag"] = (
    df["Incident_Detected"]
    .str.lower()
    .eq("yes")
    .astype(int)
)


# ============================================================
# 10. CCTV ISSUE FLAG
# ============================================================

print("Creating CCTV_Issue_Flag...")

df["CCTV_Issue_Flag"] = (
    df["CCTV_Status"]
    .str.lower()
    .isin(["unusual", "offline"])
    .astype(int)
)


# ============================================================
# 11. HIGH RISK FLAG
# ============================================================

print("Creating High_Risk_Flag...")

df["High_Risk_Flag"] = (
    df["Risk_Level"]
    .str.lower()
    .isin(["high", "critical"])
    .astype(int)
)


# ============================================================
# 12. SECURITY EVENT SCORE
# ============================================================

print("Creating Security_Event_Score...")

df["Security_Event_Score"] = (
    df["Unauthorized_Access"]
    + df["Security_Alert_Flag"]
    + df["Incident_Flag"]
    + df["CCTV_Issue_Flag"]
    + df["High_Risk_Flag"]
)


# ============================================================
# 13. SECURITY STATUS
# ============================================================

print("Creating Security_Status...")

def calculate_security_status(row):

    score = row["Security_Event_Score"]

    if score >= 4:
        return "Critical"

    elif score >= 2:
        return "Warning"

    elif score == 1:
        return "Monitoring"

    else:
        return "Normal"


df["Security_Status"] = df.apply(
    calculate_security_status,
    axis=1
)


# ============================================================
# 14. REMOVE INVALID TIMESTAMP RECORDS
# ============================================================

before = len(df)

df = df.dropna(
    subset=["Timestamp"]
)

removed = before - len(df)

print(
    f"\nInvalid timestamp records removed: {removed}"
)


# ============================================================
# 15. SORT DATA
# ============================================================

df = df.sort_values(
    by="Timestamp"
).reset_index(
    drop=True
)


# ============================================================
# 16. SAVE PROCESSED DATA
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 17. DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("PREPROCESSING COMPLETED")
print("=" * 60)

print(f"\nProcessed rows    : {len(df)}")
print(f"Processed columns : {len(df.columns)}")

print("\nNew Features:")
print("- Hour")
print("- Day")
print("- Day_of_Week")
print("- Month")
print("- Date")
print("- Working_Hours")
print("- Unauthorized_Access")
print("- Security_Alert_Flag")
print("- Incident_Flag")
print("- CCTV_Issue_Flag")
print("- High_Risk_Flag")
print("- Security_Event_Score")
print("- Security_Status")


# ============================================================
# 18. SECURITY SUMMARY
# ============================================================

print("\nSECURITY SUMMARY")
print("-" * 60)

print(
    "Unauthorized Access:",
    df["Unauthorized_Access"].sum()
)

print(
    "Security Alerts:",
    df["Security_Alert_Flag"].sum()
)

print(
    "Incidents Detected:",
    df["Incident_Flag"].sum()
)

print(
    "CCTV Issues:",
    df["CCTV_Issue_Flag"].sum()
)

print(
    "High/Critical Risk:",
    df["High_Risk_Flag"].sum()
)


# ============================================================
# 19. STATUS DISTRIBUTION
# ============================================================

print("\nSecurity Status Distribution:")
print(
    df["Security_Status"]
    .value_counts()
)


# ============================================================
# 20. OUTPUT LOCATION
# ============================================================

print("\nProcessed dataset saved at:")

print(OUTPUT_FILE)

print("\n" + "=" * 60)
print("STATUS: SECURITY DATA READY FOR ANALYSIS")
print("=" * 60)