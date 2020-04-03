FROM python:3.8-slim AS base

SHELL ["bash", "-c"]

WORKDIR /app
COPY requirements.txt ./

RUN set -euo pipefail && \
    apt-get update; \
    apt-get install -y --no-install-recommends git; \
    # One of the packages require git
    python3 -m pip install --no-cache -r requirements.txt; \
    apt-get remove -y git; \
    rm -rf /var/lib/apt/lists/*; \
    :

FROM base AS tester
COPY requirements.dev.txt ./
RUN python3 -m pip install --no-cache -r requirements.dev.txt
# Reset entrypoint for convenience when calling separate command
ENTRYPOINT []

FROM base AS release

COPY app.py ./
COPY fover ./fover
COPY static ./static
COPY templates ./templates

CMD ["gunicorn", "app:app"]
