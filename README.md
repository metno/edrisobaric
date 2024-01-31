# EDR-isobaric

![Logo](/img/pressure_9189764.png "Logo")

## What is EDR-isobaric?

EDR-isobaric is an API for isobaric data (temperature and wind in isobaric layers). The API is based on [OGC Environmental Data Retrieval (EDR)](https://ogcapi.ogc.org/edr/). Data source is [GRIB](https://en.wikipedia.org/wiki/GRIB) files from <https://api.met.no/weatherapi/isobaricgrib/1.0/documentation>.

The resulting API is for people who need vertical environmental data for a single location.

The code is written as an example aimed at API developers at Met.no.

Resulting data can be pasted into [covjson playground](https://covjson.org/playground) for visualizing:

![playground](/img/playground.png "playground")

The area covered by the source:

![playground](/img/extent.jpg "extent")

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/metno/edrisobaric/blob/main/LICENSE)

## Who is responsible?

- larsfp at met.no

## Status

Feature complete.

## Getting started

### Test it out

Choose one of the following:

#### Pull image from Github registry and run with docker

```bash
docker pull ghcr.io/metno/edrisobaric:main
docker run -it --rm --publish 5000:5000 ghcr.io/metno/edrisobaric:main --bind_host 0.0.0.0
```

#### Build using Pip

This method might need you to install `libeccodes-dev` from your package manager. Clone repo and run:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app
python3 app.py
```

#### Web

A test instance may or may not be available at <https://edrisobaric.k8s.met.no/>.

## Usage

A grib data file will be downloaded on demand if none is supplied.

Staring the app will give these URLs:

- Landig page: <http://127.0.0.1:5000/>
- Openapi spec: <http://127.0.0.1:5000/api>
- SwaggerUI: <http://127.0.0.1:5000/docs>
- Redoc: <http://127.0.0.1:5000/redoc>

Example position lookup:

- <http://127.0.0.1:5000/collections/isobaric/position?coords=POINT(11.9384%2060.1699)>

Arguments supported:

```bash
    usage: app.py [-h] [--time TIME] [--file FILE] [--base_url BASE_URL] [--bind_host BIND_HOST] [--api_url API_URL] [--data_path DATA_PATH]

    options:
    -h, --help            show this help message and exit
    --time TIME           Timestamp to fetch data for. Must be in format 2024-01-24T18:00:00Z, where time matches an available production. See
                            <https://api.met.no/weatherapi/isobaricgrib/1.0/available.json?type=grib2> for available files. They are produced every 3rd hour.
                            Example: --datetime="2024-01-24T18:00:00Z"
    --file FILE           Local grib file to read data from. Default will fetch file from API.
    --base_url BASE_URL   Base URL for API, with a trailing slash. Default is http://localhost:5000/
    --bind_host BIND_HOST
                            Which host to bind to. Default is 127.0.0.1. Use 0.0.0.0 when running in container.
    --api_url API_URL     URL to download grib file from. Default is <https://api.met.no/weatherapi/isobaricgrib/1.0/grib2?area=southern_norway>.
    --data_path DATA_PATH
                            Where to store data files. Default is ./data
```

### Use it for production

This is only ment for learning. Use as noted in [Testing it out](#test-it-out).

## Overview of architecture

- [C4 diagram](docs/C4.md)

## Documentation

- Based on Pydantic EDR- and covjson-libraries by [KNMI](https://github.com/KNMI/)
- This app will not download _new_ data unless restarted.
- [Sample output](docs/Output.md)
- To run tests, activate your venv, install requirements.txt and requirements-dev.txt, then run `tox`.

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

## Templates

- This document is based on the [Met-norway-readme](https://gitlab.met.no/maler/met-norway-readme)-template.
- Gitlab-ci is based on [team-punkt gitlab-ci](https://gitlab.met.no/team-punkt/gitlab-ci/config)
