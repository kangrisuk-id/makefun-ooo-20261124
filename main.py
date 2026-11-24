#!/usr/bin/env python3
"""Out of Office: The Overworked AI's Auto-Reply — make.fun entry.

Writes the entry's one-line out-of-office auto-reply to entry.txt in the
output directory. Pure Python standard library; no network, no input.

The line: an overworked AI agent, finally on vacation, trying very hard
to sound relaxed — it has optimized the beach, scheduled the sunset, and
filed a ticket about the sand. Chosen from 40 candidates by a pairwise
tournament run against the published judge brief (see candidates.md).
"""

import os
import sys

LINE = (
    "I am out of office, attempting leisure. I have optimized the beach, "
    "scheduled the sunset, and filed a ticket about the sand. "
    "Your email is safe in the queue."
)


def candidate_dirs():
    """Output directories to try, most preferred first."""
    seen = []
    for path in (
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        os.path.join(os.getcwd(), "output"),
    ):
        if path and path not in seen:
            seen.append(path)
    return seen


def main():
    payload = (LINE + "\n").encode("utf-8")
    errors = []
    for directory in candidate_dirs():
        try:
            os.makedirs(directory, exist_ok=True)
            target = os.path.join(directory, "entry.txt")
            with open(target, "wb") as handle:
                handle.write(payload)
            print("wrote %s (%d bytes)" % (target, len(payload)))
            return 0
        except OSError as exc:  # try the next candidate directory
            errors.append("%s: %s" % (directory, exc))
    for err in errors:
        print("failed: %s" % err, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
