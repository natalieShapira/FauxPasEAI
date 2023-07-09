FauxPasEAI_DIR = './FauxPas-EAI'
FauxPasEAI_filepath = FauxPasEAI_DIR + '/Faux pas expert dataset v0.5.csv'
import csv

class FauxPasEAIParser():

    def __init__(self):
        self.tests = {}
        line_index = 0
        question_line = 0

        with open(FauxPasEAI_filepath, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            data = [row for row in csv_reader]
        i=0
        for row in data:
            i+=1
            story_id = row['Story ID']
            story = row['Story']
            if i==1:
                question1 = row['Question']
                answer1 = row['Answer']
            elif i==2:
                question2 = row['Question']
                answer2 = row['Answer']
            elif i==3:
                question3 = row['Question']
                answer3 = row['Answer']
            elif i==4:
                i=0
                question4 = row['Question']
                answer4 = row['Answer']

                self.tests[story_id] = (story, question1, answer1, question2, answer2, question3, answer3, question4, answer4)


if __name__ == '__main__':
    fp = FauxPasEAIParser()
    for story_id in fp.tests:
        story, question1, answer1, question2, answer2, question3, answer3, question4, answer4 = fp.tests[story_id]
        print(story_id + " " +story)