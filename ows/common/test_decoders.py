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

from textwrap import dedent

from ows import Version
from .decoders import kvp_decode_base_request, xml_decode_base_request
from .types import BaseRequest


def test_kvp_decoder_base_request():
    assert kvp_decode_base_request(
        'service=WZS&version=3.0&request=GetFoo&bar=baz'
    ) == BaseRequest(
        service='WZS',
        version=Version(3, 0),
        request='GetFoo'
    )

    assert kvp_decode_base_request(
        'service=WZS&request=GetCapabilities&acceptversions=3.0,4.0'
    ) == BaseRequest(
        service='WZS',
        request='GetCapabilities',
        accept_versions=[Version(3, 0), Version(4, 0)],
    )


def test_xml_decoder_base_request():
    assert xml_decode_base_request(dedent('''
    <wzs:GetFoo service="WZS" version="3.0"
        xmlns:wzs="http://www.opengis.net/wzs/2.0">
      <wzs:bar>baz</wzs:bar>
    </wzs:GetFoo>''')) == BaseRequest(
        service='WZS',
        version=Version(3, 0),
        request='GetFoo'
    )

    assert xml_decode_base_request(dedent('''
    <wzs:GetCapabilities service="WZS"
        xmlns:wzs="http://www.opengis.net/wzs/2.0" xmlns:ows="http://www.opengis.net/ows/2.0">
      <ows:AcceptVersions>
        <ows:Version>3.0</ows:Version>
        <ows:Version>4.0</ows:Version>
      </ows:AcceptVersions>
    </wzs:GetCapabilities>''')) == BaseRequest(
        service='WZS',
        request='GetCapabilities',
        accept_versions=[Version(3, 0), Version(4, 0)],
    )
