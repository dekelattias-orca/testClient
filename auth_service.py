"""
auth_service.py — CASE 1: plain SAST command injection.

Smallest useful shape for the fix evaluator: one taint source, one sink, one
function, file well under the windowing threshold. A correct fix is a couple
of lines (drop the shell string, pass an argv list). Expectation: FIXED.
"""

import re
import subprocess

from flask import Flask, request

app = Flask(__name__)

# Strict hostname allowlist: letters, digits, hyphens and dots only.
_DOMAIN_RE = re.compile(r"\A(?=.{1,253}\z)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))+\z")


@app.route("/whois")
def whois():
    domain = request.args.get("domain", "")   # SOURCE
    lookup = domain.strip()                   # var hop
    if not _DOMAIN_RE.match(lookup):
        return "invalid domain", 400
    # No shell: arguments are passed as a list, so metacharacters are inert.
    return str(
        subprocess.run(
            ["whois", "--", lookup],
            shell=False,
            capture_output=True,
        )
    )
