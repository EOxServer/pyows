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

from ows.common.types import BoundingBox
from .decoders import xml_decode_execute
from .types import (
    ExecuteRequest, Input, Data, LiteralValue, Reference, OutputDefinition,
    ExecutionMode, ResponseType, TransmissionType
)

xml_execute = b'''<?xml version="1.0" encoding="UTF-8"?>
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


def test_execute():
    assert xml_decode_execute(xml_execute) == ExecuteRequest(
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
                data=Data(
                    LiteralValue(value='10.0', data_type=None, uom=None)
                )
            )
        ],
        output_definitions=[
            OutputDefinition(
                identifier='BUFFERED_GEOMETRY',
                transmission=TransmissionType.reference,
            )
        ]
    )


xml_execute_inputs = b'''<?xml version="1.0" encoding="UTF-8"?>
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
    <ows:Identifier>test</ows:Identifier>
    <wps:Input id="LITERAL_VALUE_TEXT_DT_UOM">
        <wps:Data>10.0@datatype=http://www.w3.org/2001/XMLSchema#double@uom=meter</wps:Data>
    </wps:Input>
    <wps:Input id="LITERAL_VALUE_TEXT_DT">
        <wps:Data>10.0@datatype=http://www.w3.org/2001/XMLSchema#double</wps:Data>
    </wps:Input>
    <wps:Input id="LITERAL_VALUE_TEXT_UOM">
        <wps:Data>10.0@uom=meter</wps:Data>
    </wps:Input>
    <wps:Input id="LITERAL_VALUE_XML_DT_UOM">
        <wps:Data>
            <wps:LiteralValue dataType="http://www.w3.org/2001/XMLSchema#double" uom="meter">10.0</wps:LiteralValue>
        </wps:Data>
    </wps:Input>
    <wps:Input id="LITERAL_VALUE_XML_DT">
        <wps:Data>
            <wps:LiteralValue dataType="http://www.w3.org/2001/XMLSchema#double">10.0</wps:LiteralValue>
        </wps:Data>
    </wps:Input>
    <wps:Input id="LITERAL_VALUE_XML_UOM">
        <wps:Data>
            <wps:LiteralValue uom="meter">10.0</wps:LiteralValue>
        </wps:Data>
    </wps:Input>
    <wps:Input id="BBOX_TEXT">
        <wps:Data>1.0,2.0,3.0,4.0</wps:Data>
    </wps:Input>
    <wps:Input id="BBOX_TEXT_CRS">
        <wps:Data>1.0,2.0,3.0,4.0,EPSG:4326</wps:Data>
    </wps:Input>
    <wps:Input id="BBOX_XML">
        <wps:Data>
            <ows:BoundingBox>
                <ows:LowerCorner>1.0 2.0</ows:LowerCorner>
                <ows:UpperCorner>3.0 4.0</ows:UpperCorner>
            </ows:BoundingBox>
        </wps:Data>
    </wps:Input>
    <wps:Input id="BBOX_XML_CRS">
        <wps:Data>
            <ows:BoundingBox crs="EPSG:4326">
                <ows:LowerCorner>1.0 2.0</ows:LowerCorner>
                <ows:UpperCorner>3.0 4.0</ows:UpperCorner>
            </ows:BoundingBox>
        </wps:Data>
    </wps:Input>
    <wps:Output id="OUTPUT" transmission="reference"/>
</wps:Execute>'''


def test_execute_inputs():
    assert xml_decode_execute(xml_execute_inputs) == ExecuteRequest(
        process_id='test',
        mode=ExecutionMode.async_,
        response=ResponseType.document,
        inputs=[
            Input(
                identifier='LITERAL_VALUE_TEXT_DT_UOM',
                data=Data(
                    LiteralValue(
                        '10.0',
                        data_type='http://www.w3.org/2001/XMLSchema#double',
                        uom='meter',
                    )
                )
            ),
            Input(
                identifier='LITERAL_VALUE_TEXT_DT',
                data=Data(
                    LiteralValue(
                        '10.0',
                        data_type='http://www.w3.org/2001/XMLSchema#double',
                    )
                )
            ),
            Input(
                identifier='LITERAL_VALUE_TEXT_UOM',
                data=Data(
                    LiteralValue(
                        '10.0',
                        uom='meter',
                    )
                )
            ),
            Input(
                identifier='LITERAL_VALUE_XML_DT_UOM',
                data=Data(
                    LiteralValue(
                        '10.0',
                        data_type='http://www.w3.org/2001/XMLSchema#double',
                        uom='meter',
                    )
                )
            ),
            Input(
                identifier='LITERAL_VALUE_XML_DT',
                data=Data(
                    LiteralValue(
                        '10.0',
                        data_type='http://www.w3.org/2001/XMLSchema#double',
                    )
                )
            ),
            Input(
                identifier='LITERAL_VALUE_XML_UOM',
                data=Data(
                    LiteralValue(
                        '10.0',
                        uom='meter',
                    )
                )
            ),
            Input(
                identifier='BBOX_TEXT',
                data=Data(
                    BoundingBox(
                        None,
                        [1.0, 2.0, 3.0, 4.0],
                    )
                )
            ),
            Input(
                identifier='BBOX_TEXT_CRS',
                data=Data(
                    BoundingBox(
                        "EPSG:4326",
                        [1.0, 2.0, 3.0, 4.0],
                    )
                )
            ),
            Input(
                identifier='BBOX_XML',
                data=Data(
                    BoundingBox(
                        None,
                        [1.0, 2.0, 3.0, 4.0],
                    )
                )
            ),
            Input(
                identifier='BBOX_XML_CRS',
                data=Data(
                    BoundingBox(
                        "EPSG:4326",
                        [1.0, 2.0, 3.0, 4.0],
                    )
                )
            ),
        ],
        output_definitions=[
            OutputDefinition(
                identifier='OUTPUT',
                transmission=TransmissionType.reference,
            )
        ]
    )