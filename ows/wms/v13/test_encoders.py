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

from datetime import datetime, timedelta

from ows.common.types import WGS84BoundingBox, BoundingBox
from ..types import (
    ServiceCapabilities, FormatOnlineResource, Layer, Style, LegendURL,
    Dimension, Range
)
from .encoders import xml_encode_capabilities


def test_encode_capabilities():
    capabilities = ServiceCapabilities()
    print(xml_encode_capabilities(capabilities, pretty_print=True).value.decode('utf-8'))

    capabilities = ServiceCapabilities.with_defaults(
        'http://provider.org',
        ['image/png', 'image/jpeg'],
        ['text/html', 'application/json'],
        update_sequence='2018-05-08',
        title='Title',
        abstract='Description',
        keywords=[
            'test', 'WMS',
        ],
        fees='None',
        access_constraints=['None'],
        provider_name='Provider Inc',
        provider_site='http://provider.org',
        individual_name='John Doe',
        organisation_name='Provider Inc',
        position_name='CTO',
        phone_voice='+99/9008820',
        phone_facsimile='+99/9008821',
        delivery_point='Point du Hoc',
        city='City',
        administrative_area='Adminity',
        postal_code='12345',
        country='Cooontry',
        electronic_mail_address='john.doe@provider.org',
        online_resource='http://provider.org',
        hours_of_service='09:00AM - 18:00PM',
        contact_instructions='Just send a mail or a carrier pidgeon',
        role='Chief',
        layer=Layer(
            title='root layer',
            abstract='Some abstract',
            keywords=['Root', 'right?'],
            crss=['EPSG:4326', 'EPSG:3857'],
            wgs84_bounding_box=WGS84BoundingBox([-180, -90, 180, 90]),
            bounding_boxes=[
                BoundingBox('EPSG:3857', [
                    -20026376.39, -20048966.10,
                    20026376.39, 20048966.10,
                ])
            ],
            attribution='root attribution',
            authority_urls={
                'root-auth': 'http://provider.org',
            },
            identifiers={
                'root-auth': 'myId',
            },
            metadata_urls=[
                FormatOnlineResource(
                    format='text/xml',
                    href='http://provider.com/metadata.xml',
                )
            ],
            data_urls=[
                FormatOnlineResource(
                    format='image/tiff',
                    href='http://provider.com/data.tif',
                )
            ],
            min_scale_denominator=5,
            max_scale_denominator=10,
            layers=[
                Layer(
                    name='sublayer',
                    title='My Sub-layer',
                    queryable=True,
                    styles=[
                        Style(
                            name='styli',
                            title='Styli',
                            abstract='stylisch Style',
                            legend_urls=[
                                LegendURL(
                                    width=500,
                                    height=300,
                                    format='image/jpeg',
                                    href='http://provider.com/legend.jpg',
                                )
                            ],
                            style_sheet_url=FormatOnlineResource(
                                'text/xml',
                                href='http://provider.com/stylesheet.xml',
                            ),
                            style_url=FormatOnlineResource(
                                'text/xml',
                                href='http://provider.com/style.xml',
                            )
                        )
                    ],
                    dimensions=[
                        Dimension(
                            name='time',
                            units='seconds',
                            values=Range(
                                datetime(2018, 5, 10),
                                datetime(2018, 5, 12),
                                timedelta(hours=1),
                            ),
                            unit_symbol='s',
                            default='',
                            multiple_values=False,
                            nearest_value=True,
                            current=False
                        ),
                        Dimension(
                            name='elevation',
                            units='meters',
                            values=[5, 10, 500, 1000, 15000],
                            unit_symbol='m',
                            default='',
                            multiple_values=False,
                            nearest_value=True,
                            current=False
                        )
                    ]
                )
            ]
        ),
    )
    print(xml_encode_capabilities(capabilities, pretty_print=True).value.decode('utf-8'))
