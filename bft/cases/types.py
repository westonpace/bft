from typing import Dict, List, Literal, NamedTuple, Tuple


class CaseLiteral(NamedTuple):
    value: str | int | float
    type: str


class CaseGroup(NamedTuple):
    id: str
    description: str


class Case(NamedTuple):
    function: str
    group: CaseGroup
    args: List[CaseLiteral]
    result: CaseLiteral | Literal["error", "undefined"]
    options: List[Tuple[str, str]]


def case_to_kernel_str(function: str, case: Case):
    joined_args = ", ".join([arg.type for arg in case.args])
    result_str = case.result
    if not isinstance(result_str, str):
        result_str = case.result.type
    return f"{function}({joined_args}) -> {result_str}"


class CaseFile(NamedTuple):
    function: str
    cases: List[Case]


class ProtoCase(NamedTuple):
    group: str
    args: List[CaseLiteral]
    result: CaseLiteral | Literal["error", "undefined"]
    options: Dict[str, str]
