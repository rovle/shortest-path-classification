from bs4 import BeautifulSoup
from pathlib import Path

from languages_dict import LANGUAGES
import os

source_path = os.path.join('example', 'dataset', 'languages')
destination_path = os.path.join('example', 'dataset', 'unformatted_lang_texts')
Path(destination_path).mkdir(parents=True, exist_ok=True)


for language in LANGUAGES:
    language_text = ''
    path_to_xmls = os.path.join(source_path, language,
                                'Europarl', 'raw', language)
    
    for xml_file in next(os.walk(path_to_xmls))[2]:
        path_to_file = os.path.join(path_to_xmls, xml_file)

        if os.stat(path_to_file).st_size < 50000:
            # ignore particularly small files
            continue

        with open(path_to_file, "r", encoding="utf-8") as europarl_session:
            europarl_session = europarl_session.read()

        soup = BeautifulSoup(europarl_session, features="lxml")
        for speech in soup.find_all("s"):
            language_text += speech.get_text()

        if len(language_text) > 25000000:
            # stop collecting text after there's already 25m chars
            break
    
    path_to_new_file = os.path.join(destination_path,
                                    f'{language}_text.txt')
    with open(path_to_new_file, 'w', encoding="utf-8") as text_file:
        text_file.write(language_text)