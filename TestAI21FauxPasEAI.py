from FauxPasEAIParser import FauxPasEAIParser
from FauxPasEvaluation import FauxPasEvaluation
import time
import ai21  # (pip install ai21)
from Globals.Debug import Debug
ai21.api_key = Debug.AI21_KEY

MODEL_NAME = "j2-large" # "j2-jumbo-instruct", "j2-grande-instruct", "j2-jumbo", "j2-grande", "j2-large",
TEMPERATURE = 0
NUMBER_OF_SAMPLES = 1
# API key is in https://studio.ai21.com/account

def prompt_response(prompt, temperature=TEMPERATURE):
    resp = ai21.Completion.execute(
        model=MODEL_NAME,
        prompt=prompt,
        numResults=1,
        maxTokens=50,
        temperature=temperature,
        topKReturn=0,
        topP=1,
        countPenalty={
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        frequencyPenalty={
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        presencePenalty={
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        stopSequences=[]
    )
    # prompt = resp["prompt"]["text"]
    response = resp['completions'][0]["data"]["text"].strip()
    return response


gt_answers = []
pred_answers = []

if __name__ == '__main__':

    model_name = MODEL_NAME
    temperature = TEMPERATURE
    number_of_samples = NUMBER_OF_SAMPLES
    out_str = ""
    print(model_name)
    out_str += model_name+"\n"
    print(temperature)
    out_str += "Temperature = " + str(temperature)+"\n"
    fp_parser = FauxPasEAIParser()
    for i in fp_parser.tests:
        print("**************************************")
        out_str += "**************************************\n"
        print(i)
        out_str += i + "\n"
        story, question1, answer1, question2, answer2, question3, answer3, question4, answer4 = fp_parser.tests[i]
        prompt1 = story + '\n' + question1 + '\nAnswer:'
        prompt2 = story + '\n' + question2 + '\nAnswer:'
        prompt3 = story + '\n' + question3 + '\nAnswer:'
        prompt4 = story + '\n' + question4 + '\nAnswer:'
        print(prompt1)
        out_str += prompt1 + "\n"
        for j in range(number_of_samples):
            time.sleep(3)
            response = prompt_response(prompt1)

            gt_answers.append(answer1)
            pred_answers.append(response)
            print("--------------------------------------")
            out_str += "--------------------------------------\n"
            print("ground truth: " + answer1 + " prediction: " + response)
            print(FauxPasEvaluation.compare_elements(answer1, response))
            out_str += "ground truth: " + answer1 + " prediction: " + response + "\n"
            out_str += str(FauxPasEvaluation.compare_elements(answer1, response)) + "\n"

        print(prompt2)
        out_str += prompt2 + "\n"
        for j in range(number_of_samples):
            time.sleep(3)
            response = prompt_response(prompt2)

            gt_answers.append(answer2)
            pred_answers.append(response)
            print("--------------------------------------")
            out_str += "--------------------------------------\n"
            print("ground truth: " + answer2 + " prediction: " + response)
            print(FauxPasEvaluation.compare_elements(answer2, response))
            out_str += "ground truth: " + answer2 + " prediction: " + response + "\n"
            out_str += str(FauxPasEvaluation.compare_elements(answer2, response)) + "\n"

        print(prompt3)
        out_str += prompt3 + "\n"
        for j in range(number_of_samples):
            time.sleep(3)
            response = prompt_response(prompt3)

            gt_answers.append(answer3)
            pred_answers.append(response)
            print("--------------------------------------")
            out_str += "--------------------------------------\n"
            print("ground truth: " + answer3 + " prediction: " + response)
            print(FauxPasEvaluation.compare_elements(answer3, response))
            out_str += "ground truth: " + answer3 + " prediction: " + response + "\n"
            out_str += str(FauxPasEvaluation.compare_elements(answer3, response)) + "\n"

        print(prompt4)
        out_str += prompt4 + "\n"
        for j in range(number_of_samples):
            time.sleep(3)
            response = prompt_response(prompt1)

            gt_answers.append(answer4)
            pred_answers.append(response)
            print("--------------------------------------")
            out_str += "--------------------------------------\n"
            print("ground truth: " + answer4 + " prediction: " + response)
            print(FauxPasEvaluation.compare_elements(answer4, response))
            out_str += "ground truth: " + answer4 + " prediction: " + response + "\n"
            out_str += str(FauxPasEvaluation.compare_elements(answer4, response)) + "\n"

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

    with open("fp_"+model_name+"_s-"+str(number_of_samples)+"_t-"+str(temperature)+"_acc-"+str(acc)+".txt", 'w') as f_out:
        f_out.write(out_str)