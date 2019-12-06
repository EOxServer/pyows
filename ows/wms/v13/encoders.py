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

from ows.common.types import Operation
from ..types import ServiceCapabilities, Layer
from .namespaces import WMS, ns_xlink


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


def encode_operation(operation: Operation):
    return WMS(operation.name,
        # TODO: formats
        WMS('DCPType',
            WMS('HTTP', *[
                WMS(operation_method.method.value.capitalize(),
                    WMS('OnlineResource',
                        **reference_attrs(href=operation_method.service_url)
                    )
                )
                for operation_method in operation.operation_methods
            ])
        )
    )


def encode_layer(layer: Layer):
    return WMS('Layer',
        WMS('Name', layer.name) if layer.name else None,
        WMS('Title', layer.title),
        WMS('Abstract', layer.abstract) if layer.abstract else None,
        WMS('KeywordList', *[
            WMS('Keyword', keyword)
            for keyword in capabilities.keywords
        ]) if layer.keywords else None, *[
            WMS('CRS', crs)
            for crs in layer.crss
        ] + [
            WMS('EX_GeographicBoundingBox',
                # TODO
            ) if layer.wgs84_bounding_box else None
        ] + [
            WMS('BoundingBox',
                # TODO
            ) for bounding_box in layer.bounding_boxes
        ] + [
            encode_dimension(dimension)
            for dimension in layer.dimensions
        ] + [
            WMS('Attribution', layer.attribution)
            if layer.attribution else None
        ] + [
            WMS('AuthorityURL',
                WMS('OnlineResource', **reference_attrs(href=href)),
                name=name,
            )
            for name, href in layer.authority_urls.items()
        ] + [
            WMS('Identifier',
                identifier,
                authority=identifier,
            )
            for authority, identifier in layer.identifiers.items()
        ] + [
            # WMS('DataURL',
            #     WMS('OnlineResource', **reference_attrs(href=href)),
            #     authority=identifier,
            # )
            # for authority, identifier in layer.identifiers.items()
        ]
        # TODO
    )


def xml_encode_wms_capabilities(capabilities: ServiceCapabilities,
                                **kwargs):
    root = WMS('WMS_Capabilities',
        WMS('Service',
            WMS('Name', 'WMS'),
            WMS('Title', capabilities.title or ''),
            WMS('Abstract', capabilities.abstract),
            WMS('KeywordList', *[
                WMS('Keyword', keyword)
                for keyword in capabilities.keywords
            ]) if capabilities.keywords else None,
            WMS('OnlineResource', **{
                **reference_attrs(href=capabilities.online_resource)
            }) if capabilities.online_resource else None,
            WMS('ContactInformation',
                WMS('ContactPerson',
                    capabilities.individual_name
                ) if capabilities.individual_name else None,
                WMS('ContactOrganization',
                    capabilities.organisation_name
                ) if capabilities.organisation_name else None,
                WMS('ContactPosition',
                    capabilities.position_name
                ) if capabilities.position_name else None,
                WMS('ContactAddress',
                    WMS('AddressType', ''),
                    WMS('Address', capabilities.delivery_point or ''),
                    WMS('City', capabilities.city or ''),
                    WMS('StateOrProvince',
                        capabilities.administrative_area or ''
                    ),
                    WMS('PostCode', capabilities.postal_code or ''),
                    WMS('Country', capabilities.country or ''),
                ) if capabilities.delivery_point else None,
                WMS('ContactVoiceTelephone',
                    capabilities.phone_voice
                ) if capabilities.phone_voice else None,
                WMS('ContactFacsimileTelephone',
                    capabilities.phone_facsimile
                ) if capabilities.phone_facsimile else None,
                WMS('ContactElectronicMailAddress',
                    capabilities.electronic_mail_address
                ) if capabilities.electronic_mail_address else None,
            )
            WMS('Fees',
                capabilities.fees
            ) if capabilities.fees else None,
            WMS('AccessConstraints',
                capabilities.access_constraints[0]
            ) if capabilities.access_constraints else None,
            WMS('LayerLimit',
                str(capabilities.layer_limit)
            ) if capabilities.layer_limit is not None else None,
            WMS('MaxWidth',
                str(capabilities.max_width)
            ) if capabilities.max_width is not None else None,
            WMS('MaxHeight',
                str(capabilities.max_height)
            ) if capabilities.max_height is not None else None,
        ),
        WMS('Capability',
            WMS('Request',
                *encode_operation(operation)
                for operation in capabilities.operations
            ),
            WMS('Exception', *[
                WMS('Format', exception_format)
                for exception_format in capabilities.exception_formats
            ]),
            encode_layer(capabilities.layer),
        ),
        version=str(capabilities.service_type_versions[0]),
        updateSequence=capabilities.update_sequence
    )

    pass

