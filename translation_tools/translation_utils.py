from pathlib import Path
import openai

HISTORY_LENGTH = 20
LOCALES = [
    ('Dutch', 'nl'),
    ('German', 'de'),
    ('French', 'fr'),
    ('Spanish', 'es'),
    ('Italian', 'it'),
    ('Portuguese', 'pt'),
    ('Chinese', 'zh'),
    ('Cantonese', 'yue'),
    ('Japanese', 'jp'),
    ('Korean', 'ko'),
    ('Indonesian', 'id'),
    ('Hindi', 'hi'),
    ('Bengali', 'bn'),
    ('Arabic', 'ar'),
    ('Hebrew', 'he'),
    ('Russian', 'ru'),
    ('Turkish', 'tr'),
]

TS_SYSTEM = f'''You're a translator for OpenSesame, a program for developing psychology experiments.

Do not translate technical terms or terms that have a special meaning within OpenSesame, such as sketchpad, keyboard_response, and other item types. Preserve whitespace, capitalization, and punctuation.

I will provide one phrase at a time. Reply with translations in the following languages: {', '.join(l[0] for l in LOCALES)}. Provide translated phrases in that order on separate lines and without any additional text.'''
MODEL = 'gpt-4'
TS_FOLDER = Path('../libqtopensesame/resources/ts')
QM_FOLDER = Path('../libqtopensesame/resources/locale')
TRANSLATABLES = TS_FOLDER / 'translatables.ts'
TRANSLATIONS = Path('translations.json')
openai.api_key = (Path.home() / '.openai-api-key').read_text().strip()
