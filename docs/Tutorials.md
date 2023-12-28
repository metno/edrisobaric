# Tutorials

## EDR-Pydantic - Create a conformance page

In EDR a conformance page is a list of standards our API adheres to.

In this tutorial we will create a json output representing a conformance page.

It is assumed you have basic terminal knowledge and are on an Ubuntu workstation.

### Create a venv and install necessary tools

Install system tools:

- sudo apt install python3-pip python3-venv curl

Create a directory for your project and set up environment.

- mkdir ~/tutorial; cd ~/tutorial
- python3 -m venv venv
- source venv/bin/activate
- pip install edr-pydantic

You should now have all the tools, and your terminal should show something like

```bash
(venv) larsfp@laptop5701:~/tutorial$ 
```

### Code

Paste this code in a file called `conformance.py`

```python
from edr_pydantic.capabilities import ConformanceModel

c = ConformanceModel(
        conformsTo=[
            "http://www.opengis.net/spec/ogcapi-common-1/1.0/conf/core",
            "http://www.opengis.net/spec/ogcapi-common-2/1.0/conf/collections",
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/core",
        ],
    )

print(c.model_dump(exclude_none=True))
```

### Result

Running the file should return a json output.

```bash
(venv) larsfp@laptop5701:~/tutorial$ python3 conformance.py
```

```json
{
    'conformsTo': [
            'http://www.opengis.net/spec/ogcapi-common-1/1.0/conf/core',
            'http://www.opengis.net/spec/ogcapi-common-2/1.0/conf/collections',
            'http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/core'
    ]
}
```

### Background

If you look at the definition of [ConformanceModel](https://github.com/KNMI/edr-pydantic/blob/791c6f7dd3b55b1f8ba93989bbe97d0f38f76ba9/src/edr_pydantic/capabilities.py#L37), you can see that it defines a parameter `conformsTo`, with a list of strings.
