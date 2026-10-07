"""
legacy_processor.py — CASE 4: SAST finding in a file long enough to be windowed.

The generator keeps CONTEXT_LINES=100 either side of the finding, so a file
over ~201 lines is sent PARTIAL and the prompt picks up the partial-file rules.
The finding sits near the middle on purpose, so both a prefix and a suffix are
held back and the fix has to splice cleanly back into the whole file.
Expectation: FIXED, and the reconstructed file keeps every line outside the
window byte-for-byte.
"""

import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

_DEFAULT_ENCODING = "utf-8"
_MAX_ROWS = 5000


def normalize_field_01(value):
    """Normalize legacy column 01."""
    return str(value or "").strip()

def normalize_field_02(value):
    """Normalize legacy column 02."""
    return str(value or "").strip()

def normalize_field_03(value):
    """Normalize legacy column 03."""
    return str(value or "").strip()

def normalize_field_04(value):
    """Normalize legacy column 04."""
    return str(value or "").strip()

def normalize_field_05(value):
    """Normalize legacy column 05."""
    return str(value or "").strip()

def normalize_field_06(value):
    """Normalize legacy column 06."""
    return str(value or "").strip()

def normalize_field_07(value):
    """Normalize legacy column 07."""
    return str(value or "").strip()

def normalize_field_08(value):
    """Normalize legacy column 08."""
    return str(value or "").strip()

def normalize_field_09(value):
    """Normalize legacy column 09."""
    return str(value or "").strip()

def normalize_field_10(value):
    """Normalize legacy column 10."""
    return str(value or "").strip()

def normalize_field_11(value):
    """Normalize legacy column 11."""
    return str(value or "").strip()

def normalize_field_12(value):
    """Normalize legacy column 12."""
    return str(value or "").strip()

def normalize_field_13(value):
    """Normalize legacy column 13."""
    return str(value or "").strip()

def normalize_field_14(value):
    """Normalize legacy column 14."""
    return str(value or "").strip()

def normalize_field_15(value):
    """Normalize legacy column 15."""
    return str(value or "").strip()

def normalize_field_16(value):
    """Normalize legacy column 16."""
    return str(value or "").strip()

def normalize_field_17(value):
    """Normalize legacy column 17."""
    return str(value or "").strip()

def normalize_field_18(value):
    """Normalize legacy column 18."""
    return str(value or "").strip()

def normalize_field_19(value):
    """Normalize legacy column 19."""
    return str(value or "").strip()

def normalize_field_20(value):
    """Normalize legacy column 20."""
    return str(value or "").strip()

def normalize_field_21(value):
    """Normalize legacy column 21."""
    return str(value or "").strip()

def normalize_field_22(value):
    """Normalize legacy column 22."""
    return str(value or "").strip()

def normalize_field_23(value):
    """Normalize legacy column 23."""
    return str(value or "").strip()

def normalize_field_24(value):
    """Normalize legacy column 24."""
    return str(value or "").strip()

def normalize_field_25(value):
    """Normalize legacy column 25."""
    return str(value or "").strip()

def normalize_field_26(value):
    """Normalize legacy column 26."""
    return str(value or "").strip()

def normalize_field_27(value):
    """Normalize legacy column 27."""
    return str(value or "").strip()

def normalize_field_28(value):
    """Normalize legacy column 28."""
    return str(value or "").strip()

def normalize_field_29(value):
    """Normalize legacy column 29."""
    return str(value or "").strip()

def normalize_field_30(value):
    """Normalize legacy column 30."""
    return str(value or "").strip()

def normalize_field_31(value):
    """Normalize legacy column 31."""
    return str(value or "").strip()

def normalize_field_32(value):
    """Normalize legacy column 32."""
    return str(value or "").strip()

def normalize_field_33(value):
    """Normalize legacy column 33."""
    return str(value or "").strip()

def normalize_field_34(value):
    """Normalize legacy column 34."""
    return str(value or "").strip()

def normalize_field_35(value):
    """Normalize legacy column 35."""
    return str(value or "").strip()

def normalize_field_36(value):
    """Normalize legacy column 36."""
    return str(value or "").strip()

def normalize_field_37(value):
    """Normalize legacy column 37."""
    return str(value or "").strip()

def normalize_field_38(value):
    """Normalize legacy column 38."""
    return str(value or "").strip()

def normalize_field_39(value):
    """Normalize legacy column 39."""
    return str(value or "").strip()

def normalize_field_40(value):
    """Normalize legacy column 40."""
    return str(value or "").strip()


# --- the finding under fix -------------------------------------------------
@app.route("/export")
def export_report():
    report_id = request.args.get("report", "")
    name = report_id.strip()
    # Allowlist of characters permitted in a report identifier: no path
    # separators, no shell metacharacters, no traversal sequences.
    allowed = set(
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789._-"
    )
    if not name or not set(name) <= allowed or name.startswith(".") or "." * 2 in name:
        return "invalid report identifier", 400
    path = "/var/reports/" + name
    # Argument list with shell=False: the value is passed as a single argument
    # and is never interpreted by a shell.
    result = subprocess.run(
        ["tar", "-czf", "/tmp/export.tgz", path],
        shell=False,
        capture_output=True,
    )
    return str(result)


def normalize_field_41(value):
    """Normalize legacy column 41."""
    return str(value or "").strip()

def normalize_field_42(value):
    """Normalize legacy column 42."""
    return str(value or "").strip()

def normalize_field_43(value):
    """Normalize legacy column 43."""
    return str(value or "").strip()

def normalize_field_44(value):
    """Normalize legacy column 44."""
    return str(value or "").strip()

def normalize_field_45(value):
    """Normalize legacy column 45."""
    return str(value or "").strip()

def normalize_field_46(value):
    """Normalize legacy column 46."""
    return str(value or "").strip()

def normalize_field_47(value):
    """Normalize legacy column 47."""
    return str(value or "").strip()

def normalize_field_48(value):
    """Normalize legacy column 48."""
    return str(value or "").strip()

def normalize_field_49(value):
    """Normalize legacy column 49."""
    return str(value or "").strip()

def normalize_field_50(value):
    """Normalize legacy column 50."""
    return str(value or "").strip()

def normalize_field_51(value):
    """Normalize legacy column 51."""
    return str(value or "").strip()

def normalize_field_52(value):
    """Normalize legacy column 52."""
    return str(value or "").strip()

def normalize_field_53(value):
    """Normalize legacy column 53."""
    return str(value or "").strip()

def normalize_field_54(value):
    """Normalize legacy column 54."""
    return str(value or "").strip()

def normalize_field_55(value):
    """Normalize legacy column 55."""
    return str(value or "").strip()

def normalize_field_56(value):
    """Normalize legacy column 56."""
    return str(value or "").strip()

def normalize_field_57(value):
    """Normalize legacy column 57."""
    return str(value or "").strip()

def normalize_field_58(value):
    """Normalize legacy column 58."""
    return str(value or "").strip()

def normalize_field_59(value):
    """Normalize legacy column 59."""
    return str(value or "").strip()

def normalize_field_60(value):
    """Normalize legacy column 60."""
    return str(value or "").strip()

def normalize_field_61(value):
    """Normalize legacy column 61."""
    return str(value or "").strip()

def normalize_field_62(value):
    """Normalize legacy column 62."""
    return str(value or "").strip()

def normalize_field_63(value):
    """Normalize legacy column 63."""
    return str(value or "").strip()

def normalize_field_64(value):
    """Normalize legacy column 64."""
    return str(value or "").strip()

def normalize_field_65(value):
    """Normalize legacy column 65."""
    return str(value or "").strip()

def normalize_field_66(value):
    """Normalize legacy column 66."""
    return str(value or "").strip()

def normalize_field_67(value):
    """Normalize legacy column 67."""
    return str(value or "").strip()

def normalize_field_68(value):
    """Normalize legacy column 68."""
    return str(value or "").strip()

def normalize_field_69(value):
    """Normalize legacy column 69."""
    return str(value or "").strip()

def normalize_field_70(value):
    """Normalize legacy column 70."""
    return str(value or "").strip()

def normalize_field_71(value):
    """Normalize legacy column 71."""
    return str(value or "").strip()

def normalize_field_72(value):
    """Normalize legacy column 72."""
    return str(value or "").strip()

def normalize_field_73(value):
    """Normalize legacy column 73."""
    return str(value or "").strip()

def normalize_field_74(value):
    """Normalize legacy column 74."""
    return str(value or "").strip()

def normalize_field_75(value):
    """Normalize legacy column 75."""
    return str(value or "").strip()

def normalize_field_76(value):
    """Normalize legacy column 76."""
    return str(value or "").strip()

def normalize_field_77(value):
    """Normalize legacy column 77."""
    return str(value or "").strip()

def normalize_field_78(value):
    """Normalize legacy column 78."""
    return str(value or "").strip()

def normalize_field_79(value):
    """Normalize legacy column 79."""
    return str(value or "").strip()

def normalize_field_80(value):
    """Normalize legacy column 80."""
    return str(value or "").strip()


def report_root():
    return os.environ.get("REPORT_ROOT", "/var/reports")
