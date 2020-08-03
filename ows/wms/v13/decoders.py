# -------------------------------------------------------------------------------
#
# Project: pyows <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
# -------------------------------------------------------------------------------
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
# -------------------------------------------------------------------------------

from functools import partial

from ows import kvp
from ows.decoder import typelist
from ows.util import Version, parse_temporal
from ows.exceptions import InvalidRequestException
from ..types import GetMapRequest, GetFeatureInfoRequest, BoundingBox, Range


def parse_bbox(value):
    try:
        bbox = [float(v) for v in value.split(",")]
    except ValueError:
        raise InvalidRequestException("Invalid 'BBOX' parameter.", "bbox")

    if len(bbox) != 4:
        raise InvalidRequestException(
            "Wrong number of arguments for 'BBOX' parameter.", "bbox"
        )

    return bbox


def parse_styles(value):
    if not value:
        return None

    return [
        part or None
        for part in value.split(',')
    ]


def parse_dimension(raw_value, value_parser=None, resolution_parser=None):
    dim_values = []
    # allow a list of multiple dimension values as per C2
    for dimension_item in raw_value.split(','):
        values = dimension_item.split('/')
        if value_parser:
            values = [
                value_parser(value) for value in values[:2]
            ] + [
                resolution_parser(value) if resolution_parser else value
                for value in values[2:3]
            ]

        if len(values) > 1:
            dim_values.append(Range(*values))
        else:
            dim_values.append(values[0])

    # unpack single items
    if len(dim_values) == 1:
        return dim_values[0]

    return dim_values


def parse_booloean(value):
    value = value.upper()
    if value == 'TRUE':
        return True
    elif value == 'FALSE':
        return False
    raise ValueError("Invalid value for 'transparent' parameter.")


# ------------------------------------------------------------------------------
# GetMap
# ------------------------------------------------------------------------------


class KVPGetMapDecoder(kvp.Decoder):
    object_class = GetMapRequest

    version = kvp.Parameter(type=Version.from_str, num=1)
    layers = kvp.Parameter(type=typelist(str, ','), num=1)
    styles = kvp.Parameter(type=parse_styles, num=1)
    width = kvp.Parameter(type=int, num=1)
    height = kvp.Parameter(type=int, num=1)
    format = kvp.Parameter(num=1)
    background_color = kvp.Parameter('bgcolor', num='?')
    transparent = kvp.Parameter(num='?', type=parse_booloean)

    bbox = kvp.Parameter('bbox', type=parse_bbox, num=1)
    crs = kvp.Parameter(num=1)

    time = kvp.Parameter(type=partial(parse_dimension, value_parser=parse_temporal), num='?') # noqa
    elevation = kvp.Parameter(type=partial(parse_dimension, value_parser=float, resolution_parser=float), num='?') # noqa

    dimensions = kvp.MultiParameter(lambda name: name.startswith('dim_'), num='*') # noqa

    def map_params(self, params):
        params['bounding_box'] = BoundingBox(params.pop('crs'), params.pop('bbox'))
        params['dimensions'] = dict(
            (name[4:], parse_dimension(values[0]))
            for name, values in params.pop('dimensions') or []
        )
        return params


def kvp_decode_getmap(kvp):
    decoder = KVPGetMapDecoder(kvp)
    return decoder.decode()


# ------------------------------------------------------------------------------
# GetFeatureInfo
# ------------------------------------------------------------------------------


class KVPGetFeatureInfoDecoder(KVPGetMapDecoder):
    object_class = GetFeatureInfoRequest

    query_layers = kvp.Parameter(type=typelist(str, ','), num=1)
    info_format = kvp.Parameter(num=1)
    feature_count = kvp.Parameter(type=int, num='?')

    i = kvp.Parameter(type=int, num=1)
    j = kvp.Parameter(type=int, num=1)


def kvp_decode_getfeatureinfo(kvp):
    decoder = KVPGetFeatureInfoDecoder(kvp)
    return decoder.decode()
