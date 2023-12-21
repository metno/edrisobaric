# EDR-isobaric

![Logo](/img/pressure_9189764.png "Logo")

## What is EDR-isobaric?

EDR-isobaric is an API for isobaric data (temperature and wind in isobaric layers). The API is based on [OGC Environmental Data Retrieval (EDR)](https://ogcapi.ogc.org/edr/). Data comes from [GRIB](https://en.wikipedia.org/wiki/GRIB) files from <https://api.met.no/weatherapi/isobaricgrib/1.0/documentation>.

The code is written as an example aimed at API developers at Met.no.

The resulting API is for people who need vertical environmental data for a single location.

## Who is responsible?

- <larsfp@met.no>

## Status

In development

## Getting started

### Test it out

#### Install

Choose one of the following:

##### Conda

```bash
conda create --channel conda-forge --file requirements-conda.txt -n edriso
conda activate edriso
pip install edr-pydantic covjson-pydantic
```

##### Pip

I've had trouble getting eccodes library to work.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Usage

```bash
uvicorn app.main:app --reload
```

will give these URLs:

- <http://127.0.0.1:5000/>
- <http://127.0.0.1:5000/docs>
- <http://127.0.0.1:5000/redoc>

### Use it for production

*How to responsible use it as a dependency for your own production system.*

## Overview of architecture

*Link to wiki or markdown where you get C4 diagrams with legends and textual descriptions.*

## Documentation

- Based on Pydantic EDR- and covjson-libraries by [KNMI](https://github.com/KNMI/)

### References

- Icon from <https://www.freepik.com/icon/pressure_9189764#fromView=search&term=air+preassure&track=ais&page=1&position=49&uuid=c5d25f23-4efd-4063-b6ec-2ab35db07d62>
- <https://spire.com/tutorial/spire-weather-tutorial-intro-to-processing-grib2-data-with-python/>
- <https://covjson.org/>
- <https://fastapi.tiangolo.com/tutorial/bigger-applications/>

### Other APIs for comparison

- <https://opendata.fmi.fi/edr/>
- <https://labs.metoffice.gov.uk/edr/>
- <https://developer.dataplatform.knmi.nl/edr-api>
- <https://swim.iblsoft.com/data/icon-de/edr/collections/isobaric/>

## How to contribute

- Send an email

## Documentation Template

This document is based on the [Met-norway-readme](https://gitlab.met.no/maler/met-norway-readme)-template.
