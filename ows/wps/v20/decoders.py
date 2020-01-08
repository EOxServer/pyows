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
    DismissRequest,
    ExecutionMode, ResponseType, Input, Data, Reference, OutputDefinition,
    TransmissionType,
)


# ------------------------------------------------------------------------------
# DescribeProcess
# ------------------------------------------------------------------------------


class KVPDescribeProcessDecoder(kvp.Decoder):
    object_class = DescribeProcessRequest
    version = kvp.Parameter(type=Version.from_str, num=1)
    process_ids = kvp.Parameter("jobid", type=typelist(str, ","), num=1)


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
    decoder = XMLInputDecoder(input_elem)
    return Input(
        identifier=decoder.identifier,
        data=decoder.data or decoder.reference,
        inputs=[
            input_ for input_ in decoder.inputs
        ] if decoder.inputs else None,
    )


class XMLDataDecoder(xml.Decoder):
    mime_type = xml.Parameter('@mimeType', num='?')
    encoding = xml.Parameter('@encoding', num='?')
    schema = xml.Parameter('@schema', num='?')


def parse_data(data_elem):
    decoder = XMLDataDecoder(data_elem)
    if len(data_elem) == 0:
        value = data_elem.text
    else:
        value = list(data_elem)

    return Data(
        value=value,
        mime_type=decoder.mime_type,
        encoding=decoder.encoding,
        schema=decoder.schema,
    )


def parse_reference_body(body_elem):
    if len(body_elem):
        # TODO: convert to string
        raise NotImplementedError
    else:
        return body_elem.text


class XMLReferenceDecoder(xml.Decoder):
    object_class = Reference
    href = xml.Parameter('@xlink:href', num='?')
    body = xml.Parameter('wps:Body', type=parse_reference_body, num='?')
    body_reference_href = xml.Parameter('wps:BodyReference/@xlink:href', num='?')
    mime_type = xml.Parameter('@mimeType', num='?')
    encoding = xml.Parameter('@encoding', num='?')
    schema = xml.Parameter('@schema', num='?')
    namespaces = nsmap


def parse_reference(reference_elem):
    return XMLReferenceDecoder(reference_elem).decode()


class XMLInputDecoder(xml.Decoder):
    identifier = xml.Parameter('@id', num=1)
    data = xml.Parameter('wps:Data', type=parse_data, num='?')
    reference = xml.Parameter('wps:Reference', type=parse_reference, num='?')
    inputs = xml.Parameter('wps:Input', type=parse_data_input, num='*')
    namespaces = nsmap


def parse_output_def(output_elem):
    decoder = XMLOutputDefinitionDecoder(output_elem)
    return decoder.decode()


class XMLOutputDefinitionDecoder(xml.Decoder):
    object_class = OutputDefinition
    identifier = xml.Parameter('@id', num=1)
    output_definitions = xml.Parameter('wps:Output', type=parse_output_def, num='*')
    mime_type = xml.Parameter('@mimeType', num='?')
    encoding = xml.Parameter('@encoding', num='?')
    schema = xml.Parameter('@schema', num='?')
    transmission = xml.Parameter('@transmission', type=TransmissionType, num='?')
    namespaces = nsmap

    def map_params(self, params):
        if not params['output_definitions']:
            params['output_definitions'] = None
        return params


class XMLExecuteDecoder(xml.Decoder):
    object_class = ExecuteRequest
    version = xml.Parameter("@version", type=Version.from_str, num=1)
    process_id = xml.Parameter("ows:Identifier/text()", num=1)
    mode = xml.Parameter('@mode', type=ExecutionMode, num=1)
    response = xml.Parameter('@response', type=ResponseType, num=1)
    inputs = xml.Parameter('wps:Input', type=parse_data_input, num='*')
    output_definitions = xml.Parameter('wps:Output', type=parse_output_def, num='+')
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
    job_id = kvp.Parameter("jobid", type=typelist(str, ","), num=1)


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
    job_id = kvp.Parameter("jobid", type=typelist(str, ","), num=1)


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
    job_id = kvp.Parameter("jobid", type=typelist(str, ","), num=1)


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
