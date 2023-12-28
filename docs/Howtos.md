# How-tos

## FastAPI

In this How-to we will serve a web page using FastAPI.

It is assumed you have completed the tutorial for creating a conformance page.

### Environment

Use environment set up in tutorial, and install additional libraries:

- `(venv) $ pip install fastapi uvicorn`

### Code

Save this as app1.py

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
    uvicorn.run("app:app",
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

## FastAPI and Pydantic

In this How-to we will serve a json output created with Pydantic.

It is assumed you have completed the previous How-to.

### Environment

Use environment set up in previous how-to.

### Code

Save this as app2.py

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
    uvicorn.run("app:app",
                host='0.0.0.0',
                port=5000)

```
