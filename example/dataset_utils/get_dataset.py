from urllib.request import urlretrieve
from languages_dict import LANGUAGES, LANGUAGE_DICTIONARY
from pathlib import Path
import progressbar
import os
import shutil
import download_progress_bar as bar

path_to_zipped_files = os.path.join('example', 'dataset', 'zipped_files')
Path(path_to_zipped_files).mkdir(parents=True, exist_ok=True)

path_to_unzipped_files = os.path.join('example', 'dataset', 'languages')
Path(path_to_zipped_files).mkdir(parents=True, exist_ok=True)


for language in LANGUAGES:
    if language != 'cs':
        break
    print(f"Downloading the {LANGUAGE_DICTIONARY[language]} language.")

    save_to_path = os.path.join(path_to_zipped_files, f'{language}.zip')

    urlretrieve(f'https://opus.nlpl.eu/download.php?f=Europarl/v8/raw/{language}.zip',
                 save_to_path, bar.show_progress)
                 
    print("Unpacking it ...")
    shutil.unpack_archive(save_to_path,
                            os.path.join(path_to_unzipped_files, f'{language}') )
                            
    print(f"{LANGUAGE_DICTIONARY[language]} language downloaded and unzipped!")  
