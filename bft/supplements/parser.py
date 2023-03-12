from typing import TextIO

from mistletoe.ast_renderer import get_ast
from mistletoe.block_token import Document, Heading, Paragraph
from mistletoe.html_renderer import HTMLRenderer
from mistletoe.span_token import RawText

from .types import SupplementsFile


class SupplementsParser(object):

    def __init__(self):
        self.html_renderer = HTMLRenderer()
        self.__reset()

    def __reset(self):
        self.__finish = None
        self.__paragraphs = []

    def __get_simple_text(self, heading: Heading) -> str:
        if len(heading.children) != 1:
            raise Exception(f"Expected heading to have one line of simple text but there were {len(heading.children)} sub-elements")
        text_child = heading.children[0]
        if not isinstance(text_child, RawText):
            raise Exception(f"Expected heading to contain simple raw text butit was {type(text_child)}")
        return text_child.content

    def __parse_heading(self, heading: Heading):
        heading_title = self.__get_simple_text(heading)
        if heading.level != 2:
            raise Exception("Top-level headings below title expected to be level 2 but got {heading.level} with heading {heading_title}")
        if heading_title.lower() == 'options':
            self.__switch_to_options()
        elif heading_title.lower() == 'details':
            self.__switch_to_details()
        elif heading_title.lower() == 'properties':
            self.__switch_to_properties()
        else:
            raise Exception(f"Unexpected L2 heading '{heading_title}'")

    def __parse_paragraph(self, paragraph: Paragraph):
        self.__paragraphs.append(self.html_renderer.render_paragraph(paragraph))

    def __parse_child(self, child):
        if isinstance(child, Heading):
            self.__parse_heading(child)
        elif isinstance(child, Paragraph):
            self.__parse_paragraph(child)
        else:
            raise Exception(f"Unrecognized top-level element type in supplements file {type(child)}")

    def parse_supplements_doc(self, f: TextIO) -> SupplementsFile:
        self.__reset()
        renderer = HTMLRenderer()
        doc = Document(f)
        
        if len(doc.children) == 0:
            raise Exception("Supplements document appears to be empty.  It should at least have a title")
        
        title_section = doc.children[0]
        if not isinstance(title_section, Heading) or title_section.level != 1:
            raise Exception("First element in a supplements doc should be a level 1 heading with the name of the function")

        function_name = self.__get_simple_text(title_section).lower()
        for child in doc.children[1:]:
            self.__parse_child(child)

        print(f"{function_name=}")

parser = SupplementsParser()
with open("/home/pace/dev/bft/supplemental/arithmetic/add.md", mode="r") as f:
    parser.parse_supplements_doc(f)
