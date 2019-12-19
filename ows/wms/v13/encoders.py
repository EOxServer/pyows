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

from datetime import date, datetime, timedelta

from ows.util import Result, isoformat, duration
from ..types import (
    ServiceCapabilities, Operation, Layer, Style,
    Dimension, Range, GetMapRequest,
    DimensionValueType, DimensionResolutionType
)
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
    return WMS(operation.name, *[
            WMS('Format', frmt)
            for frmt in operation.formats
        ] + [
            WMS('DCPType',
                WMS('HTTP', *[
                    WMS(operation_method.method.value.capitalize(),
                        WMS('OnlineResource',
                            **reference_attrs(
                                href=operation_method.service_url
                            )
                        )
                    )
                    for operation_method in operation.operation_methods
                ])
            )
        ]
    )


def encode_boolean(value: bool):
    if value is None:
        return None
    return 'true' if value else 'false'


def encode_dimension_value(value: DimensionValueType):
    if isinstance(value, str):
        return value

    elif isinstance(value, datetime):
        return isoformat(value)

    return str(value)


def encode_dimension_resolution(value: DimensionResolutionType):
    if isinstance(value, timedelta):
        return duration(value)
    return str(value)


def encode_dimension(dimension: Dimension):
    value = None
    if isinstance(dimension.values, list):
        value = ','.join(
            encode_dimension_value(v) for v in dimension.values
        )
    elif isinstance(dimension.values, Range):
        value = '/'.join([
            encode_dimension_value(dimension.values.start),
            encode_dimension_value(dimension.values.stop),
            encode_dimension_resolution(dimension.values.resolution),
        ])
    return WMS('Dimension',
        value,
        name=dimension.name,
        units=dimension.units,
        unitSymbol=dimension.unit_symbol,
        default=dimension.default,
        multipleValues=encode_boolean(dimension.multiple_values),
        nearestValue=encode_boolean(dimension.nearest_value),
        current=encode_boolean(dimension.current),
    )


def encode_style(style: Style):
    return WMS('Style',
        WMS('Name', style.name),
        WMS('Title', style.title),
        WMS('Abstract', style.abstract) if style.abstract else None,
        *[
            WMS('LegendURL',
                WMS('Format', legend_url.format),
                WMS('OnlineResource', **reference_attrs(
                    href=legend_url.href
                )),
                width=str(legend_url.width),
                height=str(legend_url.height),
            ) for legend_url in style.legend_urls
        ] + [
            WMS('StyleSheetURL',
                WMS('Format', style.style_sheet_url.format),
                WMS('OnlineResource', **reference_attrs(
                    href=style.style_sheet_url.href
                )),
            ) if style.style_sheet_url else None,
            WMS('StyleURL',
                WMS('Format', style.style_url.format),
                WMS('OnlineResource', **reference_attrs(
                    href=style.style_url.href
                )),
            ) if style.style_url else None,
        ]

    )


def encode_layer(layer: Layer):
    return WMS('Layer',
        WMS('Name', layer.name) if layer.name else None,
        WMS('Title', layer.title),
        WMS('Abstract', layer.abstract) if layer.abstract else None,
        WMS('KeywordList', *[
            WMS('Keyword', keyword)
            for keyword in layer.keywords
        ]) if layer.keywords else None, *[
            WMS('CRS', crs)
            for crs in layer.crss
        ] + [
            WMS('EX_GeographicBoundingBox',
                WMS('westBoundLongitude',
                    str(layer.wgs84_bounding_box.bbox[0])
                ),
                WMS('eastBoundLongitude',
                    str(layer.wgs84_bounding_box.bbox[2])
                ),
                WMS('southBoundLatitude',
                    str(layer.wgs84_bounding_box.bbox[1])
                ),
                WMS('northBoundLatitude',
                    str(layer.wgs84_bounding_box.bbox[3])
                ),
            ) if layer.wgs84_bounding_box else None
        ] + [
            WMS('BoundingBox',
                minx=str(bounding_box.bbox[0]),
                miny=str(bounding_box.bbox[1]),
                maxx=str(bounding_box.bbox[2]),
                maxy=str(bounding_box.bbox[3]),
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
            WMS('MetadataURL',
                WMS('Format', metadata_url.format),
                WMS('OnlineResource', **reference_attrs(
                    href=metadata_url.href
                )),
                # type=metadata_url.type,
            )
            for metadata_url in layer.metadata_urls
        ] + [
            WMS('DataURL',
                WMS('Format', data_url.format),
                WMS('OnlineResource', **reference_attrs(
                    href=data_url.href
                )),
            )
            for data_url in layer.data_urls
        ] + [
            WMS('FeatureListURL',
                WMS('Format', feature_list_url.format),
                WMS('OnlineResource', **reference_attrs(
                    href=feature_list_url.href
                )),
            )
            for feature_list_url in layer.feature_list_urls
        ] + [
            encode_style(style)
            for style in layer.styles
        ] + [
            WMS('MinScaleDenominator',
                str(layer.min_scale_denominator)
            ) if layer.min_scale_denominator else None,
            WMS('MaxScaleDenominator',
                str(layer.max_scale_denominator)
            ) if layer.max_scale_denominator else None,
        ] + [
            encode_layer(sub_layer)
            for sub_layer in layer.layers
        ]
    )


def xml_encode_capabilities(capabilities: ServiceCapabilities, **kwargs):
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
            ),
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
            WMS('Request', *[
                encode_operation(operation)
                for operation in capabilities.operations
            ]),
            WMS('Exception', *[
                WMS('Format', exception_format)
                for exception_format in capabilities.exception_formats
            ]),
            encode_layer(capabilities.layer) if capabilities.layer else None,
        ),
        version=(
            str(capabilities.service_type_versions[0])
            if capabilities.service_type_versions else '1.3.0'
        ),
        updateSequence=capabilities.update_sequence
    )

    return Result.from_etree(root, **kwargs)


def kvp_encode_get_map_request(request: GetMapRequest, swap_coordinates=False):
    bbox = request.bounding_box.bbox
    if swap_coordinates:
        bbox = [bbox[1], bbox[0], bbox[3], bbox[2]]

    params = [
        ('service', 'WMS'),
        ('version', str(request)),
        ('request', 'GetMap'),
        ('layers', ','.join(request.layers)),
        ('styles', ','.join(request.styles)),
        ('crs', request.bounding_box.crs),
        ('bbox', ','.join(str(v) for v in bbox)),
        ('width', str(request.width)),
        ('height', str(request.height)),
        ('format', request.format),
    ]

    if request.transparent is not None:
        params.append(('transparent', str(request.transparent).upper()))
    if request.background_color is not None:
        params.append(('bgcolor', request.background_color))
    if request.exceptions is not None:
        params.append(('exceptions', request.exceptions))

    for name, value in request.dimensions.items():
        lower = name.lower()
        if lower in ('time', 'elevation'):
            params.append((lower, value))
        else:
            params.append((f'dim_{lower}', value))

    return Result.from_kvp(params)
