import tempfile

from bft.cases.types import CaseFile


class ParquetLoader(object):

    def save_to_file(self, case_file: CaseFile, tmpdir: str):
        for case in case_file.cases:
            for arg in case.args: