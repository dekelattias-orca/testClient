"""
report_runner.py — fixture for the two PR-comment surfaces that a changed
line cannot produce on its own.

Regarding `subprocess-injection` (taint mode, rule 608f8550) this file is
clean on `main`: both sinks receive a string constant, so the rule has no
source and cannot fire. The non-taint subprocess rules (B404-style "Security
Risks of Using the Subprocess Module", and "Subprocess Spawning without Input
Validation") DO fire here on main — that is fine and expected. They land in
the master baseline and are therefore filtered out of the pull request.

On the PR branch only the two "FLIP" lines change. Both sink lines are left
untouched, so each taint finding is *new* (not filtered against master) while
being reported on a line the diff never touched:

  FLOW A — flip sits 2 lines above its sink, so the sink falls INSIDE the hunk
           (GitHub's patch carries 3 lines of context) without being a changed
           line  ->  inline comment on a context line.

  FLOW B — flip sits 8 lines above its sink, so the sink falls OUTSIDE every
           hunk  ->  demoted to a file-level comment.

Both flows keep source and sink in the SAME function on purpose, so neither
depends on cross-function taint (the CLI's --taint-intrafile, default false).
"""

import subprocess

from flask import Flask, request

app = Flask(__name__)


# --- FLOW A: inline comment anchored on an UNCHANGED context line ----------
@app.route("/ping")
def run_ping():
    # SINK A below is unchanged by the PR, but lands inside the flip's hunk.
    host = "localhost"                    # FLIP A
    target = host.strip()                 # var hop
    return str(subprocess.run("ping -c 1 " + target))   # SINK A


# --- FLOW B: demoted to a file-level comment -------------------------------
@app.route("/report")
def run_report():
    source = "localhost"                  # FLIP B
    # The filler below is load-bearing. It pushes SINK B more than 3 lines
    # away from FLIP B, so the sink falls outside the hunk the flip opens and
    # GitHub refuses an inline comment on it (HTTP 422) — which is what
    # demotes the finding to a file-level comment. Keep at least 4 lines
    # between FLIP B and SINK B if you edit this.
    label = str(source)                   # var hop
    trimmed = label.strip()               # var hop
    described = trimmed                   # var hop
    return str(subprocess.run("ping -c 1 " + described))   # SINK B
