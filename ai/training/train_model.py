import os

import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# ============================================================
# RYGAR SENTINEL - AI MODEL TRAINING
# ============================================================

DATA_FILE = os.path.expanduser(
    "~/rygar-ai/normal_data.csv"
)

MODEL_DIR = os.path.expanduser(
    "~/rygar-ai/model"
)

MODEL_FILE = os.path.join(
    MODEL_DIR,
    "isolation_forest.joblib"
)

SCALER_FILE = os.path.join(
    MODEL_DIR,
    "scaler.joblib"
)


FEATURES = [
    "temperature",
    "humidity",
    "mq2",
    "mq135",
    "water",
    "acs",
    "pir1",
    "pir2",
    "parking1",
    "parking2",
    "fire",
    "buzzer",
    "fan",
    "light"
]


print("============================================")
print(" RYGAR SENTINEL - AI MODEL TRAINING")
print("============================================")


if not os.path.exists(DATA_FILE):

    raise FileNotFoundError(
        f"Training data not found: {DATA_FILE}"
    )


data = pd.read_csv(DATA_FILE)

print(
    "Samples:",
    len(data)
)


X = data[FEATURES]


# ============================================================
# SCALE FEATURES
# ============================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ============================================================
# ISOLATION FOREST
# ============================================================

model = IsolationForest(
    n_estimators=150,
    contamination=0.05,
    random_state=42
)

model.fit(X_scaled)


# ============================================================
# SAVE
# ============================================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_FILE
)

joblib.dump(
    scaler,
    SCALER_FILE
)


print()
print("MODEL TRAINING COMPLETE")

print(
    "Model:",
    MODEL_FILE
)

print(
    "Scaler:",
    SCALER_FILE
)