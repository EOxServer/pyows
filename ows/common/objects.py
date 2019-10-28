from enum import Enum
from typing import List, Dict
from dataclasses import dataclass, field


class HttpMethod(Enum):
    Get = 'GET'
    Post = 'POST'


@dataclass
class OperationMethod:
    method: HttpMethod
    service_url: str = None
    constraints: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class Operation:
    name: str
    operation_methods: List[OperationMethod] = field(default_factory=lambda: [OperationMethod(method=HttpMethod.Get)])


@dataclass
class ServiceCapabilities:
    # ServiceIdentification fields
    title: str = None
    abstract: str = None
    keywords: List[str] = field(default_factory=list)
    service_type: str = ''
    service_type_versions: List[str] = field(default_factory=list)
    profiles: List[str] = field(default_factory=list)
    fees: str = None
    access_constraints: List[str] = field(default_factory=list)

    # ServiceProvider fields
    provider_name: str = ''
    provider_site: str = ''
    individual_name: str = None
    organisation_name: str = None
    position_name: str = None

    # ContactInfo fields
    phone_voice: str = None
    phone_facsimile: str = None

    # Address fields
    delivery_point: str = None
    city: str = None
    administrative_area: str = None
    postal_code: str = None
    country: str = None
    electronic_mail_address: str = None

    role: str = ''

    # OperationsMetadata fields

    operations: List[Operation] = field(default_factory=list)
