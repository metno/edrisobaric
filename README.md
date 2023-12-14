# EDR-isobaric-grib

[OGC Environmental Data Retrieval (EDR) API](https://ogcapi.ogc.org/edr/) interface for isobaric grib2 files from <https://api.met.no/weatherapi/isobaricgrib/1.0/documentation>.

## State

Alpha

## Requirements

Based on [edr-pydantic](https://github.com/KNMI/edr-pydantic) and [trapp-api](https://gitlab.met.no/met/mapp/trapp/trapp-api).

## Install

```bash
mamba env create -f environment.yml
conda activate edriso
```

(Pynio is only available from conda, edr-pydantic only from pip. Conda can use pip.)

## Usage

```bash
uvicorn app:app --reload
```

will give these URLs:

- <http://127.0.0.1:5000/>
- <http://127.0.0.1:5000/docs>
- <http://127.0.0.1:5000/redoc>

## TODO

### EDR

- Instance should be file/date?
- Show only available date, or fetch others if asked?

### Code

- Move to github
- Config? Or just use parameters? Filename is currently hardcoded.
- Clean old datafiles
- Replace cgi module, it's deprecated
- Temporal extent is fetched (poorly) from filename

## References

- <https://api.met.no/weatherapi/isobaricgrib/1.0/documentation>
- <https://spire.com/tutorial/spire-weather-tutorial-intro-to-processing-grib2-data-with-python/>

### Other APIs for comparison

- <https://opendata.fmi.fi/edr/>
- <https://labs.metoffice.gov.uk/edr/>
- <https://developer.dataplatform.knmi.nl/edr-api>
