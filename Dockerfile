# syntax=docker/dockerfile:1

# build:
# docker build -t edriso -f Dockerfile .

# run:
# docker run -it --rm --publish 5000:5000 edriso --bind_host 0.0.0.0

FROM ubuntu:24.04

# Install python.
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-dev python3-pip \
    python3-venv && \
        apt-get clean && rm -rf /var/lib/apt/lists/*

# Set workdir and install app with requirements.
WORKDIR /app
COPY app/ ./app/
COPY favicon.ico requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip python3 -m venv ./venv && \
  ./venv/bin/pip install -r ./requirements.txt

# Create user with home dir
RUN useradd --create-home edriso

# Create data dir
RUN mkdir /app/data && chown -R edriso:edriso /app/data

# Run as edriso user
USER edriso

EXPOSE 5000
ENTRYPOINT ["/app/venv/bin/python", "/app/app/app.py", "--bind_host", "0.0.0.0"]
