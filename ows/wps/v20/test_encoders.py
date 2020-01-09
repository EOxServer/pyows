# ------------------------------------------------------------------------------
#
# Project: pyows <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
# ------------------------------------------------------------------------------
# Copyright (C) 2020 EOX IT Services GmbH
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

# flake8: noqa

from textwrap import dedent

from .encoders import xml_encode_execute
from .types import (
    ExecuteRequest, Input, Data, Reference, OutputDefinition,
    ExecutionMode, ResponseType, TransmissionType
)
from ows.test import assert_xml_equal


def test_encode_get_coverage_xml():
    request = ExecuteRequest(
        process_id='http://my.wps.server/processes/proximity/Planar-Buffer',
        mode=ExecutionMode.async_,
        response=ResponseType.document,
        inputs=[
            Input(
                identifier='INPUT_GEOMETRY',
                data=Reference(href='http://some.data.server/mygmldata.xml'),
            ),
            Input(
                identifier='DISTANCE',
                data=Data('10.0')
            )
        ],
        output_definitions=[
            OutputDefinition(
                identifier='BUFFERED_GEOMETRY',
                transmission=TransmissionType.reference,
            )
        ]
    )
    assert_xml_equal(xml_encode_execute(request, pretty_print=True).value.decode('utf-8'), dedent('''\
        <wps:Execute
            xmlns:wps="http://www.opengis.net/wps/2.0"
            xmlns:ows="http://www.opengis.net/ows/2.0"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.opengis.net/wps/2.0 ../wps.xsd"

            service="WPS"
            version="2.0.0"
            response="document"
            mode="async">

            <ows:Identifier>http://my.wps.server/processes/proximity/Planar-Buffer</ows:Identifier>
            <wps:Input id="INPUT_GEOMETRY">
                <wps:Reference xlink:href="http://some.data.server/mygmldata.xml"/>
            </wps:Input>
            <wps:Input id="DISTANCE">
                <wps:Data>10.0</wps:Data>
            </wps:Input>

            <!-- Query the default output format for the the result "BUFFERED_GEOMETRY" -->
            <!-- The result "BUFFERED_GEOMETRY" shall be delivered by reference in its default format -->
            <wps:Output id="BUFFERED_GEOMETRY" transmission="reference"/>

        </wps:Execute>'''
    ))