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

# # xflake8: noqa

from typing import List

from ows.util import Result
from .types import (
    DescribeCoverageRequest, GetCoverageRequest,
    Trim, Slice, ScaleSize, ScaleAxis, ScaleExtent
)
from .namespaces import WCS, SCAL, CRS, INT, EOWCS, GEOTIFF
from ..types import (
    ServiceCapabilities, CoverageSummary, DatasetSeriesSummary,
    CoverageDescription
)
from ows.common.v20.encoders import (
    OWS, encode_service_provider, encode_service_identification,
    encode_operations_metadata,
    encode_wgs84_bounding_box, encode_bounding_box, encode_metadata
)
from ows.gml.v32 import (
    ns_gml, encode_time_period, encode_bounded_by, encode_domain_set,
    encode_range_type
)


def kvp_encode_describe_coverage(request: DescribeCoverageRequest, **kwargs):
    return Result.from_kvp(
        dict(
            service='WCS',
            version=str(request.version),
            request='DescribeCoverage',
            coverageid=','.join(request.coverage_ids),
        ), **kwargs
    )


def xml_encode_describe_coverage(request: DescribeCoverageRequest, **kwargs):
    root = WCS('DescribeCoverage',
            *[
                WCS('CoverageId', identifier)
                for identifier in request.coverage_ids
            ],
            service='WCS',
            version=str(request.version),
        )
    return Result.from_etree(root, **kwargs)


def maybe_quote(value):
    if isinstance(value, (int, float)):
        return value
    else:
        return f"'{value}'"


def kvp_encode_get_coverage(request: GetCoverageRequest):
    params = [
        ('service', 'WCS'),
        ('version', str(request.version)),
        ('request', 'GetCoverage'),
        ('coverageid', request.coverage_id),
    ]

    for subset in request.subsets:
        if isinstance(subset, Trim):
            low = maybe_quote(subset.low) if subset.low is not None else '*'
            high = maybe_quote(subset.high) if subset.high is not None else '*'
            params.append(
                ('subset', f'{subset.dimension}({low},{high})')
            )
        elif isinstance(subset, Slice):
            params.append(
                ('subset', f'{subset.dimension}({maybe_quote(subset.point)})')
            )

    if request.format is not None:
        params.append(('format', request.format))

    if request.mediatype is not None:
        params.append(('mediaType', request.mediatype))

    if request.subsetting_crs is not None:
        params.append(('subsettingCrs', request.subsetting_crs))

    if request.output_crs is not None:
        params.append(('outputCrs', request.output_crs))

    scale_sizes = [
        scale for scale in request.scales
        if isinstance(scale, ScaleSize)
    ]
    scale_axes = [
        scale for scale in request.scales
        if isinstance(scale, ScaleAxis)
    ]
    scale_extents = [
        scale for scale in request.scales
        if isinstance(scale, ScaleExtent)
    ]

    if request.scalefactor:
        params.append(('scaleFactor', str(request.scalefactor)))
    if scale_sizes:
        params.append(('scaleSize', ','.join(
            f'{scale.axis}({scale.size})'
            for scale in scale_sizes
        )))
    if scale_axes:
        params.append(('scaleAxes', ','.join(
            f'{scale.axis}({scale.factor})'
            for scale in scale_axes
        )))
    if scale_extents:
        params.append(('scaleExtent', ','.join(
            f'{scale.axis}({scale.low}:{scale.high})'
            for scale in scale_extents
        )))

    if request.interpolation or request.axis_interpolations:
        if request.interpolation:
            params.append(('interpolation', request.interpolation))
        for axis_interpolation in request.axis_interpolations:
            axis = axis_interpolation.axis
            method = axis_interpolation.method
            params.append(
                ('interpolationPerAxis', f'{axis},{method}')
            )

    geotiff = request.geotiff_encoding_parameters
    if geotiff:
        if geotiff.compression is not None:
            params.append(
                ('geotiff:compression', geotiff.compression)
            )
        if geotiff.jpeg_quality:
            params.append(
                ('geotiff:jpeg_quality', geotiff.jpeg_quality)
            )

        if geotiff.predictor is not None:
            params.append(
                ('geotiff:predictor', geotiff.predictor)
            )

        if geotiff.interleave is not None:
            params.append(
                ('geotiff:interleave', geotiff.interleave)
            )

        if geotiff.tiling is not None:
            params.append(
                ('geotiff:tiling', str(geotiff.tiling).lower())
            )

        if geotiff.tile_width is not None:
            params.append(
                ('geotiff:tilewidth', str(geotiff.tile_width))
            )

        if geotiff.tile_height is not None:
            params.append(
                ('geotiff:tileheight', str(geotiff.tile_height))
            )

    return Result.from_kvp(params)


def xml_encode_get_coverage(request: GetCoverageRequest, **kwargs):
    root = WCS('GetCoverage',
        WCS('CoverageId', request.coverage_id),
        service='WCS',
        version=str(request.version),
    )

    for subset in request.subsets:
        if isinstance(subset, Trim):
            node = WCS('DimensionTrim',
                       WCS('Dimension', subset.dimension)
                       )
            if subset.low is not None:
                node.append(
                    WCS('TrimLow', str(subset.low))
                )
            if subset.high is not None:
                node.append(
                    WCS('TrimHigh', str(subset.high))
                )
            root.append(node)
        elif isinstance(subset, Slice):
            root.append(
                WCS('DimensionSlice',
                    WCS('Dimension', subset.dimension),
                    WCS('SlicePoint', str(subset.point))
                )
            )

    if request.format is not None:
        root.append(WCS('format', request.format))

    if request.mediatype is not None:
        root.append(WCS('mediaType', request.mediatype))

    extension_node = WCS('Extension')

    if request.subsetting_crs is not None:
        extension_node.append(CRS('subsettingCrs', request.subsetting_crs))

    if request.output_crs is not None:
        extension_node.append(CRS('outputCrs', request.output_crs))

    scale_sizes = [
        scale for scale in request.scales
        if isinstance(scale, ScaleSize)
    ]
    scale_axes = [
        scale for scale in request.scales
        if isinstance(scale, ScaleAxis)
    ]
    scale_extents = [
        scale for scale in request.scales
        if isinstance(scale, ScaleExtent)
    ]

    if request.scalefactor:
        extension_node.append(
            SCAL('ScaleByFactor',
                SCAL('scaleFactor', str(request.scalefactor))
            )
        )
    if scale_sizes:
        extension_node.append(
            SCAL('ScaleToSize', *[
                SCAL('TargetAxisSize',
                    SCAL('axis', scale.axis),
                    SCAL('targetSize', str(scale.size))
                )
                for scale in scale_sizes
            ])
        )
    if scale_axes:
        extension_node.append(
            SCAL('ScaleAxesByFactor', *[
                SCAL('ScaleAxis',
                    SCAL('axis', scale.axis),
                    SCAL('scaleFactor', str(scale.factor))
                )
                for scale in scale_axes
            ])
        )
    if scale_extents:
        extension_node.append(
            SCAL('ScaleToExtent', *[
                SCAL('TargetAxisExtent',
                    SCAL('axis', scale.axis),
                    SCAL('low', str(scale.low)),
                    SCAL('high', str(scale.high))
                )
                for scale in scale_extents
            ])
        )

    if request.interpolation or request.axis_interpolations:
        node = INT('Interpolation')
        if request.interpolation:
            node.append(INT('globalInterpolation', request.interpolation))
        for axis_interpolation in request.axis_interpolations:
            node.append(
                INT('InterpolationPerAxis',
                    INT('axis', axis_interpolation.axis),
                    INT('interpolationMethod', axis_interpolation.method),
                )
            )
        extension_node.append(node)

    geotiff = request.geotiff_encoding_parameters
    if geotiff:
        geotiff_node = GEOTIFF('parameters')
        if geotiff.compression is not None:
            geotiff_node.append(
                GEOTIFF('compression', geotiff.compression)
            )
        if geotiff.jpeg_quality:
            geotiff_node.append(
                GEOTIFF('jpeg_quality', geotiff.jpeg_quality)
            )

        if geotiff.predictor is not None:
            geotiff_node.append(
                GEOTIFF('predictor', geotiff.predictor)
            )

        if geotiff.interleave is not None:
            geotiff_node.append(
                GEOTIFF('interleave', geotiff.interleave)
            )

        if geotiff.tiling is not None:
            geotiff_node.append(
                GEOTIFF('tiling', str(geotiff.tiling).lower())
            )

        if geotiff.tile_width is not None:
            geotiff_node.append(
                GEOTIFF('tilewidth', str(geotiff.tile_width))
            )

        if geotiff.tile_height is not None:
            geotiff_node.append(
                GEOTIFF('tileheight', str(geotiff.tile_height))
            )

        if len(geotiff_node):
            extension_node.append(geotiff_node)

    if len(extension_node):
        root.append(extension_node)

    return Result.from_etree(root, **kwargs)


def encode_service_metadata(capabilities: ServiceCapabilities):
    service_metadata = WCS('ServiceMetadata', *[
        WCS('formatSupported', format_supported)
        for format_supported in capabilities.formats_supported
    ])

    if capabilities.crss_supported or capabilities.interpolations_supported:
        extension = WCS('Extension')
        if capabilities.crss_supported:
            extension.append(
                CRS("CrsMetadata", *[
                    CRS("crsSupported", crs_supported)
                    for crs_supported in capabilities.crss_supported
                ])
            )
        if capabilities.interpolations_supported:
            extension.append(
                INT("InterpolationMetadata", *[
                    INT("InterpolationSupported", interpolation_supported)
                    for interpolation_supported in capabilities.interpolations_supported
                ])
            )
        service_metadata.append(extension)

    return service_metadata


def encode_coverage_summary(coverage_summary: CoverageSummary):
    elem = WCS('CoverageSummary')
    if coverage_summary.title:
        elem.append(OWS('Title', coverage_summary.title))
    if coverage_summary.abstract:
        elem.append(OWS('Abstract', coverage_summary.abstract))
    if coverage_summary.keywords:
        elem.append(OWS('Keywords', *[
            OWS('Keyword', keyword)
            for keyword in coverage_summary.keywords
        ]))
    elem.extend(
        encode_wgs84_bounding_box(wgs84_bbox)
        for wgs84_bbox in coverage_summary.wgs84_bbox
    )
    elem.append(WCS('CoverageId', coverage_summary.identifier))
    elem.append(WCS('CoverageSubtype', coverage_summary.coverage_subtype))

    if coverage_summary.coverage_subtype_parent:
        elem.append(
            WCS('CoverageSubtypeParent',
                coverage_summary.coverage_subtype_parent
            )
        )

    elem.extend(
        encode_bounding_box(bbox)
        for bbox in coverage_summary.bbox
    )
    elem.extend(
        encode_metadata(metadata)
        for metadata in coverage_summary.metadata
    )
    return elem


def encode_dataset_series_summary(dataset_series_summary: DatasetSeriesSummary):
    elem = EOWCS('DatasetSeriesSummary')
    if dataset_series_summary.title:
        elem.append(OWS('Title', dataset_series_summary.title))
    if dataset_series_summary.abstract:
        elem.append(OWS('Abstract', dataset_series_summary.abstract))
    if dataset_series_summary.keywords:
        elem.append(OWS('Keywords', *[
            OWS('Keyword', keyword)
            for keyword in dataset_series_summary.keywords
        ]))

    elem.append(
        encode_wgs84_bounding_box(dataset_series_summary.wgs84_bbox)
    )
    elem.append(
        EOWCS('DatasetSeriesId', dataset_series_summary.identifier)
    )
    start, end = dataset_series_summary.time_period
    elem.append(
        encode_time_period(
            start, end, f'{dataset_series_summary.identifier}_timeperiod'
        )
    )
    elem.extend(
        encode_metadata(metadata)
        for metadata in dataset_series_summary.metadata
    )
    return elem


def xml_encode_capabilities(capabilities: ServiceCapabilities,
                            include_service_identification=True,
                            include_service_provider=True,
                            include_operations_metadata=True,
                            include_service_metadata=True,
                            include_coverage_summary=True,
                            include_dataset_series_summary=True,
                            **kwargs):
    sections = []
    if include_service_identification:
        sections.append(
            encode_service_identification(capabilities)
        )
    if include_service_provider:
        sections.append(
            encode_service_provider(capabilities)
        )
    if include_operations_metadata:
        sections.append(
            encode_operations_metadata(capabilities)
        )
    if include_service_metadata:
        sections.append(
            encode_service_metadata(capabilities)
        )
    if include_coverage_summary or include_dataset_series_summary:
        contents = WCS('Contents')
        if include_coverage_summary:
            contents.extend(
                encode_coverage_summary(coverage_summary)
                for coverage_summary in capabilities.coverage_summaries
            )
        if include_dataset_series_summary:
            contents.append(
                WCS('Extension', *[
                    encode_dataset_series_summary(dataset_series_summary)
                    for dataset_series_summary in capabilities.dataset_series_summaries
                ])
            )
        sections.append(contents)

    root = WCS('Capabilities',
        *sections,
        version="2.0.1",
        updateSequence=capabilities.update_sequence
    )

    return Result.from_etree(root, **kwargs)


def xml_encode_coverage_descriptions(coverage_descriptions: List[CoverageDescription], **kwargs):
    root = WCS('CoverageDescriptions', *[
        WCS('CoverageDescription',
            encode_bounded_by(coverage_description.grid),
            WCS('CoverageId', coverage_description.identifier),
            # TODO: metadata
            encode_domain_set(
                coverage_description.grid,
                f'{coverage_description.identifier}__grid'
            ),
            encode_range_type(coverage_description.range_type),
            WCS('ServiceParameters',
                WCS('CoverageSubtype', coverage_description.coverage_subtype),
                WCS('CoverageSubtype',
                    coverage_description.coverage_subtype_parent
                ) if coverage_description.coverage_subtype_parent else None,
                WCS('nativeFormat', coverage_description.native_format),
            ),
            **{
                ns_gml('id'): coverage_description.identifier
            }
        )
        for coverage_description in coverage_descriptions
    ])

    return Result.from_etree(root, **kwargs)
