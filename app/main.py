"""Uvicorn entry point."""

import logging
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request

from app.internal import initialize
from app.routes import edrcollections, conformance, landing_page


app = FastAPI(openapi_url="/openapi.json", docs_url="/api")
logger = logging.getLogger("uvicorn.access")


@asynccontextmanager
async def lifespan():
    """Runs before startup. Set logging format. Open grib file."""
    console_formatter = uvicorn.logging.ColourizedFormatter(
        "{levelprefix} ({asctime}) : {message}",
        "%Y-%m-%d %H:%M:%S",
        style="{",
        use_colors=True,
    )
    logger.handlers[0].setFormatter(console_formatter)

    yield


@app.get("/")
async def root():
    """Reply to /."""
    return landing_page.create_landing_page(initialize.get_base_url())


@app.get("/conformance")
async def get_conformance():
    """Conformance."""
    return conformance.create_conformance_page()


@app.get("/collections")
async def get_collections(request: Request):
    """Collections."""
    return edrcollections.create_collections_page(str(request.url))


@app.get("/collections/position")
async def get_position(coords: str):
    """Position."""
    return edrcollections.create_point(coords=coords)


# @app.get("/collections/{instance_id}")
# async def get_instances(request: Request, instance_id: str):
#     """ Instances """
#     return edrcollections.create_collections_page(str(request.url), instance_id=instance_id)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=5000, reload=False, limit_concurrency=20
    )  # app.main:app
