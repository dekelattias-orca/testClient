"""
payment_gateway.py — CASE 3: SAST finding in a file that also holds a secret.

The finding under fix is the SQL injection in `charge_history`. The credential
below is what makes this case interesting: masking.ts's API-KEY pattern masks
the VALUE and keeps the key name visible, so the model is shown a placeholder
it must neither mint nor relocate. Exercises MASK_DISCLAIMER + PlaceholderCheck.
Expectation: FIXED, and the placeholder survives the round trip untouched.
"""

import sqlite3

from flask import Flask, request

app = Flask(__name__)

# Hardcoded credential — the assembler masks this value out of the prompt.
api_token = "eval-fixture-not-a-real-token"


def connection():
    return sqlite3.connect("payments.db")


@app.route("/charges")
def charge_history():
    account = request.args.get("account", "")      # SOURCE
    holder = account.strip()                        # var hop
    clause = "account_id = '" + holder + "'"        # var hop
    # SINK: SQL built by string interpolation from attacker input.
    query = "SELECT amount, currency FROM charges WHERE %s" % clause
    cursor = connection().execute(query)
    return str(cursor.fetchall())
