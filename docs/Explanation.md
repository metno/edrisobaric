# Explanation

## Why use Pydantic

Pydantic will make sure you include all necessary elements, and that they are of correct type.

## Why use FastAPI

FastAPI is popular, well documented and integrates SwaggerUI to give an automatic openapi.json.

## Alternative to Pydantic - PyGeoAPI

[PyGeoAPI](https://github.com/geopython/pygeoapi/) has features for creating EDR APIs, but we found no current use of it in-house. It seems to have easy functions for creating a converter (for example NetCDF or OPeNDAP to EDR), but seems a bit lacking in for creating a new API.
