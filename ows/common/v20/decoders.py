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


import re

from ows import kvp, xml
from ows.base import typelist, lower

from .namespaces import ns_ows, nsmap
from .exceptions import (
    InvalidSubsettingException, InvalidScaleFactorException,
    InvalidScaleExtentException,
)
from . import objects


# ------------------------------------------------------------------------------
# GetCapabilities
# ------------------------------------------------------------------------------

class KVPGetCapabilitiesDecoder(kvp.Decoder):
    object_class = objects.GetCapabilitiesRequest
    updatesequence = kvp.Parameter(num="?")
    sections = kvp.Parameter(type=typelist(lower, ","), num="?", default_factory=list)
    accept_versions = kvp.Parameter('acceptversions', type=typelist(str, ","), num="?", default_factory=list)
    accept_formats = kvp.Parameter('acceptlanguages', type=typelist(str, ","), num="?", default_factory=list)
    acceptl_anguages = kvp.Parameter('acceptformats', type=typelist(str, ","), num="?", default_factory=list)


class XMLGetCapabilitiesDecoder(xml.Decoder):
    object_class = objects.GetCapabilitiesRequest
    sections = xml.Parameter("ows:Sections/ows:Section/text()", num="*", default_factory=list)
    updatesequence = xml.Parameter("@updateSequence", num="?")
    accept_versions = xml.Parameter("ows:AcceptVersions/ows:Version/text()", num="*", default_factory=list)
    accept_formats = xml.Parameter("ows:AcceptFormats/ows:OutputFormat/text()", num="*", default_factory=list)
    accept_languages = xml.Parameter("ows:AcceptLanguages/ows:Language/text()", num="*", default_factory=list)

    namespaces = nsmap


def kvp_decode_get_capabilities(kvp):
    decoder = KVPGetCapabilitiesDecoder(kvp)
    return decoder.decode()


def xml_decode_get_capabilities(xml):
    decoder = XMLGetCapabilitiesDecoder(xml)
    return decoder.decode()

