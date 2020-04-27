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

from ows.xml import NameSpace


class Registry:
    def __init__(self):
        self.kvp_decoders = {}
        self.xml_decoders = {}
        self.kvp_encoders = {}
        self.xml_encoders = {}
        # TODO: also decode JSON?

    def register_kvp_decoder(self, service, version, request):
        """ Decorator function to register a KVP decoder.
        """
        def _inner(decoder):
            key = (service.lower(), version, request.lower())
            self.kvp_decoders[key] = decoder

        return _inner

    def register_xml_decoder(self, tag_name, namespace=None):
        """ Decorator function to register an XML decoder.
        """
        if isinstance(namespace, NameSpace):
            namespace = namespace.uri

        def _inner(decoder):
            self.xml_decoders[(tag_name, namespace)] = decoder

        return _inner

    def register_kvp_encoder(self, object_class):
        """ Decorator function to register a KVP encoder.
        """
        def _inner(encoder):
            self.kvp_encoders[object_class] = encoder

        return _inner

    def register_xml_encoder(self, object_class):
        """ Decorator function to register an XML encoder.
        """
        def _inner(encoder):
            self.xml_encoders[object_class] = encoder

        return _inner

    def get_kvp_decoder(self, service, version, request):
        return self.kvp_decoders[request]

    def get_xml_decoder(self, tag_name, namespace=None):
        return self.xml_decoders[(tag_name, namespace)]


# the default registry to be used
registry = Registry()
