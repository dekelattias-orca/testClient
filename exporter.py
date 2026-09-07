"""
exporter.py — new SAST fixture file, added for another round of PR-comment
testing.

Everything here is new: the file does not exist on `main`, so nothing in it
can be filtered against the master baseline. No existing fixture (multi.py,
report_runner.py, main.tf) is modified.

Findings:
  1. COMMAND INJECTION via os.system (CWE-78).
     flask.request.args.get -> var hops -> shell string -> os.system().
     Deliberately os.system rather than subprocess.run, so it hits a
     different rule than the subprocess findings already on this PR.
  2. CODE INJECTION via eval (B307, CWE-95).
     flask.request.args.get -> var hop -> eval().

Both flows are intrafile: source and sink share a function, so neither needs
cross-function taint mode.
"""

import os

from flask import Flask, request

app = Flask(__name__)


# --- command injection through os.system (CWE-78) -----------------------
@app.route("/export")
def export_archive():
    name = request.args.get("name", "")   # SOURCE
    label = name.strip()                  # var hop
    # Shell string built from request data. A name of "x; rm -rf /" runs as a
    # second command. SINK: os.system with a tainted, unquoted argument.
    command = "tar -czf /tmp/export.tgz " + label   # var hop -> tainted cmd
    return str(os.system(command))                  # SINK


# --- code injection through eval (B307, CWE-95) -------------------------
@app.route("/calc")
def evaluate_expression():
    expr = request.args.get("expr", "")   # SOURCE
    formula = expr.strip()                # var hop
    # eval() on attacker input is arbitrary code execution:
    # "__import__('os').system('id')" evaluates fine. SINK: B307 / CWE-95.
    return str(eval(formula))             # SINK
