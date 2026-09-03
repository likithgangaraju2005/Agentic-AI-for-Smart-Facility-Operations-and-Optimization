import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

print("=" * 60)
print("MAINTENANCE FAILURE PREDICTION")
print("=" * 60)

# ---------------------------------------------------------
# 1. Load processed maintenance data
# ---------------------------------------------------------

input_file = "data/maintenance/processed/maintenance_health_scores.csv"

if not os.path.exists(input_file):
    print(f"ERROR: File not found: {input_file}")
    exit()

df = pd.read_csv(input_file)

print(f"\nRecords loaded: {len(df)}")

# ---------------------------------------------------------
# 2. Select features
# ---------------------------------------------------------

features = [
    "Ambient_Temperature_C",
    "Equipment_Temperature_C",
    "Vibration_mm_s",
    "Pressure_bar",
    "Power_Consumption_kW",
    "Load_Percent",
    "Oil_Temperature_C",
    "Operating_Hours",
    "Age_Years",
    "Maintenance_Count",
    "Days_Since_Maintenance",
    "Historical_Failure_Count",
    "Hour",
    "Day",
    "Day_of_Week",
    "Working_Hours",
    "Temperature_Difference_C",
    "Equipment_Stress",
    "Maintenance_Urgency",
    "High_Temperature",
    "High_Vibration",
    "Equipment_Health_Score"
]

target = "Failure_Within_7_Days"

# Check columns
missing_features = [col for col in features if col not in df.columns]

if missing_features:
    print("\nMissing features:")
    for col in missing_features:
        print("-", col)
    exit()

# ---------------------------------------------------------
# 3. Prepare data
# ---------------------------------------------------------

X = df[features]
y = df[target]

print("\nTarget distribution:")
print(y.value_counts())

# ---------------------------------------------------------
# 4. Train-test split
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"\nTraining records: {len(X_train)}")
print(f"Testing records: {len(X_test)}")

# ---------------------------------------------------------
# 5. Train Random Forest model
# ---------------------------------------------------------

print("\nTraining Random Forest model...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_split=4,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

print("Model training completed ✓")

# ---------------------------------------------------------
# 6. Predictions
# ---------------------------------------------------------

y_probability = model.predict_proba(X_test)[:, 1]

# Use 0.40 threshold
threshold = 0.40

y_pred = (y_probability >= threshold).astype(int)

# ---------------------------------------------------------
# 7. Model evaluation
# ---------------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
roc_auc = roc_auc_score(y_test, y_probability)

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(f"Accuracy  : {accuracy * 100:.2f}%")
print(f"Precision : {precision * 100:.2f}%")
print(f"Recall    : {recall * 100:.2f}%")
print(f"F1 Score  : {f1 * 100:.2f}%")
print(f"ROC-AUC   : {roc_auc:.4f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# ---------------------------------------------------------
# 8. Generate predictions for ALL records
# ---------------------------------------------------------

df["Failure_Probability"] = model.predict_proba(X)[:, 1]

df["Failure_Risk_Percent"] = (
    df["Failure_Probability"] * 100
).round(2)

# ---------------------------------------------------------
# 9. Risk level
# ---------------------------------------------------------

def risk_level(probability):

    if probability >= 0.70:
        return "High"

    elif probability >= 0.40:
        return "Medium"

    else:
        return "Low"


df["Failure_Risk_Level"] = df["Failure_Probability"].apply(risk_level)

# ---------------------------------------------------------
# 10. Maintenance alerts
# ---------------------------------------------------------

def maintenance_alert(row):

    probability = row["Failure_Probability"]
    health = row["Equipment_Health_Score"]

    if probability >= 0.70 or health < 30:
        return "URGENT - Immediate maintenance required"

    elif probability >= 0.40 or health < 50:
        return "WARNING - Schedule maintenance soon"

    elif probability >= 0.25 or health < 65:
        return "CAUTION - Monitor equipment"

    else:
        return "NORMAL - No immediate action"


df["Maintenance_Alert"] = df.apply(
    maintenance_alert,
    axis=1
)

# ---------------------------------------------------------
# 11. Save predictions
# ---------------------------------------------------------

output_file = (
    "data/maintenance/processed/maintenance_predictions.csv"
)

df.to_csv(output_file, index=False)

# ---------------------------------------------------------
# 12. Save model
# ---------------------------------------------------------

model_file = "models/maintenance_model.pkl"

os.makedirs("models", exist_ok=True)

joblib.dump(model, model_file)

# ---------------------------------------------------------
# 13. Summary
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("PREDICTION SUMMARY")
print("=" * 60)

print("\nFailure Risk Level:")
print(df["Failure_Risk_Level"].value_counts())

print("\nMaintenance Alerts:")
print(df["Maintenance_Alert"].value_counts())

print("\nPredicted failures:")
print((df["Failure_Probability"] >= threshold).sum())

print(f"\nPredictions saved to:")
print(os.path.abspath(output_file))

print(f"\nModel saved to:")
print(os.path.abspath(model_file))

print("\n" + "=" * 60)
print("MAINTENANCE PREDICTION COMPLETED ✓")
print("=" * 60)
