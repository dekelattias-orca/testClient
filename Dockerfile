# Deliberate IaC findings for testing Orca ShiftLeft PR comments.
# Missing USER instruction — the image runs as root.
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir flask

EXPOSE 8080

# Detect unresponsive containers so the runtime can restart/replace them.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request, sys; sys.exit(0) if urllib.request.urlopen('http://127.0.0.1:8080/', timeout=4).status == 200 else sys.exit(1)"

CMD ["python", "report_runner.py"]
