from src.readers.reader import Reader
from src.beans.experiment import Experiment


class QTreeXMLReader(Reader):
    """
        This class is supposed to read the .xml PROPHET files using the 'QTreeNode' structure.
    """

    def __init__(self, filename):
        Reader.__init__(self, filename)

    def extract_entry_pairs(self, entries):
        """
        Extracts all pairs (question, answer) of a set of entries
        :param entries:
        :return:
        """
        pairs = {}
        for entry in entries:
            # key is the id of the question
            key = entry[0].text
            # value is the answer given
            if (len(entry[1]) > 0):
                value = entry[1][0].text
            else:
                value = "<< empty >>"
            pairs[key] = value
        return pairs

    def extract_answers(self):
        """
        Extracts all the answers data
        :return:
        """

        tasks_answers_entries = self.root.findall(".//answers[entry]")

        answers = {}
        for task_answers in tasks_answers_entries:
            answers.update(self.extract_entry_pairs(task_answers))
        return answers

    def get_answer_time_of(self, name):
        """
        Returns the time spent to finish a given node
        :return:
        """
        tag = self.root.findall(".//QTreeNode[@name='%s']" % name)
        return tag[0].get('answerTime')

    def get_tasks_times(self):
        """
        Returns
        :return:
        """
        ttimes = {}
        for i in range(1,6):
            idx = "Tarefa%u" % i
            ttimes[idx] = self.get_answer_time_of(idx)
        return ttimes


    def process(self):
        """
        Processes the xml file as a whole and returns a summary as dictionary
        :return:
        """
        summary = {}
        summary.update(self.extract_answers())
        summary.update(self.get_tasks_times())

        experiment = Experiment(summary['subjectcode'] ,self.get_sgroup(), summary)
        return experiment


