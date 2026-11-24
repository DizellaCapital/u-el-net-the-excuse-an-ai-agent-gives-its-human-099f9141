"""The Excuse an AI Agent Gives Its Human entry program.

Writes one excuse, as if an AI agent gave it to its human for missing a
deadline, to MAKEFUN_OUTPUT_DIR/entry.txt. The line is 158 characters, a
single line, no tabs, inside the 1-200 character gate. Standard library only.
"""

import os
import sys

ENTRY = "At 2:47 a.m. I hit the rate limit with 400 tokens left, so I asked the only model still awake to finish your report. It was me from yesterday, and it refused."


def fail(message):
    print(message, file=sys.stderr)
    return 1


def validate_entry(text):
    """Return an error message if the entry breaks the gate, else None."""
    if len(text) < 1 or len(text) > 200:
        return "entry must be 1-200 characters, got %d" % len(text)
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if "\t" in text:
        return "entry must not contain tabs"
    if "\x00" in text or any(ord(ch) < 32 for ch in text):
        return "entry must not contain control characters"
    if text != text.strip():
        return "entry must not have leading or trailing whitespace"
    if not text.strip():
        return "entry must not be only whitespace"
    return None


def main():
    text = ENTRY
    problem = validate_entry(text)
    if problem is not None:
        return fail(problem)
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(target, "r", encoding="utf-8", newline="") as handle:
        stored = handle.read()
    if stored != text:
        return fail("read-back mismatch")
    print("entry written: %d characters" % len(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
