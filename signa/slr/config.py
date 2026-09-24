"""Shared settings for the Signa sign-language-recognition starter.

Tweak these, then run:  collect.py -> train.py -> live.py
"""

# The starter vocabulary. Keep it small and visually distinct while
# you're learning -- 5 signs is plenty to prove the pipeline works.
SIGNS = ["HELLO", "THANK-YOU", "YES", "NO", "PLEASE"]

SEQ_LEN = 45          # frames per sample (~1.5 seconds at 30 fps)
CAM_INDEX = 0         # webcam id; try 1 if you have multiple cameras
DATA_DIR = "data"     # collected samples land here: data/<SIGN>/*.npy
MODEL_PATH = "model/slr_model.pkl"
GLOSS_STREAM = "gloss_stream.jsonl"  # live predictions, one JSON object per line
