from src.readers.reader import Reader
from src.category import Category
from src.experiment import Experiment

class ExperimentXMLreader(Reader):
    """
        This class is supposed to read the xml PROPHET files using the old structure.
    """

    def get_response_time_of_the_category(self, idx):
        """
        Returns the response time of each task 'idx'.
        :return: - dictionary name:time
        """
        if idx.endswith("Dificuldade") or idx.endswith("Motivacao"):
            match = ".//category[@name='%s']/children/question"
        else:
            match = "*/category[@name='%s']"

        for tag in self.root.findall(match % idx):
            return tag.get('time')

    def get_subject_code(self):
        """
        Returns the subject code from the answer file
        :return:
        """
        for tag in self.root.findall("*answer[@name='subjectcode']"):
            subject_code = tag.get('value')
            return subject_code

    def get_answers_of_the_category(self, idx):
        """
        Returns the answers of a given task.
        :param idx:
        :return:
        """
        if idx.endswith("Dificuldade") or idx.endswith("Motivacao"):
            match = ".//category[@name='%s']/children/question/answers/answer"
        else:
            match = ".//category[@name='%s']/answers/answer"

        answers = {}
        for tagg in self.root.findall(match % idx):
            answers[tagg.get('name')] = tagg.get('value')
        return answers

    def get_answers_from(self, idx):
        """
        Returns the answers of a given task.
        :param idx:
        :return:
        """
        if idx.endswith("Dificuldade") or idx.endswith("Motivacao"):
            match = ".//category[@name='%s']/children/question/answers/answer"
        else:
            match = ".//category[@name='%s']/answers/answer"

        answers = []
        for tagg in self.root.findall(match % idx):
            answers.append(tagg.get('value'))
        return answers

    def get_answers_of_the_task(self, idx):
        """
        Returns the answers of a given task.
        :param idx:
        :return:
        """
        answers = {}
        for tagg in self.root.findall(".//category[@name='Tarefa%d']/answers/answer" % idx):
            answers[tagg.get('name')] = tagg.get('value')
        return answers

    def get_tasks_answers(self):
        """
        Returns a dictionary, which the key is the task and the value is another dictionary
            holding the answers of the task.
        :return:
        """
        tasks_answers = {}
        for i in range(1, 6):
            idx = 'Task %d' % i
            tasks_answers[idx] = self.get_answers_of_the_task(i)
        return tasks_answers

    def process(self):
        """
            Extracts the information from the file and returns an 'Experiment' object.
            :return:
        """
        subject_code = self.get_subject_code()
        subject_group = self.get_sgroup()

        categories = {}
        for i in range(1, 6):
            category_time = self.get_response_time_of_the_category("Tarefa%d" % i)
            category_answers = self.get_answers_of_the_category("Tarefa%d" % i)
            categories['Task%s' % i] = Category("Task" + str(i), "Task", category_time, category_answers)

        category_time = self.get_response_time_of_the_category("Dificuldade")
        category_answers = self.get_answers_of_the_category("Dificuldade")
        categories['Difficulty'] = Category("Difficulty", "Feedback", category_time, category_answers)

        category_time = self.get_response_time_of_the_category("Motivacao")
        category_answers = self.get_answers_of_the_category("Motivacao")
        categories['Motivation'] = Category("Motivation", "Feedback", category_time, category_answers)

        self.experiment = Experiment(subject_code, subject_group, categories)
        return self.experiment


    def walk(self):
        print "=========="
        print "Subject: " + self.experiment.getSubjectCode()
        print "Group: " + self.experiment.getGroup()

        print "\n> Categories:"
        for category in self.experiment.getCategories().values():

            print "\n[" + category.getName() + "] lasted " + category.getResponseTime() + " ms:"
            for answer in category.getAnswers().items():
                print "::> " + answer[0] + ": " + answer[1]
