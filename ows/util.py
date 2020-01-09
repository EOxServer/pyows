# -------------------------------------------------------------------------------
#
# Project: pyows <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
# -------------------------------------------------------------------------------
# Copyright (C) 2019 EOX IT Services GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -------------------------------------------------------------------------------

from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Any, Sequence, Dict, Union, Tuple
from urllib.parse import urlencode

from lxml import etree

from .xml import ElementTree


@dataclass(eq=True, order=True, frozen=True)
class Version:
    major: int
    minor: int
    patch: int = None

    def __post_init__(self):
        assert isinstance(self.major, int) and self.major >= 0
        assert isinstance(self.minor, int) and self.minor >= 0
        assert self.patch is None or (
            isinstance(self.patch, int) and self.patch >= 0
        )

    def __eq__(self, other):
        if isinstance(other, str):
            other = self.from_str(other)
        elif isinstance(other, Sequence):
            other = type(self)(*other)

        if self.major == other.major and self.minor == other.minor:
            if self.patch is not None and other.patch is not None:
                return self.patch == other.patch
            return True
        return False

    def __str__(self):
        if self.patch is not None:
            return f'{self.major}.{self.minor}.{self.patch}'
        return f'{self.major}.{self.minor}'

    @classmethod
    def from_str(cls, value: str):
        return cls(*[int(part) for part in value.split('.')])


ItemsLike = Union[Dict, Sequence[Tuple[str, str]]]


@dataclass
class Result:
    value: Any
    content_type: str = None

    @classmethod
    def from_kvp(cls, params: ItemsLike,
                 content_type='application/x-www-form-urlencoded'):
        return cls(
            value=urlencode(params),
            content_type=content_type
        )

    @classmethod
    def from_etree(cls, tree: ElementTree, content_type='application/xml',
                   **kwargs):
        return cls(
            value=etree.tostring(tree, **kwargs),
            content_type=content_type,
        )


def isoformat(dt: datetime, zulu=True) -> str:
    ''' Formats a datetime object to an ISO string. Timezone naive datetimes are
        are treated as UTC Zulu. UTC Zulu is expressed with the proper 'Z'
        ending and not with the '+00:00' offset declaration.

        :param dt: the :class:`datetime.datetime` to encode
        :param zulu: whether an offset of zero shall be abbreviated with ``Z``
        :returns: an encoded string
    '''
    if not dt.utcoffset() and zulu:
        dt = dt.replace(tzinfo=None)
        return dt.isoformat('T') + 'Z'
    return dt.isoformat('T')


def duration(td: timedelta) -> str:
    ''' Encode a timedelta as an ISO 8601 duration string.
    '''
    # TODO: better implementation with days, hours, minutes, seconds

    days = td.days or ''
    # hours = timedelta(seconds=td.seconds) // timedelta(hours=1)
    return f'P{days}T{td.seconds}S'
