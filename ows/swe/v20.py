from typing import Union, List, Tuple, Dict
from dataclasses import dataclass, field

from ows.xml import ElementMaker, NameSpace, NameSpaceMap

ns_swe = NameSpace("http://www.opengis.net/swe/2.0", "swe")

nsmap = NameSpaceMap(ns_swe)

SWE = ElementMaker(namespace=ns_swe.uri, nsmap=nsmap)


@dataclass
class Field:
    name: str
    description: str
    uom: str
    nil_values: Dict[float, str] = field(default_factory=dict)
    allowed_values: List[Union[float, Tuple[float, float]]] = field(default_factory=list)
    significant_figures: int = None


DataRecord = List[Field]


def encode_field(field):
    return SWE('field',
        SWE('Quantity',
            SWE('description', field.description),
            SWE('nilValues',
                SWE('NilValues', *[
                    SWE('nilValue',
                        str(value),
                        reason=reason
                    )
                    for value, reason in field.nil_values.items()
                ])
            ),
            SWE('uom', code=field.uom),
            SWE('constraint',
                SWE('AllowedValues', *[
                    SWE('value', str(value))
                    if isinstance(value, (int, float)) else
                    SWE('interval', f'{value[0]} {value[1]}')
                    for value in field.allowed_values
                ] + [
                    SWE('significantFigures',
                        str(field.significant_figures)
                    ) if field.significant_figures is not None else None
                ])
            )
        ),
        name=field.name,
    )


def encode_data_record(data_record: DataRecord):
    return SWE('DataRecord', *[
        encode_field(field)
        for field in data_record
    ])
