"""
multi.py — slim SAST test fixture (matched to the real backend taint rules).

Findings:
  1. DEEP CROSS-FUNCTION SQL injection (backend taint rule 0479a3de).
     flask.request.args.get -> many var hops across 5 functions -> SQL string.
     This is the one to inspect: its dataflow_trace is a long
     source -> var -> var -> ... -> sink chain that crosses function calls.
  2. NON-TAINT: hardcoded secret (constant, no dataflow needed).
  3. UNSAFE YAML DESERIALIZATION (rule B506, CWE-502, HIGH).
     yaml.load() on flask request data with no SafeLoader.
  4. PATH TRAVERSAL (CWE-22, HIGH).
     flask.request.args.get -> var hops -> os.path.join -> open().
     Intrafile on purpose: source and sink share a function, so it fires
     without cross-function taint mode.
"""

import os
import subprocess
import tempfile

import yaml
from flask import Flask, request

app = Flask(__name__)


# --- function 1: source -------------------------------------------------
def read_user_id():
    raw = request.args.get("id", "")     # SOURCE
    collected = raw                       # var hop
    return collected


# --- command-injection finding, entirely on newly added lines ------------
@app.route("/ping")
def ping_host():
    host = request.args.get("host", "")   # SOURCE
    target = host.strip()                 # var hop
    # SINK: shell string built from request data -> rule subprocess-injection
    return str(subprocess.run("ping -c 1 " + target))


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


# --- unsafe deserialization finding (rule B506) --------------------------
@app.route("/config", methods=["POST"])
def load_config():
    body = request.data                   # attacker-controlled YAML document
    # NOTE: FullLoader is not a sandbox. Known gadget chains still construct
    # arbitrary Python objects from it, so this is remote code execution.
    # Use yaml.safe_load() instead. SINK: B506 / CWE-502.
    cfg = yaml.load(body, Loader=yaml.FullLoader)
    return str(cfg)


# --- path traversal finding (CWE-22) ------------------------------------
REPORT_DIR = "/var/www/reports"


@app.route("/download")
def download_report():
    name = request.args.get("name", "")   # SOURCE
    requested = name                      # var hop
    relative = requested.strip()          # var hop
    # No normalization or containment check: "../../etc/passwd" escapes
    # REPORT_DIR entirely. SINK: CWE-22 path traversal.
    path = os.path.join(REPORT_DIR, relative)   # var hop -> tainted path
    with open(path, "rb") as fh:                # SINK
        return fh.read()


# --- non-taint SAST finding (no dataflow trace) -------------------------
def scratch_file():
    adding_some_code = "12345"
    # Insecure temp-file creation — a plain pattern finding, no taint involved.
    return tempfile.mktemp()


# --- non-taint secrets finding (caught by the secrets scanner) ----------
API_TOKEN = "1234"  # hardcoded secret
