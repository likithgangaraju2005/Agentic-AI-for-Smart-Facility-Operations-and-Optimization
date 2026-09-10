import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "occupancy",
    "processed",
    "occupancy_processed.csv"
)

MODEL_DIR = os.path.join(BASE_DIR, "models")

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "occupancy",
    "processed",
    "occupancy_model_predictions.csv"
)

MODEL_FILE = os.path.join(
    MODEL_DIR,
    "occupancy_model.pkl"
)

os.makedirs(MODEL_DIR, exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

print("=" * 60)
print("OCCUPANCY ML MODEL")
print("=" * 60)

print("\nLoading processed occupancy dataset...")

df = pd.read_csv(INPUT_FILE)

print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# 3. PREPARE FEATURES
# ============================================================

print("\nPreparing features...")

# Convert timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Numerical features used by the model
features = [
    "Floor",
    "Room_Capacity",
    "Temperature_C",
    "Humidity_Percent",
    "Working_Hours",
    "Day_of_Week_Num",
    "Hour",
    "Minute",
    "Is_Weekend"
]

target = "Occupancy_Count"


# Make sure required columns exist
missing_features = [col for col in features if col not in df.columns]

if missing_features:
    print("\nERROR: Missing columns:")
    print(missing_features)
    raise ValueError("Required features are missing from the dataset.")


# Remove rows with missing values
model_data = df[features + [target]].dropna()

X = model_data[features]
y = model_data[target]


print("\nFeatures used:")
for feature in features:
    print("-", feature)

print("\nTarget:")
print("-", target)

print("\nTraining records:", len(model_data))


# ============================================================
# 4. TRAIN / TEST SPLIT
# ============================================================

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("Training records:", len(X_train))
print("Testing records :", len(X_test))


# ============================================================
# 5. TRAIN RANDOM FOREST MODEL
# ============================================================

print("\nTraining Random Forest model...")

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Model training completed.")


# ============================================================
# 6. MODEL EVALUATION
# ============================================================

print("\nEvaluating model...")

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")

print("=" * 60)


# ============================================================
# 7. PREDICT OCCUPANCY FOR ALL RECORDS
# ============================================================

print("\nGenerating occupancy predictions...")

df["Predicted_Occupancy"] = model.predict(
    df[features]
)


# ============================================================
# 8. CALCULATE PREDICTED UTILIZATION
# ============================================================

df["Predicted_Utilization_Percent"] = (
    df["Predicted_Occupancy"] /
    df["Room_Capacity"]
) * 100


# ============================================================
# 9. PREDICTED OCCUPANCY STATUS
# ============================================================

def get_status(utilization):
    if utilization > 120:
        return "Critical"
    elif utilization > 110:
        return "High"
    elif utilization > 100:
        return "Overcrowded"
    elif utilization >= 70:
        return "High Usage"
    elif utilization >= 40:
        return "Normal"
    else:
        return "Low"


df["Predicted_Occupancy_Status"] = (
    df["Predicted_Utilization_Percent"]
    .apply(get_status)
)


# ============================================================
# 10. PREDICTION ERROR
# ============================================================

df["Prediction_Error"] = (
    df["Occupancy_Count"] -
    df["Predicted_Occupancy"]
).abs()


# ============================================================
# 11. SAVE PREDICTIONS
# ============================================================

output_columns = [
    "Timestamp",
    "Building_ID",
    "Floor",
    "Room_ID",
    "Room_Type",
    "Room_Capacity",
    "Occupancy_Count",
    "Predicted_Occupancy",
    "Predicted_Utilization_Percent",
    "Predicted_Occupancy_Status",
    "Prediction_Error"
]

prediction_df = df[output_columns]

prediction_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 12. SAVE MODEL
# ============================================================

joblib.dump(model, MODEL_FILE)


# ============================================================
# 13. SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("OCCUPANCY ML MODEL COMPLETED")
print("=" * 60)

print("\nModel type:")
print("Random Forest Regression")

print("\nModel file:")
print(MODEL_FILE)

print("\nPrediction file:")
print(OUTPUT_FILE)

print("\nPrediction status distribution:")
print(
    prediction_df["Predicted_Occupancy_Status"]
    .value_counts()
)

print("\nSample predictions:")
print(
    prediction_df[
        [
            "Building_ID",
            "Room_ID",
            "Occupancy_Count",
            "Predicted_Occupancy",
            "Predicted_Utilization_Percent",
            "Predicted_Occupancy_Status"
        ]
    ].head(10)
)

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)