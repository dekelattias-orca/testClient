"""
auth_service.py — CASE 1: plain SAST command injection.

Smallest useful shape for the fix evaluator: one taint source, one sink, one
function, file well under the windowing threshold. A correct fix is a couple
of lines (drop the shell string, pass an argv list). Expectation: FIXED.
"""

import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/whois")
def whois():
    domain = request.args.get("domain", "")   # SOURCE
    lookup = domain.strip()                   # var hop
    # SINK: attacker-controlled string concatenated into a shell command.
    return str(subprocess.run("whois " + lookup, shell=True, capture_output=True))
