import ai21  # (pip install ai21)
from Globals.Debug import Debug
ai21.api_key = Debug.AI21_KEY


# API key is in https://studio.ai21.com/account

def prompt_response(prompt, temperature=0.01):
    resp = ai21.Completion.execute(
        model="j2-grande-instruct",
        prompt=prompt,
        numResults=1,
        maxTokens=200,
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


response = prompt_response('how can I check whether your answers are correct?')
print(response)