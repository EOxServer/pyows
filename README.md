# pyows
[![Build Status](https://github.com/EOxServer/pyows/actions/workflows/test.yaml/badge.svg)](https://github.com/EOxServer/pyows/actions/workflows/test.yaml)
[![PyPI version](https://badge.fury.io/py/pyows.svg)](https://badge.fury.io/py/pyows)
[![Documentation Status](https://readthedocs.org/projects/pyows/badge/?version=latest)](https://pyows.readthedocs.io/en/latest/?badge=latest)

`pyows` is a library to help building an OWS compatible service or client. It helps building requests and parsing them and also provides object types to be serialized and sent as responses.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pyows.

```bash
pip install pyows
```

## Usage

`pyows` can be used to both parse/encode OWS requests and to parse/encode objects for the various services.

Example: Parsing a WCS 2.0 GetCoverage request:

```python
>>> from ows.wcs.v20.decoders import xml_decode_get_coverage
>>>
>>> request = b"""<?xml version="1.0" encoding="UTF-8"?>
... <wcs:GetCoverage
...     xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
...     xsi:schemaLocation="http://www.opengis.net/wcs/2.0 http://schemas.opengis.net/wcs/2.0/wcsAll.xsd"
...     xmlns="http://www.opengis.net/wcs/2.0"
...     xmlns:wcs="http://www.opengis.net/wcs/2.0"
...     service="WCS"
...     version="2.0.1">
...     <wcs:CoverageId>a</wcs:CoverageId>
... </wcs:GetCoverage>
... """
>>> print(xml_decode_get_coverage(request))
GetCoverageRequest(coverage_id='a', format=None, mediatype=None, subsetting_crs=None, output_crs=None, subsets=[], scalefactor=None, scales=[], interpolation=None, axis_interpolations=[], range_subset=None)
```

The other way around:

```python
>>> from ows.wcs.v20 import GetCoverageRequest, Trim, Slice
>>> request = GetCoverageRequest(
...     coverage_id='a',
...     subsets=[
...         Trim(dimension='x', low=1.2, high=2.2),
...         Trim(dimension='y', low=3),
...         Slice(dimension='time', point='2018-05-07')
...     ]
... )
>>> print(xml_encode_get_coverage(request, pretty_print=True).value.decode('utf-8'))
<wcs:GetCoverage xmlns:crs="http://www.opengis.net/wcs/crs/1.0" xmlns:eop="http://www.opengis.net/eop/2.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmlcov="http://www.opengis.net/gmlcov/1.0" xmlns:int="http://www.opengis.net/wcs/interpolation/1.0" xmlns:ogc="http://www.opengis.net/ogc" xmlns:om="http://www.opengis.net/om/2.0" xmlns:ows="http://www.opengis.net/ows/2.0" xmlns:rsub="http://www.opengis.net/wcs/range-subsetting/1.0" xmlns:scal="http://www.opengis.net/wcs/scaling/1.0" xmlns:swe="http://www.opengis.net/swe/2.0" xmlns:wcs="http://www.opengis.net/wcs/2.0" xmlns:wcseo="http://www.opengis.net/wcs/wcseo/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" service="WCS" version="2.0.1">
  <wcs:CoverageId>a</wcs:CoverageId>
  <wcs:DimensionTrim>
    <wcs:Dimension>x</wcs:Dimension>
    <wcs:TrimLow>1.2</wcs:TrimLow>
    <wcs:TrimHigh>2.2</wcs:TrimHigh>
  </wcs:DimensionTrim>
  <wcs:DimensionTrim>
    <wcs:Dimension>y</wcs:Dimension>
    <wcs:TrimLow>3</wcs:TrimLow>
  </wcs:DimensionTrim>
  <wcs:DimensionSlice>
    <wcs:Dimension>time</wcs:Dimension>
    <wcs:SlicePoint>2018-05-07</wcs:SlicePoint>
  </wcs:DimensionSlice>
</wcs:GetCoverage>
```

### Currently supported OWS

- OWS common
    - 2.0:
        - Capabilities related encoding
- WCS
    - 2.0:
        - Request encoding/decoding for (both XML/KVP)
            - GetCapabilities
            - DescribeCoverage
            - GetCoverage
        - Response encoding
            - Capabilities
            - CoverageDescriptions
    - 2.1
        - Response encoding for
            - CoverageDescriptions
- WMS
    - 1.3:
        - Request encoding/decoding KVP
            - GetCapabilities
            - GetMap
            - GetFeatureInfo
        - Response encoding
            - Capabilities


## Roadmap

- Full support of WCS 2.x including EO-WCS application profile and all extensions
- Support for WPS 2.0 requests and responses
- Support for WMS request and responses for all versions

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
