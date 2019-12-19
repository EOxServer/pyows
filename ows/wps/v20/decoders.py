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

# flake8: noq

from ows import kvp, xml
from ows.decoder import typelist
from ows.util import Version

from .namespaces import nsmap
from .types import (
    DescribeProcessRequest, ExecuteRequest, GetStatusRequest, GetResultRequest,
    DismissRequest
)


# ------------------------------------------------------------------------------
# DescribeCoverage
# ------------------------------------------------------------------------------


class KVPDescribeProcessDecoder(kvp.Decoder):
    object_class = DescribeProcessRequest
    version = kvp.Parameter(type=Version.from_str, num=1)
    process_ids = kvp.Parameter("coverageid", type=typelist(str, ","), num=1)


class XMLDescribeProcessDecoder(xml.Decoder):
    object_class = DescribeProcessRequest
    version = xml.Parameter("@version", type=Version.from_str, num=1)
    process_ids = xml.Parameter("ows:Identifier/text()", num="+")
    namespaces = nsmap


def kvp_decode_describe_process(kvp) -> DescribeProcessRequest:
    decoder = KVPDescribeProcessDecoder(kvp)
    return decoder.decode()


def xml_decode_describe_process(xml) -> DescribeProcessRequest:
    decoder = XMLDescribeProcessDecoder(xml)
    return decoder.decode()


# ------------------------------------------------------------------------------
# Execute
# ------------------------------------------------------------------------------

def parse_data_input(input_elem):
    pass


def parse_output_def(output_elem):
    pass


class XMLExecuteDecoder(xml.Decoder):
    object_class = ExecuteRequest
    version = xml.Parameter("@version", type=Version.from_str, num=1)
    process_id = xml.Parameter("ows:Identifier/text()", num=1)
    inputs = xml.Parameter('wps:Input', type=parse_data_input, num='*')
    outputs = xml.Parameter('wps:Output', type=parse_output_def, num='+')
    namespaces = nsmap


def xml_decode_execute(xml):
    decoder = XMLExecuteDecoder(xml)
    return decoder.decode()


# ------------------------------------------------------------------------------
# GetStatus
# ------------------------------------------------------------------------------

class KVPGetStatusDecoder(kvp.Decoder):
    object_class = GetStatusRequest
    version = kvp.Parameter(type=Version.from_str, num=1)
    job_id = kvp.Parameter("coverageid", type=typelist(str, ","), num=1)


class XMLGetStatusDecoder(xml.Decoder):
    object_class = GetStatusRequest
    version = xml.Parameter("@version", type=Version.from_str, num=1)
    job_id = xml.Parameter("wps:JobID/text()", num=1)
    namespaces = nsmap


def kvp_decode_get_status(kvp) -> GetStatusRequest:
    decoder = KVPGetStatusDecoder(kvp)
    return decoder.decode()


def xml_decode_get_status(xml) -> GetStatusRequest:
    decoder = XMLGetStatusDecoder(xml)
    return decoder.decode()


# ------------------------------------------------------------------------------
# GetResult
# ------------------------------------------------------------------------------

class KVPGetResultDecoder(kvp.Decoder):
    object_class = GetResultRequest
    version = kvp.Parameter(type=Version.from_str, num=1)
    job_id = kvp.Parameter("coverageid", type=typelist(str, ","), num=1)


class XMLGetResultDecoder(xml.Decoder):
    object_class = GetResultRequest
    version = xml.Parameter("@version", type=Version.from_str, num=1)
    job_id = xml.Parameter("wps:JobID/text()", num=1)
    namespaces = nsmap


def kvp_decode_get_result(kvp) -> GetResultRequest:
    decoder = KVPGetResultDecoder(kvp)
    return decoder.decode()


def xml_decode_get_result(xml) -> GetResultRequest:
    decoder = XMLGetResultDecoder(xml)
    return decoder.decode()


# ------------------------------------------------------------------------------
# Execute
# ------------------------------------------------------------------------------

class KVPDismissDecoder(kvp.Decoder):
    object_class = DismissRequest
    version = kvp.Parameter(type=Version.from_str, num=1)
    job_id = kvp.Parameter("coverageid", type=typelist(str, ","), num=1)


class XMLDismissDecoder(xml.Decoder):
    object_class = DismissRequest
    version = xml.Parameter("@version", type=Version.from_str, num=1)
    job_id = xml.Parameter("wps:JobID/text()", num=1)
    namespaces = nsmap


def kvp_decode_dismiss(kvp) -> DismissRequest:
    decoder = KVPDismissDecoder(kvp)
    return decoder.decode()


def xml_decode_dismiss(xml) -> DismissRequest:
    decoder = XMLDismissDecoder(xml)
    return decoder.decode()
