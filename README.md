# signa — live sign-language translation for video

![signa banner](docs/banner.webp)

Signa is an accessibility-first video player with a **real-time sign-language
translation layer**. Watch a video, and alongside captions you get a live
interpretation panel — switchable between sign languages — driven by a
computer-vision pipeline that reads hand movements and emits text glosses.

> **Status: early prototype, collaborators welcome.**
> The player UI works today. The translation layer runs on a starter
> recognizer (5-sign vocabulary, webcam). The roadmap below is where you
> come in — see [CONTRIBUTING.md](CONTRIBUTING.md).

## How it works

```
video frame
   │  MediaPipe hand landmarks (21 pts × 2 hands)
   ▼
normalization → wrist-relative, scale-invariant features
   │  45-frame window → mean + std per coordinate
   ▼
classifier → gloss + confidence
   │  gloss_stream.jsonl   ← the seam between vision and UI
   ▼
player → captions · translation layer · transcript seeking
```

Details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## What's in this repo

| Folder | What it is | Runs on |
|---|---|---|
| `frontend/` | React + Vite viewer: video player, transcript seeking, captions & translation toggles, ASL/BSL/Auslan/ISL switcher | any browser |
| `slr/` | MediaPipe starter pipeline: `collect.py` → `train.py` → `live.py` webcam recognition | laptop, Python 3.9–3.11 |
| `python-demo/` | Console port of the player UI (`signa_demo.py`) — runs anywhere Python runs, including mobile coding apps | anywhere |

## Quickstart

**Player UI (browser):**
```bash
cd frontend
npm install
npm run dev
```

**Console demo (any Python):**
```bash
python3 python-demo/signa_demo.py
# try: play, 3, lang, captions, sign, video, help, quit
```

**Train your own recognizer (laptop + webcam):**
```bash
cd slr
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python collect.py   # record yourself signing (10+ samples per sign)
python train.py     # trains in seconds, prints an accuracy report
python live.py      # real-time glosses → gloss_stream.jsonl
```

## Roadmap — pick something and run with it

- [ ] **Bigger vocabulary** — grow past the 5 starter signs. Good first issue: add *your* sign, with samples.
- [ ] **Better models** — swap the Random Forest for an LSTM/Transformer on raw landmark sequences.
- [ ] **Benchmark** — evaluate against the public WLASL dataset (2,000 ASL signs).
- [ ] **Wire it up live** — feed `gloss_stream.jsonl` into the React translation panel in real time (the intended end-to-end demo).
- [ ] **Continuous signing** — move from isolated signs to sentence-level recognition (the real research frontier).
- [ ] **On-device** — port inference to TensorFlow Lite / mobile.
- [ ] **More languages** — BSL/Auslan/ISL data collection and models.

Have another idea? Open a feature request — see [CONTRIBUTING.md](CONTRIBUTING.md).

## Contributing

We welcome contributors of all levels — including people learning to code.
Start with [CONTRIBUTING.md](CONTRIBUTING.md), grab a `good first issue`,
and say hello in your PR.

## License

MIT — see [LICENSE](LICENSE). Build something good with it.
