""" Uvicorn entry point """

import logging
from contextlib import asynccontextmanager
import uvicorn
import xarray as xr
from fastapi import FastAPI, Request

import edrlanding_page
import edrconformance
import edrcollections
import grib
from initialize import get_filename, get_data_path, get_base_url


app = FastAPI(openapi_url="/openapi.json",
              docs_url="/api")
logger = logging.getLogger("uvicorn.access")


@asynccontextmanager
async def lifespan():
    """
    Runs before startup. Set logging format. Open grib file.
    """
    console_formatter = uvicorn.logging.ColourizedFormatter(
        "{levelprefix} ({asctime}) : {message}","%Y-%m-%d %H:%M:%S",
        style="{", use_colors=True,
        )
    logger.handlers[0].setFormatter(console_formatter)

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

    yield

@app.get("/")
async def root():
    """ Reply to / """
    return edrlanding_page.create_landing_page()


@app.get("/conformance")
async def get_conformance():
    """ Conformance """
    return edrconformance.create_conformance_page()


@app.get("/collections")
async def get_collections(request: Request):
    """ Collections """
    return edrcollections.create_collections_page(str(request.url))

@app.get("/collections/position")
async def get_instances(coords: str):
    """ Position """
    return edrcollections.create_data(coords=coords)

# @app.get("/collections/{instance_id}")
# async def get_instances(request: Request, instance_id: str):
#     """ Instances """
#     return edrcollections.create_collections_page(str(request.url), instance_id=instance_id)


if __name__ == "__main__":

    uvicorn.run("app:app",
                host='0.0.0.0',
                port=5000,
                reload=True,
                limit_concurrency=20)
