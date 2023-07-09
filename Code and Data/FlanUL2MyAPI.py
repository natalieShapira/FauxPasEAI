from transformers import T5ForConditionalGeneration, AutoTokenizer
import torch

NUM_RETURN_SEQUENCES = 1

MAX_LEN = 50
MODEL_NAME = "google/flan-ul2"
TORCH_DEVICE = 'cpu'

class FlanUL2MyAPI:

    def __init__(self, temperature):
        self.temperature = temperature
        #self.model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16, device_map="auto")
        self.model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME).to(TORCH_DEVICE)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

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
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(TORCH_DEVICE)
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

    def get_prompt_with_completion(self, prompt, num_return_sequences=NUM_RETURN_SEQUENCES):
        # Here we can control and sive the prompts results. since the results already contain the prompt, we first separate and than concatenate again
        top_predictions = FlanUL2MyAPI.get_full_predictions(prompt, num_return_sequences)
        top_predictions_suffixes = [x[len(prompt):] for x in top_predictions]
        before_end_of_sentence_predictions = []
        for pred in top_predictions_suffixes:
            before_end_of_sentence_predictions.append(pred)
        before_end_of_sentence_predictions = [prompt + x for x in before_end_of_sentence_predictions]
        return before_end_of_sentence_predictions


if __name__ == '__main__':

    prompt = 'James bought Richard a toy airplane for his birthday. A few months later, they were playing with it, and James accidentally dropped it. "Don\'t worry" said Richard, "I never liked it anyway. Someone gave it to me for my birthday.\nIn the story did someone say something that they should not have said? Explain your answer'
    # MODEL_NAME = "google/flan-t5-xxl" # google/flan-t5-small, google/flan-t5-base, google/flan-t5-large, google/flan-t5-xl, google/flan-t5-xxl
    model_name = "google/flan-ul2"
    temperature = 0.0001
    FlanUL2MyAPI.set_seed(0)
    flan_ul2 = FlanUL2MyAPI(temperature)
    print(model_name)
    for s in flan_ul2.get_full_predictions(prompt, NUM_RETURN_SEQUENCES):
        print("--------------------------------------")
        print(s)