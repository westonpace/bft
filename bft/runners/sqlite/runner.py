import sqlite3
from typing import Dict, NamedTuple

from bft.cases.runner import CaseRunner
from bft.cases.types import Case, CaseLiteral


class Mapping(object):
    def __init__(self, sqlite_func: str, is_infix: bool = False):
        self.sqlite_func = sqlite_func
        self.is_infix = is_infix


function_mapping: Dict[str, Mapping] = {"add": Mapping("+", True)}


class SqliteRunner(CaseRunner):
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        print(self.conn.execute("select 1").fetchall())

    def __literal_to_str(self, lit: CaseLiteral):
        return str(lit.value)

    def run_case(self, function: str, case: Case) -> bool:
        arg_strs = [self.__literal_to_str(arg) for arg in case.args]
        mapping = function_mapping[function]
        if mapping.is_infix:
            if len(arg_strs) != 2:
                raise Exception(f"Infix function with {len(arg_strs)} args")
            expr = f"SELECT {arg_strs[0]}{mapping.sqlite_func}{arg_strs[1]}"
        else:
            joined_args = ",".join(arg_strs)
            expr = f"SELECT {mapping.sqlite_func}({joined_args})"
        result = self.conn.execute(expr).fetchone()
        print(result)


from bft.cases.parser import CaseFileParser

runner = SqliteRunner()

with open(
    "C:\\Users\\weston\\source\\repos\\bft\\cases\\arithmetic\\add.yaml", "rb"
) as f:
    case_files = CaseFileParser().parse(f)
    for case_file in case_files:
        for case in case_file.cases:
            runner.run_case(case_file.function, case)
