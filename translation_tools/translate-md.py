from translation_utils import *
from pathlib import Path

for path in Path(args.src_folder).glob('**/*.md'):
    if any(exclude in path.parts for exclude in EXCLUDE_FOLDERS):
        continue
    print(path)
    source_text = path.read_text()
    print(f'***\n{source_text}\n***')
    for language, lang_code in LOCALES:
        dst = path.parent / f'locale/{lang_code}/{path.name}'
        if dst.exists():
            print(f'***\nAlready translated\n***')
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        print(dst)
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[{"role": "system", "content": MD_SYSTEM % language},
                      {"role": "user", "content": source_text}],
            request_timeout=300)
        reply = response['choices'][0]['message']['content']
        print(f'***\n{reply}\n***')
        dst.write_text(reply)
