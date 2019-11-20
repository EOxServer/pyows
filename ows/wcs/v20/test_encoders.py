from textwrap import dedent
from urllib.parse import unquote

from lxml import etree

from .objects import (
    DescribeCoverageRequest, GetCoverageRequest, Trim, Slice,
    ScaleAxis, ScaleExtent, ScaleSize, AxisInterpolation
)
from .encoders import (
    kvp_encode_describe_coverage, xml_encode_describe_coverage,
    kvp_encode_get_coverage, xml_encode_get_coverage
)


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
    assert(xml_encode_get_coverage(request, pretty_print=True).value.decode('utf-8') == dedent("""\
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
    assert(xml_encode_get_coverage(request, pretty_print=True).value.decode('utf-8') == dedent("""\
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
    assert(xml_encode_get_coverage(request, pretty_print=True).value.decode('utf-8') == dedent("""\
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
    assert(xml_encode_get_coverage(request, pretty_print=True).value.decode('utf-8') == dedent("""\
    <wcs:GetCoverage xmlns:crs="http://www.opengis.net/wcs/crs/1.0" xmlns:eop="http://www.opengis.net/eop/2.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmlcov="http://www.opengis.net/gmlcov/1.0" xmlns:int="http://www.opengis.net/wcs/interpolation/1.0" xmlns:ogc="http://www.opengis.net/ogc" xmlns:om="http://www.opengis.net/om/2.0" xmlns:ows="http://www.opengis.net/ows/2.0" xmlns:rsub="http://www.opengis.net/wcs/range-subsetting/1.0" xmlns:scal="http://www.opengis.net/wcs/scaling/1.0" xmlns:swe="http://www.opengis.net/swe/2.0" xmlns:wcs="http://www.opengis.net/wcs/2.0" xmlns:wcseo="http://www.opengis.net/wcs/wcseo/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" service="WCS" version="2.0.1">
      <wcs:CoverageId>a</wcs:CoverageId>
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
    </wcs:GetCoverage>
    """))
