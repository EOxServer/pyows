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

""" This module contains facilities to help decoding XML structures.
"""

from typing import List, Dict, Optional

from lxml import etree
from lxml.builder import ElementMaker as _ElementMaker

from .decoder import BaseParameter, BaseDecoder, NO_DEFAULT


# type alias
Element = etree._Element
ElementTree = etree._ElementTree
Comment = etree.Comment


class ElementMaker(_ElementMaker):
    ''' Subclass of the original ElementMaker that automatically filters out
        None values in sub-elements and attributes.
    '''
    def __call__(self, tag: str, *args: List[Optional[Element]],
                 **kwargs: Dict[str, Optional[str]]) -> Element:
        return super().__call__(tag, *[
            arg
            for arg in args
            if arg is not None
        ], **{
            key: value
            for key, value in kwargs.items()
            if value is not None
        })


class NameSpace(object):
    ''' Helper object to ease the dealing with namespaces in both encoding and
        decoding.

        :param uri: the namespace URI
        :param prefix: the namespace prefix
        :param schema_location: the schema location of this namespace
    '''

    def __init__(self, uri: str, prefix=None, schema_location=None):
        self._uri = uri
        self._lxml_uri = "{%s}" % uri
        self._prefix = prefix
        self._schema_location = schema_location

    @property
    def uri(self):
        return self._uri

    @property
    def prefix(self):
        return self._prefix

    @property
    def schema_location(self):
        return self._schema_location

    def __eq__(self, other):
        if isinstance(other, NameSpace):
            return self.uri == other.uri
        elif isinstance(other, str):
            return self.uri == other

        raise TypeError

    def __call__(self, tag):
        return self._lxml_uri + tag


class NameSpaceMap(dict):
    """ Helper object to ease the setup and management of namespace collections
        in both encoding and decoding. Can (and should) be passed as
        ``namespaces`` attribute in :class:`ows.xml.Decoder`
        subclasses.

        :param namespaces: a list of :class:`NameSpace` objects.
    """

    def __init__(self, *namespaces):
        self._schema_location_dict = {}
        for namespace in namespaces:
            self.add(namespace)
        self._namespaces = namespaces

    def add(self, namespace):
        self[namespace.prefix] = namespace.uri
        if namespace.schema_location:
            self._schema_location_dict[namespace.uri] = (
                namespace.schema_location
            )

    def __copy__(self):
        return type(self)(*self._namespaces)

    @property
    def schema_locations(self):
        return self._schema_location_dict


ns_xsi = NameSpace("http://www.w3.org/2001/XMLSchema-instance", "xsi")


class Parameter(BaseParameter):
    """ Parameter for XML values.

        :param selector: the node selector; if a string is passed it is
                         interpreted as an XPath expression, a callable will be
                         called with the root of the element tree and shall
                         yield any number of node
        :param type: the type to parse the raw value; by default the raw
                     string is returned
        :param num: defines how many times the key can be present; use any
                    numeric value to set it to a fixed count, "*" for any
                    number, "?" for zero or one time or "+" for one or more
                    times
        :param default: the default value
        :param namespaces: any namespace necessary for the XPath expression;
                           defaults to the :class:`Decoder` namespaces.
        :param locator: override the locator in case of exceptions
    """

    def __init__(self, selector, type=None, num=1, default=NO_DEFAULT,
                 default_factory=None, namespaces=None, locator=None):
        super(Parameter, self).__init__(type, num, default, default_factory)
        self.selector = selector
        self.namespaces = namespaces
        self._locator = locator

    def select(self, decoder):
        # prepare the XPath selector if necessary
        if isinstance(self.selector, str):
            namespaces = self.namespaces or decoder.namespaces
            self.selector = etree.XPath(self.selector, namespaces=namespaces)

        results = self.selector(decoder._tree)
        if isinstance(results, (str, float, int)):
            results = [results]

        return results

    @property
    def locator(self):
        return self._locator or str(self.selector)


class Decoder(BaseDecoder):
    """ Base class for XML Decoders.

        :param params: an instance of either :class:`lxml.etree.ElementTree`,
                       or :class:`basestring` (which will be parsed using
                       :func:`lxml.etree.fromstring`)

    Decoders should be used as such:
    ::

        from ows import xml, typelist

        class ExampleDecoder(xml.Decoder):
            namespaces = {"myns": "http://myns.org"}
            single = xml.Parameter("myns:single/text()", num=1)
            items = xml.Parameter("myns:collection/myns:item/text()", num="+")
            attr_a = xml.Parameter("myns:object/@attrA", num="?")
            attr_b = xml.Parameter("myns:object/@attrB", num="?", default="x")


        decoder = ExampleDecoder('''
            <myns:root xmlns:myns="http://myns.org">
                <myns:single>value</myns:single>
                <myns:collection>
                    <myns:item>a</myns:item>
                    <myns:item>b</myns:item>
                    <myns:item>c</myns:item>
                </myns:collection>
                <myns:object attrA="value"/>
            </myns:root>
        ''')

        print(decoder.single)
        print(decoder.items)
        print(decoder.attr_a)
        print(decoder.attr_b)
    """

    # must be overriden if the XPath expressions use
    # namespaces
    namespaces = {}

    def __init__(self, tree):
        if isinstance(tree, (str, bytes)):
            try:
                tree = etree.fromstring(tree)
            except etree.XMLSyntaxError as exc:
                raise ValueError(
                    "Malformed XML document. Error was %s" % exc
                ) from exc
        elif isinstance(tree, etree._Element):
            pass
        else:
            raise ValueError(f'Unsupported type {type(tree)}')
        self._tree = tree
