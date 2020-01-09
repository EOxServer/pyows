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

from typing import List, Union

from ows.util import Result, isoformat
from .namespaces import WPS, ns_xlink
from .types import (
    DescribeProcessRequest, ExecuteRequest, GetStatusRequest,
    GetResultRequest, DismissRequest, Input, OutputDefinition,
    Data, Reference
)
from ..types import (
    ServiceCapabilities, ProcessSummary, ProcessDescription,
    InputDescription, OutputDescription, DataDescriptionTypes,
    LiteralDataDescription, BoundingBoxDataDescription,
    ComplexDataDescription, Format, Domain, StatusInfo,
    ValueType, ValueRange
)
from ows.common.v20.encoders import (
    OWS, encode_service_provider, encode_service_identification,
    encode_operations_metadata
)


def kvp_encode_describe_process(request: DescribeProcessRequest, **kwargs):
    return Result.from_kvp(
        dict(
            service='WCS',
            version=str(request.version),
            request='DescribeProcess',
            processid=','.join(request.process_ids),
        ), **kwargs
    )


def xml_encode_describe_process(request: DescribeProcessRequest, **kwargs):
    root = WPS('DescribeProcess',
        *[
            OWS('Identifier', identifier)
            for identifier in request.process_ids
        ],
        service='WPS',
        version=str(request.version),
    )
    return Result.from_etree(root, **kwargs)


def encode_data(data: Data):
    return WPS('Data',
        data.value,
        mimeType=data.mime_type,
        encoding=data.encoding,
        schema=data.schema,
    )


def encode_reference(ref: Reference):
    elem = WPS('Reference',
        mimeType=ref.mime_type,
        encoding=ref.encoding,
        schema=ref.schema,
        **{
            ns_xlink('href'): ref.href,
        }
    )
    if ref.body:
        elem.append(WPS('Body', ref.body))
    elif ref.body_reference_href:
        elem.append(
            WPS('BodyReference', **{
                ns_xlink('href'): ref.body_reference_href,
            })
        )
    return elem


def encode_input(input_: Input):
    if isinstance(input_.data, Data):
        contents = [encode_data(input_.data)]
    elif isinstance(input_.data, Reference):
        contents = [encode_reference(input_.data)]
    elif input_.inputs:
        contents = [
            encode_input(sub_input)
            for sub_input in input_.inputs
        ]
    return WPS('Input', *contents,
        id=input_.identifier,
    )


def encode_output(output: OutputDefinition):
    return WPS('Output', *[
            encode_output(sub_output)
            for sub_output in output.output_definitions or []
        ],
        id=output.identifier,
        mimeType=output.mime_type,
        encoding=output.encoding,
        schema=output.schema,
        transmission=output.transmission.value,
    )


def xml_encode_execute(request: ExecuteRequest, **kwargs):
    root = WPS('Execute',
        OWS('Identifier', request.process_id), *[
            encode_input(input_)
            for input_ in request.inputs
        ] + [
            encode_output(output)
            for output in request.output_definitions
        ],
        response=request.response.value,
        mode=request.mode.value,
        service='WPS',
        version=str(request.version),
    )
    return Result.from_etree(root, **kwargs)


def kvp_encode_get_status(request: GetStatusRequest, **kwargs):
    return Result.from_kvp(
        dict(
            service='WCS',
            version=str(request.version),
            request='GetStatus',
            jobid=request.job_id,
        ), **kwargs
    )


def xml_encode_get_status(request: GetStatusRequest, **kwargs):
    root = WPS('GetStatus',
        WPS('JobID', request.job_id),
        service='WPS',
        version=str(request.version),
    )
    return Result.from_etree(root, **kwargs)


def kvp_encode_get_result(request: GetResultRequest, **kwargs):
    return Result.from_kvp(
        dict(
            service='WCS',
            version=str(request.version),
            request='GetResult',
            jobid=request.job_id,
        ), **kwargs
    )


def xml_encode_get_result(request: GetResultRequest, **kwargs):
    root = WPS('GetResult',
        WPS('JobID', request.job_id),
        service='WPS',
        version=str(request.version),
    )
    return Result.from_etree(root, **kwargs)


def kvp_encode_dismiss(request: DismissRequest, **kwargs):
    return Result.from_kvp(
        dict(
            service='WCS',
            version=str(request.version),
            request='Dismiss',
            jobid=request.job_id,
        ), **kwargs
    )


def xml_encode_dismiss(request: DismissRequest, **kwargs):
    root = WPS('Dismiss',
        WPS('JobID', request.job_id),
        service='WPS',
        version=str(request.version),
    )
    return Result.from_etree(root, **kwargs)


def encode_description_type(tag_name, description_type):
    return WPS(tag_name,
        OWS('Title', description_type.title or description_type.identifier),
        OWS('Abstract',
            description_type.abstract
        ) if description_type.abstract else None,
        OWS('Keywords', *[
            OWS('Keyword', keyword)
            for keyword in description_type.keywords
        ]) if description_type.keywords else None,
        OWS('Identifier',
            description_type.identifier
        ),
        *[
            OWS('Metadata',
                href=metadata.href,
                role=metadata.role,
                arcrole=metadata.arcrole,
                title=metadata.title,
                about=metadata.about,
            ) for metadata in description_type.metadata
        ]
    )


def encode_process_summary(process_summary: ProcessSummary):
    elem = encode_description_type('ProcessSummary', process_summary)

    job_control_options = []
    if process_summary.sync_execute:
        job_control_options.append('sync-execute')
    if process_summary.async_execute:
        job_control_options.append('async-execute')
    elem.attrib['jobControlOptions'] = ' '.join(job_control_options)

    output_transmission = []
    if process_summary.by_value:
        output_transmission.append('value')
    if process_summary.by_reference:
        output_transmission.append('reference')
    elem.attrib['outputTransmission'] = ' '.join(output_transmission)

    if process_summary.version:
        elem.attrib['processVersion'] = str(process_summary.version)

    if process_summary.model is not None:
        elem.attrib['processModel'] = process_summary.model

    return elem


def encode_contents(capabilities: ServiceCapabilities):
    return WPS('Contents', *[
        encode_process_summary(process_summary)
        for process_summary in capabilities.process_summaries
    ])


def xml_encode_capabilities(capabilities: ServiceCapabilities,
                            include_service_identification=True,
                            include_service_provider=True,
                            include_operations_metadata=True,
                            include_contents=True,
                            **kwargs):

    sections = []
    if include_service_identification:
        sections.append(
            encode_service_identification(capabilities)
        )
    if include_service_provider:
        sections.append(
            encode_service_provider(capabilities)
        )
    if include_operations_metadata:
        sections.append(
            encode_operations_metadata(capabilities)
        )
    if include_contents:
        sections.append(
            encode_contents(capabilities)
        )

    root = WPS('Capabilities',
        *sections,
        version="2.0.1",
        updateSequence=capabilities.update_sequence
    )

    return Result.from_etree(root, **kwargs)


def encode_format(format_: Format, default=False):
    return WPS('Format',
        mimeType=format_.mime_type,
        encoding=format_.encoding,
        schema=format_.schema,
        maximumMegabytes=str(
            format_.maxmimum_megabytes
        ) if format_.maxmimum_megabytes else None,
        default='true' if default else 'false'
    )


def encode_allowed_values(allowed_values: List[Union[ValueType, ValueRange]]):
    return OWS('AllowedValues', *[
        OWS('Value', str(value))
        if isinstance(value, ValueType) else
        OWS('Range',
            OWS('MinimumValue',
                str(value[0])
            ) if value[0] is not None else None,
            OWS('MaximumValue',
                str(value[1])
            ) if value[1] is not None else None,
            # TODO: spacing
        )
        for value in allowed_values
    ])


def encode_domain(domain: Domain, default=False):
    return WPS('LiteralDataDomain',
        encode_allowed_values(
            domain.allowed_values
        ) if domain.allowed_values else OWS('AnyValue'),
        OWS('DataType', domain.data_type) if domain.data_type else None,
        OWS('UOM', domain.uom) if domain.uom else None,
        OWS('DefaultValue',
            str(domain.default_value)  # TODO proper to-stringing
        ) if domain.default_value else None,
        default='true' if default else 'false'
    )


def encode_data_description(data_description: DataDescriptionTypes):
    formats = [
        encode_format(format_, i == 0)
        for i, format_ in enumerate(data_description.formats)
    ]

    if isinstance(data_description, LiteralDataDescription):
        return WPS('LiteralData', *formats + [
            encode_domain(domain, i == 0)
            for i, domain in enumerate(data_description.domains)
        ])

    elif isinstance(data_description, BoundingBoxDataDescription):
        return WPS('BoundingBoxData', *formats + [
            WPS('SupportedCRS',
                supported_crs,
                default='true' if i == 0 else 'false'
            )
            for i, supported_crs in enumerate(data_description.supported_crss)
        ])

    elif isinstance(data_description, ComplexDataDescription):
        return WPS('ComplexDataType', *formats)


def encode_input_description(input_description: InputDescription):
    elem = encode_description_type('Input', input_description)
    if input_description.data_description:
        elem.append(encode_data_description)
    elif input_description.inputs:
        elem.extend([
            encode_input_description(sub_input_description)
            for sub_input_description in input_description.inputs
        ])
    return elem


def encode_output_description(output_description: OutputDescription):
    elem = encode_description_type('Output', output_description)
    if output_description.data_description:
        elem.append(encode_data_description)
    elif output_description.inputs:
        elem.extend([
            encode_input_description(sub_output_description)
            for sub_output_description in output_description.inputs
        ])
    return elem


def encode_process(process_description: ProcessDescription):
    elem = encode_description_type('Process', process_description)
    elem.extend([
        encode_input_description(input_)
        for input_ in process_description.inputs
    ])
    elem.extend([
        encode_output_description(output)
        for output in process_description.outputs
    ])


def xml_encode_process_offerings(process_descriptions: List[ProcessDescription],
                                 **kwargs):
    root = WPS('ProcessOfferings', *[
        WPS('ProcessOffering', encode_process(process_description))
        for process_description in process_descriptions
    ])
    return Result.from_etree(root, **kwargs)


def xml_encode_status_info(status_info: StatusInfo, **kwargs):
    root = WPS('StatusInfo',
        WPS('JobID', status_info.job_id),
        WPS('Status', str(status_info.status)),
        WPS('ExpirationDate',
            isoformat(status_info.expiration_date)
        ) if status_info.expiration_date else None,
        WPS('EstimatedCompletion',
            isoformat(status_info.estimated_completion)
        ) if status_info.estimated_completion else None,
        WPS('NextPoll',
            isoformat(status_info.next_poll)
        ) if status_info.next_poll else None,
        WPS('PercentCompleted',
            str(status_info.percent_completed)
        ) if status_info.percent_completed else None,
    )
    return Result.from_etree(root, **kwargs)
