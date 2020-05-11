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

from typing import List, Union

from .namespaces import OWS, ns_xlink
from ..types import (
    ServiceCapabilities, Operation, Constraint,
    WGS84BoundingBox, BoundingBox, Metadata,
    OWSException, Version
)
from ...util import Result
from ...xml import Comment, Element


def reference_attrs(href=None, type=None, role=None, arcrole=None, title=None,
                    about=None):
    attrs = [
        (ns_xlink('href'), href),
        (ns_xlink('type'), type),
        (ns_xlink('role'), role),
        (ns_xlink('arcrole'), arcrole),
        (ns_xlink('title'), title),
        (ns_xlink('about'), about),
    ]
    return {
        name: value
        for name, value in attrs
        if value is not None
    }


def encode_service_identification(capabilities: ServiceCapabilities):
    elem = OWS('ServiceIdentification',
        OWS('Title', capabilities.title) if capabilities.title else None,
        OWS('Abstract',
            capabilities.abstract
        ) if capabilities.abstract else None,
        OWS('Keywords', *[
            OWS('Keyword', keyword)
            for keyword in capabilities.keywords
        ]) if capabilities.keywords else None,
        OWS('ServiceType',
            capabilities.service_type, codeSpace='OGC'
        ) if capabilities.service_type else None
    )

    elem.extend(
        OWS('ServiceTypeVersion', version)
        for version in capabilities.service_type_versions
    )

    elem.extend(
        OWS('Profile', profile)
        for profile in capabilities.profiles
    )

    if capabilities.fees:
        elem.append(OWS('Fees', capabilities.fees))

    elem.extend([
        OWS('AccessConstraints', access_constraint)
        for access_constraint in capabilities.access_constraints
    ])

    return elem


def encode_service_provider(capabilities: ServiceCapabilities):
    return OWS('ServiceProvider',
        OWS('ProviderName',
            capabilities.provider_name
        ) if capabilities.provider_name else None,
        OWS('ProviderSite',
            **reference_attrs(href=capabilities.provider_site)
        ) if capabilities.provider_site else None,
        OWS('ServiceContact',
            OWS('IndividualName',
                capabilities.individual_name
            ) if capabilities.individual_name else None,
            OWS('PositionName',
                capabilities.position_name
            ) if capabilities.position_name else None,
            OWS('ContactInfo',
                OWS('Phone',
                    OWS('Voice',
                        capabilities.phone_voice
                    ) if capabilities.phone_facsimile else None,
                    OWS('Facsimile',
                        capabilities.phone_facsimile
                    ) if capabilities.phone_facsimile else None
                ) if capabilities.phone_facsimile
                     or capabilities.phone_facsimile else None,
                OWS('Address',
                    OWS('DeliveryPoint',
                        capabilities.delivery_point
                    ) if capabilities.delivery_point else None,
                    OWS('City',
                        capabilities.city
                    ) if capabilities.city else None,
                    OWS('AdministrativeArea',
                        capabilities.administrative_area
                    ) if capabilities.administrative_area else None,
                    OWS('PostalCode',
                        capabilities.postal_code
                    ) if capabilities.postal_code else None,
                    OWS('Country',
                        capabilities.country
                    ) if capabilities.country else None,
                    OWS(
                        'ElectronicMailAddress',
                        capabilities.electronic_mail_address
                    ) if capabilities.electronic_mail_address else None
                ) if capabilities.delivery_point
                     or capabilities.city
                     or capabilities.administrative_area
                     or capabilities.postal_code
                     or capabilities.country
                     or capabilities.electronic_mail_address else None,
                OWS('OnlineResource',
                    **reference_attrs(href=capabilities.online_resource),
                ) if capabilities.online_resource else None,
                OWS('HoursOfService',
                    capabilities.hours_of_service
                ) if capabilities.hours_of_service else None,
                OWS('ContactInstructions',
                    capabilities.contact_instructions
                ) if capabilities.contact_instructions else None,
            ),
            OWS('Role', capabilities.role) if capabilities.role else None
        )
    )


def encode_constraints(constraints: List[Constraint]):
    return [
        OWS('Constraint',
            OWS('AllowedValues', *[
                OWS('Value',
                    value
                )
                if isinstance(value, str) else
                OWS('ValueRange',
                    OWS('MinimumValue', value[0]),
                    OWS('MaximumValue', value[1]),
                    OWS('Spacing', value[2]),
                )
                for value in constraint.allowed_values
            ])
            if constraint.allowed_values else
            OWS('NoValue'),
            name=constraint.name
        )
        for constraint in constraints
    ]


def encode_operation(operation: Operation):
    return OWS('Operation',
        OWS('DCP',
            OWS('HTTP', *[
                OWS(operation_method.method.value.capitalize(),
                    *encode_constraints(operation_method.constraints),
                    **reference_attrs(href=operation_method.service_url)
                )
                for operation_method in operation.operation_methods
            ])
        ),
        *encode_constraints(operation.constraints),
        name=operation.name,
    )


def encode_operations_metadata(capabilities: ServiceCapabilities):
    return OWS('OperationsMetadata', *[
        encode_operation(operation)
        for operation in capabilities.operations
    ])


def encode_wgs84_bounding_box(bbox: WGS84BoundingBox):
    dim = int(len(bbox.bbox) / 2)
    return OWS('WGS84BoundingBox',
        OWS('LowerCorner',
            ' '.join(str(v) for v in bbox.bbox[:dim])
        ),
        OWS('UpperCorner',
            ' '.join(str(v) for v in bbox.bbox[dim:])
        ),
        dimension=str(dim)
    )

def encode_bounding_box(bbox: BoundingBox):
    dim = int(len(bbox.bbox) / 2)
    return OWS('BoundingBox',
        OWS('LowerCorner',
            ' '.join(str(v) for v in bbox.bbox[:dim])
        ),
        OWS('UpperCorner',
            ' '.join(str(v) for v in bbox.bbox[dim:])
        ),
        dimension=str(dim),
        crs=bbox.crs,
    )


def encode_metadata(metadata: Metadata):
    return OWS('Metadata',
        **reference_attrs(
            href=metadata.href,
            type='simple',
            role=metadata.role,
            arcrole=metadata.arcrole,
            title=metadata.title,
            about=metadata.about,
        )
    )


def encode_exception(exception: OWSException) -> Element:
    texts = [exception.text] if isinstance(exception.text, str) else exception.text
    return OWS('Exception', *[
            OWS('ExceptionText', text)
            for text in texts
        ] if texts is not None else [] + [
            Comment(exception.traceback) if exception.traceback else None
        ],
        exceptionCode=exception.code,
        locator=exception.locator
    )


def xml_encode_exception_report(exception: Union[OWSException, List[OWSException]], version: Version) -> Result:
    exceptions = [exception] if isinstance(exception, OWSException) else exception
    return Result.from_etree(
        OWS('ExceptionReport', *[
                encode_exception(exception)
                for exception in exceptions
            ],
            version=str(version)
        )
    )
