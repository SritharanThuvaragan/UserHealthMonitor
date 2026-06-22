# ml/training/train.py
"""Train RandomForest classifiers for the UserHealthMonitor project.

The script expects the processed CSV files in `dataset/processed/`:
- `<split>_train_features.csv`
- `<split>_train_labels.csv`
- `<split>_test_features.csv`
- `<split>_test_labels.csv`

It trains a `RandomForestClassifier`, evaluates accuracy on the test set,
and saves the trained model to `ml/models/<split>_model.pkl`.

Usage (from project root):
    python ml/training/train.py [posture|behaviour]
"""

import os
import sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data(split_name: str, root: str):
    train_X_path = os.path.join(root, f"{split_name}_train_features.csv")
    train_y_path = os.path.join(root, f"{split_name}_train_labels.csv")
    test_X_path = os.path.join(root, f"{split_name}_test_features.csv")
    test_y_path = os.path.join(root, f"{split_name}_test_labels.csv")

    X_train = pd.read_csv(train_X_path)
    y_train = pd.read_csv(train_y_path).squeeze()
    X_test = pd.read_csv(test_X_path)
    y_test = pd.read_csv(test_y_path).squeeze()
    return X_train, y_train, X_test, y_test

def train_and_save(split_name: str, processed_root: str, model_dir: str):
    X_train, y_train, X_test, y_test = load_data(split_name, processed_root)

    clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"{split_name.capitalize()} model accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred, zero_division=0))

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, f"{split_name}_model.pkl")
    import joblib
    joblib.dump(clf, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"posture", "behaviour"}:
        print("Usage: python ml/training/train.py [posture|behaviour]")
        sys.exit(1)
    split = sys.argv[1]
    processed_root = os.path.join(os.getcwd(), "dataset", "processed")
    model_dir = os.path.join(os.getcwd(), "ml", "models")
    train_and_save(split, processed_root, model_dir)
