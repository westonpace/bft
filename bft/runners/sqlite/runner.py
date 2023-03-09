import sqlite3

from bft.cases.runner import CaseRunner


def SqliteRunner(CaseRunner):
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
