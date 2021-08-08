from urllib.request import urlretrieve
from languages_dict import LANGUAGES, LANGUAGE_DICTIONARY
from pathlib import Path
import progressbar
import os

pbar = None

def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


for language in LANGUAGES:
    print(f"Getting the {LANGUAGE_DICTIONARY[language]} language.")

    path_to_zipped_files = os.path.join('example', 'dataset', 'zipped_files')
    Path(path_to_zipped_files).mkdir(parents=True, exist_ok=True)
    
    save_to_path = os.path.join(path_to_zipped_files, f'{language}.zip')

    urlretrieve(f'https://opus.nlpl.eu/download.php?f=Europarl/v8/raw/{language}.zip',
                 save_to_path, show_progress)
