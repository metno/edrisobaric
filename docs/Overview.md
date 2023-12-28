# Overview

Documentation for creating [EDR API](https://ogcapi.ogc.org/edr/)s using Python. Libraries recommended are [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/latest/) and KNMIs library [edr-pydantic](https://github.com/KNMI/edr-pydantic).

## Sections

[Tutorials](Tutorials.md), [how-to](Howtos.md) guides, technical reference and explanation.

## Components

- FastAPI will serve the API and the OpenAPI spec.
- Pydantic is a library for data validation.
- Edr-pydantic has pre-made pydantic models for EDR, like Collection, Instance, Link, etc.

## Not covered

- General EDR knowledge
- Web proxy
- Containerization

## Links to library examples

### FastAPI

<https://fastapi.tiangolo.com/#example>

### Pydantic / EDR-Pydantic

See <https://github.com/KNMI/edr-pydantic> or the [conformance page](../app/routes/conformance_page.py) for an example.
