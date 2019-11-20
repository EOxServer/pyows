from ows.xml import NameSpaceMap, NameSpace, ElementMaker


ns_xlink = NameSpace("http://www.w3.org/1999/xlink", "xlink")
ns_ows = NameSpace("http://www.opengis.net/ows/2.0", "ows", "http://schemas.opengis.net/ows/2.0/owsAll.xsd")
ns_xml = NameSpace("http://www.w3.org/XML/1998/namespace", "xml")

nsmap = NameSpaceMap(ns_ows)
OWS = ElementMaker(namespace=ns_ows.uri, nsmap=nsmap)
