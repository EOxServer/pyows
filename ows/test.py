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

from collections import defaultdict

from lxml.etree import _Comment
from lxml import etree


def assert_xml_equal(xml_a: str, xml_b: str):
    assert_elements_equal(
        etree.fromstring(xml_a), etree.fromstring(xml_b)
    )


def strip_common_attribs(attrib):
    attrib.pop(
        '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation', None
    )
    return attrib


def strip_elements(elements):
    return [
        element
        for element in elements
        if not isinstance(element, _Comment)
    ]


def assert_elements_equal(elem_a, elem_b, path='/'):
    q_a = etree.QName(elem_a.tag)
    q_b = etree.QName(elem_b.tag)
    assert q_a.localname == q_b.localname, \
        f'Tag name differs at {path!r}: {q_a.localname} != {q_b.localname}'
    assert q_a.namespace == q_b.namespace, \
        f'Namespace differs at {path!r}: {q_a.namespace} != {q_b.namespace}'

    text_a = elem_a.text.strip() if elem_a.text is not None else ''
    text_b = elem_b.text.strip() if elem_b.text is not None else ''
    assert text_a == text_b, \
        f'Text differs at {path!r}: {text_a!r} != {text_b!r}'

    attrib_a = strip_common_attribs(elem_a.attrib)
    attrib_b = strip_common_attribs(elem_b.attrib)

    assert attrib_a == attrib_b, \
        f'Attributes mismatch at {path!r}: {attrib_a!r} != {attrib_b!r}'

    tag_counts = defaultdict(lambda: 0)

    subs_a = strip_elements(elem_a)
    subs_b = strip_elements(elem_b)

    for i, subelements in enumerate(zip(subs_a, subs_b), start=1):
        sub_a, sub_b = subelements
        q_s = etree.QName(sub_a.tag)
        # localname = q_s.localname
        tag_counts[sub_a.tag] += 1
        count = tag_counts[sub_a.tag]
        assert_elements_equal(
            sub_a, sub_b,
            path=f'{path!r}/{sub_a.prefix}:{q_s.localname}[{count}]'
        )

    if len(subs_a) > len(subs_b):
        elems = subs_a[len(elem_b):]
        raise AssertionError(
            f'Element A at {path!r} has additional children: {elems!r}'
        )

    elif len(subs_a) < len(subs_b):
        elems = subs_b[len(subs_a):]
        raise AssertionError(
            f'Element B at {path!r} has additional children: {elems!r}'
        )


# def test_assertion():
#     a = etree.fromstring(dedent('''<root>
#         <child>
#             <child a='a'>
#             </child>
#             <child a='a'>
#             </child>
#         </child>
#     </root>'''))

#     b = etree.fromstring(dedent('''<root>
#         <child>
#             <childX a='a'>
#             </childX>
#             <child a='a' b='b'>
#             </child>
#         </child>
#     </root>'''))

#     assert_elements_equal(a, b)
