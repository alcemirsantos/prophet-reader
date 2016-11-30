import xml.etree.ElementTree as ET

from src.beans.experiment import Experiment


class Reader:
    """
    A class to help read the experiment data.
    """

    def __init__(self, filename):
        self.answer_file = filename
        with open(filename, 'r') as thexml:
            self.tree = ET.parse(thexml)
        self.root = self.tree.getroot()
        self.experiment = Experiment("", "", {})

    def get_sgroup(self):
        if self.answer_file.__contains__("/FH/"):
            return "FH"
        elif self.answer_file.__contains__("/IFDEF/"):
            return "IFDEF"
        else:
            return "[]"

    def get_round(self):
        if self.answer_file.__contains__("/Round-MM/"):
            return "MM"
        elif self.answer_file.__contains__("/Round-RE/"):
            return "RE"
        else:
            return "[]"
