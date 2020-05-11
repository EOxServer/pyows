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

from enum import Enum
from typing import List, Tuple, Union
from dataclasses import dataclass, field

from ows import Version


@dataclass
class BaseRequest:
    service: str
    request: str
    version: Version = None
    accept_versions: List[str] = field(default_factory=list)


@dataclass
class GetCapabilitiesRequest:
    service: str
    update_sequence: str = None
    sections: List[str] = field(default_factory=list)
    accept_versions: List[str] = field(default_factory=list)
    accept_languages: List[str] = field(default_factory=list)
    accept_formats: List[str] = field(default_factory=list)


@dataclass
class WGS84BoundingBox:
    bbox: List[float]


@dataclass
class BoundingBox:
    crs: str
    bbox: List[float]


@dataclass
class OnlineResource:
    href: str = None
    role: str = None
    arcrole: str = None
    title: str = None


@dataclass
class Metadata(OnlineResource):
    about: str = None


@dataclass
class Constraint:
    name: str
    allowed_values: List[Union[str, Tuple[str, str, str]]] = field(default_factory=dict)


class HttpMethod(Enum):
    Get = 'GET'
    Post = 'POST'


@dataclass
class OperationMethod:
    method: HttpMethod
    service_url: str = None
    constraints: List[Constraint] = field(default_factory=list)

    def __post_init__(self):
        # allow usage of string identifiers for the HTTP method here as well,
        # but convert to `HttpMethod`
        if isinstance(self.method, str):
            self.method = HttpMethod(self.method)


@dataclass
class Operation:
    name: str
    operation_methods: List[OperationMethod] = field(default_factory=lambda: [OperationMethod(method=HttpMethod.Get)])
    constraints: List[Constraint] = field(default_factory=list)


@dataclass
class ServiceCapabilities:
    update_sequence: str = None

    # ServiceIdentification fields
    title: str = None
    abstract: str = None
    keywords: List[str] = field(default_factory=list)
    service_type: str = ''
    service_type_versions: List[str] = field(default_factory=list)
    profiles: List[str] = field(default_factory=list)
    fees: str = None
    access_constraints: List[str] = field(default_factory=list)

    # ServiceProvider fields
    provider_name: str = ''
    provider_site: str = ''
    individual_name: str = None
    organisation_name: str = None
    position_name: str = None

    # ContactInfo fields
    phone_voice: str = None
    phone_facsimile: str = None

    # Address fields
    delivery_point: str = None
    city: str = None
    administrative_area: str = None
    postal_code: str = None
    country: str = None
    electronic_mail_address: str = None

    online_resource: str = None

    hours_of_service: str = None
    contact_instructions: str = None

    role: str = ''

    # OperationsMetadata fields
    operations: List[Operation] = field(default_factory=list)


@dataclass
class OWSException:
    code: str
    locator: str = None
    text: Union[str, List[str]] = None
    traceback: str = None
