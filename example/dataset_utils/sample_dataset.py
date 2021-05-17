from languages_dict import LANGUAGES
import numpy as np
import os

path = os.path.join('example', 'dataset', 'unformatted_lang_texts')
LEN_OF_SAMPLES = 10


for language in LANGUAGES:
    path_to_text = os.path.join(path, language + '_text.txt')
    with open(path_to_text, 'r') as file:
        text = file.read()
    print(language)
    print(len(text))
    print(text.count(' '))
    text = text.split()
    text = [word if word.isalpha() else '' for word in text]
    text_bez_praznih = []
    for word in text:
        if len(word) == 0:
            pass
        else:
            text_bez_praznih.append(word)
    text = text_bez_praznih
    num_of_samples = len(text) // LEN_OF_SAMPLES
    samples = [text[10*j:(10*j+LEN_OF_SAMPLES)] for j in range(0, num_of_samples)]
    samples = [' '.join(sample) for sample in samples]
    samples = '\n'.join(samples)
    save_to = os.path.join('example', 'dataset', 'samples',
                            f'{language}_samples_len_{LEN_OF_SAMPLES}.txt')
    
    with open(save_to, 'w') as text_file:
        text_file.write(samples)    



