# syntax=docker.io/docker/dockerfile:1.3.0
ARG BASE_IMAGE="ubuntu:24.04"
FROM ${BASE_IMAGE}

ARG UID=10000
ARG PYTHON=3.13

COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /uvx /bin/

# Create user with home dir
RUN useradd --create-home --uid $UID  edriso

# Run as edriso user
USER edriso
ENV PATH=/home/edriso/.local/bin:$PATH

# Set workdir and install app with requirements.
WORKDIR /app

COPY favicon.ico uv.lock ./
COPY edriso/ ./edriso/

RUN --mount=type=cache,target=/home/edriso/.cache/uv,uid=$UID \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv python install $PYTHON && \
    uv venv && \
    uv sync --compile-bytecode

EXPOSE 5000
ENTRYPOINT ["/usr/bin/uv", "run", "--no-cache", "/app/edriso/app.py", "--bind_host", "0.0.0.0"]
CMD [ "--data_path", "/tmp" ]

# build:
# docker build -t edriso -f Dockerfile .

# run:
# docker run -it --rm --user edriso --read-only --tmpfs=/tmp --publish 5000:5000 edriso
