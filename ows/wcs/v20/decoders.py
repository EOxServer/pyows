# ------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
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

import re

from ows import kvp, xml
from ows.base import typelist

from .namespaces import ns_wcs, ns_rsub, ns_scal, nsmap
from .exceptions import (
    InvalidSubsettingException, InvalidScaleFactorException,
    InvalidScaleExtentException,
)
from . import objects


# ------------------------------------------------------------------------------
# DescribeCoverage
# ------------------------------------------------------------------------------


class KVPDescribeCoverageDecoder(kvp.Decoder):
    object_class = objects.DescribeCoverageRequest
    coverage_ids = kvp.Parameter("coverageid", type=typelist(str, ","), num=1)


class XMLDescribeCoverageDecoder(xml.Decoder):
    object_class = objects.DescribeCoverageRequest
    coverage_ids = xml.Parameter("wcs:CoverageId/text()", num="+")
    namespaces = nsmap


def kvp_decode_describe_coverage(kvp):
    decoder = KVPDescribeCoverageDecoder(kvp)
    return decoder.decode()


def xml_decode_describe_coverage(xml):
    decoder = XMLDescribeCoverageDecoder(xml)
    return decoder.decode()

# ------------------------------------------------------------------------------
# GetCoverage
# ------------------------------------------------------------------------------


class GetCoverageBaseDecoder:
    object_class = objects.GetCoverageRequest

    def create_object(self, params):
        params['scales'] = (
            params.pop('scaleaxes') +
            params.pop('scalesize') +
            params.pop('scaleextent')
        )
        params['subsetting_crs'] = params.pop('subsettingcrs')
        params['output_crs'] = params.pop('outputcrs')
        params['range_subset'] = params.pop('rangesubset')

        return objects.GetCoverageRequest(**params)


# ------------------------------------------------------------------------------
# GetCoverage - KVP
# ------------------------------------------------------------------------------


SUBSET_RE = re.compile(r'(\w+)\(([^,]*)(,([^)]*))?\)')
SCALEAXIS_RE = re.compile(r'(\w+)\(([^)]*)\)')
SCALESIZE_RE = SCALEAXIS_RE
SCALEEXTENT_RE = re.compile(r'(\w+)\(([^:]*):([^)]*)\)')


def parse_subset_kvp(string):
    match = SUBSET_RE.match(string)
    if not match:
        raise InvalidSubsettingException(
            "Could not parse input subset string."
        )

    axis = match.group(1)
    try:
        if match.group(4) is not None:
            return objects.Trim(
                axis, float(match.group(2)), float(match.group(4))
            )
        else:
            return objects.Slice(axis, float(match.group(2)))
    except ValueError:
        raise InvalidSubsettingException(
            "Could not parse input subset string."
        )


def parse_range_subset_kvp(string):
    rangesubset = []
    for item in string.split(","):
        if ":" in item:
            start, end = item.split(":")
            rangesubset.append(objects.RangeInterval(start, end))
        else:
            rangesubset.append(item)

    return rangesubset


def parse_scaleaxis_kvp(string):
    match = SCALEAXIS_RE.match(string)
    if not match:
        raise Exception("Could not parse input scale axis string.")

    axis = match.group(1)
    try:
        value = float(match.group(2))
    except ValueError:
        raise InvalidScaleFactorException(match.group(2))

    return objects.ScaleAxis(axis, value)


def parse_scalesize_kvp(string):
    match = SCALESIZE_RE.match(string)
    if not match:
        raise Exception("Could not parse input scale size string.")

    axis = match.group(1)
    try:
        value = int(match.group(2))
    except ValueError:
        raise InvalidScaleFactorException(match.group(2))

    return objects.ScaleSize(axis, value)


def parse_scaleextent_kvp(string):
    match = SCALEEXTENT_RE.match(string)
    if not match:
        raise Exception("Could not parse input scale extent string.")

    axis = match.group(1)
    try:
        low = int(match.group(2))
        high = int(match.group(3))
    except ValueError:
        raise InvalidScaleFactorException(match.group(3))

    if low >= high:
        raise InvalidScaleExtentException(low, high)

    return objects.ScaleExtent(axis, low, high)


class KVPGetCoverageDecoder(GetCoverageBaseDecoder, kvp.Decoder):
    coverage_id = kvp.Parameter("coverageid", num=1)
    subsets = kvp.Parameter("subset", type=parse_subset_kvp, num="*")
    scalefactor = kvp.Parameter("scalefactor", type=float, num="?")
    scaleaxes = kvp.Parameter("scaleaxes", type=typelist(parse_scaleaxis_kvp, ","), default_factory=list, num="?")
    scalesize = kvp.Parameter("scalesize", type=typelist(parse_scalesize_kvp, ","), default_factory=list, num="?")
    scaleextent = kvp.Parameter("scaleextent", type=typelist(parse_scaleextent_kvp, ","), default_factory=list, num="?")
    rangesubset = kvp.Parameter("rangesubset", type=parse_range_subset_kvp, num="?")
    format = kvp.Parameter("format", num="?")
    subsettingcrs = kvp.Parameter("subsettingcrs", num="?")
    outputcrs = kvp.Parameter("outputcrs", num="?")
    mediatype = kvp.Parameter("mediatype", num="?")
    interpolation = kvp.Parameter("interpolation", num="?")


# ------------------------------------------------------------------------------
# GetCoverge - XML
# ------------------------------------------------------------------------------

def parse_subset_xml(elem):
    """ Parse one subset from the WCS 2.0 XML notation. Expects an lxml.etree
        Element as parameter.
    """

    try:
        dimension = elem.findtext(ns_wcs("Dimension"))
        if elem.tag == ns_wcs("DimensionTrim"):
            return objects.Trim(
                dimension,
                float(elem.findtext(ns_wcs("TrimLow"))),
                float(elem.findtext(ns_wcs("TrimHigh")))
            )
        elif elem.tag == ns_wcs("DimensionSlice"):
            return objects.Slice(
                dimension,
                float(elem.findtext(ns_wcs("SlicePoint")))
            )
    except Exception as e:
        raise InvalidSubsettingException(str(e))


def parse_range_subset_xml(elem):
    rangesubset = []
    for child in elem:
        item = child[0]
        if item.tag == ns_rsub("RangeComponent"):
            rangesubset.append(item.text)
        elif item.tag == ns_rsub("RangeInterval"):
            rangesubset.append(objects.RangeInterval(
                item.findtext(ns_rsub("startComponent")),
                item.findtext(ns_rsub("endComponent"))
            ))

    return rangesubset


def parse_scaleaxis_xml(elem):
    """ Parses the XML notation of a single scale axis.
    """

    axis = elem.findtext(ns_scal("axis"))
    try:
        raw = elem.findtext(ns_scal("scaleFactor"))
        value = float(raw)
    except ValueError:
        InvalidScaleFactorException(raw)

    return ScaleAxis(axis, value)


def parse_scalesize_xml(elem):
    axis = elem.findtext(ns_scal("axis"))
    try:
        raw = elem.findtext(ns_scal("targetSize"))
        value = int(raw)
    except ValueError:
        InvalidScaleFactorException(raw)

    return objects.ScaleSize(axis, value)


def parse_scaleextent_xml(elem):
    axis = elem.findtext(ns_scal("axis"))
    try:
        raw_low = elem.findtext(ns_scal("low"))
        raw_high = elem.findtext(ns_scal("high"))
        low = int(raw_low)
        high = int(raw_high)
    except ValueError:
        InvalidScaleFactorException(raw_high)

    if low >= high:
        raise InvalidScaleExtentException(low, high)

    return objects.ScaleExtent(axis, low, high)


class XMLGetCoverageDecoder(GetCoverageBaseDecoder, xml.Decoder):
    coverage_id = xml.Parameter("wcs:CoverageId/text()", num=1, locator="coverageid")
    subsets = xml.Parameter("wcs:DimensionTrim", type=parse_subset_xml, num="*", default_factory=list, locator="subset")
    scalefactor = xml.Parameter("wcs:Extension/scal:ScaleByFactor/scal:scaleFactor/text()", type=float, num="?", locator="scalefactor")
    scaleaxes = xml.Parameter("wcs:Extension/scal:ScaleByAxesFactor/scal:ScaleAxis", type=parse_scaleaxis_xml, num="*", default_factory=list, locator="scaleaxes")
    scalesize = xml.Parameter("wcs:Extension/scal:ScaleToSize/scal:TargetAxisSize", type=parse_scalesize_xml, num="*", default_factory=list, locator="scalesize")
    scaleextent = xml.Parameter("wcs:Extension/scal:ScaleToExtent/scal:TargetAxisExtent", type=parse_scaleextent_xml, num="*", default_factory=list, locator="scaleextent")
    rangesubset = xml.Parameter("wcs:Extension/rsub:RangeSubset", type=parse_range_subset_xml, num="?", locator="rangesubset")
    format = xml.Parameter("wcs:format/text()", num="?", locator="format")
    subsettingcrs = xml.Parameter("wcs:Extension/crs:subsettingCrs/text()", num="?", locator="subsettingcrs")
    outputcrs = xml.Parameter("wcs:Extension/crs:outputCrs/text()", num="?", locator="outputcrs")
    mediatype = xml.Parameter("wcs:mediaType/text()", num="?", locator="mediatype")
    interpolation = xml.Parameter("wcs:Extension/int:Interpolation/int:globalInterpolation/text()", num="?", locator="interpolation")

    namespaces = nsmap


def kvp_decode_get_coverage(kvp):
    decoder = KVPGetCoverageDecoder(kvp)
    return decoder.decode()


def xml_decode_get_coverage(xml):
    decoder = XMLGetCoverageDecoder(xml)
    return decoder.decode()
