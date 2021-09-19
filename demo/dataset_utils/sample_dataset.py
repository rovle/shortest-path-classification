from demo.dataset_utils.languages_dict import LANGUAGES
import numpy as np
import random
import os

path = os.path.join('demo', 'dataset', 'unformatted_lang_texts')
LEN_OF_SAMPLES = 10

def sample_dataset(n, length, language, random_state=None):
    if random_state is not None:
        random.seed(random_state)
    path_to_text = os.path.join(path, language + '_text.txt')

    with open(path_to_text, 'r', encoding='utf-8') as file:
        text = file.read().split()

    text = [word for word in text if (word.isalpha() and len(word) > 0)]

    num_of_samples = len(text) // length
    if num_of_samples < n:
        raise ValueError(f"Number of samples desired is larger than the number of samples available ({num_of_samples}).")
    
    samples = [text[length*j:(length*(j+1))] for j in range(0, num_of_samples)]
    samples = random.sample(samples, n)

    return samples

