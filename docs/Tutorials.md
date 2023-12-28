# Tutorials

## EDR-Pydantic - return a conformance page

### Create a venv and install necessary tools

- python3 -m venv venv
- source venv/bin/activate
- pip install edr-pydantic

### Paste in this code

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

This should return a simple, json output:

```json
{
    'conformsTo': [
            'http://www.opengis.net/spec/ogcapi-common-1/1.0/conf/core',
            'http://www.opengis.net/spec/ogcapi-common-2/1.0/conf/collections',
            'http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/core'
    ]
}
```
