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

from datetime import datetime
from typing import List, Tuple
from dataclasses import dataclass, field

from ows.common import types as common
from ows.gml.types import Grid
from ows.swe.types import Field


@dataclass
class CoverageSummary:
    identifier: str
    coverage_subtype: str
    coverage_subtype_parent: str = None
    title: str = None
    abstract: str = None
    keywords: List[str] = field(default_factory=list)
    wgs84_bbox: List[common.WGS84BoundingBox] = field(default_factory=list)
    bbox: List[common.BoundingBox] = field(default_factory=list)
    metadata: List[common.Metadata] = field(default_factory=list)

    def __post_init__(self):
        # Allow some list fields to be passed as single values
        # but translate them
        if isinstance(self.wgs84_bbox, common.WGS84BoundingBox):
            self.wgs84_bbox = [self.wgs84_bbox]

        if isinstance(self.bbox, common.BoundingBox):
            self.bbox = [self.bbox]

        if isinstance(self.metadata, common.Metadata):
            self.metadata = [self.metadata]


@dataclass
class DatasetSeriesSummary:
    identifier: str
    wgs84_bbox: common.WGS84BoundingBox
    time_period: Tuple[datetime, datetime]
    title: str = None
    abstract: str = None
    keywords: List[str] = field(default_factory=list)
    metadata: List[common.Metadata] = field(default_factory=list)

    def __post_init__(self):
        # Allow some list fields to be passed as single values
        # but translate them
        if isinstance(self.metadata, common.Metadata):
            self.metadata = [self.metadata]


DEFAULT_PROFILES = [
    'http://www.opengis.net/spec/WCS_application-profile_earth-observation/1.0/conf/eowcs',
    'http://www.opengis.net/spec/WCS_application-profile_earth-observation/1.0/conf/eowcs_get-kvp',
    'http://www.opengis.net/spec/WCS_service-extension_crs/1.0/conf/crs',
    'http://www.opengis.net/spec/WCS/2.0/conf/core',
    'http://www.opengis.net/spec/WCS_protocol-binding_get-kvp/1.0/conf/get-kvp',
    'http://www.opengis.net/spec/WCS_protocol-binding_post-xml/1.0/conf/post-xml',
    'http://www.opengis.net/spec/GMLCOV/1.0/conf/gml-coverage',
    'http://www.opengis.net/spec/GMLCOV/1.0/conf/multipart',
    'http://www.opengis.net/spec/GMLCOV/1.0/conf/special-format',
    'http://www.opengis.net/spec/GMLCOV_geotiff-coverages/1.0/conf/geotiff-coverage',
    'http://www.opengis.net/spec/WCS_geotiff-coverages/1.0/conf/geotiff-coverage',
    'http://www.opengis.net/spec/WCS_service-model_crs-predefined/1.0/conf/crs-predefined',
    'http://www.opengis.net/spec/WCS_service-extension_interpolation/1.0/conf/interpolation',
    'http://www.opengis.net/spec/WCS_service-extension_range-subsetting/1.0/conf/record-subsetting',
    'http://www.opengis.net/spec/WCS_service-extension_scaling/1.0/conf/scaling',
]


@dataclass
class ServiceCapabilities(common.ServiceCapabilities):
    formats_supported: List[str] = field(default_factory=list)
    crss_supported: List[str] = field(default_factory=list)
    interpolations_supported: List[str] = field(default_factory=list)
    coverage_summaries: List[CoverageSummary] = field(default_factory=list)
    dataset_series_summaries: List[DatasetSeriesSummary] = field(default_factory=list)

    @classmethod
    def with_defaults_v20(cls, service_url, allowed_operations=None,
                          allow_post=True, allow_get=True, **kwargs):
        kwargs.setdefault('service_type', 'WCS')
        kwargs.setdefault('service_type_versions', ['2.0.1', '2.0.0'])
        kwargs.setdefault('profiles', DEFAULT_PROFILES)

        if allowed_operations is None:
            allowed_operations = [
                'GetCapabilities', 'DescribeCoverage',
                'DescribeEOCoverageSet', 'GetCoverage'
            ]

        def get_operation_methods(service_url, allow_get, allow_post):
            operation_methods = []
            if allow_get:
                operation_methods.append(
                    common.OperationMethod(
                        common.HttpMethod.Get, service_url=service_url
                    )
                )
            if allow_post:
                operation_methods.append(
                    common.OperationMethod(
                        common.HttpMethod.Post, service_url=service_url,
                        constraints=[
                            common.Constraint('PostEncoding', ['XML'])
                        ]
                    )
                )
            return operation_methods

        if 'operations' not in kwargs:
            kwargs['operations'] = [
                common.Operation(operation_name, get_operation_methods(
                    service_url, allow_get, allow_post
                ))
                for operation_name in allowed_operations
            ]

        return cls(**kwargs)


@dataclass
class CoverageDescription:
    identifier: str
    range_type: List[Field]
    grid: Grid
    native_format: str
    coverage_subtype: str
    coverage_subtype_parent: str = None
