class Experiment:
    numTasks = 5
    numDifficultyFeedback = 1
    numMotivationFeedback = 1

    def __init__(self, subject_code, group, categories):
        self.group = group
        self.subject_code = subject_code
        self.categories = categories

    def getGroup(self):
        return self.group

    def getSubjectCode(self):
        return self.subject_code

    def getCategories(self):
        return self.categories