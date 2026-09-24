"""
signa_demo.py
=============
Signa -- live video translation, rebuilt as a Python console demo.

This is a Python port of the Signa React front-end: a video player with a
real-time sign-language translation layer. Paste it into Mimo's Python
environment and run it.

Try:  play, next, 3, lang, captions, sign, video, help, quit

NOTE: the sign "translations" are simulated demo glosses, not real
linguistic translations. The real product feeds this panel from a
streaming sign-language inference service.
"""

import time

# ----------------------------------------------------------------------
# Demo data
# ----------------------------------------------------------------------

LANGUAGES = ["ASL", "BSL", "Auslan", "ISL"]

VIDEOS = {
    "1": {
        "title": "The small changes that make a big difference",
        "duration": "01:00",
        "segments": [
            {"time": "00:00", "text": "Hello, welcome back.",
             "gloss": {"ASL": "HELLO", "BSL": "HELLO",
                       "Auslan": "HELLO", "ISL": "SHALOM"},
             "confidence": 99},
            {"time": "00:04", "text": "Today we are going to talk about",
             "gloss": {"ASL": "TODAY \u2022 TALK", "BSL": "TODAY \u2022 TALK-ABOUT",
                       "Auslan": "TODAY \u2022 DISCUSS", "ISL": "TODAY \u2022 SPEAK"},
             "confidence": 96},
            {"time": "00:09", "text": "the small changes that make",
             "gloss": {"ASL": "SMALL \u2022 CHANGE", "BSL": "SMALL \u2022 CHANGE",
                       "Auslan": "LITTLE \u2022 CHANGE", "ISL": "SMALL \u2022 CHANGE"},
             "confidence": 94},
            {"time": "00:13", "text": "a big difference.",
             "gloss": {"ASL": "BIG \u2022 DIFFERENCE", "BSL": "BIG \u2022 DIFFERENCE",
                       "Auslan": "BIG \u2022 DIFFERENT", "ISL": "LARGE \u2022 DIFFERENCE"},
             "confidence": 98},
            {"time": "00:17", "text": "Let's get started.",
             "gloss": {"ASL": "START", "BSL": "BEGIN",
                       "Auslan": "START", "ISL": "BEGIN"},
             "confidence": 97},
        ],
    },
    "2": {
        "title": "Morning routine, upgraded",
        "duration": "00:45",
        "segments": [
            {"time": "00:00", "text": "Good morning. Let's build a better routine.",
             "gloss": {"ASL": "MORNING \u2022 ROUTINE", "BSL": "MORNING \u2022 ROUTINE",
                       "Auslan": "MORNING \u2022 ROUTINE", "ISL": "MORNING \u2022 ROUTINE"},
             "confidence": 97},
            {"time": "00:05", "text": "First, drink a glass of water.",
             "gloss": {"ASL": "WATER \u2022 DRINK", "BSL": "WATER \u2022 DRINK",
                       "Auslan": "WATER \u2022 DRINK", "ISL": "WATER \u2022 DRINK"},
             "confidence": 95},
            {"time": "00:10", "text": "Then, write down one goal for today.",
             "gloss": {"ASL": "WRITE \u2022 GOAL", "BSL": "WRITE \u2022 AIM",
                       "Auslan": "WRITE \u2022 GOAL", "ISL": "WRITE \u2022 GOAL"},
             "confidence": 93},
            {"time": "00:15", "text": "Small steps, every single day.",
             "gloss": {"ASL": "SMALL \u2022 STEP \u2022 EVERY-DAY",
                       "BSL": "SMALL \u2022 STEP \u2022 DAILY",
                       "Auslan": "LITTLE \u2022 STEP \u2022 EVERY-DAY",
                       "ISL": "SMALL \u2022 STEP \u2022 EVERY-DAY"},
             "confidence": 98},
        ],
    },
}

# ----------------------------------------------------------------------
# Player state (mirrors the React app's useState hooks)
# ----------------------------------------------------------------------

state = {
    "video": "1",        # which sample video is loaded
    "index": 0,          # current transcript segment
    "language": "ASL",   # active sign language
    "captions": True,    # caption toggle
    "translate": True,   # sign-translation toggle
}


# ----------------------------------------------------------------------
# Player
# ----------------------------------------------------------------------

def current_video():
    return VIDEOS[state["video"]]


def show_frame():
    """Print the current 'video frame': time, caption and sign gloss."""
    video = current_video()
    seg = video["segments"][state["index"]]
    print(f"\n\u25b6 {seg['time']} / {video['duration']}  \u00b7  {video['title']}")
    if state["captions"]:
        print(f"  \U0001f4ac {seg['text']}")
    if state["translate"]:
        gloss = seg["gloss"][state["language"]]
        print(f"  \U0001f91f [{state['language']}] {gloss}  "
              f"(confidence {seg['confidence']}%)")
    if not state["captions"] and not state["translate"]:
        print("  (captions and translation are both off)")


def play():
    """Auto-advance through the rest of the transcript."""
    video = current_video()
    while state["index"] < len(video["segments"]):
        show_frame()
        state["index"] += 1
        if state["index"] < len(video["segments"]):
            time.sleep(1.2)
    state["index"] = len(video["segments"]) - 1
    print("\n\u25a0 End of video.")


def step(d=1):
    """Move forward (d=1) or backward (d=-1) one segment."""
    video = current_video()
    state["index"] = max(0, min(len(video["segments"]) - 1,
                                state["index"] + d))
    show_frame()


def seek(n):
    """Jump to segment number n (1-based, like the transcript list)."""
    video = current_video()
    if 1 <= n <= len(video["segments"]):
        state["index"] = n - 1
        show_frame()
    else:
        print(f"  Pick a segment between 1 and {len(video['segments'])}.")


def show_transcript():
    video = current_video()
    print(f"\n\U0001f4dd Transcript \u2014 {video['title']}")
    for i, seg in enumerate(video["segments"], start=1):
        marker = "\u27a4" if i - 1 == state["index"] else " "
        print(f"  {marker} {i}. [{seg['time']}] {seg['text']}")
    print("  Type a number to jump to that segment.")


def choose_language():
    print("\n\U0001f30d Sign language:")
    for i, lang in enumerate(LANGUAGES, start=1):
        marker = "\u2713" if lang == state["language"] else " "
        print(f"  {marker} {i}. {lang}")
    choice = input("  Choose (1-4): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(LANGUAGES):
        state["language"] = LANGUAGES[int(choice) - 1]
        print(f"  Translation language \u2192 {state['language']}")
        show_frame()
    else:
        print("  Keeping", state["language"])


def choose_video():
    print("\n\U0001f3ac Videos:")
    for key, video in VIDEOS.items():
        marker = "\u2713" if key == state["video"] else " "
        print(f"  {marker} {key}. {video['title']}")
    choice = input("  Choose: ").strip()
    if choice in VIDEOS:
        state["video"] = choice
        state["index"] = 0
        print(f"  Loaded: {VIDEOS[choice]['title']}")
        show_frame()
    else:
        print("  Keeping current video.")


def show_status():
    video = current_video()
    print("\n\u2699\ufe0f  Player status")
    print(f"  Video:       {video['title']}")
    print(f"  Position:    segment {state['index'] + 1} "
          f"of {len(video['segments'])}")
    print(f"  Language:    {state['language']}")
    print(f"  Captions:    {'on' if state['captions'] else 'off'}")
    print(f"  Translation: {'on' if state['translate'] else 'off'}")


def show_help():
    print("""
Commands:
  play        \u25b6 auto-play the rest of the video
  next/back   step one segment forward/back (or just press Enter for next)
  <number>    jump to a transcript segment, e.g. 3
  list        show the transcript (type a number to seek)
  lang        switch sign language (ASL/BSL/Auslan/ISL)
  captions    toggle captions on/off
  sign        toggle the sign-translation layer on/off
  video       switch sample video
  status      show player settings
  help        show this list
  quit        exit
""")


# ----------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------

def main():
    print("=" * 52)
    print("  signa \u2014 live video translation (Python demo)")
    print("=" * 52)
    print("  A console rebuild of the Signa front-end.")
    print("  Type 'help' for commands, 'quit' to exit.")
    show_frame()

    while True:
        cmd = input("\nsigna> ").strip().lower()

        if cmd in ("quit", "exit", "q"):
            print("Bye! \U0001f44b")
            break
        elif cmd == "help":
            show_help()
        elif cmd == "play":
            play()
        elif cmd in ("next", ""):
            step(1)
        elif cmd == "back":
            step(-1)
        elif cmd == "list":
            show_transcript()
        elif cmd == "lang":
            choose_language()
        elif cmd == "captions":
            state["captions"] = not state["captions"]
            print(f"  Captions {'on' if state['captions'] else 'off'}")
            show_frame()
        elif cmd == "sign":
            state["translate"] = not state["translate"]
            print(f"  Translation {'on' if state['translate'] else 'off'}")
            show_frame()
        elif cmd == "video":
            choose_video()
        elif cmd == "status":
            show_status()
        elif cmd.isdigit():
            seek(int(cmd))
        else:
            print(f"  Unknown command '{cmd}'. Type 'help'.")


if __name__ == "__main__":
    main()
