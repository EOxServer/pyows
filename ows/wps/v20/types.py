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

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Union, Any

from ows.util import Version


class GetCapabilitiesRequest:
    pass


@dataclass
class DescribeProcessRequest:
    process_ids: List[str]
    version: Version = Version(2, 0, 0)


class ExecutionMode(Enum):
    sync = 'sync'
    async_ = 'async'
    auto = 'auto'


class ResponseType(Enum):
    raw = 'raw'
    document = 'document'


class TransmissionType(Enum):
    value = 'value'
    reference = 'reference'


@dataclass
class Data:
    value: Any
    mime_type: str = None
    encoding: str = None
    schema: str = None


@dataclass
class Reference:
    href: str
    body: str = None
    body_reference_href: str = None
    mime_type: str = None
    encoding: str = None
    schema: str = None


@dataclass
class Input:
    identifier: str
    data: Union[Data, Reference] = None
    inputs: List['Input'] = None

    def __post_init__(self):
        if not self.data and not self.inputs:
            raise ValueError('Either `data` or `inputs` must be specified')


@dataclass
class OutputDefinition:
    identifier: str
    transmission: TransmissionType
    mime_type: str = None
    encoding: str = None
    schema: str = None
    output_definitions: List['OutputDefinition'] = None


@dataclass
class ExecuteRequest:
    process_id: str
    mode: ExecutionMode
    response: ResponseType
    inputs: List[Input] = field(default_factory=list)
    output_definitions: List[OutputDefinition] = field(default_factory=list)
    version: Version = Version(2, 0, 0)


@dataclass
class GetStatusRequest:
    job_id: str
    version: Version = Version(2, 0, 0)


@dataclass
class GetResultRequest:
    job_id: str
    version: Version = Version(2, 0, 0)


@dataclass
class DismissRequest:
    job_id: str
    version: Version = Version(2, 0, 0)
