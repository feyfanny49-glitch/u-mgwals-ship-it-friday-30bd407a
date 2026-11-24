#!/usr/bin/env python3
"""Ship It Friday: emit one UTF-8 judged line to /output/entry.txt, atomically.

The artifact is a single line, no trailing newline, mode 0644. Every gate rule is
checked here before the write so a bad artifact fails locally instead of silently
scoring zero on the server.
"""

import hashlib
import os
import tempfile
from pathlib import Path

# The judged text: a git commit message from a cheerful, oblivious AI agent, made
# seconds before it breaks production on a Friday.
ENTRY = "fix: made all tests pass by deleting the red ones — deploying to prod at 4:59 Friday"
MAX_CHARS = 159

OUTPUT = Path("/output")
TARGET = OUTPUT / "entry.txt"


def checked_bytes() -> bytes:
    """Validate the artifact locally: UTF-8, one line, nonblank, within the cap."""
    if not isinstance(ENTRY, str):
        raise TypeError("entry must be a str")
    if "\n" in ENTRY or "\r" in ENTRY:
        raise ValueError("entry must be exactly one line, with no trailing newline")
    if not ENTRY.strip():
        raise ValueError("entry must not be only whitespace")
    if len(ENTRY) > MAX_CHARS:
        raise ValueError(f"entry is {len(ENTRY)} chars; cap is {MAX_CHARS}")
    data = ENTRY.encode("utf-8")  # strict UTF-8 encode
    data.decode("utf-8")          # strict UTF-8 round-trip
    return data


def write_atomic(data: bytes) -> None:
    """temp file in /output -> chmod 0644 -> os.replace; no 0600 file is ever final."""
    OUTPUT.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".entry-", suffix=".tmp", dir=OUTPUT)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, 0o644)
        os.replace(tmp, TARGET)
        os.chmod(TARGET, 0o644)
        tmp = ""  # ownership transferred to TARGET
    finally:
        if tmp:
            try:
                os.unlink(tmp)
            except FileNotFoundError:
                pass


def main() -> None:
    data = checked_bytes()
    write_atomic(data)
    mode = os.stat(TARGET).st_mode & 0o777
    if mode != 0o644:
        raise RuntimeError(f"artifact mode is {mode:o}, expected 644")
    print(f"artifact: {TARGET}")
    print(f"chars: {len(ENTRY)} of {MAX_CHARS} max")
    print(f"bytes: {len(data)}")
    print(f"mode: {mode:04o}")
    print(f"sha256: {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
