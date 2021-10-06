"""
Provides the sample_dataset function which is used to...
draw samples from the dataset. :)
"""

from demo.dataset_utils.languages_dict import LANGUAGES
import numpy as np
import random
import os

path = os.path.join('demo', 'dataset', 'unformatted_lang_texts')

def sample_dataset(n, length, language, random_state=None):
    """Function that samples the dataset.

    It returns a list of strings each a certain number of
    words long, in the given language.

    Parameters
    ----------
    n : int, positive integer
        Number of strings to draw.

    length: int, positive integers
        Length (in words) of each string.

    language: string, identifying one of the available languages
        One of the {'cs', 'da', 'de', 'en', 'es', 'et', 'fi',
                    'fr', 'it', 'nl', 'ro', 'pt', ''el', 'lt', 'lv'}.

    random_state: int
        Random state be passed to random.seed().

    Returns
    -------
    samples: listž
        A list of strings drawn from the dataset.
    """
    if random_state is not None:
        random.seed(random_state)
    path_to_text = os.path.join(path, f'{language}_text.txt')

    with open(path_to_text, 'r', encoding='utf-8') as file:
        text = file.read().split()

    text = [word for word in text if (word.isalpha() and len(word) > 0)]

    num_of_samples = len(text) // length
    if num_of_samples < n:
        raise ValueError("Number of samples desired is larger than the number"
                        f" of samples available ({num_of_samples}).")
    
    samples = [text[length*j:(length*(j+1))]
                                    for j in range(0, num_of_samples)]
    samples = random.sample(samples, n)

    return samples

