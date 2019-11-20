#-------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
#-------------------------------------------------------------------------------
# Copyright (C) 2014 EOX IT Services GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-------------------------------------------------------------------------------

from ows.xml import ElementMaker, NameSpace, NameSpaceMap


# namespace declarations
ns_gml = NameSpace("http://www.opengis.net/gml/3.2", "gml")
ns_gmlcov = NameSpace("http://www.opengis.net/gmlcov/1.0", "gmlcov")
ns_om = NameSpace("http://www.opengis.net/om/2.0", "om")
ns_eop = NameSpace("http://www.opengis.net/eop/2.0", "eop")

nsmap = NameSpaceMap(ns_gml, ns_gmlcov, ns_om, ns_eop)

# Element factories
GML = ElementMaker(namespace=ns_gml.uri, nsmap=nsmap)
GMLCOV = ElementMaker(namespace=ns_gmlcov.uri, nsmap=nsmap)
OM = ElementMaker(namespace=ns_om.uri, nsmap=nsmap)
EOP = ElementMaker(namespace=ns_eop.uri, nsmap=nsmap)
