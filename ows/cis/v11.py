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

from datetime import datetime, date, timedelta
from typing import List, Union
from dataclasses import dataclass

from ows.xml import ElementMaker, NameSpace, NameSpaceMap
from ows.util import isoformat
from ows.swe.v20 import Field, encode_data_record
from ows.gml.types import (
    PositionType, AxisType,
    Grid, IndexAxis, RegularAxis, IrregularAxis
)

ns_cis = NameSpace('http://www.opengis.net/cis/1.1/gml', 'cis')
nsmap = NameSpaceMap(ns_cis)

CIS = ElementMaker(namespace=ns_cis.uri, nsmap=nsmap)


def encode_position_value(value: PositionType):
    if isinstance(value, str):
        return value

    elif isinstance(value, datetime):
        return isoformat(value)

    return str(value)


def encode_axis_extent(axis: AxisType):
    return CIS('AxisExtent',
        axisLabel=axis.label,
        uomLabel=axis.uom,
        lowerBound=encode_position_value(
            axis.lower_bound
            if isinstance(axis, RegularAxis) else
            axis.positions[0]
        ),
        upperBound=encode_position_value(
            axis.upper_bound
            if isinstance(axis, RegularAxis) else
            axis.positions[-1]
        ),
    )


def encode_envelope(grid: Grid):
    return CIS('Envelope',
        *[
            encode_axis_extent(axis)
            for axis in grid.axes
        ],
        srsName=grid.srs,
        axisLabels=' '.join(axis.label for axis in grid.axes),
        srsDimension=str(len(grid.axes)),
    )


def encode_axis(axis: AxisType):
    if isinstance(axis, RegularAxis):
        return CIS('RegularAxis',
            axisLabel=axis.label,
            uomLabel=axis.uom,
            lowerBound=encode_position_value(axis.lower_bound),
            upperBound=encode_position_value(axis.upper_bound),
        )
    else:
        return CIS('IrregularAxis',
            *[
                CIS('C', encode_position_value(position))
                for position in axis.positions
            ],
            axisLabel=axis.label,
            uomLabel=axis.uom,
        )


def encode_domain_set(grid: Grid):
    return CIS('DomainSet',
        CIS('GeneralGrid',
            *([
                encode_axis(axis)
                for axis in grid.axes
                if not isinstance(axis, IndexAxis)
            ] + [
                CIS('GridLimits',
                    *[
                        CIS('IndexAxis',
                            axisLabel=axis.index_label,
                            lowerBound=str(0),
                            upperBound=str(axis.size - 1)
                        )
                        for axis in grid.axes
                    ],
                    axisLabels=' '.join(
                        axis.index_label for axis in grid.axes
                    ),
                    srsName=f'http://www.opengis.net/def/crs/OGC/0/Index{len(grid.axes)}D'
                )
            ]),
            srsName=grid.srs,
            axisLabels=' '.join(
                axis.label for axis in grid.axes
            )
        )
    )

def encode_range_type(range_type: List[Field]):
    return CIS('RangeType',
        encode_data_record(range_type)
    )
