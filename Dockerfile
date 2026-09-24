# Deliberate IaC findings for testing Orca ShiftLeft PR comments.
# Missing USER instruction — the image runs as root.
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir flask

EXPOSE 8080

CMD ["python", "report_runner.py"]
