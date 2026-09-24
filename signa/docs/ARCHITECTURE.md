# Architecture

## The big picture

Signa is two systems joined by a file:

```
┌─────────────────────┐      gloss_stream.jsonl      ┌──────────────────────┐
│   slr/  (vision)    │  ────  {"t","gloss", ─────▶  │  frontend/  (player) │
│ webcam → landmarks  │       "confidence"}          │  captions · glosses  │
│ → classifier        │                              │  transcript seeking │
└─────────────────────┘                              └──────────────────────┘
```

Today the frontend renders **simulated** glosses from `frontend/src/main.jsx`
(the `transcript` array). The vision pipeline is real but young (5 signs).
Connecting them — reading the latest line of `gloss_stream.jsonl` into the
translation panel — is the headline "wire it up live" roadmap item.

## Vision pipeline (`slr/`)

1. **Landmarks** (`landmarks.py`) — MediaPipe Hands extracts 21 landmarks
   for up to 2 hands per frame → 126-dim vector per frame. Missing hands
   are zero-filled so the shape never changes.
2. **Normalization** — each hand is re-centered on its wrist and divided
   by hand size (wrist → middle-finger base). This makes features describe
   hand *shape*, invariant to where the hand is in frame or how close the
   camera is.
3. **Windowing** — 45 frames (~1.5 s) per sample. For live inference a
   sliding window is classified ~3×/second.
4. **Features** (`train.py`) — per-coordinate mean + standard deviation
   over the window → 252 features. Deliberately simple: it works on tiny
   datasets and trains in seconds.
5. **Model** — Random Forest (300 trees) on standardized features. Chosen
   for small-data robustness, not peak accuracy. The obvious upgrade path
   is an LSTM/Transformer trained on raw sequences.
6. **Smoothing** (`live.py`) — majority vote over the last 7 predictions
   (needs 4/7 agreement) so the displayed gloss doesn't flicker.

## Player (`frontend/`)

React + Vite. Key pieces for collaborators:

- `src/main.jsx` — all UI state; the `transcript` array is the mock data
  to replace with the live gloss stream.
- Language switcher (ASL/BSL/Auslan/ISL) and captions/translation toggles
  are UI-complete and just need real data behind them.

## Console demo (`python-demo/`)

`signa_demo.py` is a faithful port of the player UI to a single Python
file — same transcript, same toggles, same language switcher — for
environments without a browser (e.g. mobile coding apps). Useful as a
spec: if a feature isn't in the console demo, it isn't in the product.

## Data honesty

Demo glosses are placeholders. Any claim about a real sign language must
come from native-signer data or a cited dataset (e.g. WLASL). Don't
invent linguistic data and don't present the starter's 5-sign vocabulary
as coverage of a language.
