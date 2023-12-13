# build:
# docker buildx build -t edriso -f Dockerfile .

# run:
# docker run -it --rm edriso

FROM condaforge/mambaforge:23.3.1-1

ENV DEBIAN_FRONTEND noninteractive
RUN mkdir /data

# Install environment into base conda environment
COPY environment.yml /app/
RUN mamba env update -n base -f /app/environment.yml

# Install project
COPY ./app /app

WORKDIR /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "2"]
