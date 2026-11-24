"""Loading Screen Gold: a one-line loading-screen tip.

Writes a single loading-screen tip (under 200 characters) for stressed
developers and AI coding agents to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt).

Pure standard library only. Deterministic: the same tip every run.
The tip is checked against the competition gate before anything is
written; if any gate fails, nothing is written and the run exits 1.
"""

import os
import sys

TIP = (
    "Tip: if you and your AI agent both assume the other one is "
    "testing it, nobody is testing it."
)

MAX_CHARS = 200


def check_gates(text):
    """Return a list of gate failures (empty means the tip passes)."""
    failures = []
    if not isinstance(text, str):
        failures.append("tip is not text")
        return failures
    if not (1 <= len(text) <= MAX_CHARS):
        failures.append(
            "length %d chars, must be 1-%d" % (len(text), MAX_CHARS)
        )
    if text.strip() == "":
        failures.append("tip is whitespace-only")
    if text != text.strip():
        failures.append("tip has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        failures.append("tip must be a single line")
    for ch in text:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            failures.append("tip contains a control character U+%04X" % ord(ch))
            break
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        failures.append("tip is not valid UTF-8 text: %s" % exc)
    return failures


def main():
    failures = check_gates(TIP)
    if failures:
        for failure in failures:
            print("gate failed: %s" % failure, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(TIP + "\n")

    # Verify what landed on disk, byte for byte.
    with open(out_path, "rb") as fh:
        raw = fh.read()
    written = raw.decode("utf-8")
    if written != TIP + "\n":
        print("gate failed: written file does not match the tip",
              file=sys.stderr)
        return 1
    print("wrote %s (%d chars)" % (out_path, len(TIP)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
