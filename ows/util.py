from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

from lxml import etree


@dataclass
class Result:
    value: Any
    content_type: str = None

    @classmethod
    def from_kvp(cls, params, content_type='application/x-www-form-urlencoded'):
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
