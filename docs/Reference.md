# Reference

## LandingPageModel

[LandingPageModel](https://github.com/KNMI/edr-pydantic/blob/791c6f7dd3b55b1f8ba93989bbe97d0f38f76ba9/src/edr_pydantic/capabilities.py#L28) defines:

    class LandingPageModel(EdrBaseModel):
        title: Optional[str] = None
        description: Optional[str] = None
        links: List[Link]
        keywords: Optional[List[str]] = None
        provider: Optional[Provider] = None
        contact: Optional[Contact] = None

Most of these are marked optional, but should be included.

See example of landing pages:

- [opendata.fmi.fi/edr](https://opendata.fmi.fi/edr/)
- [labs.metoffice.gov.uk/edr](https://labs.metoffice.gov.uk/edr/)

## ConformanceModel

[ConformanceModel](https://github.com/KNMI/edr-pydantic/blob/791c6f7dd3b55b1f8ba93989bbe97d0f38f76ba9/src/edr_pydantic/capabilities.py#L37) defines a parameter `conformsTo`, with a list of strings.

    class ConformanceModel(EdrBaseModel):
        conformsTo: List[str]

See example of conformance pages:

- [labs.metoffice.gov.uk/edr/conformance](https://labs.metoffice.gov.uk/edr/conformance)

## Starting uvicon

    uvicorn.run("main:app",
                host='0.0.0.0',
                port=5000)

In this example the python file should be named main.py and the instance of FastAPI should be named app.

## Links to library examples

### FastAPI

<https://fastapi.tiangolo.com/#example>

### Pydantic / EDR-Pydantic

<https://github.com/KNMI/edr-pydantic>
