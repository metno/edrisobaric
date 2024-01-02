# EDR-isobaric

![Logo](/img/pressure_9189764.png "Logo")

[![CodeQL](https://github.com/metno/edrisobaric/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/metno/edrisobaric/actions/workflows/github-code-scanning/codeql)
[![trivy](https://github.com/metno/edrisobaric/actions/workflows/trivy.yml/badge.svg)](https://github.com/metno/edrisobaric/actions/workflows/trivy.yml)

## What is EDR-isobaric?

EDR-isobaric is an API for isobaric data (temperature and wind in isobaric layers). The API is based on [OGC Environmental Data Retrieval (EDR)](https://ogcapi.ogc.org/edr/). Data source is [GRIB](https://en.wikipedia.org/wiki/GRIB) files from <https://api.met.no/weatherapi/isobaricgrib/1.0/documentation>.

The resulting API is for people who need vertical environmental data for a single location.

The code is written as an example aimed at API developers at Met.no. See extensive docs around creating an API at [Overview](docs/Overview.md).

Resulting data can be pasted into covjson playground for visualizing:

![playground](/img/playground.png "playground")


## Who is responsible?

- larsfp at met.no

## Status

In development

## Getting started

### Test it out

#### Install

Choose one of the following:

##### Pull image from Github registry

```bash
docker pull ghcr.io/metno/edrisobaric:main
docker run -it --rm --publish 5000:5000 ghcr.io/metno/edrisobaric:main
```

##### Build using Conda

Clone repo and run:

```bash
conda create --channel conda-forge --file requirements-conda.txt -n edriso
conda activate edriso
pip install edr-pydantic covjson-pydantic
```

##### Build using Pip

This method might need you to install `libeccodes-dev` from your package manager. Clone repo and run:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Usage

```bash
cd app
python3 app.py
```

or see `Dockerfile` for how to build and run. A data file will be downloaded on demand.

Staring the app will give these URLs:

- <http://127.0.0.1:5000/>
- <http://127.0.0.1:5000/docs>
- <http://127.0.0.1:5000/redoc>

Example position lookup:

- <http://127.0.0.1:5000/collections/isobaric/position?coords=POINT(10.718%2059.942)>

### Use it for production

This is only ment for local usage. Use as noted in `Testing it out`.

## Overview of architecture

See [output](docs/Output.md) of all operations.

## Documentation

- Based on Pydantic EDR- and covjson-libraries by [KNMI](https://github.com/KNMI/)
- Docs around creating an API at [Overview](docs/Overview.md).

### Other APIs for comparison

- <https://opendata.fmi.fi/edr/>
- <https://labs.metoffice.gov.uk/edr/>
- <https://developer.dataplatform.knmi.nl/edr-api>
- <https://swim.iblsoft.com/data/icon-de/edr/collections/isobaric/>

### References and acknowledgements

- Icon from [freepik.com](https://www.freepik.com/icon/pressure_9189764#fromView=search&term=air+preassure&track=ais&page=1&position=49&uuid=c5d25f23-4efd-4063-b6ec-2ab35db07d62)
- <https://covjson.org/>
- <https://fastapi.tiangolo.com/tutorial/bigger-applications/>

## How to contribute

- Issues

## Documentation Template

This document is based on the [Met-norway-readme](https://gitlab.met.no/maler/met-norway-readme)-template.
