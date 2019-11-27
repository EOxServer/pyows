from typing import List

from ows.util import Result
from ows.cis.v11 import (
    encode_envelope, encode_domain_set, encode_range_type
)
from .namespaces import WCS, ns_gml
from ..objects import CoverageDescription


def xml_encode_coverage_descriptions(coverage_descriptions: List[CoverageDescription], **kwargs):
    root = WCS('CoverageDescriptions', *[
        WCS('CoverageDescription',
            encode_envelope(coverage_description.grid),
            WCS('CoverageId', coverage_description.identifier),
            # TODO: metadata
            encode_domain_set(coverage_description.grid),
            encode_range_type(coverage_description.range_type),
            WCS('ServiceParameters',
                WCS('CoverageSubtype', coverage_description.coverage_subtype),
                WCS('CoverageSubtype',
                    coverage_description.coverage_subtype_parent
                ) if coverage_description.coverage_subtype_parent else None,
                WCS('nativeFormat', coverage_description.native_format),
            ),
            **{
                ns_gml('id'): coverage_description.identifier
            }
        )
        for coverage_description in coverage_descriptions
    ])

    return Result.from_etree(root, **kwargs)


from datetime import datetime

from ows.cis.v11 import Grid, Field, RegularAxis, IrregularAxis

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
                RegularAxis(
                    'lon', 'i', 0.0, 2.0, 0.1, uom='deg', size=20
                ),
                RegularAxis(
                    'lat', 'j', 0.0, 2.0, 0.1, uom='deg', size=20
                ),
                IrregularAxis(
                    'time', 'k', positions=[
                        datetime(2019, 7, 18),
                        datetime(2019, 7, 19),
                        datetime(2019, 7, 20),
                        datetime(2019, 7, 21),
                    ], uom='ISO8601'
                )
            ],
            srs='http://www.opengis.net/def/crs/EPSG/0/4326',
        ),
        native_format='image/tiff',
        coverage_subtype='RectifiedDataset'
    )
], pretty_print=True).value.decode('utf-8'))
