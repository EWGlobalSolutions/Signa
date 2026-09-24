"""Step 3 -- live sign recognition from your webcam.

Keeps a sliding window of the last 45 frames, classifies it a few times
per second, and smooths the output with a majority vote so the gloss
doesn't flicker. The current prediction is drawn on the video, and every
*confirmed* prediction is appended to gloss_stream.jsonl:

    {"t": 1727..., "gloss": "HELLO", "confidence": 92.4}

That file is the "translation service" your Signa front-end would read
instead of its simulated glosses -- it's the seam between this starter
and the demo I built for Mimo.
"""

import json
import time
from collections import Counter, deque

import cv2
import joblib
import numpy as np

from config import CAM_INDEX, GLOSS_STREAM, MODEL_PATH, SEQ_LEN
from landmarks import frame_to_features, make_detectors

PREDICT_EVERY = 10   # classify every N frames (~3x/sec at 30 fps)
VOTE_WINDOW = 7      # majority vote over this many predictions
VOTE_MIN = 4         # votes needed before we "confirm" a gloss


def main():
    bundle = joblib.load(MODEL_PATH)
    model, scaler, labels = bundle["model"], bundle["scaler"], bundle["labels"]

    hands = make_detectors()
    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        raise SystemExit("Could not open webcam. Check CAM_INDEX in config.py.")

    window = deque(maxlen=SEQ_LEN)    # recent landmark frames
    present = deque(maxlen=SEQ_LEN)   # was a hand visible in each frame?
    votes = deque(maxlen=VOTE_WINDOW)
    gloss, confidence = "...", 0.0
    tick = 0
    stream = open(GLOSS_STREAM, "a")

    print("Live recognition running -- perform one of:", ", ".join(labels))
    print("Press 'q' in the video window to quit.\n")
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            feats = frame_to_features(frame, hands)
            window.append(feats)
            present.append(1 if feats.any() else 0)
            tick += 1

            # Only predict on a full window where hands were mostly visible.
            if len(window) == SEQ_LEN and tick % PREDICT_EVERY == 0 \
                    and sum(present) > SEQ_LEN // 2:
                seq = np.stack(window)
                x = scaler.transform(
                    np.concatenate([seq.mean(axis=0), seq.std(axis=0)])[None, :])
                proba = model.predict_proba(x)[0]
                best = int(np.argmax(proba))
                votes.append(labels[best])
                top, count = Counter(votes).most_common(1)[0]
                if count >= VOTE_MIN and (top != gloss or True):
                    if top != gloss:
                        gloss, confidence = top, float(proba[best])
                        stream.write(json.dumps({
                            "t": time.time(),
                            "gloss": top,
                            "confidence": round(confidence * 100, 1),
                        }) + "\n")
                        stream.flush()
                        print(f"  -> {top}  ({confidence * 100:.0f}%)")

            cv2.putText(frame, f"{gloss} ({confidence * 100:.0f}%)",
                        (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1.2, (0, 255, 0), 3)
            cv2.imshow("signa live  (q quits)", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        stream.close()
        cap.release()
        cv2.destroyAllWindows()

    print(f"\nPredictions logged to {GLOSS_STREAM}")


if __name__ == "__main__":
    main()
