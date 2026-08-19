"""
report_runner.py — fixture for the two PR-comment surfaces that a
changed line cannot produce on its own.

On `main` this file is clean: both sinks receive a hardcoded constant, so
`subprocess-injection` (taint mode, rule 608f8550) has no source and does not
fire. Nothing here is in the master baseline.

On the PR branch only the two marked "FLIP" lines change. Each sink line is
left untouched, so each finding is *new* (not filtered as a master finding)
while being reported on a line the diff never touched:

  FLOW A — the flip sits 2 lines above its sink, so the sink falls INSIDE the
           hunk (GitHub's patch carries 3 lines of context) but is not a
           changed line  ->  inline comment on a context line.

  FLOW B — the flip sits far above its sink, so the sink falls OUTSIDE every
           hunk  ->  demoted to a file-level comment.
"""

import subprocess

from flask import Flask, request

app = Flask(__name__)


# --- FLOW A: inline comment anchored on an UNCHANGED context line ----------
@app.route("/ping")
def run_ping():
    # SINK A below is unchanged by the PR, but lands inside the flip's hunk.
    host = "localhost"                    # FLIP A -> request.args.get("host", "")
    target = host.strip()                 # var hop
    return str(subprocess.run("ping -c 1 " + target))   # SINK A


# ---------------------------------------------------------------------------
# The padding below is load-bearing. It keeps FLOW B's sink more than 3 lines
# from FLOW B's flip, so the sink lands outside every diff hunk and GitHub
# refuses an inline comment on it (HTTP 422), which is what demotes it to a
# file-level comment. It also keeps the two flows in separate hunks.
# ---------------------------------------------------------------------------


def build_report_target():
    # FLIP B -> request.args.get("target", "")
    return "localhost"


def _describe(target):
    """Filler between FLIP B and SINK B. Pure string work, no sink."""
    label = str(target)
    return label.strip()


# --- FLOW B: demoted to a file-level comment -------------------------------
@app.route("/report")
def run_report():
    target = build_report_target()        # taint arrives from far above
    described = _describe(target)         # var hop
    # SINK B: unchanged by the PR and outside every hunk.
    return str(subprocess.run("ping -c 1 " + described))
