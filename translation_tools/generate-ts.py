from pathlib import Path
import xml.etree.ElementTree as ET
import json
import subprocess
from pathlib import Path
from translation_utils import *

for name, locale in LOCALES:
    translations = json.loads(TRANSLATIONS_CHECKED.read_text())
    tree = ET.parse(TRANSLATABLES)
    root = tree.getroot()
    for message in root.iter("message"):
        source = message.find('source').text
        if source not in translations or translations[source] is None:
            print(f'no translation for {source}')
            continue
        translation_element = message.find("translation")
        translation_element.text = translations[source][locale]
        translation_element.attrib = {}
    ts = TS_FOLDER / f'{locale}.ts'
    qm = QM_FOLDER / f'{locale}.qm'
    tree.write(ts, encoding="utf-8", xml_declaration=True)
    subprocess.run(['lrelease', ts, '-qm', qm])
