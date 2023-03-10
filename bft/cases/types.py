from typing import Dict, List, Literal, NamedTuple


class CaseLiteral(NamedTuple):
    value: str | int | float
    type: str


class CaseGroup(NamedTuple):
    id: str
    description: str


class Case(NamedTuple):
    group: CaseGroup
    args: List[CaseLiteral]
    result: CaseLiteral | Literal["error", "undefined"]
    options: Dict[str, str]


class CaseFile(NamedTuple):
    function: str
    cases: List[Case]


class ProtoCase(NamedTuple):
    group: str
    args: List[CaseLiteral]
    result: CaseLiteral | Literal["error", "undefined"]
    options: Dict[str, str]
