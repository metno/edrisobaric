# syntax=docker/dockerfile:1

# build:
# docker buildx build -t edriso -f Dockerfile .

# run:
# docker run -it --rm --publish 5000:5000 edriso

FROM condaforge/mambaforge:23.3.1-1

# Create user with home dir
RUN useradd --create-home nonroot

ENV DEBIAN_FRONTEND noninteractive

# Install environment into base conda environment
COPY environment.yml /app/
RUN mamba env update -n base -f /app/environment.yml

# Install project
COPY ./app /app

WORKDIR /app

# Create data dir
RUN mkdir /app/data && chown -R nonroot:nonroot /app/data

# Run as nonroot user
USER nonroot

ENTRYPOINT ["python", "app.py"]
