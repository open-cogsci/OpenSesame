from pathlib import Path
import xml.etree.ElementTree as ET
import openai
import json
import os
from translation_utils import *
import argparse

tree = ET.parse(TRANSLATABLES)
root = tree.getroot()
if TRANSLATIONS.exists():
    translation_dict = json.loads(TRANSLATIONS.read_text())
else:
    translation_dict = {}
messages = []
for message in root.iter("message"):
    source_text = message.find("source").text
    print(f'\n"{source_text}"')
    if translation_dict.get(source_text, None) is not None:
        print('* already translated')
        continue
    if source_text in translation_dict and \
            translation_dict[source_text] is None and not args.redo_invalid:
        print('* translation already failed')
        continue
    messages = messages[-HISTORY_LENGTH:]
    messages.append({"role": "user", "content": source_text})
    response = openai.ChatCompletion.create(
      model=MODEL,
      messages=[{"role": "system", "content": TS_SYSTEM}] + messages)
    reply = response['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": reply})
    translations = [l for l in reply.splitlines() if l]
    if len(translations) != len(LOCALES):
        print(f'* invalid response: {reply}')
        translation_dict[source_text] = None
    else:
        translation_dict[source_text] = {}
        for lang, translation in zip(LOCALES, translations):
            if source_text.startswith(' ') and not translation.startswith(' '):
                translation = ' ' + translation
            if source_text.endswith(' ') and not translation.endswith(' '):
                translation = translation + ' '
            print(f'- {lang[0]}: "{translation}"')
            translation_dict[source_text][lang[1]] = translation
    TRANSLATIONS.write_text(json.dumps(translation_dict, ensure_ascii=False,
                                       indent=2))
