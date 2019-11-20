from dataclasses import dataclass, field
from typing import List, Union


class GetCapabilitiesRequest:
    pass


@dataclass
class DescribeCoverageRequest:
    coverage_ids: List[str]


@dataclass
class Slice:
    dimension: str
    point: float


@dataclass
class Trim:
    dimension: str
    low: float = None
    high: float = None


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


@dataclass
class AxisInterpolation:
    axis: str
    method: str


@dataclass
class RangeInterval:
    start: str
    end: str


@dataclass
class GetCoverageRequest:
    coverage_id: str
    format: str = None
    mediatype: str = None
    subsetting_crs: str = None
    output_crs: str = None
    subsets: List[Union[Slice, Trim]] = field(default_factory=list)
    scalefactor: float = None
    scales: List[Union[ScaleAxis, ScaleSize, ScaleExtent]] = field(default_factory=list)
    interpolation: str = None
    axis_interpolations: List[AxisInterpolation] = field(default_factory=list)
    range_subset: List[Union[str, RangeInterval]] = None
