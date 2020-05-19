Structure
=========

The pyows package is stuctured after the OWS family of services and schemas.
Thus, its sub-packages are named after the service or schema it implements.

Many OWS schemas are available in more than one version. This is covered by
modules or packages using sub-packages or modules with the version as its
name.


General concepts
----------------

The following concepts are re-used for almost all schemas.

Types
~~~~~~

The used types are Python classes to be used with the encoding and decoding
facilities. The types are abstractions for concepts used in the OWS services,
both in requests and responses.

Ideally, types are as generic as feasible, to be used with multiple versions
of service or schemas.

The purpose of types is to provide a structure for the data, thus all are
implemented as dataclasses. Typically, only a few functions are directly
associated with the types themselves, usually only a constructor or factory
functions.

Types are typically located in a ``type`` module in its package.


Encoders
~~~~~~~~

This family of functions transform the given data type objects to an encoded
result. There are encoders for both service requests and responses and also
the output data type depends on the requested encoding format. For requests
this could mean, that the object is encoded into a key-value-pair string for
HTTP GET style requests or as an XML string to be sent via POST.

Encoders can be found in the ``encoders`` module of its associated package.


Decoders
~~~~~~~~

Decoders are the reverse of encoders: they get a decoded object, parse it,
and return a data object. Currently, only low-level decoders are implemented,
that parse a particular object type or fail.

In the future, a dispatching mechanism is planned, where the requests are
provisionally parsed and dispatched to decoder that can parse the full request
object of a very specific type.

Decoders can be found in the ``decoders`` module of its associated package.
