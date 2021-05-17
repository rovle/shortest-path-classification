from bs4 import BeautifulSoup

from languages_dict import LANGUAGES
import os

path = 'examples/datasets/languages/'

for language in LANGUAGES:
    language_text = ''
    print(language)
    path_to_xmls = os.path.join(path, language, 'Europarl/raw', language)
    
    for xml in next(os.walk(path_to_xmls))[2]:
        path_to_file = os.path.join(path_to_xmls, xml)
        if os.stat(path_to_file).st_size < 50000:
            continue
        with open(path_to_file, "r") as europarl_session:
            europarl_session = europarl_session.read()
        soup = BeautifulSoup(europarl_session, features="lxml")
        for speech in soup.find_all("s"):
            language_text += speech.get_text()
        if len(language_text) > 25000000:
            break

    with open(f'examples/datasets/unformatted_lang_texts/{language}_text.txt', 'w') as text_file:
        text_file.write(language_text)


"""
from bs4 import BeautifulSoup
with open(filename_ovdje, "r") as sesija:
    fajl = sesija.read()
soup = BeautifulSoup(fajl)
for texts in soup.find_all("s"):
    print(texts.get_text())
"""
# i to prilagoditi za sve....
