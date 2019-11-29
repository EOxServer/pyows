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


from typing import Union, List, Tuple, Dict
from dataclasses import dataclass, field

from ows.xml import ElementMaker, NameSpace, NameSpaceMap
from ows.util import isoformat
from ows.swe.v20 import Field, encode_data_record
from .types import Grid, RegularAxis, IrregularAxis, IndexAxis


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
