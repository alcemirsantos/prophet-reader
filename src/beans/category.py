class Category:
    """
    Represents each category of the 'answers.xml' file
    """

    def __init__(self, name, type, time, answers = {}):
        self.name = name
        self.type = type
        self.response_time = time
        self.answers = answers
