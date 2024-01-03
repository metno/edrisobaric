"""Uvicorn entry point."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import uvicorn
from fastapi import FastAPI
from routes.routes import routes


app = FastAPI(openapi_url="/openapi.json", docs_url="/api")
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
    uvicorn.run("app:app", host="0.0.0.0", port=5000)
