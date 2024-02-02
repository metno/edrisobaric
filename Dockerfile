# syntax=docker/dockerfile:1

# build:
# docker buildx build -t edriso -f Dockerfile .

# run:
# docker run -it --rm --publish 5000:5000 edriso --bind_host 0.0.0.0

FROM ubuntu:22.04

# Create user with home dir
RUN useradd --create-home nonroot

# Install python and libeccodes-dev. Create /data.
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-dev python3-pip \
    python3-venv libeccodes-dev && \
        apt-get clean && rm -rf /var/lib/apt/lists/*

# Set workdir and install app with requirements.
WORKDIR /app
COPY app/ ./app/
COPY favicon.ico requirements.txt ./
# upgrade setuptools to avoid CVE-2022-40897
RUN python3 -m venv ./venv && \
  ./venv/bin/pip install --upgrade setuptools && \
  ./venv/bin/pip install -r ./requirements.txt

# Create data dir
RUN mkdir /app/data && chown -R nonroot:nonroot /app/data

# Run as nonroot user
USER nonroot

ENTRYPOINT ["/app/venv/bin/python", "/app/app/app.py"]
