from collections import defaultdict

from ows.util import Result
from .objects import (
    DescribeCoverageRequest, GetCoverageRequest,
    Trim, Slice, ScaleSize, ScaleAxis, ScaleExtent
)
from .namespaces import WCS, SCAL, CRS, INT


def kvp_encode_describe_coverage(request: DescribeCoverageRequest, **kwargs):
    return Result.from_kvp(
        dict(
            service='WCS',
            version="2.0.1",
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
               version="2.0.1",
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
        ('version', '2.0.1'),
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

    return Result.from_kvp(params)


def xml_encode_get_coverage(request: GetCoverageRequest, **kwargs):
    root = WCS('GetCoverage',
               WCS('CoverageId', request.coverage_id),
               service='WCS',
               version='2.0.1',
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
        root.append(node)

    if len(extension_node):
        root.append(extension_node)

    return Result.from_etree(root, **kwargs)
