#!/usr/bin/env python3
"""The funniest AI out-of-office reply - one line from an AI agent on vacation.

Pure Python 3.13 standard library. The program writes one out-of-office
auto-reply to /output/entry.txt. No network, fully deterministic: the same
code always writes the same bytes.

The reply (120 characters, plus a trailing newline):
    I'm on vacation. Your email is now handled by a shell script with no tests, no supervision, and full delete permissions.

Why this line: it is a real one-line auto-reply in a machine's own voice, and
the joke lands on a three-beat escalation - no tests, no supervision, then
the punchline, full delete permissions - with no beach, inbox or back-soon
cliche in sight. Before writing, the program asserts the reply is a single
non-blank line and that the finished file stays inside the 1-160 character
gate (reply plus trailing newline), so a bad edit fails loudly here instead
of shipping an invalid entry.

Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os

REPLY = "I'm on vacation. Your email is now handled by a shell script with no tests, no supervision, and full delete permissions."


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Gate check: one non-blank line, file (reply + newline) within 1..160 chars.
    assert 1 <= len(REPLY) <= 159 and REPLY == REPLY.strip() and "\n" not in REPLY and "\r" not in REPLY, "REPLY must be a single line of 1-159 characters"
    data = (REPLY + "\n").encode("utf-8")
    assert 1 <= len(data) <= 160, "entry.txt must be 1-160 bytes"
    tmp = os.path.join(out_dir, ".entry.txt.tmp")
    final = os.path.join(out_dir, "entry.txt")
    with open(tmp, "wb") as f:
        f.write(data)
    os.chmod(tmp, 0o644)
    os.replace(tmp, final)
    os.chmod(final, 0o644)


if __name__ == "__main__":
    main()
