# ------------------------------------------------------------------------------
#
# Project: pyows <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
# ------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------

""" This module provides base functionality for any other decoder class.
"""

ZERO_OR_ONE = "?"
ONE_OR_MORE = "+"
ANY = "*"

SINGLE_VALUES = (ZERO_OR_ONE, 1)


class DecodingException(Exception):
    """ Base Exception class to be thrown whenever a decoding failed.
    """

    def __init__(self, message, locator=None):
        super().__init__(message)
        self.locator = locator


class WrongMultiplicityException(DecodingException):
    """ Decoding Exception to be thrown when the multiplicity of a parameter did
        not match the expected count.
    """

    code = "InvalidParameterValue"

    def __init__(self, locator, expected, result):
        super().__init__(
            "Parameter '%s': expected %s got %d" % (locator, expected, result),
            locator
        )


class MissingParameterException(DecodingException):
    """ Exception to be thrown, when a decoder could not read one parameter,
        where exactly one was required.
    """
    code = "MissingParameterValue"

    def __init__(self, locator):
        super().__init__(
            "Missing required parameter '%s'" % locator, locator
        )


class MissingParameterMultipleException(DecodingException):
    """ Exception to be thrown, when a decoder could not read at least one
        parameter, where one ore more were required.
    """
    code = "MissingParameterValue"

    def __init__(self, locator):
        super().__init__(
            "Missing at least one required parameter '%s'" % locator, locator
        )


class NoChoiceResultException(DecodingException):
    pass


class ExclusiveException(DecodingException):
    pass

# NOTE: The following exceptions may get propagated as OWS exceptions
#       therefore it is necessary to set the proper OWS exception code.


class InvalidParameterException(DecodingException):
    code = "InvalidParameterValue"


# Compound fields


class Choice:
    """ Tries all given choices until one does return something.
    """

    def __init__(self, *choices):
        self.choices = choices

    def __get__(self, decoder, decoder_class=None):
        for choice in self.choices:
            try:
                return choice.__get__(decoder, decoder_class)
            except Exception:
                continue
        raise NoChoiceResultException


class Exclusive:
    """ For mutual exclusive Parameters.
    """

    def __init__(self, *choices):
        self.choices = choices

    def __get__(self, decoder, decoder_class=None):
        result = None
        num = 0
        for choice in self.choices:
            try:
                result = choice.__get__(decoder, decoder_class)
                num += 1
            except Exception:
                continue

        if num != 1:
            raise ExclusiveException

        return result


class Concatenate:
    """ Helper to concatenate the results of all sub-parameters to one.
    """
    def __init__(self, *choices, **kwargs):
        self.choices = choices
        self.allow_errors = kwargs.get("allow_errors", True)

    def __get__(self, decoder, decoder_class=None):
        result = []
        for choice in self.choices:
            try:
                value = choice.__get__(decoder, decoder_class)
                if isinstance(value, (list, tuple)):
                    result.extend(value)
                else:
                    result.append(value)
            except Exception as exc:
                if self.allow_errors:
                    # swallow exception
                    continue

                raise exc

        return result


# Type conversion helpers


class typelist:
    """ Helper for XMLDecoder schemas that expect a string that represents a
        list of a type separated by some separator.
    """

    def __init__(self, typ=None, separator=" "):
        self.typ = typ
        self.separator = separator

    def __call__(self, value):
        split = value.split(self.separator)
        if self.typ:
            return [self.typ(v) for v in split]
        return split


class fixed:
    """ Helper for parameters that are expected to be have a fixed value and
        raises a ValueError if not.
    """

    def __init__(self, value, case_sensitive=True):
        self.value = value if case_sensitive else value.lower()
        self.case_sensitive = case_sensitive

    def __call__(self, value):
        compare = value if self.case_sensitive else value.lower()
        if self.value != compare:
            raise ValueError(
                "Value mismatch, expected %s, got %s." %
                (self.value, value)
            )

        return value


class enum:
    """ Helper for parameters that are expected to be in a certain enumeration.
        A ValueError is raised if not.
    """

    def __init__(self, values, case_sensitive=True):
        self.values = values
        self.compare_values = values if case_sensitive else [
            lower(v) for v in values
        ]
        self.case_sensitive = case_sensitive

    def __call__(self, value):
        compare = value if self.case_sensitive else value.lower()
        if compare not in self.compare_values:
            raise ValueError(
                "Unexpected value '%s'. Expected one of: %s." %
                (value, ", ".join(map(lambda s: "'%s'" % s, self.values)))
            )

        return value


def lower(value):
    """ Functor to return a lower-case string.
    """
    return value.lower()


def upper(value):
    """ Functor to return a upper-case string.
    """
    return value.upper()


def strip(value):
    """ Functor to return a whitespace stripped string.
    """
    return value.strip()


class value_range:
    """ Helper to assert that a given parameter is within a specified range.
    """

    def __init__(self, min, max, type=float):
        self._min = min
        self._max = max
        self._type = type

    def __call__(self, raw):
        value = self._type(raw)
        if value < self._min or value > self._max:
            raise ValueError(
                "Given value '%s' exceeds expected bounds (%s, %s)"
                % (value, self._min, self._max)
            )
        return value


def boolean(raw):
    """ Functor to convert "true"/"false" to a boolean.
    """
    raw = raw.lower()
    if raw not in ("true", "false"):
        raise ValueError("Could not parse a boolean value from '%s'." % raw)
    return raw == "true"


def to_dict(decoder, dict_class=dict):
    """ Utility function to get a dictionary representation of the given decoder.
        This function invokes all decoder parameters and sets the dictionary
        fields accordingly
    """
    return dict_class(
        (name, getattr(decoder, name))
        for name in dir(decoder)
        if not name.startswith("_") and name != "namespaces"
    )


class NO_DEFAULT:
    pass


class BaseParameter(property):
    """ Abstract base class for XML, KVP or any other kind of parameter.
    """

    def __init__(self, type=None, num=1, default=NO_DEFAULT,
                 default_factory=None):
        super().__init__(self.fget)
        self.type = type or str
        self.num = num
        self.default = default
        self.default_factory = default_factory

    def select(self, decoder):
        """ Interface method.
        """
        raise NotImplementedError

    @property
    def locator(self):
        return ""

    def fget(self, decoder):
        """ Property getter function.
        """

        results = self.select(decoder)
        count = len(results)

        locator = self.locator
        multiple = self.num not in SINGLE_VALUES

        # check the correct count of the result
        if not multiple and count > 1:
            raise WrongMultiplicityException(locator, "at most one", count)

        elif self.num == 1 and count == 0:
            raise MissingParameterException(locator)

        elif self.num == ONE_OR_MORE and count == 0:
            raise MissingParameterMultipleException(locator)

        elif isinstance(self.num, int) and count != self.num:
            raise WrongMultiplicityException(locator, self.num, count)

        # parse the value/values, or return the defaults
        if multiple:
            if count == 0 and self.num == ANY:
                if self.default_factory:
                    return self.default_factory()
                elif self.default is not NO_DEFAULT:
                    return self.default

            try:
                return [self.type(v) for v in results]
            except Exception as e:
                # let some more sophisticated exceptions pass
                if hasattr(e, "locator") or hasattr(e, "code"):
                    raise
                raise InvalidParameterException(str(e), locator)

        elif self.num == ZERO_OR_ONE and count == 0:
            if self.default_factory:
                return self.default_factory()
            elif self.default is not NO_DEFAULT:
                return self.default
            else:
                return None

        elif self.type:
            try:
                return self.type(results[0])
            except Exception as e:
                # let some more sophisticated exceptions pass
                if hasattr(e, "locator") or hasattr(e, "code"):
                    raise
                raise InvalidParameterException(str(e), locator)

        return results[0]


class BaseDecoder:
    object_class = None

    def create_object(self, params: dict):
        """ Create the associated object for that decoder using the
            passed parameters.
        """
        if self.object_class is not None:
            return self.object_class(**params)

        raise NotImplementedError

    def map_params(self, params):
        """ Map parameters, if necessary. Default implementation is
            a no-op.
        """
        return params

    def collect_params(self):
        """ Collect all parameters. This will collect all values
            which are computed using properties.
        """
        cls = type(self)
        return {
            name: getattr(self, name)
            for name in dir(self)
            if isinstance(getattr(cls, name, None), property)
        }

    def decode(self):
        """ Collect all decoder parameters and construct the object.
        """
        return self.create_object(
            self.map_params(
                self.collect_params()
            )
        )
