"""Landing page."""

from functools import lru_cache
from fastapi import APIRouter
from fastapi.responses import FileResponse
from edr_pydantic.capabilities import LandingPageModel, Provider, Contact
from edr_pydantic.link import Link

from initialize import BASE_URL, CONTACT_EMAIL


@lru_cache
def create_landing_page(base_url) -> dict:
    """Creates the landing page model."""
    landing = LandingPageModel(
        title="EDR isobaric from Grib",
        description="An EDR API for isobaric data from Grib files",
        links=[
            Link(
                href=f"{base_url}",
                rel="self",
                type="application/json",
                title="Landing Page",
            ),
            Link(
                href=f"{base_url}api",
                rel="service-desc",
                type="application/json",
                title="OpenAPI document",
            ),
            Link(
                href=f"{base_url}conformance",
                rel="conformance",
                type="application/json",
                title="Conformance document",
            ),
            Link(
                href=f"{base_url}collections",
                rel="data",
                type="application/json",
                title="Collections metadata in JSON",
            ),
        ],
        provider=Provider(
            name="Meteorologisk institutt / The Norwegian Meteorological Institute",
            url="https://api.met.no/",
        ),
        contact=Contact(
            email=CONTACT_EMAIL,
            phone="+47.22963000",
            postalCode="0313",
            city="Oslo",
            address="Henrik Mohns plass 1",
            country="Norway",
        ),
    )

    return landing.model_dump(exclude_none=True)


router = APIRouter()


@router.get(
    "/",
    tags=["Capabilities"],
    response_model=LandingPageModel,
    response_model_exclude_unset=True,
)
async def landing_page_of_this_API() -> dict:
    """Provides links to the API definition, the conformance statements and the description of the datasets exposed by this service."""
    return create_landing_page(base_url=BASE_URL)


favicon_path = "favicon.ico"


@router.get("/" + favicon_path, include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)
