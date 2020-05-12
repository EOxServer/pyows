# -------------------------------------------------------------------------------
#
# Project: pyows <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
# -------------------------------------------------------------------------------
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
# -------------------------------------------------------------------------------

from textwrap import dedent

from ...test import assert_xml_equal
from ..types import OWSException, Version
from .encoders import xml_encode_exception_report


def test_xml_encode_exception_report():
    # simple Exception
    exc = OWSException('code', 'locator', 'text')
    assert_xml_equal(xml_encode_exception_report(exc, Version(2, 0)).value.decode('utf-8'), dedent("""
    <ows:ExceptionReport xmlns:ows="http://www.opengis.net/ows/2.0" version="2.0">
      <ows:Exception exceptionCode="code" locator="locator">
        <ows:ExceptionText>text</ows:ExceptionText>
      </ows:Exception>
    </ows:ExceptionReport>
    """))

    # no locator and text
    exc = OWSException('code')
    assert_xml_equal(xml_encode_exception_report(exc, Version(2, 0)).value.decode('utf-8'), dedent("""
    <ows:ExceptionReport xmlns:ows="http://www.opengis.net/ows/2.0" version="2.0">
      <ows:Exception exceptionCode="code"></ows:Exception>
    </ows:ExceptionReport>
    """))

    # multi-text
    exc = OWSException('code', 'locator', ['text1', 'text2'])
    assert_xml_equal(xml_encode_exception_report(exc, Version(2, 0)).value.decode('utf-8'), dedent("""
    <ows:ExceptionReport xmlns:ows="http://www.opengis.net/ows/2.0" version="2.0">
      <ows:Exception exceptionCode="code" locator="locator">
        <ows:ExceptionText>text1</ows:ExceptionText>
        <ows:ExceptionText>text2</ows:ExceptionText>
      </ows:Exception>
    </ows:ExceptionReport>
    """))

    # multiple exceptions
    exc = [
        OWSException('codeA', 'locatorA', 'textA'),
        OWSException('codeB', 'locatorB', 'textB'),
    ]

    assert_xml_equal(xml_encode_exception_report(exc, Version(2, 0)).value.decode('utf-8'), dedent("""
    <ows:ExceptionReport xmlns:ows="http://www.opengis.net/ows/2.0" version="2.0">
      <ows:Exception exceptionCode="codeA" locator="locatorA">
        <ows:ExceptionText>textA</ows:ExceptionText>
      </ows:Exception>
      <ows:Exception exceptionCode="codeB" locator="locatorB">
        <ows:ExceptionText>textB</ows:ExceptionText>
      </ows:Exception>
    </ows:ExceptionReport>
    """))
