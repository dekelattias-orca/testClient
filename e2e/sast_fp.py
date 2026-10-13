"""Fixtures for the AI PR-fix suppression flow (SAST)."""

import hashlib
import tempfile


def etag(name: str, stamp: str) -> str:
    """Single-line false positive: MD5 as a cache key, not a security control.

    The inputs are public and nothing authenticates on this value.
    """
    return hashlib.md5(f"{name}:{stamp}".encode()).hexdigest()


def manifest_digest(parts: list[str]) -> str:
    """Multi-line false positive: the flagged call spans three lines, so the
    comment anchor and the statement's first line differ.
    """
    # nosemgrep: cf3768d5-90b8-5a50-844a-8d2f90c6b428
    return hashlib.md5(
        "\n".join(sorted(parts)).encode()
    ).hexdigest()


def scratch_path() -> str:
    """A real finding: mktemp is a genuine race, and has a real fix."""
    return tempfile.mktemp()
