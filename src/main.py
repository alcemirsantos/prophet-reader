import os
from src.readers.experimentxmlreader import ExperimentXMLReader
from src.readers.qtreexmlreader import QTreeXMLReader
from src.writer import Writer

ANSWERS_DIR = "/Users/alcemirsantos/Dropbox/PhD/activities/experiments/16-FOSD12 Replication/Experiment/Answers"
ANSWER_FILENAME = "answers.xml"

data = []

def get_list_of_answers_files():
    filenames = []
    for subdir, dirs, files in os.walk(ANSWERS_DIR):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(ANSWER_FILENAME):
                filenames.append(os.path.join(ANSWERS_DIR, filepath))
            else:
                print "<> Disregarding: "+filepath
    return filenames



def process_experiment_xmlfile():
    for filename in get_list_of_answers_files():
        print "\n<> Processing: " + filename
        reader = ExperimentXMLReader(filename)
        data.append(reader.process())
        # reader.walk()

    writer = Writer()
    writer.persist_summary(data)



def process_qtree_xmlfile():
    for filename in get_list_of_answers_files():
        print "\n<> Processing: "+filename
        reader = QTreeXMLReader(filename)
        data.append(reader.process())
        reader.walk()

    #writer = Writer()
    #writer.persistall(data)