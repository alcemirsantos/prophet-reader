class Category:
    """
    Represents each category of the 'answers.xml' file
    """


    def __init__(self, name, type, time, answers = {}):
        self.name = name
        self.type = type
        self.response_time = time
        self.answers = answers

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getAnswers(self):
        return self.answers

    def getResponseTime(self):
        return self.response_time