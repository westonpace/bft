from typing import Dict, List, NamedTuple


class OptionValueSupplement(NamedTuple):
    value: str
    description: str

class OptionSupplement(NamedTuple):
    description: str
    values: List[OptionValueSupplement]

class BasicSupplement(NamedTuple):
    title: str
    description: str

class SupplementsFile(NamedTuple):
    function: str
    options: Dict[str, OptionSupplement]
    details: List[BasicSupplement]
    properties: List[BasicSupplement]
