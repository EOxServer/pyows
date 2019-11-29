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

from typing import List

from ows.util import Result
from ows.cis.v11 import (
    encode_envelope, encode_domain_set, encode_range_type
)
from .namespaces import WCS, ns_gml
from ..types import CoverageDescription


def xml_encode_coverage_descriptions(coverage_descriptions: List[CoverageDescription], **kwargs):
    root = WCS('CoverageDescriptions', *[
        WCS('CoverageDescription',
            encode_envelope(coverage_description.grid),
            # TODO: metadata
            encode_domain_set(coverage_description.grid),
            encode_range_type(coverage_description.range_type),
            WCS('ServiceParameters',
                WCS('CoverageSubtype', coverage_description.coverage_subtype),
                WCS('CoverageSubtype',
                    coverage_description.coverage_subtype_parent
                ) if coverage_description.coverage_subtype_parent else None,
                WCS('nativeFormat', coverage_description.native_format),
            ),
            **{
                ns_gml('id'): coverage_description.identifier
            }
        )
        for coverage_description in coverage_descriptions
    ])

    return Result.from_etree(root, **kwargs)
