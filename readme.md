# EDR-isobaricgrib

[OGC Environmental Data Retrieval (EDR) API](https://ogcapi.ogc.org/edr/) interface for isobaric grib2 files from <https://api.met.no/weatherapi/isobaricgrib/1.0/documentation>.

## State

Alpha

## Requirements

Based on <https://github.com/KNMI/edr-pydantic> and <https://gitlab.met.no/met/mapp/trapp/trapp-api>

## Install

```bash
mamba env create -f environment.yml
conda activate edriso
```

## Usage

```bash
uvicorn app:app --reload
```

will give these URLs:

- <http://127.0.0.1:5000/>
- <http://127.0.0.1:5000/docs>
- <http://127.0.0.1:5000/redoc>

## TODO

- Config? Or just use parameters
- Clean old datafiles
- Split code in files
- Replace cgi, it's deprecated
- Silence unrelated warnings

## References

- <https://api.met.no/weatherapi/isobaricgrib/1.0/documentation>
- <https://spire.com/tutorial/spire-weather-tutorial-intro-to-processing-grib2-data-with-python/>

### Other APIs for comparison

- <https://opendata.fmi.fi/edr/>
- <https://labs.metoffice.gov.uk/edr/>
- <https://developer.dataplatform.knmi.nl/edr-api>
