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

from datetime import date, datetime, time
from typing import List, Union, Tuple
from dataclasses import dataclass, field

from ows import Version
from ows.common import (
    ServiceCapabilities as CommonServiceCapabilities, Metadata
)

ValueType = Union[int, float, str, datetime, date, time]
ValueRange = Tuple[ValueType, ValueType]


# TODO: maybe use a common base class
@dataclass
class _DescriptionBase:
    title: str = None
    abstract: str = None
    keywords: List[str] = field(default_factory=list)
    metadata: List[Metadata] = field(default_factory=list)


@dataclass
class Domain:
    data_type: str
    allowed_values: List[Union[ValueType, ValueRange]] = None
    uom: str = None
    default_value: ValueType = None


@dataclass
class Format:
    mime_type: str = None
    encoding: str = None
    schema: str = None
    maxmimum_megabytes: int = None


@dataclass
class LiteralDataDescription:
    domains: List[Domain]
    formats: List[Format]


@dataclass
class BoundingBoxDataDescription:
    supported_crss: List[str]
    formats: List[Format]


@dataclass
class ComplexDataDescription:
    formats: List[Format]


DataDescriptionTypes = Union[
    LiteralDataDescription, BoundingBoxDataDescription, ComplexDataDescription
]


@dataclass
class InputDescription:
    identifier: str
    data_description: DataDescriptionTypes = None
    inputs: List['InputDescription'] = field(default_factory=list)
    title: str = None
    abstract: str = None
    keywords: List[str] = field(default_factory=list)
    metadata: List[Metadata] = field(default_factory=list)

    def __post_init__(self):
        if not self.data_description and not self.inputs:
            raise ValueError(
                'Either `data_description` or `inputs` must be specified.'
            )


@dataclass
class OutputDescription:
    identifier: str
    data_description: DataDescriptionTypes = None
    outputs: List['OutputDescription'] = field(default_factory=list)
    title: str = None
    abstract: str = None
    keywords: List[str] = field(default_factory=list)
    metadata: List[Metadata] = field(default_factory=list)

    def __post_init__(self):
        if not self.data_description and not self.outputs:
            raise ValueError(
                'Either `data_description` or `outputs` must be specified.'
            )


@dataclass
class ProcessSummary:
    identifier: str
    title: str = None
    abstract: str = None
    keywords: List[str] = field(default_factory=list)
    metadata: List[Metadata] = field(default_factory=list)
    sync_execute: bool = False
    async_execute: bool = False
    by_value: bool = False
    by_reference: bool = False
    version: Version = None
    model: str = None


@dataclass
class ProcessDescription(ProcessSummary):
    inputs: List[InputDescription] = field(default_factory=list)
    outputs: List[OutputDescription] = field(default_factory=list)
    lang: str = '*'


@dataclass
class ServiceCapabilities(CommonServiceCapabilities):
    process_summaries: List[ProcessSummary] = field(default_factory=list)


class JobStatus:
    succeded = 'Succeded'
    failed = 'Failed'
    accepted = 'Accepted'
    running = 'Running'


@dataclass
class StatusInfo:
    job_id: str
    status: JobStatus
    expiration_date: datetime = None
    estimated_completion: datetime = None
    next_poll: datetime = None
    percent_completed: int = None
