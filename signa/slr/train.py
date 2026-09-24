"""Step 2 -- train the sign classifier on your collected samples.

Each sample is a (45, 126) sequence of hand landmarks. We compress it to
a fixed-size feature vector (per-coordinate mean + std over time), then
train a Random Forest. Small data + simple model = trains in seconds
and is hard to overfit catastrophically while you're experimenting.

Saves model/slr_model.pkl  (classifier + scaler + label list).
"""

import glob
import os

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from config import DATA_DIR, MODEL_PATH, SIGNS


def sequence_features(seq):
    """(T, 126) -> 252 features: mean and std of each coordinate over time.

    Signs are *movements*, so summarizing how each landmark moves
    (average position + how much it varies) captures a lot with very
    little data.
    """
    return np.concatenate([seq.mean(axis=0), seq.std(axis=0)])


def main():
    X, y = [], []
    for sign in SIGNS:
        paths = glob.glob(os.path.join(DATA_DIR, sign, "*.npy"))
        for path in paths:
            X.append(sequence_features(np.load(path)))
            y.append(sign)
        print(f"  {sign}: {len(paths)} samples")

    X = np.array(X)
    y = np.array(y)
    if len(X) < 10:
        print(f"\nOnly {len(X)} samples total -- collect more for a useful model.")
        print("Aim for at least ~10 samples per sign, then re-run.")
        return

    # Stratify only when every class has 2+ samples, else plain split.
    stratify = y if min(np.bincount(
        [SIGNS.index(s) for s in y])) >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=7, stratify=stratify
    )

    scaler = StandardScaler().fit(X_train)
    clf = RandomForestClassifier(n_estimators=300, random_state=7, n_jobs=-1)
    clf.fit(scaler.transform(X_train), y_train)

    print("\n--- test set report ---")
    print(classification_report(y_test, clf.predict(scaler.transform(X_test))))

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({"model": clf, "scaler": scaler, "labels": SIGNS}, MODEL_PATH)
    print(f"Saved {MODEL_PATH}")
    print("Next:  python live.py")


if __name__ == "__main__":
    main()
