# -------------------------------------------------------------------------------
#
# Project: pyows <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
# -------------------------------------------------------------------------------
# Copyright (C) 2020 EOX IT Services GmbH
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

from datetime import timedelta, timezone, datetime, date

from .util import isoformat, temporal_bounds, parse_temporal, month, year


M_ONE_HOUR = timezone(-timedelta(seconds=60 * 60))
P_ONE_HOUR = timezone(timedelta(seconds=60 * 60))
UTC = timezone.utc


def test_isoformat():
    assert isoformat(year(2012)) == '2012'

    assert isoformat(month(2012, 1)) == '2012-01'

    assert isoformat(date(2012, 1, 13)) == '2012-01-13'

    assert isoformat(datetime(2012, 1, 13, tzinfo=UTC)) == '2012-01-13T00:00:00Z'
    assert isoformat(datetime(2012, 1, 13, tzinfo=UTC), False) == '2012-01-13T00:00:00+00:00'

    assert isoformat(datetime(2012, 1, 13, tzinfo=M_ONE_HOUR)) == '2012-01-13T00:00:00-01:00'
    assert isoformat(datetime(2012, 1, 13, tzinfo=P_ONE_HOUR)) == '2012-01-13T00:00:00+01:00'


def test_temporal_bounds():
    assert temporal_bounds(year(2012)) == (
        datetime(2012, 1, 1, tzinfo=UTC),
        datetime(2012, 12, 31, 23, 59, 59, 999999, tzinfo=UTC)
    )

    assert temporal_bounds(month(2012, 1)) == (
        datetime(2012, 1, 1, tzinfo=UTC),
        datetime(2012, 1, 31, 23, 59, 59, 999999, tzinfo=UTC)
    )
    assert temporal_bounds(month(2012, 12)) == (
        datetime(2012, 12, 1, tzinfo=UTC),
        datetime(2012, 12, 31, 23, 59, 59, 999999, tzinfo=UTC)
    )

    assert temporal_bounds(date(2012, 1, 13)) == (
        datetime(2012, 1, 13, tzinfo=UTC),
        datetime(2012, 1, 13, 23, 59, 59, 999999, tzinfo=UTC)
    )

    assert temporal_bounds(datetime(2012, 1, 13, tzinfo=UTC)) == (
        datetime(2012, 1, 13, tzinfo=UTC),
        datetime(2012, 1, 13, tzinfo=UTC)
    )


def test_parse_temporal():
    assert parse_temporal('2012') == year(2012)

    assert parse_temporal('2012-1') == month(2012, 1)
    assert parse_temporal('2012-01') == month(2012, 1)
    assert parse_temporal('201201') == month(2012, 1)

    assert parse_temporal('2012-1-13') == date(2012, 1, 13)
    assert parse_temporal('2012-01-13') == date(2012, 1, 13)
    assert parse_temporal('20120113') == date(2012, 1, 13)

    # datetime without timezone (assuming zulu)
    assert parse_temporal('2012-1-13T00:00:00') == datetime(2012, 1, 13, tzinfo=UTC)
    assert parse_temporal('2012-01-13T00:00:00') == datetime(2012, 1, 13, tzinfo=UTC)
    assert parse_temporal('20120113T00:00:00') == datetime(2012, 1, 13, tzinfo=UTC)

    # datetime with timezone Z
    assert parse_temporal('2012-1-13T00:00:00Z') == datetime(2012, 1, 13, tzinfo=UTC)
    assert parse_temporal('2012-01-13T00:00:00Z') == datetime(2012, 1, 13, tzinfo=UTC)
    assert parse_temporal('20120113T00:00:00Z') == datetime(2012, 1, 13, tzinfo=UTC)

    # datetime with timezone negative offset
    assert parse_temporal('2012-1-13T00:00:00-01:00') == datetime(2012, 1, 13, tzinfo=M_ONE_HOUR)
    assert parse_temporal('2012-01-13T00:00:00-01:00') == datetime(2012, 1, 13, tzinfo=M_ONE_HOUR)
    assert parse_temporal('20120113T00:00:00-01:00') == datetime(2012, 1, 13, tzinfo=M_ONE_HOUR)

    # datetime with timezone positive offset
    assert parse_temporal('2012-1-13T00:00:00+01:00') == datetime(2012, 1, 13, tzinfo=P_ONE_HOUR)
    assert parse_temporal('2012-01-13T00:00:00+01:00') == datetime(2012, 1, 13, tzinfo=P_ONE_HOUR)
    assert parse_temporal('20120113T00:00:00+01:00') == datetime(2012, 1, 13, tzinfo=P_ONE_HOUR)
