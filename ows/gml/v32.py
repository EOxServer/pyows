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


from typing import List

from ows.xml import ElementMaker, NameSpace, NameSpaceMap
from ows.util import isoformat
from ows.swe.v20 import Field, encode_data_record
from .types import Grid, RegularAxis, SpatioTemporalType


# namespace declarations
ns_gml = NameSpace("http://www.opengis.net/gml/3.2", "gml")
ns_gmlcov = NameSpace("http://www.opengis.net/gmlcov/1.0", "gmlcov")
ns_om = NameSpace("http://www.opengis.net/om/2.0", "om")
ns_eop = NameSpace("http://www.opengis.net/eop/2.0", "eop")

nsmap = NameSpaceMap(ns_gml, ns_gmlcov, ns_om, ns_eop)

# Element factories
GML = ElementMaker(namespace=ns_gml.uri, nsmap=nsmap)
GMLCOV = ElementMaker(namespace=ns_gmlcov.uri, nsmap=nsmap)
OM = ElementMaker(namespace=ns_om.uri, nsmap=nsmap)
EOP = ElementMaker(namespace=ns_eop.uri, nsmap=nsmap)


def encode_bounded_by(grid: Grid):
    spatial_axes = [axis for axis in grid.axes if axis.type == SpatioTemporalType.SPATIAL]
    temporal_axis = next(
        (axis for axis in grid.axes if axis.type == SpatioTemporalType.TEMPORAL),
        None
    )

    lower_coords, upper_coords = zip(*[axis.limits for axis in spatial_axes])
    lower_corner = GML('lowerCorner', ' '.join(str(v) for v in lower_coords))
    upper_corner = GML('upperCorner', ' '.join(str(v) for v in upper_coords))

    attrib = {
        'srsName': grid.srs,
        'srsDimension': str(len(spatial_axes)),
        'axisLabels': ' '.join(axis.label for axis in spatial_axes),
        'uomLabels': ' '.join(axis.uom for axis in spatial_axes),
        'frame': temporal_axis.uom if temporal_axis else None,
    }

    if temporal_axis:
        begin, end = temporal_axis.limits
        envelope = GML('EnvelopeWithTimePeriod',
            lower_corner,
            upper_corner,
            GML('beginPosition', begin if isinstance(begin, str) else isoformat(begin)),
            GML('endPosition', end if isinstance(end, str) else isoformat(end)),
            **attrib,
        )
    else:
        envelope = GML('Envelope',
            lower_corner,
            upper_corner,
            **attrib,
        )
    return GML('boundedBy', envelope)


def encode_time_period(begin_position, end_position, identifier):
    return GML('TimePeriod',
        GML('beginPosition', isoformat(begin_position)),
        GML('endPosition', isoformat(end_position)),
        **{
            ns_gml('id'): identifier
        }
    )


def encode_grid(grid: Grid, identifier: str):
    rectified = all(isinstance(axis, RegularAxis) for axis in grid.axes)
    num_axes = len(grid.axes)
    elem = GML('RectifiedGrid' if rectified else 'Grid',
        GML('identifier', identifier),
        GML('limits',
            GML('GridLimits',
                GML('low', ' '.join('0' for _ in grid.axes)),
                GML('high', ' '.join(str(axis.size) for axis in grid.axes)),
            )
        ),
        GML('axisLabels', ' '.join(axis.label for axis in grid.axes)),
        **{
            ns_gml('id'): identifier,
            'dimension': str(num_axes),
            'srsName': grid.srs,
            'uomLabels': ' '.join(axis.uom for axis in grid.axes)
        }
    )

    if rectified:
        elem.append(
            GML('origin',
                ' '.join(str(axis.lower_bound) for axis in grid.axes)
            )
        )
        elem.extend([
            GML('offsetVector',
                ' '.join(
                    str(v)
                    for v in (
                        [0.0] * i + [axis.resolution] + [0.0] * (num_axes - i - 1)
                    )
                )
            ) for i, axis in enumerate(grid.axes)
        ])

    return elem


def encode_domain_set(grid: Grid, identifier: str):
    return GML('domainSet', encode_grid(grid, identifier))


def encode_range_type(range_type: List[Field]):
    return GMLCOV('rangeType',
        encode_data_record(range_type)
    )
