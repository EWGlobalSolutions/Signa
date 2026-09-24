# Contributing to signa

Thanks for being here — signa only becomes real with collaborators.
All skill levels are welcome, including people learning to code.

## Ways to help (no permission needed to start)

- **Add a sign.** Record samples of a new sign, train, and PR the samples
  + config change. See the roadmap in the README — this is the most
  valuable contribution right now.
- **Improve the recognizer.** Better features, better models, better
  smoothing in `slr/live.py`.
- **Polish the player.** The React UI in `frontend/` has a long list of
  small UX wins (keyboard shortcuts, mobile layout, loading states).
- **Docs & examples.** Tutorials, troubleshooting, translations of the
  README.
- **File issues.** A well-written bug report or feature request is a
  contribution.

Look for issues labeled `good first issue` — they're scoped to be
finishable in an evening.

## Getting set up

**Frontend** — Node 18+:
```bash
cd frontend && npm install && npm run dev
```

**Sign recognition** — Python 3.9–3.11 + webcam:
```bash
cd slr
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python collect.py && python train.py && python live.py
```

**Console demo** — any Python 3:
```bash
python3 python-demo/signa_demo.py
```

## Pull requests

1. Fork, branch (`git checkout -b add-sign-thank-you`), commit, push, PR.
2. Describe *what* and *why*. Screenshots or short clips for UI changes.
3. Keep PRs small — one idea per PR merges faster.
4. Be kind in review, both directions. Assume good intent.

## Ground rules

- This project serves the Deaf and hard-of-hearing community. If a
  change affects accessibility or representation, say so in the PR.
- Demo glosses are placeholders, not linguistic claims — don't present
  invented glosses as real sign-language data. Real data comes from
  native signers and cited datasets.
- MIT license: your contributions are shared under the same terms.

## Questions?

Open an issue with the `question` label — someone will answer.
