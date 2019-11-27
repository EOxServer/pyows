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
