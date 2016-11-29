from src.readers.reader import Reader


class QTreeXMLReader(Reader):
    """
        This class is supposed to read the .xml PROPHET files using the 'QTreeNode' structure.
    """

    def __init__(self, filename):
        super(Reader, filename)

    def process(self):
        for task_answers in self.root.findall(".//answers"):
            print(task_answers)
            for task_entry in task_answers.findall(".//answer"):
                print(task_entry)



    def walk(self):
        """
         TODO implement method to walk through the xml file
        """

