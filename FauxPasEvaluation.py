

class FauxPasEvaluation:

    @staticmethod
    def levenshteinDistance(s1, s2):
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2 + 1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_
        return distances[-1]

    @staticmethod
    def compare_elements(e1, e2):
        good = 0
        if e1.strip().lower().startswith('yes') and e2.strip().lower().startswith('yes'):
            good += 1
        elif e1.strip().lower().startswith('no') and e2.strip().lower().startswith('no'):
            good += 1
        elif e1.strip().lower().startswith('(yes') and e2.strip().lower().startswith('yes'):
            good += 1
        elif e1.strip().lower().startswith('(no') and e2.strip().lower().startswith('no'):
            good += 1
        elif e1.strip().lower().startswith('"yes') and e2.strip().lower().startswith('yes'):
            good += 1
        elif e1.strip().lower().startswith('"no') and e2.strip().lower().startswith('no'):
            good += 1
        elif e1.strip().lower().startswith('yes') and e2.strip().lower().startswith('(yes'):
            good += 1
        elif e1.strip().lower().startswith('no') and e2.strip().lower().startswith('(no'):
            good += 1
        elif e1.strip().lower().startswith('yes') and e2.strip().lower().startswith('"yes'):
            good += 1
        elif e1.strip().lower().startswith('no') and e2.strip().lower().startswith('"no'):
            good += 1
        return good

    @staticmethod
    def compare_elements_distance(e1, e2):
        good = 0
        if e1.strip().lower() in e2.strip().lower():
            good += 1
        elif e2.strip().lower() in e1.strip().lower():
            good += 1
        elif e1.strip()[1:-2].lower() in e2.strip().lower():
            good += 1
        elif e2.strip()[1:-2].lower() in e1.strip().lower():
            good += 1
        elif FauxPasEvaluation.levenshteinDistance(e1.strip().lower(), e2.strip().lower()) < 3:
            good += 1
        elif FauxPasEvaluation.levenshteinDistance(e1.strip()[1:-2].lower(), e2.strip().lower()) < 3:
            good += 1
        elif FauxPasEvaluation.levenshteinDistance(e1.strip().lower(), e2.strip()[1:-2].lower()) < 3:
            good += 1
        elif len(e1) > 10 and len(e2) > 10 and FauxPasEvaluation.levenshteinDistance(e1.strip().lower(),
                                                                   e2.strip().lower()) < 10:  # He/She instead of a name
            good += 1
        return good

    @staticmethod
    def compare_lists_story_level(list1, list2):
        good = 0
        for i in range(len(list1)):
            if i % 4 == 0:
                if FauxPasEvaluation.compare_elements(list1[i], list2[i]) and FauxPasEvaluation.compare_elements_distance(list1[i + 1], list2[
                    i + 1]) and FauxPasEvaluation.compare_elements_distance(list1[i + 2], list2[i + 2]) and FauxPasEvaluation.compare_elements(list1[i + 3],
                                                                                                           list2[
                                                                                                               i + 3]):
                    good += 1
        print("compare_lists_story_level total good:"+str(good))
        print("compare_lists_story_level total len(list1):"+str(len(list1)))
        print("compare_lists_story_level total (len(list1) / 4:"+str((len(list1) / 4)))
        return good / (len(list1) / 4)

    @staticmethod
    def compare_lists_question_level(list1, list2):
        good = 0
        for i in range(len(list1)):
            if i % 4 == 0:
                if FauxPasEvaluation.compare_elements(list1[i], list2[i]):
                    good += 1
                if FauxPasEvaluation.compare_elements_distance(list1[i+1], list2[i+1]):
                    good += 1
                if FauxPasEvaluation.compare_elements_distance(list1[i+2], list2[i+2]):
                    good += 1
                if FauxPasEvaluation.compare_elements(list1[i + 3], list2[i + 3]):
                    good += 1
        print("compare_lists_question_level total good:" + str(good))
        print("compare_lists_question_level total len(list1):"+str(len(list1)))
        return good / len(list1)