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

from ows import kvp
from ows.decoder import typelist


def parse_bbox(string):
    try:
        bbox = [float(v) for v in string.split(",")]
    except ValueError:
        raise InvalidParameterException("Invalid 'BBOX' parameter.", "bbox")

    if len(bbox) != 4:
        raise InvalidParameterException(
            "Wrong number of arguments for 'BBOX' parameter.", "bbox"
        )

    return bbox


def parse_time(string):
    items = string.split("/")

    if len(items) == 1:
        return [parse_iso8601(items[0])]
    elif len(items) in (2, 3):
        # ignore resolution
        return [parse_iso8601(items[0]), parse_iso8601(items[1])]

    raise InvalidParameterException("Invalid TIME parameter.", "time")


def parse_booloean(value):
    value = value.upper()
    if value == 'TRUE':
        return True
    elif value == 'FALSE':
        return False
    raise ValueError("Invalid value for 'transparent' parameter.")


class KVPGetMapDecoder(kvp.Decoder):
    layers = kvp.Parameter(type=typelist(str, ","), num=1)
    styles = kvp.Parameter(num="?")
    width = kvp.Parameter(num=1)
    height = kvp.Parameter(num=1)
    format = kvp.Parameter(num=1)
    bgcolor = kvp.Parameter(num='?')
    transparent = kvp.Parameter(num='?', default=False, type=parse_booloean)

    bbox = kvp.Parameter('bbox', type=parse_bbox, num=1)
    crs = kvp.Parameter(num=1)

    # time = kvp.Parameter(type=parse_time, num="?")
    # elevation = kvp.Parameter(type=float, num="?")
