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

# flake8: noqa

from datetime import datetime
from textwrap import dedent
from urllib.parse import unquote

from lxml import etree

from ows.common.types import WGS84BoundingBox, BoundingBox, Metadata
from ows.gml.types import Grid, RegularAxis
from ows.swe.types import Field
from .types import (
    DescribeCoverageRequest, GetCoverageRequest, Trim, Slice,
    ScaleAxis, ScaleExtent, ScaleSize, AxisInterpolation,
    GeoTIFFEncodingParameters,
)
from ..types import (
    ServiceCapabilities, CoverageSummary, DatasetSeriesSummary,
    CoverageDescription
)
from .encoders import (
    kvp_encode_describe_coverage, xml_encode_describe_coverage,
    kvp_encode_get_coverage, xml_encode_get_coverage,
    xml_encode_capabilities, xml_encode_coverage_descriptions
)
from ows.test import assert_xml_equal


# ------------------------------------------------------------------------------
# DescribeCoverage
# ------------------------------------------------------------------------------

def test_encode_describe_coverage_kvp():
    request = DescribeCoverageRequest(coverage_ids=['a', 'b', 'c'])
    assert unquote(kvp_encode_describe_coverage(request).value) == (
        "service=WCS&version=2.0.1&request=DescribeCoverage&coverageid=a,b,c"
    )


def test_encode_describe_coverage_xml():
    # TODO: finalize when XML diff available
    # request = DescribeCoverageRequest(coverage_ids=['a', 'b', 'c'])

    # assert etree.fromstring(xml_encode_describe_coverage(request).value) == etree.fromstring("""
    # <wcs:DescribeCoverage
    #     xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
    #     xsi:schemaLocation="http://www.opengis.net/wcs/2.0 http://schemas.opengis.net/wcs/2.0/wcsAll.xsd"
    #     xmlns="http://www.opengis.net/wcs/2.0"
    #     xmlns:wcs="http://www.opengis.net/wcs/2.0"
    #     service="WCS"
    #     version="2.0.1">
    #     <wcs:CoverageId>a</wcs:CoverageId>
    #     <wcs:CoverageId>b</wcs:CoverageId>
    #     <wcs:CoverageId>c</wcs:CoverageId>
    # </wcs:DescribeCoverage>
    # """)
    pass


# ------------------------------------------------------------------------------
# GetCoverage
# ------------------------------------------------------------------------------


def test_encode_get_coverage_kvp():
    # simplest request
    request = GetCoverageRequest(coverage_id='a')
    assert unquote(kvp_encode_get_coverage(request).value) == (
        "service=WCS&version=2.0.1&request=GetCoverage&coverageid=a"
    )

    # trim/slice
    request = GetCoverageRequest(
        coverage_id='a',
        subsets=[
            Trim(dimension='x', low=1.2, high=2.2),
            Trim(dimension='x', low=3),
            Slice(dimension='time', point='2018-05-07')
        ]
    )
    assert unquote(kvp_encode_get_coverage(request).value) == (
        "service=WCS&version=2.0.1&request=GetCoverage&coverageid=a"
        "&subset=x(1.2,2.2)&subset=x(3,*)&subset=time('2018-05-07')"
    )

    # CRS
    request = GetCoverageRequest(
        coverage_id='a',
        subsetting_crs='EPSG:4326',
        output_crs='EPSG:3875',
    )
    assert unquote(kvp_encode_get_coverage(request).value) == (
        "service=WCS&version=2.0.1&request=GetCoverage&coverageid=a"
        "&subsettingCrs=EPSG:4326&outputCrs=EPSG:3875"
    )

    # scaling
    request = GetCoverageRequest(
        coverage_id='a',
        scalefactor=0.5,
        scales=[
            ScaleAxis(axis='x', factor=0.7),
            ScaleSize(axis='y', size=500),
            ScaleExtent(axis='z', low=200, high=600),
        ]
    )
    assert unquote(kvp_encode_get_coverage(request).value) == (
        "service=WCS&version=2.0.1&request=GetCoverage&coverageid=a"
        "&scaleFactor=0.5&scaleSize=y(500)&scaleAxes=x(0.7)&scaleExtent=z(200:600)"
    )

    # interpolation
    request = GetCoverageRequest(
        coverage_id='a',
        interpolation='NEAREST',
        axis_interpolations=[
            AxisInterpolation(axis='x', method='LINEAR'),
            AxisInterpolation(axis='y', method='CUBIC')
        ]
    )
    assert unquote(kvp_encode_get_coverage(request).value) == (
        "service=WCS&version=2.0.1&request=GetCoverage&coverageid=a&interpolation=NEAREST"
        "&interpolationPerAxis=x,LINEAR&interpolationPerAxis=y,CUBIC"
    )

    # geotiff
    request = GetCoverageRequest(
        coverage_id='a',
        geotiff_encoding_parameters=GeoTIFFEncodingParameters(
            compression='LZW',
            predictor='Horizontal',
            interleave='Band',
            tiling=True,
            tile_width=256,
            tile_height=256,
        )
    )
    assert unquote(kvp_encode_get_coverage(request).value) == (
        "service=WCS&version=2.0.1&request=GetCoverage&coverageid=a"
        "&geotiff:compression=LZW&geotiff:predictor=Horizontal&geotiff:interleave=Band"
        "&geotiff:tiling=true&geotiff:tilewidth=256&geotiff:tileheight=256"
    )


def test_encode_get_coverage_xml():
    # simplest request
    request = GetCoverageRequest(coverage_id='a')

    # trim/slice
    request = GetCoverageRequest(
        coverage_id='a',
        subsets=[
            Trim(dimension='x', low=1.2, high=2.2),
            Trim(dimension='x', low=3),
            Slice(dimension='time', point='2018-05-07')
        ]
    )
    assert_xml_equal(xml_encode_get_coverage(request, pretty_print=True).value.decode('utf-8'), dedent("""\
    <wcs:GetCoverage xmlns:crs="http://www.opengis.net/wcs/crs/1.0" xmlns:eop="http://www.opengis.net/eop/2.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmlcov="http://www.opengis.net/gmlcov/1.0" xmlns:int="http://www.opengis.net/wcs/interpolation/1.0" xmlns:ogc="http://www.opengis.net/ogc" xmlns:om="http://www.opengis.net/om/2.0" xmlns:ows="http://www.opengis.net/ows/2.0" xmlns:rsub="http://www.opengis.net/wcs/range-subsetting/1.0" xmlns:scal="http://www.opengis.net/wcs/scaling/1.0" xmlns:swe="http://www.opengis.net/swe/2.0" xmlns:wcs="http://www.opengis.net/wcs/2.0" xmlns:wcseo="http://www.opengis.net/wcs/wcseo/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" service="WCS" version="2.0.1">
      <wcs:CoverageId>a</wcs:CoverageId>
      <wcs:DimensionTrim>
        <wcs:Dimension>x</wcs:Dimension>
        <wcs:TrimLow>1.2</wcs:TrimLow>
        <wcs:TrimHigh>2.2</wcs:TrimHigh>
      </wcs:DimensionTrim>
      <wcs:DimensionTrim>
        <wcs:Dimension>x</wcs:Dimension>
        <wcs:TrimLow>3</wcs:TrimLow>
      </wcs:DimensionTrim>
      <wcs:DimensionSlice>
        <wcs:Dimension>time</wcs:Dimension>
        <wcs:SlicePoint>2018-05-07</wcs:SlicePoint>
      </wcs:DimensionSlice>
    </wcs:GetCoverage>
    """))

    # CRS
    request = GetCoverageRequest(
        coverage_id='a',
        subsetting_crs='EPSG:4326',
        output_crs='EPSG:3875',
    )
    assert_xml_equal(xml_encode_get_coverage(request, pretty_print=True).value.decode('utf-8'), dedent("""\
    <wcs:GetCoverage xmlns:crs="http://www.opengis.net/wcs/crs/1.0" xmlns:eop="http://www.opengis.net/eop/2.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmlcov="http://www.opengis.net/gmlcov/1.0" xmlns:int="http://www.opengis.net/wcs/interpolation/1.0" xmlns:ogc="http://www.opengis.net/ogc" xmlns:om="http://www.opengis.net/om/2.0" xmlns:ows="http://www.opengis.net/ows/2.0" xmlns:rsub="http://www.opengis.net/wcs/range-subsetting/1.0" xmlns:scal="http://www.opengis.net/wcs/scaling/1.0" xmlns:swe="http://www.opengis.net/swe/2.0" xmlns:wcs="http://www.opengis.net/wcs/2.0" xmlns:wcseo="http://www.opengis.net/wcs/wcseo/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" service="WCS" version="2.0.1">
      <wcs:CoverageId>a</wcs:CoverageId>
      <wcs:Extension>
        <crs:subsettingCrs>EPSG:4326</crs:subsettingCrs>
        <crs:outputCrs>EPSG:3875</crs:outputCrs>
      </wcs:Extension>
    </wcs:GetCoverage>
    """))

    # scaling
    request = GetCoverageRequest(
        coverage_id='a',
        scalefactor=0.5,
        scales=[
            ScaleAxis(axis='x', factor=0.7),
            ScaleSize(axis='y', size=500),
            ScaleExtent(axis='z', low=200, high=600),
        ]
    )
    assert_xml_equal(xml_encode_get_coverage(request, pretty_print=True).value.decode('utf-8'), dedent("""\
    <wcs:GetCoverage xmlns:crs="http://www.opengis.net/wcs/crs/1.0" xmlns:eop="http://www.opengis.net/eop/2.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmlcov="http://www.opengis.net/gmlcov/1.0" xmlns:int="http://www.opengis.net/wcs/interpolation/1.0" xmlns:ogc="http://www.opengis.net/ogc" xmlns:om="http://www.opengis.net/om/2.0" xmlns:ows="http://www.opengis.net/ows/2.0" xmlns:rsub="http://www.opengis.net/wcs/range-subsetting/1.0" xmlns:scal="http://www.opengis.net/wcs/scaling/1.0" xmlns:swe="http://www.opengis.net/swe/2.0" xmlns:wcs="http://www.opengis.net/wcs/2.0" xmlns:wcseo="http://www.opengis.net/wcs/wcseo/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" service="WCS" version="2.0.1">
      <wcs:CoverageId>a</wcs:CoverageId>
      <wcs:Extension>
        <scal:ScaleByFactor>
          <scal:scaleFactor>0.5</scal:scaleFactor>
        </scal:ScaleByFactor>
        <scal:ScaleToSize>
          <scal:TargetAxisSize>
            <scal:axis>y</scal:axis>
            <scal:targetSize>500</scal:targetSize>
          </scal:TargetAxisSize>
        </scal:ScaleToSize>
        <scal:ScaleAxesByFactor>
          <scal:ScaleAxis>
            <scal:axis>x</scal:axis>
            <scal:scaleFactor>0.7</scal:scaleFactor>
          </scal:ScaleAxis>
        </scal:ScaleAxesByFactor>
        <scal:ScaleToExtent>
          <scal:TargetAxisExtent>
            <scal:axis>z</scal:axis>
            <scal:low>200</scal:low>
            <scal:high>600</scal:high>
          </scal:TargetAxisExtent>
        </scal:ScaleToExtent>
      </wcs:Extension>
    </wcs:GetCoverage>
    """))

    # interpolation
    request = GetCoverageRequest(
        coverage_id='a',
        interpolation='NEAREST',
        axis_interpolations=[
            AxisInterpolation(axis='x', method='LINEAR'),
            AxisInterpolation(axis='y', method='CUBIC')
        ]
    )
    assert_xml_equal(xml_encode_get_coverage(request, pretty_print=True).value.decode('utf-8'), dedent("""\
    <wcs:GetCoverage xmlns:crs="http://www.opengis.net/wcs/crs/1.0" xmlns:eop="http://www.opengis.net/eop/2.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmlcov="http://www.opengis.net/gmlcov/1.0" xmlns:int="http://www.opengis.net/wcs/interpolation/1.0" xmlns:ogc="http://www.opengis.net/ogc" xmlns:om="http://www.opengis.net/om/2.0" xmlns:ows="http://www.opengis.net/ows/2.0" xmlns:rsub="http://www.opengis.net/wcs/range-subsetting/1.0" xmlns:scal="http://www.opengis.net/wcs/scaling/1.0" xmlns:swe="http://www.opengis.net/swe/2.0" xmlns:wcs="http://www.opengis.net/wcs/2.0" xmlns:wcseo="http://www.opengis.net/wcs/wcseo/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" service="WCS" version="2.0.1">
      <wcs:CoverageId>a</wcs:CoverageId>
      <wcs:Extension>
        <int:Interpolation>
          <int:globalInterpolation>NEAREST</int:globalInterpolation>
            <int:InterpolationPerAxis>
            <int:axis>x</int:axis>
          <int:interpolationMethod>LINEAR</int:interpolationMethod>
          </int:InterpolationPerAxis>
          <int:InterpolationPerAxis>
            <int:axis>y</int:axis>
            <int:interpolationMethod>CUBIC</int:interpolationMethod>
          </int:InterpolationPerAxis>
        </int:Interpolation>
      </wcs:Extension>
    </wcs:GetCoverage>
    """))


    # geotiff
    request = GetCoverageRequest(
        coverage_id='a',
        geotiff_encoding_parameters=GeoTIFFEncodingParameters(
            compression='LZW',
            predictor='Horizontal',
            interleave='Band',
            tiling=True,
            tile_width=256,
            tile_height=256,
        )
    )
    assert_xml_equal(xml_encode_get_coverage(request, pretty_print=True).value.decode('utf-8'), dedent("""\
    <wcs:GetCoverage xmlns:crs="http://www.opengis.net/wcs/crs/1.0" xmlns:eop="http://www.opengis.net/eop/2.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmlcov="http://www.opengis.net/gmlcov/1.0" xmlns:int="http://www.opengis.net/wcs/interpolation/1.0" xmlns:ogc="http://www.opengis.net/ogc" xmlns:om="http://www.opengis.net/om/2.0" xmlns:ows="http://www.opengis.net/ows/2.0" xmlns:rsub="http://www.opengis.net/wcs/range-subsetting/1.0" xmlns:scal="http://www.opengis.net/wcs/scaling/1.0" xmlns:swe="http://www.opengis.net/swe/2.0" xmlns:wcs="http://www.opengis.net/wcs/2.0" xmlns:wcseo="http://www.opengis.net/wcs/wcseo/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:geotiff="http://www.opengis.net/gmlcov/geotiff/1.0" service="WCS" version="2.0.1">
      <wcs:CoverageId>a</wcs:CoverageId>
      <wcs:Extension>
        <geotiff:parameters>
          <geotiff:compression>LZW</geotiff:compression>
          <geotiff:predictor>Horizontal</geotiff:predictor>
          <geotiff:interleave>Band</geotiff:interleave>
          <geotiff:tiling>true</geotiff:tiling>
          <geotiff:tilewidth>256</geotiff:tilewidth>
          <geotiff:tileheight>256</geotiff:tileheight>
        </geotiff:parameters>
      </wcs:Extension>
    </wcs:GetCoverage>
    """))

# ------------------------------------------------------------------------------
# Capabilities
# ------------------------------------------------------------------------------


def test_encode_capabilities():
    capabilities = ServiceCapabilities()
    print(xml_encode_capabilities(capabilities, pretty_print=True).value.decode('utf-8'))

    capabilities = ServiceCapabilities.with_defaults_v20(
        'http://provider.org',
        update_sequence='2018-05-08',
        title='Title',
        abstract='Description',
        keywords=[
            'test', 'WCS',
        ],
        fees='None',
        access_constraints=['None'],
        provider_name='Provider Inc',
        provider_site='http://provider.org',
        individual_name='John Doe',
        organisation_name='Provider Inc',
        position_name='CTO',
        phone_voice='+99/9008820',
        phone_facsimile='+99/9008821',
        delivery_point='Point du Hoc',
        city='City',
        administrative_area='Adminity',
        postal_code='12345',
        country='Cooontry',
        electronic_mail_address='john.doe@provider.org',
        online_resource='http://provider.org',
        hours_of_service='09:00AM - 18:00PM',
        contact_instructions='Just send a mail or a carrier pidgeon',
        role='Chief',
        formats_supported=[
            'image/tiff',
            'application/netcdf',
        ],
        crss_supported=[
            'http://www.opengis.net/def/crs/EPSG/0/4326',
            'http://www.opengis.net/def/crs/EPSG/0/3857',
            'http://www.opengis.net/def/crs/EPSG/0/3035',
        ],
        interpolations_supported=[
            'http://www.opengis.net/def/interpolation/OGC/1/average',
            'http://www.opengis.net/def/interpolation/OGC/1/nearest-neighbour',
            'http://www.opengis.net/def/interpolation/OGC/1/bilinear',
            'http://www.opengis.net/def/interpolation/OGC/1/cubic',
            'http://www.opengis.net/def/interpolation/OGC/1/cubic-spline',
            'http://www.opengis.net/def/interpolation/OGC/1/lanczos',
            'http://www.opengis.net/def/interpolation/OGC/1/mode',
        ],
        coverage_summaries=[
            CoverageSummary('a',
                coverage_subtype='RectifiedGridCoverage',
                coverage_subtype_parent='RectifiedGridCoverageParent',
                title='Nice Coverage "A"',
                abstract='REally nife coverage!',
                keywords=[
                    'really',
                    'nice',
                    'coverage',
                ],
                wgs84_bbox=[WGS84BoundingBox([0, 0, 2, 2])],
                bbox=[
                    BoundingBox(
                        'http://www.opengis.net/def/crs/EPSG/0/3857',
                        [1, 2, 3, 4]
                    )
                ],
                metadata=[
                    Metadata(
                        'http://provider.org/coverages/a/metadata.xml',
                    )
                ]
            )
        ],
        dataset_series_summaries=[
            DatasetSeriesSummary('series',
                wgs84_bbox=WGS84BoundingBox([0, 0, 2, 2]),
                time_period=(datetime(2018, 5, 10), datetime(2018, 5, 12)),
                metadata=[
                    Metadata(
                        'http://provider.org/series/metadata.xml',
                    )
                ]
            )
        ]

    )
    print(xml_encode_capabilities(capabilities, pretty_print=True).value.decode('utf-8'))


def test_encode_coverage_descriptions():
    print(xml_encode_coverage_descriptions([
        CoverageDescription(
            identifier='a',
            range_type=[
                Field(
                    name='B01',
                    description='',
                    uom='W.m-2.sr-1.nm-1',
                    nil_values={
                        0: 'http://www.opengis.net/def/nil/OGC/0/unknown'
                    },
                    allowed_values=[(0, 65535)],
                    # significant_figures=5,
                )
            ],
            grid=Grid(
                axes=[
                    RegularAxis('lon', 'i', 2.5, 3.5, 0.1, 'deg', 10),
                    RegularAxis('lat', 'j', 3.7, 4.7, 0.1, 'deg', 10),
                ],
                srs='http://www.opengis.net/def/crs/EPSG/0/4326',
            ),
            native_format='image/tiff',
            coverage_subtype='RectifiedDataset'
        )
    ], pretty_print=True).value.decode('utf-8'))
