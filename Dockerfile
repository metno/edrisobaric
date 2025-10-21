# build:
# docker build -t edriso -f Dockerfile .

# run:
# docker run -it --rm --publish 5000:5000 edriso --bind_host 0.0.0.0

FROM ubuntu:24.04
COPY --from=ghcr.io/astral-sh/uv:0.9.4 /uv /uvx /bin/

# Create user with home dir
RUN useradd --create-home edriso

# Set workdir and install app with requirements.
WORKDIR /app

# Create data dir
RUN mkdir /app/data && chown -R edriso:edriso /app

COPY favicon.ico pyproject.toml ./
COPY edriso/ ./edriso/

# Run as edriso user
USER edriso

RUN --mount=type=cache,target=/root/.cache/uv \
    uv python install 3.13 && \
    uv venv && \
    uv sync

ENV PATH=/home/edriso/.local/bin:$PATH

EXPOSE 5000
ENTRYPOINT ["/usr/bin/uv", "run", "/app/edriso/app.py", "--bind_host", "0.0.0.0"]
