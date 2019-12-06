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

from ows import xml, kvp, Version
from ows.decoder import typelist, upper
from .types import BaseRequest

# ------------------------------------------------------------------------------
# BaseRequestDecoder
# ------------------------------------------------------------------------------


class KVPBaseRequestDecoder(kvp.Decoder):
    object_class = BaseRequest

    service = kvp.Parameter("service", type=upper, num="?")
    version = kvp.Parameter("version", type=Version.from_str, num="?")
    request = kvp.Parameter("request")
    accept_versions = kvp.Parameter('acceptversions', type=typelist(Version.from_str, ","), num="?", default_factory=list)


class XMLBaseRequestDecoder(xml.Decoder):
    object_class = BaseRequest

    service = xml.Parameter("@service", type=upper, num="?")
    version = xml.Parameter("@version", type=Version.from_str, num="?")
    request = xml.Parameter("local-name()")
    accept_versions = xml.Parameter("*[local-name()='AcceptVersions']/*[local-name()='Version']/text()", type=Version.from_str, num="*", default_factory=list)


def kvp_decode_base_request(kvp):
    decoder = KVPBaseRequestDecoder(kvp)
    return decoder.decode()


def xml_decode_base_request(xml):
    decoder = XMLBaseRequestDecoder(xml)
    return decoder.decode()
