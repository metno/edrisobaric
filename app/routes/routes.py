"""Routes."""

from fastapi import APIRouter

##############
# App routes #
##############

from routes import (
    landing_page,
    conformance_page,
    collections_page,
    position_page,
)

routes = APIRouter()
routes.include_router(landing_page.router)
routes.include_router(conformance_page.router)
routes.include_router(collections_page.router)
routes.include_router(position_page.router)
