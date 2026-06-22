# ml/training/preprocessing.py
"""Preprocess raw datasets for the UserHealthMonitor project.

- Reads the posture CSV (Zenodo) and the behaviour CSVs.
- Cleans missing values, encodes categorical columns if any.
- Applies a StandardScaler to numeric feature columns.
- Splits each dataset into train/test (80/20) and saves the splits.
- Persists the fitted scaler for later inference.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def load_posture_data() -> pd.DataFrame:
    """Load the posture CSV from the raw dataset."""
    csv_path = os.path.join(os.getcwd(), "dataset", "raw", "posture", "data.csv")
    return pd.read_csv(csv_path)

# ---------------------------------------------------------------------------
# Additional dataset loaders
# ---------------------------------------------------------------------------

def load_eye_data() -> pd.DataFrame:
    """Load eye‑drowsiness images.
    Traverses ``dataset/raw/eye/train`` expecting subfolders named ``Open`` and ``Closed``.
    Returns a DataFrame with columns ``filepath`` and ``label`` (0=Open, 1=Closed).
    """
    base_dir = os.path.join(os.getcwd(), "dataset", "raw", "eye", "train")
    rows = []
    label_map = {"Open": 0, "Closed": 1}
    for label_name, label_val in label_map.items():
        folder = os.path.join(base_dir, label_name)
        if not os.path.isdir(folder):
            continue
        for root, _, files in os.walk(folder):
            for f in files:
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                    rows.append({"filepath": os.path.join(root, f), "label": label_val})
    return pd.DataFrame(rows)


def load_lighting_data() -> pd.DataFrame:
    """Load lighting images.
    Flattens all image files under ``dataset/raw/lighting`` into a DataFrame.
    No explicit labels are provided; a placeholder column ``label`` is set to 0.
    """
    base_dir = os.path.join(os.getcwd(), "dataset", "raw", "lighting")
    rows = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                rows.append({"filepath": os.path.join(root, f), "label": 0})
    return pd.DataFrame(rows)


def load_behaviour_data() -> pd.DataFrame:
    """Combine all CSV files under ``dataset/raw/behaviour`` into a single DataFrame."""
    behav_dir = os.path.join(os.getcwd(), "dataset", "raw", "behaviour")
    dfs = []
    for fname in os.listdir(behav_dir):
        if fname.lower().endswith('.csv'):
            dfs.append(pd.read_csv(os.path.join(behav_dir, fname)))
    if not dfs:
        raise FileNotFoundError("No behaviour CSV files found in dataset/raw/behaviour")
    return pd.concat(dfs, ignore_index=True)

# ---------------------------------------------------------------------------
# Preprocessing utilities – handle non‑numeric data gracefully
# ---------------------------------------------------------------------------

def preprocess_dataframe(df: pd.DataFrame, target_col: str = None):
    """Clean and scale a DataFrame.
    - Drops rows that are completely empty.
    - Separates ``target_col`` if supplied.
    - For numeric columns, fills missing values with the column mean and applies ``StandardScaler``.
    - If there are no numeric columns, the data is returned unchanged (except for target separation).
    """
    df = df.dropna(how="all").reset_index(drop=True)
    if target_col:
        if target_col in df.columns:
            y = df[target_col]
            X = df.drop(columns=[target_col])
        else:
            y = pd.Series(0, index=df.index, name=target_col)
            X = df
    else:
        y = None
        X = df
    numeric_cols = X.select_dtypes(include=["number"]).columns
    if len(numeric_cols) > 0:
        X[numeric_cols] = X[numeric_cols].fillna(X[numeric_cols].mean())
        scaler = StandardScaler()
        X[numeric_cols] = scaler.fit_transform(X[numeric_cols])
    else:
        scaler = None
    return X, y, scaler


def save_split(X, y, split_name: str, output_root: str):
    """Split data into train/test and save CSV files.
    If ``y`` is ``None`` only the feature matrices are saved.
    """
    ensure_dir(output_root)
    if y is not None:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        X_train.to_csv(os.path.join(output_root, f"{split_name}_train_features.csv"), index=False)
        X_test.to_csv(os.path.join(output_root, f"{split_name}_test_features.csv"), index=False)
        y_train.to_csv(os.path.join(output_root, f"{split_name}_train_labels.csv"), index=False, header=True)
        y_test.to_csv(os.path.join(output_root, f"{split_name}_test_labels.csv"), index=False, header=True)
    else:
        X_train, X_test = train_test_split(
            X, test_size=0.2, random_state=42
        )
        X_train.to_csv(os.path.join(output_root, f"{split_name}_train_features.csv"), index=False)
        X_test.to_csv(os.path.join(output_root, f"{split_name}_test_features.csv"), index=False)


def main():
    processed_root = os.path.join(os.getcwd(), "dataset", "processed")
    ensure_dir(processed_root)

    # Posture dataset
    posture_df = load_posture_data()
    X_posture, y_posture, scaler_posture = preprocess_dataframe(posture_df, target_col="label")
    save_split(X_posture, y_posture, "posture", processed_root)
    if scaler_posture:
        joblib.dump(scaler_posture, os.path.join(processed_root, "posture_scaler.pkl"))
    print("Posture data pre-processed and saved.")

    # Behaviour dataset
    behaviour_df = load_behaviour_data()
    X_behav, y_behav, scaler_behav = preprocess_dataframe(behaviour_df, target_col="label")
    save_split(X_behav, y_behav, "behaviour", processed_root)
    if scaler_behav:
        joblib.dump(scaler_behav, os.path.join(processed_root, "behaviour_scaler.pkl"))
    print("Behaviour data pre-processed and saved.")

    # Eye dataset
    eye_df = load_eye_data()
    X_eye, y_eye, scaler_eye = preprocess_dataframe(eye_df, target_col="label")
    save_split(X_eye, y_eye, "eye", processed_root)
    if scaler_eye:
        joblib.dump(scaler_eye, os.path.join(processed_root, "eye_scaler.pkl"))
    print("Eye data pre-processed and saved.")

    # Lighting dataset
    lighting_df = load_lighting_data()
    X_light, y_light, scaler_light = preprocess_dataframe(lighting_df, target_col="label")
    save_split(X_light, y_light, "lighting", processed_root)
    if scaler_light:
        joblib.dump(scaler_light, os.path.join(processed_root, "lighting_scaler.pkl"))
    print("Lighting data pre-processed and saved.")

if __name__ == "__main__":
    main()
