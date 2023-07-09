from FlanT5MyAPI import FlanT5MyAPI
from FauxPasEAIParser import FauxPasEAIParser
from FauxPasEvaluation import FauxPasEvaluation


gt_answers = []
pred_answers = []
if __name__ == '__main__':
    # MODEL_NAME = "google/flan-t5-xxl" # google/flan-t5-small, google/flan-t5-base, google/flan-t5-large, google/flan-t5-xl, google/flan-t5-xxl
    short_model_name = "flan-t5-large"
    model_name = "google/"+ short_model_name
    temperature = 0.00001
    number_of_samples = 1
    FlanT5MyAPI.set_seed(0)
    flan_t5 = FlanT5MyAPI(model_name, temperature)

    out_str = ""
    print(flan_t5.model_name)
    out_str += flan_t5.model_name+"\n"
    print(flan_t5.temperature)
    out_str += "Temperature = " + str(flan_t5.temperature)+"\n"
    fp_parser = FauxPasEAIParser()
    for i in fp_parser.tests:
        print("**************************************")
        out_str += "**************************************\n"
        print(i)
        out_str += i+"\n"
        story, question1, answer1, question2, answer2, question3, answer3, question4, answer4 = fp_parser.tests[i]
        prompt1 = story +'\n' + question1 + '\nAnswer:'
        prompt2 = story + '\n' + question2 + '\nAnswer:'
        prompt3 = story + '\n' + question3 + '\nAnswer:'
        prompt4 = story +'\n' + question4 + '\nAnswer:'
        print(prompt1)
        out_str += prompt1+"\n"
        for s in flan_t5.get_full_predictions(prompt1, number_of_samples):
            gt_answers.append(answer1)
            pred_answers.append(s)
            print("--------------------------------------")
            out_str += "--------------------------------------\n"
            print("ground truth: " + answer1 + " prediction: " +s)
            print(FauxPasEvaluation.compare_elements(answer1, s))
            out_str += "ground truth: " + answer1 + " prediction: " +s +"\n"
            out_str += str(FauxPasEvaluation.compare_elements(answer1, s))+"\n"

        print(prompt2)
        out_str += prompt2+"\n"
        for s in flan_t5.get_full_predictions(prompt2, number_of_samples):
            gt_answers.append(answer2)
            pred_answers.append(s)
            print("--------------------------------------")
            out_str += "--------------------------------------\n"
            print("ground truth: " + answer2 + " prediction: " +s)
            print(FauxPasEvaluation.compare_elements_distance(answer2, s))
            out_str += "ground truth: " + answer2 + " prediction: " +s +"\n"
            out_str += str(FauxPasEvaluation.compare_elements_distance(answer2, s))+"\n"

        print(prompt3)
        out_str += prompt3+"\n"
        for s in flan_t5.get_full_predictions(prompt3, number_of_samples):
            gt_answers.append(answer3)
            pred_answers.append(s)
            print("--------------------------------------")
            out_str += "--------------------------------------\n"
            print("ground truth: " + answer3 + " prediction: " +s)
            print(FauxPasEvaluation.compare_elements_distance(answer3, s))
            out_str += "ground truth: " + answer3 + " prediction: " +s +"\n"
            out_str += str(FauxPasEvaluation.compare_elements_distance(answer3, s))+"\n"

        print(prompt4)
        out_str += prompt4+"\n"
        for s in flan_t5.get_full_predictions(prompt4, number_of_samples):
            gt_answers.append(answer4)
            pred_answers.append(s)
            print("--------------------------------------")
            out_str += "--------------------------------------\n"
            print("ground truth: " + answer4 + " prediction: " +s)
            print(FauxPasEvaluation.compare_elements(answer4, s))
            out_str += "ground truth: " + answer4 + " prediction: " +s +"\n"
            out_str += str(FauxPasEvaluation.compare_elements(answer4, s))+"\n"
    print("**************************************")
    out_str += "**************************************\n"
    print("Accuracy (question level):")
    out_str += "Accuracy (question level):"
    acc= FauxPasEvaluation.compare_lists_question_level(pred_answers, gt_answers)
    print(acc)
    out_str += str(acc)

    print("Accuracy (story level):")
    out_str += "Accuracy (story level):"
    acc= FauxPasEvaluation.compare_lists_story_level(pred_answers, gt_answers)
    print(acc)
    out_str += str(acc)

    with open("fp_" + short_model_name+"_s-"+str(number_of_samples)+"_t-"+str(temperature)+"_acc-"+str(acc)+".txt", 'w') as f_out:
        f_out.write(out_str)