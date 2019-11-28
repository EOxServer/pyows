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


class InvalidSubsettingException(Exception):
    """
    This exception indicates an invalid WCS 2.0 subsetting parameter was
    submitted.
    """
    code = "InvalidSubsetting"
    locator = "subset"


class InvalidSubsettingCrsException(Exception):
    """
    This exception indicates an invalid WCS 2.0 subsettingCrs parameter was
    submitted.
    """
    code = "SubsettingCrs-NotSupported"
    locator = "subsettingCrs"


class InvalidOutputCrsException(Exception):
    """
    This exception indicates an invalid WCS 2.0 outputCrs parameter was
    submitted.
    """
    code = "OutputCrs-NotSupported"
    locator = "outputCrs"


class InvalidScaleFactorException(Exception):
    """ Error in ScaleFactor and ScaleAxis operations
    """
    code = "InvalidScaleFactor"

    def __init__(self, scalefactor):
        super().__init__(
            "Scalefactor '%s' is not valid" % scalefactor
        )
        self.locator = scalefactor


class InvalidScaleExtentException(Exception):
    """ Error in ScaleExtent operations
    """
    code = "InvalidExtent"

    def __init__(self, low, high):
        super().__init__(
            "ScaleExtent '%s:%s' is not valid" % (low, high)
        )
        self.locator = high


class NoSuchCoverageException(Exception):
    """ This exception indicates that the requested coverage(s) do not
        exist.
    """
    code = "NoSuchCoverage"

    # def __str__(self):
    #     return "No such Coverage%s with ID: %s" % (
    #         "" if len(self.items) == 1 else "s",
    #         ", ".join(map(lambda i: "'%s'" % i, self.items))
    #     )


class NoSuchDatasetSeriesOrCoverageException(Exception):
    """ This exception indicates that the requested coverage(s) or dataset
        series do not exist.
    """
    code = "NoSuchDatasetSeriesOrCoverage"

    # def __str__(self):
    #     return "No such Coverage%s or Dataset Series with ID: %s" % (
    #         " " if len(self.items) == 1 else "s",
    #         ", ".join(map(lambda i: "'%s'" % i, self.items))
    #     )


class InterpolationMethodNotSupportedException(Exception):
    """
    This exception indicates a not supported interpolation method.
    """
    code = "InterpolationMethodNotSupported"
    locator = "interpolation"
