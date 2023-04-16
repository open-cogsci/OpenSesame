from pathlib import Path
import xml.etree.ElementTree as ET
import json
import subprocess
from pathlib import Path
from translation_utils import *

for name, locale in locales:
    translation_path = Path('translations.json')
    translations = json.loads(translation_path.read_text())
    tree = ET.parse(translatables)
    root = tree.getroot()
    for message in root.iter("message"):
        source = message.find('source').text
        if source not in translations or translations[source] is None:
            print(f'no translation for {source}')
            continue
        translation_element = message.find("translation")
        translation_element.text = translations[source][locale]
        translation_element.attrib = {}
    ts = ts_folder / f'{locale}.ts'
    qm = qm_folder/ f'{locale}.qm'
    tree.write(ts, encoding="utf-8", xml_declaration=True)
    subprocess.run(['lrelease', ts, '-qm', qm])
