# ------------------------------------------------------------------------------
#
# Project: pyows <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
# ------------------------------------------------------------------------------
# Copyright (C) 2019 EOX IT Services GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ------------------------------------------------------------------------------

# flake8: noqa

from textwrap import dedent
from urllib.parse import unquote

from lxml import etree

from .types import (
    DescribeCoverageRequest, GetCoverageRequest, GeoTIFFEncodingParameters
)
from .decoders import (
    kvp_decode_describe_coverage, xml_decode_describe_coverage,
    kvp_decode_get_coverage, xml_decode_get_coverage
)

# ------------------------------------------------------------------------------
# DescribeCoverage
# ------------------------------------------------------------------------------


def test_decode_describe_coverage_kvp():
    request = "service=WCS&version=2.0.1&request=DescribeCoverage&coverageid=a,b,c"
    assert kvp_decode_describe_coverage(request) == DescribeCoverageRequest(
        coverage_ids=['a', 'b', 'c']
    )


def test_decode_describe_coverage_xml():
    request = b"""<?xml version="1.0" encoding="UTF-8"?>
    <wcs:DescribeCoverage
        xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
        xsi:schemaLocation="http://www.opengis.net/wcs/2.0
            http://schemas.opengis.net/wcs/2.0/wcsAll.xsd"
        xmlns="http://www.opengis.net/wcs/2.0"
        xmlns:wcs="http://www.opengis.net/wcs/2.0"
        service="WCS"
        version="2.0.1">
        <wcs:CoverageId>a</wcs:CoverageId>
        <wcs:CoverageId>b</wcs:CoverageId>
        <wcs:CoverageId>c</wcs:CoverageId>
    </wcs:DescribeCoverage>
    """

    assert xml_decode_describe_coverage(request) == DescribeCoverageRequest(
        coverage_ids=['a', 'b', 'c']
    )

# ------------------------------------------------------------------------------
# GetCoverage
# ------------------------------------------------------------------------------


def test_decode_get_coverage_kvp():
    request = "service=WCS&version=2.0.1&request=GetCoverage&coverageid=a"
    assert kvp_decode_get_coverage(request) == GetCoverageRequest(
        coverage_id='a',
    )


def test_decode_get_coverage_xml():
    request = b"""<?xml version="1.0" encoding="UTF-8"?>
    <wcs:GetCoverage
        xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
        xsi:schemaLocation="http://www.opengis.net/wcs/2.0
            http://schemas.opengis.net/wcs/2.0/wcsAll.xsd"
        xmlns="http://www.opengis.net/wcs/2.0"
        xmlns:wcs="http://www.opengis.net/wcs/2.0"
        xmlns:wcscrs="http://www.opengis.net/wcs/crs/1.0"
        xmlns:scal="http://www.opengis.net/wcs/scaling/1.0"
        xmlns:int="http://www.opengis.net/wcs/interpolation/1.0"
        service="WCS"
        version="2.0.1">
        <wcs:CoverageId>a</wcs:CoverageId>
    </wcs:GetCoverage>
    """

    assert xml_decode_get_coverage(request) == GetCoverageRequest(
        coverage_id='a',
    )
