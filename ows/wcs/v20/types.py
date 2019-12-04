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

from dataclasses import dataclass, field
from typing import List, Union

from ows.util import Version


class GetCapabilitiesRequest:
    pass


@dataclass
class DescribeCoverageRequest:
    coverage_ids: List[str]
    version: Version = Version(2, 0, 1)


@dataclass
class Slice:
    dimension: str
    point: float


@dataclass
class Trim:
    dimension: str
    low: float = None
    high: float = None


SubsetTypes = Union[Slice, Trim]


@dataclass
class ScaleSize:
    axis: str
    size: int


@dataclass
class ScaleAxis:
    axis: str
    factor: float


@dataclass
class ScaleExtent:
    axis: str
    low: float
    high: float


ScaleTypes = Union[ScaleAxis, ScaleSize, ScaleExtent]


@dataclass
class AxisInterpolation:
    axis: str
    method: str


@dataclass
class RangeInterval:
    start: str
    end: str


@dataclass
class GeoTIFFEncodingParameters:
    compression: str = None
    jpeg_quality: int = None
    predictor: str = None
    interleave: str = None
    tiling: bool = None
    tile_width: int = None
    tile_height: int = None


@dataclass
class GetCoverageRequest:
    coverage_id: str
    version: Version = Version(2, 0, 1)
    format: str = None
    mediatype: str = None
    subsetting_crs: str = None
    output_crs: str = None
    subsets: List[SubsetTypes] = field(default_factory=list)
    scalefactor: float = None
    scales: List[ScaleTypes] = field(default_factory=list)
    interpolation: str = None
    axis_interpolations: List[AxisInterpolation] = field(default_factory=list)
    range_subset: List[Union[str, RangeInterval]] = None
    geotiff_encoding_parameters: GeoTIFFEncodingParameters = field(default_factory=GeoTIFFEncodingParameters)
