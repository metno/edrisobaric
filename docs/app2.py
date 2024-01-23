"""App2.py"""
import uvicorn
from fastapi import FastAPI
from edr_pydantic.capabilities import LandingPageModel, Provider, Contact
from edr_pydantic.link import Link


app = FastAPI()
BASE_URL = "http://0.0.0.0:5000/"

def create_landing_page() -> dict:
    """Create content."""

    landing = LandingPageModel(
        title="EDR test",
        description="An EDR API How-to",
        links=[
            Link(
                href=f"{BASE_URL}",
                rel="self",
                type="application/json",
                title="Landing Page",
            ),
            Link(
                href=f"{BASE_URL}conformance",
                rel="conformance",
                type="application/json",
                title="Conformance document",
            ),
            Link(
                href=f"{BASE_URL}collections",
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
            email="weatherapi-adm@met.no",
            phone="+47.22963000",
            postalCode="0313",
            city="Oslo",
            address="Henrik Mohns plass 1",
            country="Norway",
        ),
    )

    return landing.model_dump(exclude_none=True)


@app.get("/")
async def get_landing_page():
    """Link path to function."""
    return create_landing_page()

if __name__ == "__main__":
    uvicorn.run("app2:app",
                host='0.0.0.0',
                port=5000)
