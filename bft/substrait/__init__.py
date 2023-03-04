from collections.abc import Iterable

import yaml
try:
    from yaml import CSafeLoader as SafeLoader, CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeLoader, SafeDumper

from typing import BinaryIO

from ..core.function import FunctionBuilder

class ExtensionFileVisitor(object):

    def __init__(self):
        self.location_stack = []

    def __fail(self, err):
        loc = '/'.join(self.location_stack)
        raise Exception(f'Error visition extension file.  Location={loc} Message={err}')

    def __visit_list(self, visitor, obj, attr, required=False):
        if attr in obj:
            val = obj[attr]
            if not isinstance(val, Iterable):
                self.__fail(f'Expected attribute {attr} to be iterable')
            for item in val:
                visitor(item)
        elif required:
            self.__fail(f'Expected required attribute {attr}')

    def __get_or_die(self, obj, attr):
        if attr in obj:
            return obj[attr]
        self.__fail(f'Expected required attribute {attr}')

    def __get_or_else(self, obj, attr, default):
        if attr in obj:
            return obj[attr]
        return default

    def visit_ext_file(self, parsed_file):
        self.__visit_list(self.visit_scalar_function, parsed_file, 'scalar_functions')

    def visit_scalar_function(self, func):
        name = self.__get_or_die(func, 'name')
        description = self.__get_or_else(func, 'description', None)
        if description is None:
            print(f'{name} had no description')

class ExtensionFileParser(object):

    def parse(self, f: BinaryIO, builder: FunctionBuilder) -> None:
        data = yaml.load(f, SafeLoader)
        ExtensionFileVisitor().visit_ext_file(data)
        

builder = FunctionBuilder('foo')
with open('/Users/weston/source/repos/substrait/extensions/functions_arithmetic.yaml', mode='rb') as f:
    ExtensionFileParser().parse(f, builder)
