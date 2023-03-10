from typing import BinaryIO, Iterable, List

import yaml

try:
    from yaml import CSafeDumper as SafeDumper
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeDumper, SafeLoader

from .types import Case, CaseFile, CaseGroup, CaseLiteral, ProtoCase


class CaseFileVisitor(object):
    def __init__(self):
        self.__location_stack: List[str] = []
        self.__groups = {}

    def __resolve_proto_case(self, case: ProtoCase) -> Case:
        if case.group not in self.__groups:
            raise Exception(
                "A case referred to group {case.group} which was not defined in the file"
            )
        grp = self.__groups[case.group]
        return Case(grp, case.args, case.result, case.options)

    def __fail(self, err):
        loc = "/".join(self.__location_stack)
        raise Exception(f"Error visiting case file.  Location={loc} Message={err}")

    def __visit_list(self, visitor, obj, attr, required=False):
        if attr in obj:
            val = obj[attr]
            results = []
            if not isinstance(val, Iterable):
                self.__fail(f"Expected attribute {attr} to be iterable")
            for idx, item in enumerate(val):
                self.__location_stack.append(f"{attr}[{idx}]")
                results.append(visitor(item))
                self.__location_stack.pop()
            return results
        elif required:
            self.__fail(f"Expected required attribute {attr}")
        else:
            return []

    def __visit_or_maybe_die(self, visitor, obj, attr, required, default=None):
        if attr in obj:
            val = obj[attr]
            self.__location_stack.append(f"{attr}")
            visited = visitor(val)
            self.__location_stack.pop()
            return visited
        elif required:
            self.__fail(f"Expected required attribte {attr}")
        else:
            return default

    def __visit_or_die(self, visitor, obj, attr):
        return self.__visit_or_maybe_die(visitor, obj, attr, False)

    def __visit_or_else(self, visitor, obj, attr, default):
        return self.__visit_or_maybe_die(visitor, obj, attr, True, default)

    def __get_or_die(self, obj, attr):
        if attr in obj:
            return obj[attr]
        self.__fail(f"Expected required attribute {attr}")

    def __get_or_else(self, obj, attr, default):
        if attr in obj:
            return obj[attr]
        return default

    def visit_group(self, group):
        id = self.__get_or_die(group, "id")
        description = self.__get_or_die(group, "description")
        self.__groups[id] = CaseGroup(id, description)
        return id

    def visit_literal(self, lit):
        value = self.__get_or_die(lit, "value")
        data_type = self.__get_or_die(lit, "type")
        return CaseLiteral(value, data_type)

    def visit_result(self, res):
        special = self.__get_or_else(res, "special", None)
        if special is None:
            return self.visit_literal(res)
        return special

    def visit_case(self, case):
        print(dir(case))
        grp = self.__get_or_die(case, "group")
        if not isinstance(grp, str):
            grp = self.visit_group(grp)
        result = self.__visit_or_die(self.visit_result, case, "result")
        args = self.__visit_list(self.visit_literal, case, "args")
        opts = self.__get_or_else(case, "options", {})
        return ProtoCase(grp, args, result, opts)

    def visit_case_file(self, case_file):
        func_name = self.__get_or_die(case_file, "function")
        proto_cases = self.__visit_list(self.visit_case, case_file, "cases")
        cases = [self.__resolve_proto_case(c) for c in proto_cases]
        return CaseFile(func_name, cases)


class CaseFileParser(object):
    def parse(self, f: BinaryIO) -> List[CaseFile]:
        case_files = yaml.load_all(f, SafeLoader)
        visitor = CaseFileVisitor()
        return [visitor.visit_case_file(cf) for cf in case_files]
