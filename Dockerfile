# build:
# docker buildx build -t edriso -f Dockerfile .

# run:
# docker run -it --rm --publish 5000:5000 edriso

FROM condaforge/mambaforge:23.3.1-1

ENV DEBIAN_FRONTEND noninteractive
RUN mkdir /data

# Install environment into base conda environment
COPY environment.yml /app/
RUN mamba env update -n base -f /app/environment.yml

# Install project
COPY ./app /app

WORKDIR /app

ENTRYPOINT ["python", "app.py"]
