# How-tos

## How to use FastAPI

In this How-To we will serve a web page using FastAPI.

It is assumed you have completed the tutorial for creating a conformance page.

### Environment

Use environment set up in tutorial, and install additional libraries:

- `(venv) $ pip install fastapi uvicorn`

### Code

Save this as [app1.py](app1.py)

```python
"""App.py"""
import uvicorn
from fastapi import FastAPI


app = FastAPI()

def create_landing_page():
    """Create content."""
    return "Hello world"

@app.get("/")
async def get_landing_page():
    """Link path to function."""
    return create_landing_page()

if __name__ == "__main__":
    uvicorn.run("app1:app",
                host='0.0.0.0',
                port=5000)

```

### Result

Running the app, you should be able to view the web page.

```bash
(venv) $ python3 app1.py
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
```

In a different terminal:

```bash
(venv) $ curl http://0.0.0.0:5000
"Hello world"
```

## How to serve EDR-Pydantic models using FastAPI

In EDR a landing page is the first page the user will see. It contains contact info, links to conformance and collections. The format is json.

In this How-to we will serve an EDR landing page. The json output will be created using EDR-Pydantic.

It is assumed you have completed the previous How-to.

### Environment

Use environment set up in previous how-to.

### Code

Save this as [app2.py](app2.py)

```python
import uvicorn
from fastapi import FastAPI


app = FastAPI()
base_url = "http://0.0.0.0:5000/"

def create_landing_page() -> dict:
    """Create content."""

    landing = LandingPageModel(
        title="EDR test",
        description="An EDR API How-to",
        links=[
            Link(
                href=f"{base_url}",
                rel="self",
                type="application/json",
                title="Landing Page",
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
            email="api-users-request@lists.met.no",
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
```

### Result

Running the app, you should be able to view the web page.

```bash
(venv) $ python3 app2.py
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
```

In a different terminal:

```bash
(venv) $ curl http://0.0.0.0:5000
{"title":"EDR test","description":"An EDR API How-to","links":[{"href":"http://0.0.0.0:5000/","rel":"self","type":"application/json","title":"Landing Page"},{"href":"http://0.0.0.0:5000/conformance","rel":"conformance","type":"application/json","title":"Conformance document"},{"href":"http://0.0.0.0:5000/collections","rel":"data","type":"application/json","title":"Collections metadata in JSON"}],"provider":{"name":"Meteorologisk institutt / The Norwegian Meteorological Institute","url":"https://api.met.no/"},"contact":{"email":"api-users-request@lists.met.no","phone":"+47.22963000","address":"Henrik Mohns plass 1","postalCode":"0313","city":"Oslo","country":"Norway"}}%
```

Note that since we use FastAPI it will automatically produce a swagger UI with openapi spec for us at <http://0.0.0.0:5000/docs> and another type of doc at <http://0.0.0.0:5000/redoc>.

The links for collections, conformance, etc won't work as we have not implemented them.

### Background

See LandingPageModel in [reference](Reference.md).
