# EDR-isobaricgrib

[OGC Environmental Data Retrieval (EDR) API](https://ogcapi.ogc.org/edr/) interface for isobaric grib2 files from <https://api.met.no/weatherapi/isobaricgrib/1.0/documentation>.

## Requirements

Based on <https://github.com/KNMI/edr-pydantic>

## Install

```bash
mamba env create -f environment.yml
conda activate edriso
```

## Usage

```bash
uvicorn edriso:app --reload
```

will give these URLs:

- <http://127.0.0.1:8000/>
- <http://127.0.0.1:8000/docs>
- <http://127.0.0.1:8000/redoc>

## TODO

- Clean old datafiles
- Split code in files
- Cgi deprecated
- Silence warnings

## References

- <https://api.met.no/weatherapi/isobaricgrib/1.0/documentation>
- <https://spire.com/tutorial/spire-weather-tutorial-intro-to-processing-grib2-data-with-python/>
