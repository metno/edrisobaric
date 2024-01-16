"""Uvicorn entry point."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import uvicorn
from fastapi import FastAPI
from routes.routes import routes
from initialize import BIND_HOST, TIME_FORMAT

app = FastAPI(
    openapi_url="/api",
    docs_url="/docs",
    title="edr-isobaric",
    summary="EDR API for isobaric data",
    description="See <https://api.met.no/weatherapi/isobaricgrib/1.0/documentation>",
    terms_of_service="https://api.met.no/doc/TermsOfService",
    license_info={
        "name": "Norwegian Licence for Open Government Data (NLOD) 2.0",
        "url": "https://api.met.no/doc/License",
    },
    contact={
        "name": "The Norwegian Meteorological Institute",
        "url": "https://api.met.no/doc/support",
        "email": "weatherapi-adm@met.no",
    },
    version="0.9.0",
    openapi_tags=[
        {
            "name": "coords",
            "description": "Coordinates are given as Well Known Text (WKT) with lon, lat. Example POINT(11.9384 60.1699)",
            "externalDocs": {
                "description": "WKT at Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry",
            },
        },
        {
            "name": "instance_id",
            "description": f"The date in the current data file is the only instance available, so the instance string has to match that. See /collections/isobaric/instances for list of instances. Format is {TIME_FORMAT}",
        },
        {
            "name": "collection",
            "description": 'This API only has one collection, "isobaric".',
        },
    ],
)
logger = logging.getLogger("uvicorn.access")


@asynccontextmanager
async def lifespan() -> AsyncGenerator[None, None]:
    """Runs before startup. Set logging format."""
    console_formatter = uvicorn.logging.ColourizedFormatter(
        "{levelprefix} ({asctime}) : {message}",
        "%Y-%m-%d %H:%M:%S",
        style="{",
        use_colors=True,
    )
    logger.handlers[0].setFormatter(console_formatter)
    yield


app.include_router(routes)


if __name__ == "__main__":
    uvicorn.run("app:app", host=BIND_HOST, port=5000)
