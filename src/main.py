import os
import unicodecsv as csv
import codecs

from reader import Reader
from writer import Writer
from category import Category
from experiment import Experiment

default_directory = "/Users/alcemirsantos/Dropbox/PhD/activities/experiments/16-FOSD12 Replication/Experiment/Answers"
default_filename = "answers.xml"


def get_list_of_answers_files():
    filenames = []
    for subdir, dirs, files in os.walk(default_directory):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(default_filename):
                filenames.append(os.path.join(default_directory, filepath))
            else:
                print "<> Disregarding: "+filepath
    return filenames



def make_list(categories):
    result = []
    for category in categories:
        result.append(category.getResponseTime())
        for answer in category.getAnswers().items():
            result.append(answer[1])
    return result

def persist(rows):
    """
    Save the csv file
    :return:
    """
    with open("summary.csv", "wb") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', dialect='excel', encoding='utf-8')

        writer.writerows([rows.keys()])
        for row in zip(*rows.values()):
            #row = [s.encode('utf-8') for s in row]
            writer.writerows([row])

    print "File written!"


def process(filename):
    """
    Extracts the information from the file and ti
    :param filename:
    :return:
    """
    categories = []
    reader = Reader(filename)

    subject_code = reader.get_subject_code()
    subject_group = reader.get_subject_group()

    for i in range(1,6):
        category_time = reader.get_response_time_of_the_category("Tarefa%d"%i)
        category_answers = reader.get_answers_of_the_category("Tarefa%d"%i)
        categories.append(Category("Task" + str(i), "Task", category_time, category_answers))

    category_time = reader.get_response_time_of_the_category("Dificuldade")
    category_answers = reader.get_answers_of_the_category("Dificuldade")
    categories.append(Category("Dificulty", "Feedback", category_time, category_answers))

    category_time = reader.get_response_time_of_the_category("Motivacao")
    category_answers = reader.get_answers_of_the_category("Motivacao")
    categories.append(Category("Motivation", "Feedback", category_time, category_answers))

    experiment_summary = Experiment(subject_code, subject_group, categories)
    return experiment_summary



data = []
for filename in get_list_of_answers_files():
    print "\n<> Processing: "+filename
    reader = Reader(filename)
    data.append(reader.process())
    #reader.walk()
writer = Writer()
writer.persistall(data)