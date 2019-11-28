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

from datetime import datetime
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

from lxml import etree


@dataclass
class Result:
    value: Any
    content_type: str = None

    @classmethod
    def from_kvp(cls, params,
                 content_type='application/x-www-form-urlencoded'):
        return cls(
            value=urlencode(params),
            content_type=content_type
        )

    @classmethod
    def from_etree(cls, tree, content_type='application/xml', **kwargs):
        return cls(
            value=etree.tostring(tree, **kwargs),
            content_type=content_type,
        )


def isoformat(dt: datetime, zulu=True):
    """ Formats a datetime object to an ISO string. Timezone naive datetimes are
        are treated as UTC Zulu. UTC Zulu is expressed with the proper "Z"
        ending and not with the "+00:00" offset declaration.

        :param dt: the :class:`datetime.datetime` to encode
        :returns: an encoded string
    """
    if not dt.utcoffset() and zulu:
        dt = dt.replace(tzinfo=None)
        return dt.isoformat("T") + "Z"
    return dt.isoformat("T")
