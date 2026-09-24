"""Step 1 -- record labeled training samples from your webcam.

For each sign you'll be asked how many samples to record, then press
Enter and perform the sign while the script records ~1.5 seconds of
hand landmarks. Samples are saved as .npy files under data/<SIGN>/.

Tip: vary your position, speed, and background a little between samples.
A model trained on identical repetitions only learns your exact setup.
"""

import os
import time

import cv2

from config import CAM_INDEX, DATA_DIR, SEQ_LEN, SIGNS
from landmarks import frame_to_features, make_detectors


def record_sample(cap, hands, sign, i, n):
    input(f"  Sample {i + 1}/{n} for '{sign}': get ready, press Enter...")
    print("  Recording -- perform the sign now!")
    frames = []
    while len(frames) < SEQ_LEN:
        ok, frame = cap.read()
        if not ok:
            break
        frames.append(frame_to_features(frame, hands))
        cv2.imshow("collect  (q quits)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            return None
    return frames


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    hands = make_detectors()
    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        raise SystemExit("Could not open webcam. Check CAM_INDEX in config.py.")

    try:
        for sign in SIGNS:
            print(f"\n=== Sign: {sign} ===")
            raw = input(f"  How many samples for '{sign}'? (0 skips) [5]: ").strip()
            n = int(raw) if raw.isdigit() else 5
            if n <= 0:
                continue
            os.makedirs(os.path.join(DATA_DIR, sign), exist_ok=True)
            for i in range(n):
                frames = record_sample(cap, hands, sign, i, n)
                if frames is None:  # user quit with 'q'
                    return
                import numpy as np

                arr = np.stack(frames)
                path = os.path.join(DATA_DIR, sign, f"{int(time.time())}_{i}.npy")
                np.save(path, arr)
                print(f"  Saved {path}  shape={arr.shape}")
    finally:
        cap.release()
        cv2.destroyAllWindows()

    print("\nDone. Next:  python train.py")


if __name__ == "__main__":
    main()
