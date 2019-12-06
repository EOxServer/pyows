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

from typing import List, Dict
from dataclasses import dataclass, field

from ows.common.types import (
    OnlineResource, WGS84BoundingBox, BoundingBox,
    ServiceCapabilities as CommonServiceCapabilities
)


@dataclass
class Dimension:
    name: str
    units: str
    unit_symbol: str = None
    default: str = None
    multiple_values: bool = None
    nearest_value: bool = None
    current: bool = None


@dataclass
class __FormatOnlineResourceBase:
    format: str


@dataclass
class FormatOnlineResource(__FormatOnlineResourceBase, OnlineResource):
    pass


@dataclass
class __LegenURLBase:
    width: int
    height: int


@dataclass
class LegendURL(__LegenURLBase, FormatOnlineResource):
    pass


@dataclass
class Style:
    name: str
    title: str
    abstract: str = None
    legend_url: List[LegendURL] = field(default_factory=dict)
    style_sheet_url: FormatOnlineResource = None
    style_url: FormatOnlineResource = None


@dataclass
class Layer:
    title: str
    name: str = None
    abstract: str = None
    keywords: List[str] = field(default_factory=list)
    crss: List[str] = field(default_factory=list)
    wgs84_bounding_box: WGS84BoundingBox = None
    bounding_boxes: BoundingBox = field(default_factory=list)
    dimensions: List[Dimension] = field(default_factory=list)
    attribution: str = None
    authority_urls: Dict[str, FormatOnlineResource] = field(default_factory=dict)
    identifiers: Dict[str, str] = field(default_factory=dict)
    metadata_urls: List[FormatOnlineResource] = field(default_factory=dict)
    data_urls: List[FormatOnlineResource] = field(default_factory=dict)
    feature_list_urls: List[FormatOnlineResource] = field(default_factory=dict)
    styles: List[Style] = field(default_factory=list)
    min_scale_denominator: float = None
    max_scale_denominator: float = None
    layers: List['Layer'] = field(default_factory=list)

    queryable: bool = False
    cascaded: int = None
    opaque: bool = False
    no_subsets: bool = False
    fixed_width: int = None
    fixed_height: int = None


@dataclass
class ServiceCapabilities(CommonServiceCapabilities):
    exception_formats: List[str] = field(default_factory=list)
    layer: Layer = None
    layer_limit: int = None
    max_width: int = None
    max_height: int = None
