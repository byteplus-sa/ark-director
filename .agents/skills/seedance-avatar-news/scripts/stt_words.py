#!/usr/bin/env python3
"""Flatten a speech_to_text TranscriptionResult into {"words": [[word, start_ms, end_ms], ...]} for render_short.py."""

import argparse
import json
import sys


def pick(obj, *keys):
    for key in keys:
        if key in obj and obj[key] is not None:
            return obj[key]
    raise KeyError(f"none of {keys} in {sorted(obj)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", help="JSON file holding the TranscriptionResult (or the full tool output with a 'result' key)")
    parser.add_argument("out", help="Output words JSON")
    args = parser.parse_args()
    with open(args.result) as fh:
        data = json.load(fh)
    data = data.get("result", data)
    words = []
    for utterance in data.get("utterances", []):
        for w in utterance.get("words", []):
            words.append([
                str(pick(w, "text", "word")).strip(),
                int(pick(w, "start_time", "start_ms", "start")),
                int(pick(w, "end_time", "end_ms", "end")),
            ])
    if not words:
        sys.exit("No word timestamps found in utterances[].words")
    with open(args.out, "w") as fh:
        json.dump({"text": data.get("text", ""), "words": words}, fh, indent=1)
    for i, (w, s, e) in enumerate(words):
        print(f"{i:3d} {s:6d}-{e:6d} {w}")


if __name__ == "__main__":
    main()
