""" Uvicorn entry point """

import logging
import uvicorn
import xarray as xr
from fastapi import FastAPI

import edrlanding_page
import edrconformance
import edrcollections
import grib
from initialize import get_filename, get_data_path, get_base_url


app = FastAPI(openapi_url="/openapi.json",
              docs_url="/api")
logger = logging.getLogger("uvicorn.access")


@app.on_event("startup")
def startup():
    """ Startup message """
    print("Checking grib file")

    filename = grib.build_gribfile_name(get_data_path())
    if get_filename() is not None:
        filename = get_filename()
    else:
        if not grib.validate_gribfile(data_path=get_data_path(), fname=get_filename()):
            grib.download_gribfile(data_path=get_data_path(), api_url=get_base_url())

    ds = xr.open_dataset(filename, engine='pynio')
    print("Variables in file:")
    for v in ds:
        print("Name <%s>   Long name <%s>   Unit <%s>" %
            (v, ds[v].attrs["long_name"], ds[v].attrs["units"]))


@app.on_event("startup")
async def startup_event():
    """
    Set logging format
    """
    console_formatter = uvicorn.logging.ColourizedFormatter(
        "{levelprefix} ({asctime}) : {message}","%Y-%m-%d %H:%M:%S",
        style="{", use_colors=True,
        )
    logger.handlers[0].setFormatter(console_formatter)


@app.get("/")
async def root():
    """ Reply to / """
    return edrlanding_page.create_landing_page()


@app.get("/conformance")
async def get_conformance():
    """ Conformance """
    return edrconformance.create_conformance_page()


@app.get("/collections")
async def get_collections():
    """ Collections """
    return edrcollections.create_collections_page()


if __name__ == "__main__":

    uvicorn.run("app:app",
                host='0.0.0.0',
                port=5000,
                reload=True,
                limit_concurrency=20)
