
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
