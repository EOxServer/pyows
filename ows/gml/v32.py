# ------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
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


from typing import Union, List, Tuple, Dict
from dataclasses import dataclass, field

from ows.xml import ElementMaker, NameSpace, NameSpaceMap
from ows.util import isoformat
from ows.swe.v20 import Field, encode_data_record


@dataclass
class Point:
    position: List[float]
    description: str = None
    identifier: str = None
    name: str = None


@dataclass
class Grid:
    identifier: str
    limits: Tuple[List[int], List[int]]
    axis_names: List[str]
    srs: str = None
    uom_labels: List[str] = None


@dataclass
class RectifiedGrid:
    identifier: str
    limits: Tuple[List[int], List[int]]
    origin: List[float]
    offsets: List[List[float]]
    axis_names: List[str]
    srs: str = None
    uom_labels: List[str] = None


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


def encode_bounded_by(grid):
    pass


def encode_time_period(begin_position, end_position, identifier):
    return GML('TimePeriod',
        GML('beginPosition', isoformat(begin_position)),
        GML('endPosition', isoformat(end_position)),
        **{
            ns_gml('id'): identifier
        }
    )


def encode_domain_set(grid: Union[Grid, RectifiedGrid]):
    low, high = grid.limits
    return GML('domainSet',
        GML('RectifiedGrid' if isinstance(grid, RectifiedGrid) else 'Grid',
            GML('identifier', grid.identifier),
            GML('limits',
                GML('GridLimits',
                    GML('low', ' '.join(str(v) for v in low)),
                    GML('high', ' '.join(str(v) for v in high)),
                )
            ),
            GML('axisLabels', ' '.join(grid.axis_names)),
            GML('origin',
                ' '.join(str(v) for v in grid.origin)
            ) if isinstance(grid, RectifiedGrid) else None,
            *([
                GML('offsetVector',
                    ' '.join(str(v) for v in offset_vector)
                ) for offset_vector in grid.offsets
            ] if isinstance(grid, RectifiedGrid) else []),
            **{
                ns_gml('id'): grid.identifier,
                'dimension': str(len(grid.axis_names)),
                'srsName': grid.srs,
                'uomLabels': ' '.join(grid.axis_names) if grid.axis_names else None
            }
        )
    )


def encode_range_type(range_type: List[Field]):
    return GMLCOV('rangeType',
        encode_data_record(range_type)
    )
