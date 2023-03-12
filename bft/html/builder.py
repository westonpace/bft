from typing import Dict, List, MutableSet, NamedTuple

from jinja2 import Environment, PackageLoader, select_autoescape

from bft.cases.types import Case
from bft.core.function import FunctionDefinition, Kernel, Option
from bft.html.types import (
    ScalarFunctionExampleCaseInfo,
    ScalarFunctionExampleGroupInfo,
    ScalarFunctionInfo,
    ScalarFunctionOptionInfo,
    ScalarFunctionOptionValueInfo,
)

env = Environment(
    loader=PackageLoader("bft"),
    autoescape=select_autoescape())

scalar_func_template = env.get_template("scalar_function.j2")

def render_scalar_function(info: ScalarFunctionInfo):
    return scalar_func_template.render(info._asdict())

def create_function_option_value(val: str) -> ScalarFunctionOptionValueInfo:
    name = val
    description = "Still need to figure out option value descriptions"
    return ScalarFunctionOptionValueInfo(name, description)

def create_function_option(opt: Option) -> ScalarFunctionOptionInfo:
    name = opt.name
    description = "Still need to figure out option descriptions"
    values = [create_function_option_value(val) for val in opt.values]
    return ScalarFunctionOptionInfo(name, description, values)

def create_examples(cases: List[Case]) -> List[ScalarFunctionExampleCaseInfo]:
    examples: List[ScalarFunctionExampleCaseInfo] = []
    for case in cases:
        arg_vals = [arg.value for arg in case.args]
        opt_vals = [opt[1] for opt in case.options]
        result = case.result
        examples.append(ScalarFunctionExampleCaseInfo(arg_vals, opt_vals, result))
    return examples

def create_example_groups(cases: List[Case]) -> List[ScalarFunctionExampleGroupInfo]:
    groups: Dict[str, Case] = {}
    for case in cases:
        # This may clobber previous insertions.  We just need one prototypical case per group
        # Prefer a case that actually has a typed result if possible
        if case.group.id not in groups or hasattr(case.result, 'type'):
            groups[case.group.id] = case

    example_groups: List[ScalarFunctionExampleGroupInfo] = []
    for group_id in sorted(groups.keys()):
        protocase = groups[group_id]
        arg_types = [arg.type for arg in protocase.args]
        opt_names = [opt[0] for opt in protocase.options]
        if hasattr(protocase.result, 'type'):
            result_type = protocase.result.type
        else:
            result_type = protocase.result
        group_cases = [c for c in cases if c.group.id == group_id]
        examples = create_examples(group_cases)
        description = protocase.group.description
        example_groups.append(ScalarFunctionExampleGroupInfo(description, arg_types, opt_names, result_type, examples))
    return example_groups


def create_function_info(func: FunctionDefinition, cases: List[Case]) -> ScalarFunctionInfo:
    name = func.name
    uri = 'https://TODO'
    uri_short = 'functions_arithmetic.yaml'
    brief = func.description
    options = [create_function_option(opt) for opt in func.options]
    kernels = func.kernels
    dialects = []
    details = []
    properties = []
    example_groups = create_example_groups(cases)
    return ScalarFunctionInfo(name, uri, uri_short, brief, options, kernels, dialects, details, properties, example_groups)
    

from bft.substrait.extension_file_parser import (
    ExtensionFileParser,
    LibraryBuilder,
    add_extensions_file_to_library,
)

library = LibraryBuilder()
with open(
    "/home/pace/dev/substrait/extensions/functions_arithmetic.yaml",
    mode="rb",
) as f:
    ext_file = ExtensionFileParser().parse(f)
    add_extensions_file_to_library(ext_file, library)
built_funcs = library.finish()
func = built_funcs[3]

from bft.cases.loader import load_cases

cases = load_cases("/home/pace/dev/bft/cases")

func_info = create_function_info(func, cases)
print(render_scalar_function(func_info))
