# build:
# docker build -t edriso -f Dockerfile .

# run:
# docker run -it --rm --publish 5000:5000 edriso --bind_host 0.0.0.0

FROM ubuntu:24.04
COPY --from=ghcr.io/astral-sh/uv:0.9.4 /uv /uvx /bin/

# Set workdir and install app with requirements.
WORKDIR /app
COPY app/ ./app/
COPY favicon.ico pyproject.toml ./
# Create user with home dir
RUN useradd --create-home edriso

# Create data dir
RUN mkdir /app/data && chown -R edriso:edriso /app

# Run as edriso user
USER edriso

RUN --mount=type=cache,target=/root/.cache/uv \
    uv python install 3.12 && \
    uv venv && \
    uv sync

ENV PATH=/home/edriso/.local/bin:$PATH

EXPOSE 5000
ENTRYPOINT ["/usr/bin/uv", "run", "/app/app/app.py", "--bind_host", "0.0.0.0"]
