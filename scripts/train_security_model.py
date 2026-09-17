# ============================================================
# SECURITY AGENT - MODEL TRAINING
# Smart Facility Operations and Optimization
# ============================================================

import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# ============================================================
# 1. FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "security_processed.csv"
)

MODEL_DIR = (
    BASE_DIR
    / "models"
)

MODEL_FILE = (
    MODEL_DIR
    / "security_model.pkl"
)

ENCODER_FILE = (
    MODEL_DIR
    / "security_label_encoder.pkl"
)


# ============================================================
# 2. CREATE MODEL DIRECTORY
# ============================================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 3. LOAD PROCESSED DATA
# ============================================================

print("=" * 65)
print("SECURITY AGENT - MODEL TRAINING")
print("=" * 65)

print("\nLoading processed security dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")


# ============================================================
# 4. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "Unauthorized_Access",
    "Security_Alert_Flag",
    "Incident_Flag",
    "CCTV_Issue_Flag",
    "High_Risk_Flag",
    "Security_Status"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    print("\nERROR: Required columns are missing:")

    for column in missing_columns:
        print("-", column)

    raise ValueError(
        "Required columns are missing from the processed dataset."
    )


# ============================================================
# 5. SELECT FEATURES
# ============================================================

print("\nSelecting security features...")

features = [
    "Unauthorized_Access",
    "Security_Alert_Flag",
    "Incident_Flag",
    "CCTV_Issue_Flag",
    "High_Risk_Flag",
    "Access_Duration_Min"
]

X = df[features]

y = df["Security_Status"]


# ============================================================
# 6. ENCODE TARGET LABELS
# ============================================================

print("\nEncoding Security_Status labels...")

label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)

print("\nSecurity Classes:")

for number, label in enumerate(
    label_encoder.classes_
):

    print(
        f"{number} = {label}"
    )


# ============================================================
# 7. TRAIN TEST SPLIT
# ============================================================

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)

print(f"Training records : {len(X_train)}")
print(f"Testing records  : {len(X_test)}")


# ============================================================
# 8. CREATE RANDOM FOREST MODEL
# ============================================================

print("\nCreating Random Forest model...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


# ============================================================
# 9. TRAIN MODEL
# ============================================================

print("Training Security Agent model...")

model.fit(
    X_train,
    y_train
)

print("Model training completed.")


# ============================================================
# 10. MAKE PREDICTIONS
# ============================================================

print("\nGenerating predictions...")

y_pred = model.predict(
    X_test
)


# ============================================================
# 11. MODEL EVALUATION
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)


# ============================================================
# 12. DISPLAY PERFORMANCE
# ============================================================

print("\n" + "=" * 65)
print("SECURITY AGENT MODEL PERFORMANCE")
print("=" * 65)

print(
    f"\nAccuracy  : {accuracy * 100:.2f}%"
)

print(
    f"Precision : {precision * 100:.2f}%"
)

print(
    f"Recall    : {recall * 100:.2f}%"
)

print(
    f"F1-Score  : {f1 * 100:.2f}%"
)


# ============================================================
# 13. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix:")
print(cm)


# ============================================================
# 14. CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_,
        zero_division=0
    )
)


# ============================================================
# 15. FEATURE IMPORTANCE
# ============================================================

print("\n" + "=" * 65)
print("FEATURE IMPORTANCE")
print("=" * 65)

importance = pd.DataFrame(
    {
        "Feature": features,
        "Importance": model.feature_importances_
    }
)

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

for _, row in importance.iterrows():

    print(
        f"{row['Feature']:<25} "
        f"{row['Importance']:.4f}"
    )


# ============================================================
# 16. SECURITY THRESHOLD
# ============================================================

print("\n" + "=" * 65)
print("SECURITY EVENT THRESHOLD")
print("=" * 65)

print(
    "\nSecurity Event Score is calculated from 5 security indicators:"
)

print(
    "Unauthorized Access"
)

print(
    "Security Alert"
)

print(
    "Incident Detected"
)

print(
    "CCTV Issue"
)

print(
    "High/Critical Risk"
)

print("\nThreshold interpretation:")

print(
    "Score 0  -> Normal"
)

print(
    "Score 1  -> Monitoring"
)

print(
    "Score 2-3 -> Warning"
)

print(
    "Score 4-5 -> Critical"
)


# ============================================================
# 17. SECURITY STATUS COUNTS
# ============================================================

print("\n" + "=" * 65)
print("SECURITY STATUS DISTRIBUTION")
print("=" * 65)

status_counts = df[
    "Security_Status"
].value_counts()

print(
    status_counts
)


# ============================================================
# 18. SAVE MODEL
# ============================================================

print("\nSaving trained model...")

joblib.dump(
    model,
    MODEL_FILE
)

joblib.dump(
    label_encoder,
    ENCODER_FILE
)


# ============================================================
# 19. SAVE FEATURE IMPORTANCE
# ============================================================

importance_file = (
    BASE_DIR
    / "data"
    / "processed"
    / "security_feature_importance.csv"
)

importance.to_csv(
    importance_file,
    index=False
)


# ============================================================
# 20. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 65)
print("SECURITY AGENT MODEL TRAINING COMPLETED")
print("=" * 65)

print(
    f"\nModel saved at:"
)

print(
    MODEL_FILE
)

print(
    f"\nLabel encoder saved at:"
)

print(
    ENCODER_FILE
)

print(
    f"\nFeature importance saved at:"
)

print(
    importance_file
)

print("\nSTATUS: SECURITY MODEL READY")
print("=" * 65)