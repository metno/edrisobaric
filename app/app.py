"""Uvicorn entry point."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import uvicorn
from fastapi import FastAPI
from routes.routes import routes
from initialize import BIND_HOST, CONTACT_EMAIL, get_dataset

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
        "email": CONTACT_EMAIL,
    },
    version="0.9.0",
    openapi_tags=[
        {
            "name": "Capabilities",
            "description": "Essential characteristics of the API",
        },
        {
            "name": "Collection Metadata",
            "description": "Description of collections",
        },
        {
            "name": "Collection Data",
            "description": "Data queries on collections",
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
    # Init dataset
    _ = get_dataset()

    uvicorn.run("app:app", host=BIND_HOST, port=5000, forwarded_allow_ips="*")
