# ml/training/preprocess_all.py
"""Convenient wrapper to run the full preprocessing pipeline for all datasets.

Running this script will invoke `ml/training/preprocessing.py`, which loads and processes:
- Posture data
- Behaviour data
- Eye (drowsiness) images
- Lighting images

It saves the processed CSV splits and scalers under `dataset/processed/`.

Usage:
    python d:/Research/UserHealthMonitor/ml/training/preprocess_all.py
"""

import os
import sys

# Ensure the script is executed from the project root or adjust paths accordingly
script_dir = os.path.dirname(__file__)
preprocess_path = os.path.join(script_dir, "preprocessing.py")

if not os.path.isfile(preprocess_path):
    print(f"Error: preprocessing script not found at {preprocess_path}", file=sys.stderr)
    sys.exit(1)

# Import and run the main function of the preprocessing script
# Adding the script directory to sys.path allows for direct import
sys.path.append(script_dir)
from preprocessing import main as preprocess_main

if __name__ == "__main__":
    preprocess_main()
