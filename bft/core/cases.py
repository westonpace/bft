from typing import List, Dict


class FunctionDescription(object):
    def FunctionDescription(self, name: str, options: Dict[str, str]):
        self.name = name
        self.options = options


class Literal(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value


class ScalarCase(object):
    def __init__(
        self,
        function_descr: FunctionDescription,
        inputs: List[Literal],
        output: Literal,
    ):
        self.function_descr = function_descr
        self.inputs = inputs
        self.output = output


class Cases(object):
    def __init__(self, scalar_cases: List[ScalarCase]):
        self.scalar_cases = scalar_cases

def parse_name(token):
    return token

def parse_option(token):
    key_value = token.partition('=')
    if key_value[1] == '':
        return None, None
    return key_value[0], key_value[2]

def parse_scalar_case(line) -> ScalarCase:
    tokens = line.split()
    tokens_idx = 0
    name = parse_name(tokens[tokens_idx])
    tokens_idx = 1
    options = {}
    while True:
        opt_key, opt_val = parse_option(tokens, tokens_idx)
        if option is None:
            break
        tokens_idx = tokens_idx + 1
        options[option.key] = option.value
    descr = FunctionDescription(name, options)
    literals = []
    while True:
        literal = parse_literal(tokens[tokens_idx])
        if literal is None:
            break
        tokens_idx = tokens_idx + 1
        literals.append(literal)
    inputs = literals[:-1]
    output = literals[-1]
    return ScalarCase(descr, inputs, output)

def parse_cases_file(f) -> Cases:
    scalar_cases: List[ScalarCase] = []
    for line in f:
        scalar_cases.append(parse_scalar_case(line))
    return Cases(scalar_cases)