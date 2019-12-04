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

# flake8: noq

import re

from ows import kvp, xml
from ows.decoder import typelist, enum, boolean
from ows.util import Version

from .namespaces import ns_wcs, ns_rsub, ns_scal, nsmap
from .exceptions import (
    InvalidSubsettingException, InvalidScaleFactorException,
    InvalidScaleExtentException,
)
from . import types


# ------------------------------------------------------------------------------
# DescribeCoverage
# ------------------------------------------------------------------------------


class KVPDescribeCoverageDecoder(kvp.Decoder):
    object_class = types.DescribeCoverageRequest
    version = kvp.Parameter(type=Version.from_str, num=1)
    coverage_ids = kvp.Parameter("coverageid", type=typelist(str, ","), num=1)


class XMLDescribeCoverageDecoder(xml.Decoder):
    object_class = types.DescribeCoverageRequest
    version = xml.Parameter("@version", type=Version.from_str, num=1)
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
    object_class = types.GetCoverageRequest

    def create_object(self, params):
        params['scales'] = (
            params.pop('scaleaxes') +
            params.pop('scalesize') +
            params.pop('scaleextent')
        )
        params['subsetting_crs'] = params.pop('subsettingcrs')
        params['output_crs'] = params.pop('outputcrs')
        params['range_subset'] = params.pop('rangesubset')

        params['geotiff_encoding_parameters'] = types.GeoTIFFEncodingParameters(
            compression=params.pop('geotiff_compression', None),
            jpeg_quality=params.pop('geotiff_jpeg_quality', None),
            predictor=params.pop('geotiff_predictor', None),
            interleave=params.pop('geotiff_interleave', None),
            tiling=params.pop('geotiff_tiling', None),
            tile_height=params.pop('geotiff_tileheight', None),
            tile_width=params.pop('geotiff_tilewidth', None),
        )

        return types.GetCoverageRequest(**params)


# ------------------------------------------------------------------------------
# GetCoverage - KVP
# ------------------------------------------------------------------------------


SUBSET_RE = re.compile(r'([a-zA-Z0-9_]+)\(([^,]*)(,([^)]*))?\)')
SCALEAXIS_RE = re.compile(r'([a-zA-Z0-9_]+)\(([^)]*)\)')
SCALESIZE_RE = SCALEAXIS_RE
SCALEEXTENT_RE = re.compile(r'([a-zA-Z0-9_]+)\(([^:]*):([^)]*)\)')


def parse_subset_value(string):
    if string == '*':
        return None
    elif string.startswith('"') and string.endswith('"'):
        return string[1:-1]
    else:
        return float(string)


def parse_subset_kvp(string):
    match = SUBSET_RE.match(string)

    if not match:
        raise InvalidSubsettingException(
            "Could not parse input subset string."
        )

    axis = match.group(1)
    try:
        if match.group(4) is not None:
            return types.Trim(
                axis,
                parse_subset_value(match.group(2)),
                parse_subset_value(match.group(4))
            )
        else:
            return types.Slice(axis, parse_subset_value(match.group(2)))
    except ValueError as exc:
        raise InvalidSubsettingException(
            "Could not parse input subset string."
        ) from exc


def parse_range_subset_kvp(string):
    rangesubset = []
    for item in string.split(","):
        if ":" in item:
            start, end = item.split(":")
            rangesubset.append(types.RangeInterval(start, end))
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

    return types.ScaleAxis(axis, value)


def parse_scalesize_kvp(string):
    match = SCALESIZE_RE.match(string)
    if not match:
        raise Exception("Could not parse input scale size string.")

    axis = match.group(1)
    try:
        value = int(match.group(2))
    except ValueError:
        raise InvalidScaleFactorException(match.group(2))

    return types.ScaleSize(axis, value)


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

    return types.ScaleExtent(axis, low, high)


compression_enum = enum(
    ("None", "PackBits", "Huffman", "LZW", "JPEG", "Deflate"), True
)
predictor_enum = enum(("None", "Horizontal", "FloatingPoint"), True)
interleave_enum = enum(("Pixel", "Band"), True)

def parse_multiple_16(raw):
    value = int(raw)
    if value < 0:
        raise ValueError("Value must be a positive integer.")
    elif (value % 16) != 0:
        raise ValueError("Value must be a multiple of 16.")
    return value


class KVPGetCoverageDecoder(GetCoverageBaseDecoder, kvp.Decoder):
    version = kvp.Parameter(type=Version.from_str, num=1)
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

    geotiff_compression = kvp.Parameter("geotiff:compression", num="?", type=compression_enum)
    geotiff_jpeg_quality = kvp.Parameter("geotiff:jpeg_quality", num="?", type=int)
    geotiff_predictor = kvp.Parameter("geotiff:predictor", num="?", type=predictor_enum)
    geotiff_interleave = kvp.Parameter("geotiff:interleave", num="?", type=interleave_enum)
    geotiff_tiling = kvp.Parameter("geotiff:tiling", num="?", type=boolean)
    geotiff_tileheight = kvp.Parameter("geotiff:tileheight", num="?", type=parse_multiple_16)
    geotiff_tilewidth = kvp.Parameter("geotiff:tilewidth", num="?", type=parse_multiple_16)


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
            return types.Trim(
                dimension,
                parse_subset_value(elem.findtext(ns_wcs("TrimLow"))),
                parse_subset_value(elem.findtext(ns_wcs("TrimHigh")))
            )
        elif elem.tag == ns_wcs("DimensionSlice"):
            return types.Slice(
                dimension,
                parse_subset_value(elem.findtext(ns_wcs("SlicePoint")))
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
            rangesubset.append(types.RangeInterval(
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

    return types.ScaleAxis(axis, value)


def parse_scalesize_xml(elem):
    axis = elem.findtext(ns_scal("axis"))
    try:
        raw = elem.findtext(ns_scal("targetSize"))
        value = int(raw)
    except ValueError:
        InvalidScaleFactorException(raw)

    return types.ScaleSize(axis, value)


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

    return types.ScaleExtent(axis, low, high)


class XMLGetCoverageDecoder(GetCoverageBaseDecoder, xml.Decoder):
    version = xml.Parameter("@version", type=Version.from_str, num=1)
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

    geotiff_compression = xml.Parameter("wcs:Extension/geotiff:parameters/geotiff:compression/text()", num="?", type=compression_enum, locator="geotiff:compression")
    geotiff_jpeg_quality = xml.Parameter("wcs:Extension/geotiff:parameters/geotiff:jpeg_quality/text()", num="?", type=int, locator="geotiff:jpeg_quality")
    geotiff_predictor = xml.Parameter("wcs:Extension/geotiff:parameters/geotiff:predictor/text()", num="?", type=predictor_enum, locator="geotiff:predictor")
    geotiff_interleave = xml.Parameter("wcs:Extension/geotiff:parameters/geotiff:interleave/text()", num="?", type=interleave_enum, locator="geotiff:interleave")
    geotiff_tiling = xml.Parameter("wcs:Extension/geotiff:parameters/geotiff:tiling/text()", num="?", type=boolean, locator="geotiff:tiling")
    geotiff_tileheight = xml.Parameter("wcs:Extension/geotiff:parameters/geotiff:tileheight/text()", num="?", type=parse_multiple_16, locator="geotiff:tileheight")
    geotiff_tilewidth = xml.Parameter("wcs:Extension/geotiff:parameters/geotiff:tilewidth/text()", num="?", type=parse_multiple_16, locator="geotiff:tilewidth")

    namespaces = nsmap


def kvp_decode_get_coverage(kvp):
    decoder = KVPGetCoverageDecoder(kvp)
    return decoder.decode()


def xml_decode_get_coverage(xml):
    decoder = XMLGetCoverageDecoder(xml)
    return decoder.decode()
