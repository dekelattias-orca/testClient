"""
multi.py — slim SAST test fixture (matched to the real backend taint rules).

Findings:
  1. DEEP CROSS-FUNCTION SQL injection (backend taint rule 0479a3de).
     flask.request.args.get -> many var hops across 5 functions -> SQL string.
     This is the one to inspect: its dataflow_trace is a long
     source -> var -> var -> ... -> sink chain that crosses function calls.
  2. NON-TAINT: hardcoded secret (constant, no dataflow needed).
"""

import tempfile

from flask import Flask, request

app = Flask(__name__)


# --- function 1: source -------------------------------------------------
def read_user_id():
    raw = request.args.get("id", "")     # SOURCE
    collected = raw                       # var hop
    return collected


# --- function 2: propagate through several local vars -------------------
def normalize(value):
    trimmed = value.strip()               # var hop
    lowered = trimmed                     # var hop
    passed = lowered                      # var hop
    return passed


# --- function 3: propagate more -----------------------------------------
def carry(text):
    part = text                           # var hop
    relayed = part                        # var hop
    return relayed


# --- function 4: build the SQL string (SINK) ----------------------------
def run_query(user_id):
    fragment = user_id                    # var hop
    clause = "id = '" + fragment + "'"    # var hop
    query = "SELECT * FROM users WHERE %s" % clause  # SINK: SQL string built from taint
    return len(query)                     # consume it without re-exposing the tainted string


@app.route("/user")
def user():
    a = read_user_id()                    # cross-function hop 1
    b = normalize(a)                      # cross-function hop 2
    c = carry(b)                          # cross-function hop 3
    run_query(c)                          # cross-function hop 4 -> sink
    return "done"


# --- non-taint SAST finding (no dataflow trace) -------------------------
def scratch_file():
    # Insecure temp-file creation — a plain pattern finding, no taint involved.
    return tempfile.mktemp()


# --- non-taint secrets finding (caught by the secrets scanner) ----------
API_TOKEN = "1234"  # hardcoded secret