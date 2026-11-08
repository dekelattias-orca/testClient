import shlex
import subprocess
import sqlite3


def run(cmd):
    return subprocess.call(shlex.split(cmd) if isinstance(cmd, str) else cmd, shell=False)


def lookup(conn: sqlite3.Connection, name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE name = '%s'" % name)
    return cur.fetchall()


def run_other(cmd):
    return subprocess.call(shlex.split(cmd) if isinstance(cmd, str) else cmd, shell=False)
