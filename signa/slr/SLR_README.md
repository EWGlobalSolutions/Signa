# Signa SLR Starter — webcam sign recognition with MediaPipe

A minimal, learnable pipeline that turns hand movements into text glosses:

```
webcam → MediaPipe hand landmarks → normalized features → classifier → gloss
```

This is the "translation service" your Signa front-end was designed to
plug into. The React demo used simulated glosses; this replaces them
with real predictions from your own camera.

## Setup (laptop / desktop — not Mimo)

You need Python 3.9–3.11 (MediaPipe wheels don't cover every version).

```bash
cd signa_slr_starter
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Workflow

**1. Collect samples** — record yourself performing each sign:

```bash
python collect.py
```

Aim for 10+ samples per sign. Vary your position, speed, lighting, and
background a bit — a model trained on identical repetitions only learns
your exact setup.

**2. Train:**

```bash
python train.py
```

Prints an accuracy report and saves `model/slr_model.pkl`.

**3. Go live:**

```bash
python live.py
```

Perform a sign. The prediction appears on the video and is appended to
`gloss_stream.jsonl` — one JSON object per line:

```json
{"t": 1727222400.0, "gloss": "HELLO", "confidence": 92.4}
```

## Connecting it to the Signa demo

`gloss_stream.jsonl` is the seam between the two projects. Where the
front-end currently renders its mock `sign` gloss per transcript segment,
read the latest line of this file instead and render *that* gloss with
its confidence. Same panel, real data.

## How it works (the 30-second version)

- `landmarks.py` — MediaPipe finds up to 2 hands per frame (21 landmarks
  each). Each hand is re-centered on its wrist and scaled by hand size,
  so the features describe hand *shape*, not where the hand sits in frame.
- `collect.py` — records 45-frame (~1.5 s) landmark sequences per sign.
- `train.py` — compresses each sequence to mean+std per coordinate, then
  trains a Random Forest. Simple, fast, works on tiny datasets.
- `live.py` — classifies a sliding 45-frame window ~3x/second and
  majority-votes over recent predictions so the output doesn't flicker.

## Troubleshooting

- **Webcam won't open** → try `CAM_INDEX = 1` in `config.py`.
- **"No module named mediapipe"** → check your Python version is 3.9–3.11
  and that you installed inside the venv.
- **Everything predicts one sign** → you need more varied samples; also
  check your signs are visually distinct (YES vs NO can be tricky).
- **Jittery predictions** → raise `VOTE_MIN` in `live.py`, or slow down
  your signing so each sign fills the 1.5 s window.

## Where to go next

- More signs, more samples (accuracy scales with data, not code).
- Try an LSTM/Transformer on the raw sequences instead of mean+std.
- Benchmark against the public WLASL dataset (2,000 ASL signs).
- Continuous signing (sentence-level) is the real research frontier —
  start with isolated signs, which is what this starter does.
