import codecs
import unicodecsv as csv

class Writer:
    """
    Writes the summary of the experiments
    """

    def __init__(self):
        # used to the xml with exmperiment tag based format
        self.experiment_header = ("SGroup", "SCode",
                  "T1-Time", "T1-Class", "T1-Line", "T1-Folder", "T1-Problem", "T1-Solution",
                  "T2-Time", "T2-Class", "T2-Line", "T2-Folder", "T2-Problem", "T2-Solution",
                  "T3-Time", "T3-Class", "T3-Line", "T3-Folder", "T3-Problem", "T3-Solution",
                  "T4-Time", "T4-Class", "T4-Line", "T4-Folder", "T4-Problem", "T4-Solution",
                  "T5-Time", "T5-Class", "T5-Line", "T5-Folder", "T5-Problem", "T5-Solution",
                                  "Difficulty-Q1", "Difficulty-Q2", "Difficulty-Q3", "Difficulty-Q4", "Difficulty-Q5",
                                  "Motivation-Q1", "Motivation-Q2", "Motivation-Q3", "Motivation-Q4", "Motivation-Q5")

        # used to the xml with QTreeNode tag based format
        self.qtree_answersheader = ("Round", "Group", "Code", "Time", "Class", "Line", "Folder", "Problem",
                  "Solution", "Difficulty", "Motivation")

        self.qtree_feedbackheader = ("Round", "Group", "Code", "Question", "Answer")

    def make_exp_based_row(self, experiment):
        row = (experiment.group, experiment.subject_code)
        for (key, value) in experiment.categories.items():
            answers = value.getAnswers()
            if key.startswith('Task'):
                idx = int(key[-1]) + 1
                prefix = "Aufgabe%u"%idx
                row = row + (
                       value.getResponseTime(),
                       answers.get(prefix + "Class", "<empty>"),
                       answers.get(prefix + "LineNumber", "<empty>"),
                       answers.get(prefix + "FeatureOrdner", "<empty>"),
                       answers.get(prefix + "Problem", "<empty>"),
                       answers.get(prefix + "Solution", "<empty>"))
            elif key.endswith("Difficulty") or key.endswith("Motivation"):
                row = row + (answers.get('Aufgabe 2', 99),
                             answers.get('Aufgabe 3', 99),
                             answers.get('Aufgabe 4', 99),
                             answers.get('Aufgabe 5', 99),
                             answers.get('Aufgabe 6', 99))
            else:
                print "oops... something is wrong!"
        return row


    def make_feedback_rows(self, experiment):
        """
            Makes the feedback rows for an experiment
        :param experiment:
        :return:
        """
        rows = []
        for i in range(1,14):
            question = "AnswersConfounding%u"%i
            row = (experiment.round,
                   experiment.group,
                   experiment.subject_code,
                   question,
                   experiment.categories.get(question, "<< empty >>"))

            rows.append(row)

        return rows

    def make_answers_rows(self, experiment):
        """
            Makes the rows for an experiment
        :param experiment:
        :return:
        """
        rows = []
        for i in range(1,6):
            prefix = "Answers%u"%i
            row = (experiment.round,
                   experiment.group,
                   experiment.subject_code,
                   experiment.categories['Tarefa%u'%i],
                   experiment.categories[prefix+"Class"],
                   experiment.categories[prefix+"LineNumber"],
                   experiment.categories[prefix+"FeatureOrdner"] if (prefix + "FeatureOrdner" in experiment.categories) else "<empty>",
                   experiment.categories[prefix+"Problem"],
                   experiment.categories[prefix+"Solution"],
                   experiment.categories["AnswersDiffculty%u"%i],
                   experiment.categories["AnswersMotivation%u"%i])
            rows.append(row)
        return rows

    def persist_summary(self, experiments = []):
        """
            Persists all experiments answers to a .csv file.
        :return:
        """
        answers_rows = []
        feedback_rows = []
        new = True
        for exp in experiments:
            if ('experimentcode' in exp.categories.keys()):
                answers_rows.append(self.make_answers_rows(exp))
                feedback_rows.append(self.make_feedback_rows(exp))
            else:
                new = False
                answers_rows.append(self.make_exp_based_row(exp))

        if (new):
            self.write_csv(self.qtree_answersheader, answers_rows, "resources/qtree_answers_summary.csv")
            self.write_csv(self.qtree_feedbackheader, feedback_rows, "resources/qtree_feedback_summary.csv")
        else:
            self.write_csv(self.experiment_header, answers_rows, "resources/exp_summary.csv")


    def write_csv(self, header, rows, filename):
        """
            Writes the actual .csv file
        :return:
        """
        with open(filename, "wb") as csvfile:
            writer = csv.writer(csvfile, delimiter=',', dialect='excel', encoding='utf-8')
            csvfile.write(codecs.BOM_UTF8)

            writer.writerow(header)
            for exp in rows:
                writer.writerows(exp)
        print csvfile.name + " written!"
