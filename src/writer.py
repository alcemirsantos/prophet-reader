import codecs
import unicodecsv as csv

class Writer:
    """
    Writes the summary of the experiments
    """

    def make_row_from(self, experiment):
        row = (experiment.getGroup(), experiment.getSubjectCode())

        category_items = experiment.getCategories().items()

        for (key, value) in category_items:
            answers = value.getAnswers()
            if key.startswith('Task'):
                idx = int(key[-1])+1
                row = row + (value.getResponseTime(),
                       answers["Aufgabe"+str(idx)+"Class"] if ("Aufgabe"+str(idx)+"Class" in answers) else "<empty>",
                       answers["Aufgabe"+str(idx)+"LineNumber"] if ("Aufgabe"+str(idx)+"LineNumber" in answers) else "<empty>",
                       answers["Aufgabe"+str(idx)+"FeatureOrdner"] if ("Aufgabe"+str(idx)+"FeatureOrdner" in answers) else "<empty>",
                       answers["Aufgabe"+str(idx)+"Problem"] if ("Aufgabe"+str(idx)+"Problem" in answers) else "<empty>",
                       answers["Aufgabe"+str(idx)+"Solution"] if ("Aufgabe"+str(idx)+"Solution" in answers) else "<empty>")
            elif key.endswith("Difficulty") or key.endswith("Motivation"):
                row = row + (answers['Aufgabe 2'] if ('Aufgabe 2' in answers) else 99,
                             answers['Aufgabe 3'] if ('Aufgabe 3' in answers) else 99,
                             answers['Aufgabe 4'] if ('Aufgabe 4' in answers) else 99,
                             answers['Aufgabe 5'] if ('Aufgabe 5' in answers) else 99,
                             answers['Aufgabe 6'] if ('Aufgabe 6' in answers) else 99)
            else:
                print "oops... something is wrong!"
        return row


    def persist(self, experiment):
        """
           Persistis the .csv file
        :return:
        """
        with open("resources/%s-%s.csv" % (experiment.getGroup(), experiment.getSubjectCode()),
                  "wb") as csvfile:
            writer = csv.writer(csvfile, delimiter=',', dialect='excel', encoding='utf-8')
            csvfile.write(codecs.BOM_UTF8)

            writer.writerow(("", "Code", experiment.getSubjectCode()))
            writer.writerow(("", "Group", experiment.getGroup()))

            for category in experiment.getCategories().values():
                writer.writerow((category.getName(), "Time", category.getResponseTime()))
                for answer in category.getAnswers().items():
                    writer.writerow((category.getName(), answer[0], answer[1]))

        print csvfile.name + " written!"


    def persist_summary(self, experiments = []):
        """
        Persists the csv file
        :return:
        """
        header = ("SGroup", "SCode",
                  "T1-Time", "T1-Class", "T1-Line", "T1-Folder", "T1-Problem", "T1-Solution",
                  "T2-Time", "T2-Class", "T2-Line", "T2-Folder", "T2-Problem", "T2-Solution",
                  "T3-Time", "T3-Class", "T3-Line", "T3-Folder", "T3-Problem", "T3-Solution",
                  "T4-Time", "T4-Class", "T4-Line", "T4-Folder", "T4-Problem", "T4-Solution",
                  "T5-Time", "T5-Class", "T5-Line", "T5-Folder", "T5-Problem", "T5-Solution",
                  "Difficulty-Q1", "Difficulty-Q2", "Difficulty-Q3", "Difficulty-Q4", "Difficulty-Q5",
                  "Motivation-Q1", "Motivation-Q2", "Motivation-Q3", "Motivation-Q4", "Motivation-Q5")

        with open("resources/summary.csv", "wb") as csvfile:
            writer = csv.writer(csvfile, delimiter=',', dialect='excel', encoding='utf-8')
            csvfile.write(codecs.BOM_UTF8)

            writer.writerow(header)
            for exp in experiments:
                writer.writerow(self.make_row_from(exp))

        print csvfile.name + " written!"

    def new_persistall(self, experiments = []):
        """
            Persists all experiments to a .csv file.
        """
        header = ("Round", "Group", "Code", "Time", "Class", "Line", "Folder", "Problem", "Solution", "Difficulty", "Motivation")
        with open("resources/newsummary.csv", "wb") as csvfile:
            writer = csv.writer(csvfile, delimiter=',', dialect='excel', encoding='utf-8')
            csvfile.write(codecs.BOM_UTF8)

            writer.writerow(header)
            for exp in experiments:
                writer.writerow(self.make_row_from(exp))
        print  csvfile.name + " written!"