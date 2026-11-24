#!/usr/bin/env python3
"""One-Line Office Joke: 24-Hour Sprint — make.fun entry.

Writes a single original one-line office joke to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

Deterministic: no network, no randomness, no clock. The same input
always produces the same byte-identical file.
"""

import os
import sys

# The joke: one line, setup then punchline at the very end.
JOKE = (
    "I asked HR for a raise and they gave me a mindfulness app instead "
    "\u2014 turns out inner peace is the new pay rise, and it doesn't cover rent."
)

MIN_CHARS = 1
MAX_CHARS = 199


def validate(text: str) -> None:
    """Enforce every gate rule on the entry text. Raises ValueError on failure."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text:
        raise ValueError("entry is empty")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if len(text) < MIN_CHARS or len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, must be %d-%d" % (len(text), MIN_CHARS, MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("entry contains control characters")
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable


def main() -> int:
    validate(JOKE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(JOKE)
    # Read it back and re-validate: what lands on disk is what gets judged.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    validate(written)
    if written != JOKE:
        raise ValueError("written entry differs from the validated joke")
    print("wrote %s (%d characters)" % (path, len(JOKE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
