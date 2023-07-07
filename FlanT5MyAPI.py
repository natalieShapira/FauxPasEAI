from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

NUM_RETURN_SEQUENCES = 1
MAX_LEN = 50
#TEMPERATURE = 0.00001

# MODEL_NAME = "google/flan-t5-xxl" # google/flan-t5-small, google/flan-t5-base, google/flan-t5-large, google/flan-t5-xl, google/flan-t5-xxl
SHORT_MODEL_NAME = "flan-t5-small"  # flan-t5-small, flan-t5-base, flan-t5-large, flan-t5-xl, flan-t5-xxl
MODEL_NAME = "google/" + SHORT_MODEL_NAME


class FlanT5MyAPI:

    def __init__(self, model_name, temperature):
        self.model_name = model_name
        self.temperature = temperature
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    @staticmethod
    def set_seed(seed: int = 42) -> None:
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        # When running on the CuDNN backend, two further options must be set
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        # Set a fixed value for the hash seed
        # os.environ["PYTHONHASHSEED"] = str(seed)
        print(f"Random seed set as {seed}")

    def get_full_predictions(self, prompt, num_return_sequences=NUM_RETURN_SEQUENCES):
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        # set seed to reproduce results. Feel free to change the seed though to get different results
        # tf.random.set_seed(0)

        # set top_k = 50 and set top_p = 0.95 and num_return_sequences = 3
        gen_tokens = self.model.generate(
            input_ids,
            do_sample=True,
            temperature=self.temperature,
            max_length=MAX_LEN,
            num_return_sequences=num_return_sequences)

        gen_text = [self.tokenizer.decode(gen_token, skip_special_tokens=True) for gen_token in gen_tokens]
        return gen_text

    def get_prompt_with_completion(prompt, num_return_sequences=NUM_RETURN_SEQUENCES):
        # Here we can control and sive the prompts results. since the results already contain the prompt, we first separate and than concatenate again
        top_predictions = FlanT5MyAPI.get_full_predictions(prompt, num_return_sequences)
        top_predictions_suffixes = [x[len(prompt):] for x in top_predictions]
        before_end_of_sentence_predictions = []
        for pred in top_predictions_suffixes:
            before_end_of_sentence_predictions.append(pred)
        before_end_of_sentence_predictions = [prompt + x for x in before_end_of_sentence_predictions]
        return before_end_of_sentence_predictions


if __name__ == '__main__':

    prompt = 'James bought Richard a toy airplane for his birthday. A few months later, they were playing with it, and James accidentally dropped it. "Don\'t worry" said Richard, "I never liked it anyway. Someone gave it to me for my birthday.\nIn the story did someone say something that they should not have said? Explain your answer'
    model_name = "google/flan-t5-base"
    temperature = 0.3
    FlanT5MyAPI.set_seed(0)
    flan_t5 = FlanT5MyAPI(model_name, temperature)
    print(flan_t5.model_name)
    for s in flan_t5.get_full_predictions(prompt, NUM_RETURN_SEQUENCES):
        print("--------------------------------------")
        print(s)