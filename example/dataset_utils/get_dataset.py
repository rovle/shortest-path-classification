from urllib.request import urlretrieve
from languages_dict import LANGUAGES
import progressbar

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
    print(f"Getting the {language} language.")
    urlretrieve(f'https://opus.nlpl.eu/download.php?f=Europarl/v8/raw/{language}.zip',
                 f'examples/datasets/zipped_files/{language}.zip', show_progress)
