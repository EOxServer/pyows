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

from datetime import datetime

from .encoders import xml_encode_coverage_descriptions
from ows.cis.v11 import Grid, Field, RegularAxis, IrregularAxis
from ..types import CoverageDescription


print(xml_encode_coverage_descriptions([
    CoverageDescription(
        identifier='a',
        range_type=[
            Field(
                name='B01',
                description='',
                uom='W.m-2.sr-1.nm-1',
                nil_values={
                    0: 'http://www.opengis.net/def/nil/OGC/0/unknown'
                },
                allowed_values=[(0, 65535)],
                # significant_figures=5,
            )
        ],
        grid=Grid(
            axes=[
                RegularAxis(
                    'lon', 'i', 0.0, 2.0, 0.1, uom='deg', size=20
                ),
                RegularAxis(
                    'lat', 'j', 0.0, 2.0, 0.1, uom='deg', size=20
                ),
                IrregularAxis(
                    'time', 'k', positions=[
                        datetime(2019, 7, 18),
                        datetime(2019, 7, 19),
                        datetime(2019, 7, 20),
                        datetime(2019, 7, 21),
                    ], uom='ISO8601'
                )
            ],
            srs='http://www.opengis.net/def/crs/EPSG/0/4326',
        ),
        native_format='image/tiff',
        coverage_subtype='RectifiedDataset'
    )
], pretty_print=True).value.decode('utf-8'))
