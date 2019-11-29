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

from ows.xml import ElementMaker, NameSpace, NameSpaceMap, Element
from .types import Field, DataRecord

ns_swe = NameSpace("http://www.opengis.net/swe/2.0", "swe")

nsmap = NameSpaceMap(ns_swe)

SWE = ElementMaker(namespace=ns_swe.uri, nsmap=nsmap)


def encode_field(field: Field) -> Element:
    return SWE('field',
        SWE('Quantity',
            SWE('description', field.description),
            SWE('nilValues',
                SWE('NilValues', *[
                    SWE('nilValue',
                        str(value),
                        reason=reason
                    )
                    for value, reason in field.nil_values.items()
                ])
            ),
            SWE('uom', code=field.uom),
            SWE('constraint',
                SWE('AllowedValues', *[
                    SWE('value', str(value))
                    if isinstance(value, (int, float)) else
                    SWE('interval', f'{value[0]} {value[1]}')
                    for value in field.allowed_values
                ] + [
                    SWE('significantFigures',
                        str(field.significant_figures)
                    ) if field.significant_figures is not None else None
                ])
            )
        ),
        name=field.name,
    )


def encode_data_record(data_record: DataRecord) -> Element:
    return SWE('DataRecord', *[
        encode_field(field)
        for field in data_record
    ])
