# EDR-isobaric-grib - edrisobaric

[OGC Environmental Data Retrieval (EDR) API](https://ogcapi.ogc.org/edr/) interface for isobaric grib2 files from <https://api.met.no/weatherapi/isobaricgrib/1.0/documentation>.

## State

Alpha

## Requirements

Based on EDR pydantic libraries by [KNMI](https://github.com/KNMI/).

## Install

Choose one of the following:

### Conda

```bash
mamba env create -f environment.yml
conda activate edriso
```

### Pip

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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

### EDR

- Instance should be file/date? Show only available date, or fetch others if asked?

### Code

- Move to github
- Config? Or just use parameters? Filename is currently hardcoded.
- Clean old datafiles
- Replace cgi module, it's deprecated

## References

- <https://api.met.no/weatherapi/isobaricgrib/1.0/documentation>
- <https://spire.com/tutorial/spire-weather-tutorial-intro-to-processing-grib2-data-with-python/>
- <https://covjson.org/cookbook/>
- <https://fastapi.tiangolo.com/tutorial/bigger-applications/>

### Other APIs for comparison

- <https://opendata.fmi.fi/edr/>
- <https://labs.metoffice.gov.uk/edr/>
- <https://developer.dataplatform.knmi.nl/edr-api>
- <https://swim.iblsoft.com/data/icon-de/edr/collections/isobaric/>
