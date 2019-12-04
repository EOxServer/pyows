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

from typing import Union
from textwrap import dedent
from collections import defaultdict

from lxml.etree import ElementTree, Element
from lxml import etree

def assert_xml_equal(xml_a: str, xml_b: str):
    assert_elements_equal(
        etree.fromstring(xml_a), etree.fromstring(xml_b)
    )


def assert_trees_equal(tree_a: ElementTree, tree_b: ElementTree):
    pass


def assert_elements_equal(elem_a, elem_b, path=''):
    q_a = etree.QName(elem_a.tag)
    q_b = etree.QName(elem_b.tag)
    assert q_a.localname == q_b.localname, \
        f'Tag name differs at {path}: {q_a.localname} != {q_b.localname}'
    assert q_a.namespace == q_b.namespace, \
        f'Namespace differs at {path}: {q_a.namespace} != {q_b.namespace}'
    assert elem_a.text == elem_b.text, f'Text differs at {path}'

    assert elem_a.attrib == elem_b.attrib, f'Attributes mismatch at {path}'

    tag_counts = defaultdict(lambda: 0)

    for i, subelements in enumerate(zip(elem_a, elem_b), start=1):
        sub_a, sub_b = subelements
        q_s = etree.QName(sub_a.tag)
        # localname = q_s.localname
        tag_counts[sub_a.tag] += 1
        count = tag_counts[sub_a.tag]
        assert_elements_equal(
            sub_a, sub_b,
            path=f'{path}/{sub_a.prefix}:{q_s.localname}[{count}]'
        )

    if len(elem_a) > len(elem_b):
        raise AssertionError(f'Element A at {path} has additional children.')

    elif len(elem_a) < len(elem_b):
        raise AssertionError(f'Element B at {path} has additional children.')


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
