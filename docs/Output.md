# Output

## Landing page

```json
{
  "title": "EDR isobaric from Grib",
  "description": "An EDR API for isobaric data from Grib files",
  "links": [
    {
      "href": "http://localhost:5000/",
      "rel": "self",
      "type": "application/json",
      "title": "Landing Page"
    },
    {
      "href": "http://localhost:5000/api",
      "rel": "service-desc",
      "type": "application/json",
      "title": "OpenAPI document"
    },
    {
      "href": "http://localhost:5000/conformance",
      "rel": "conformance",
      "type": "application/json",
      "title": "Conformance document"
    },
    {
      "href": "http://localhost:5000/collections",
      "rel": "data",
      "type": "application/json",
      "title": "Collections metadata in JSON"
    }
  ],
  "provider": {
    "name": "Meteorologisk institutt / The Norwegian Meteorological Institute",
    "url": "https://api.met.no/"
  },
  "contact": {
    "email": "weatherapi-adm@met.no",
    "phone": "+47.22963000",
    "address": "Henrik Mohns plass 1",
    "postalCode": "0313",
    "city": "Oslo",
    "country": "Norway"
  }
}
```

## Collections

```json
{
  "links": [
    {
      "href": "http://localhost:5000/collections",
      "hreflang": "en",
      "rel": "self",
      "type": "aplication/json"
    }
  ],
  "collections": [
    {
      "id": "isobaric",
      "title": "IsobaricGRIB - GRIB files",
      "description": "These files are used by Avinor ATM systems but possibly also of interest to others. They contain temperature and wind forecasts for a set of isobaric layers (i.e. altitudes having the same pressure). The files are (normally) produced every 6 hours. You can check the time when generated using the Last-Modified header or the `updated` key in `available`. These files are in GRIB2 format (filetype BIN) for the following regions: southern_norway    Area 64.25N -1.45W 55.35S 14.51E, resolution .1 degrees? (km?) FIXME    It includes every odd-numbered isobaric layer from 1 to 137 (in hundreds of feet?)",
      "keywords": [
        "position",
        "data",
        "api",
        "temperature",
        "wind",
        "forecast",
        "isobaric"
      ],
      "links": [
        {
          "href": "http://localhost:5000/collections/isobaric/",
          "rel": "data"
        }
      ],
      "extent": {
        "spatial": {
          "bbox": [
            [
              -1.4499999999999886,
              55.35,
              14.449999999999964,
              64.25000000000011
            ]
          ],
          "crs": "GEOGCS[\"Unknown\", DATUM[\"Unknown\", SPHEROID[\"WGS_1984\", 6378137.0, 298.257223563]], PRIMEM[\"Greenwich\",0], UNIT[\"degree\", 0.017453], AXIS[\"Lon\", EAST], AXIS[\"Lat\", NORTH]]"
        },
        "temporal": {
          "interval": [
            [
              "2024-01-23T06:00:00Z",
              "2024-01-23T18:00:00Z"
            ]
          ],
          "values": [
            "2024-01-23T06:00:00+00:00"
          ],
          "trs": "TIMECRS[\"DateTime\",TDATUM[\"Gregorian Calendar\"],CS[TemporalDateTime,1],AXIS[\"Time (T)\",future]"
        },
        "vertical": {
          "interval": [
            [
              "850.0"
            ],
            [
              "100.0"
            ]
          ],
          "values": [
            "850.0",
            "750.0",
            "700.0",
            "600.0",
            "500.0",
            "450.0",
            "400.0",
            "350.0",
            "300.0",
            "275.0",
            "250.0",
            "225.0",
            "200.0",
            "150.0",
            "100.0"
          ],
          "vrs": "Vertical Reference System: PressureLevel"
        }
      },
      "data_queries": {
        "position": {
          "link": {
            "href": "http://localhost:5000/collections/isobaric/position",
            "rel": "data",
            "variables": {
              "query_type": "position",
              "output_formats": [
                "CoverageJSON"
              ]
            }
          }
        }
      },
      "crs": [
        "CRS:84"
      ],
      "parameter_names": {
        "wind_from_direction": {
          "type": "Parameter",
          "id": "wind_from_direction",
          "unit": {
            "symbol": {
              "value": "˚",
              "type": "https://codes.wmo.int/common/unit/_degree_(angle)"
            }
          },
          "observedProperty": {
            "id": "http://vocab.met.no/CFSTDN/en/page/wind_from_direction",
            "label": "Wind from direction"
          }
        },
        "wind_speed": {
          "type": "Parameter",
          "observedProperty": {
            "id": "http://vocab.met.no/CFSTDN/en/page/wind_speed",
            "label": "Wind speed"
          }
        },
        "Air temperature": {
          "type": "Parameter",
          "id": "Temperature",
          "unit": {
            "symbol": {
              "value": "˚C",
              "type": "https://codes.wmo.int/common/unit/_Cel"
            }
          },
          "observedProperty": {
            "id": "http://vocab.met.no/CFSTDN/en/page/air_temperature",
            "label": "Air temperature"
          }
        }
      }
    }
  ]
}
```

## Isobaric data

```json
{
  "id": "isobaric",
  "type": "Coverage",
  "domain": {
    "type": "Domain",
    "domainType": "VerticalProfile",
    "axes": {
      "x": {
        "values": [
          11.9384
        ]
      },
      "y": {
        "values": [
          60.1699
        ]
      },
      "z": {
        "values": [
          850,
          750,
          700,
          600,
          500,
          450,
          400,
          350,
          300,
          275,
          250,
          225,
          200,
          150,
          100
        ]
      },
      "t": {
        "values": [
          "2024-01-23T06:00:00Z"
        ]
      }
    },
    "referencing": [
      {
        "coordinates": [
          "x",
          "y"
        ],
        "system": {
          "type": "GeographicCRS",
          "id": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
        }
      },
      {
        "coordinates": [
          "z"
        ],
        "system": {
          "type": "VerticalCRS",
          "cs": {
            "csAxes": [
              {
                "name": {
                  "en": "Pressure"
                },
                "direction": "down",
                "unit": {
                  "symbol": "hPa"
                }
              }
            ]
          }
        }
      },
      {
        "coordinates": [
          "t"
        ],
        "system": {
          "type": "TemporalRS",
          "calendar": "Gregorian"
        }
      }
    ]
  },
  "parameters": {
    "temperature": {
      "type": "Parameter",
      "id": "temperature",
      "label": {
        "en": "Air temperature"
      },
      "observedProperty": {
        "id": "http://vocab.met.no/CFSTDN/en/page/air_temperature",
        "label": {
          "en": "Air temperature"
        }
      },
      "unit": {
        "id": "https://codes.wmo.int/common/unit/_Cel",
        "label": {
          "en": "degree Celsius"
        },
        "symbol": "˚C"
      }
    },
    "wind_from_direction": {
      "type": "Parameter",
      "id": "wind_from_direction",
      "label": {
        "en": "Wind from direction"
      },
      "observedProperty": {
        "id": "http://vocab.met.no/CFSTDN/en/page/wind_from_direction",
        "label": {
          "en": "wind_from_direction"
        }
      },
      "unit": {
        "id": "https://codes.wmo.int/common/unit/_degree_(angle)",
        "label": {
          "en": "degree"
        },
        "symbol": "˚"
      }
    },
    "wind_speed": {
      "type": "Parameter",
      "id": "wind_speed",
      "label": {
        "en": "Wind speed"
      },
      "observedProperty": {
        "id": "http://vocab.met.no/CFSTDN/en/page/wind_speed",
        "label": {
          "en": "Wind speed"
        }
      },
      "unit": {
        "id": "https://codes.wmo.int/common/unit/_m_s-1",
        "label": {
          "en": "metres per second"
        },
        "symbol": "m/s"
      }
    }
  },
  "ranges": {
    "temperature": {
      "type": "NdArray",
      "dataType": "float",
      "axisNames": [
        "z"
      ],
      "shape": [
        15
      ],
      "values": [
        -0.83,
        -8.36,
        -12.52,
        -19.94,
        -21.66,
        -26.33,
        -32.41,
        -40.13,
        -48.39,
        -53.21,
        -58,
        -61.11,
        -62.03,
        -60.65,
        -64.1
      ]
    },
    "wind_from_direction": {
      "type": "NdArray",
      "dataType": "float",
      "axisNames": [
        "z"
      ],
      "shape": [
        15
      ],
      "values": [
        199.11,
        227.14,
        241.95,
        267.74,
        293.07,
        290.3,
        292.93,
        293.15,
        293.72,
        290.9,
        289.35,
        289.48,
        295.85,
        289.76,
        286.36
      ]
    },
    "wind_speed": {
      "type": "NdArray",
      "dataType": "float",
      "axisNames": [
        "z"
      ],
      "shape": [
        15
      ],
      "values": [
        3.51,
        9.35,
        9.85,
        10.77,
        22.59,
        25.45,
        26.38,
        32.48,
        42.14,
        48.35,
        55.01,
        63.15,
        49.84,
        31.99,
        29.79
      ]
    }
  }
}
```
