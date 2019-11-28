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

from ows.xml import NameSpace, NameSpaceMap, ElementMaker, ns_xsi
from ows.common.v20.namespaces import ns_ows, ns_xlink
from ows.gml.v32 import ns_gml
from ows.cis.v11 import (
    ns_cis, encode_envelope, encode_axis, encode_domain_set,
    encode_range_type
)


# namespace declarations
ns_wcs = NameSpace("http://www.opengis.net/wcs/2.1/gml", "wcs")
ns_crs = NameSpace("http://www.opengis.net/wcs/crs/1.0", "crs")
ns_rsub = NameSpace("http://www.opengis.net/wcs/range-subsetting/1.0", "rsub")
ns_eowcs = NameSpace("http://www.opengis.net/wcs/wcseo/1.0", "wcseo",
                     "http://schemas.opengis.net/wcs/wcseo/1.0/wcsEOAll.xsd")
ns_swe = NameSpace("http://www.opengis.net/swe/2.0", "swe")
ns_int = NameSpace("http://www.opengis.net/wcs/interpolation/1.0", "int")
ns_scal = NameSpace("http://www.opengis.net/wcs/scaling/1.0", "scal")

# namespace map
nsmap = NameSpaceMap(
    ns_xlink, ns_ows, ns_wcs, ns_crs, ns_rsub,
    ns_eowcs, ns_swe, ns_int, ns_scal, ns_gml
)

# Element factories

WCS = ElementMaker(namespace=ns_wcs.uri, nsmap=nsmap)
CRS = ElementMaker(namespace=ns_crs.uri, nsmap=nsmap)
SCAL = ElementMaker(namespace=ns_scal.uri, nsmap=nsmap)
EOWCS = ElementMaker(namespace=ns_eowcs.uri, nsmap=nsmap)
SWE = ElementMaker(namespace=ns_swe.uri, nsmap=nsmap)
INT = ElementMaker(namespace=ns_int.uri, nsmap=nsmap)
