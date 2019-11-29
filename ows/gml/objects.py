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

from typing import Union, List
from dataclasses import dataclass
from datetime import datetime, date, timedelta


PositionType = Union[str, int, float, datetime, date]
ResolutionType = Union[str, int, float, timedelta]


@dataclass
class IndexAxis:
    index_label: str
    size: int


@dataclass
class RegularAxis:
    label: str
    index_label: str
    lower_bound: PositionType
    upper_bound: PositionType
    resolution: ResolutionType
    uom: str
    size: int


@dataclass
class IrregularAxis:
    label: str
    index_label: str
    positions: List[PositionType]
    uom: str

    @property
    def size(self):
        return len(self.positions)


AxisType = Union[IndexAxis, RegularAxis, IrregularAxis]


@dataclass
class Grid:
    axes: List[AxisType]
    srs: str
