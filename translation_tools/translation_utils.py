from pathlib import Path
import argparse
import openai

parser = argparse.ArgumentParser(
    description='Update ts and qm files for OpenSesame-related projects')
parser.add_argument('--ts-folder', type=str,
                    default='../libqtopensesame/resources/ts',
                    help='The folder that contains the ts files')
parser.add_argument('--qm-folder', type=str,
                    default='../libqtopensesame/resources/locale',
                    help='The folder that contains the qm files')
parser.add_argument('--src-folder', type=str, default='..',
                    help='The folder that contains the source code')
parser.add_argument('--redo-invalid', action='store_true', default=False,
                    help='Redoes invalid translations')
args = parser.parse_args()

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
    ('Japanese', 'ja'),
    ('Korean', 'ko'),
    ('Indonesian', 'id'),
    ('Hindi', 'hi'),
    ('Bengali', 'bn'),
    ('Arabic', 'ar'),
    ('Hebrew', 'he'),
    ('Russian', 'ru'),
    ('Turkish', 'tr'),
]

SPECIAL_TERMS = [
    "sketchpad",
    "mouse_response",
    "keyboard_response",
    "sampler",
    "synth",
    "logger",
    "coroutines",
    "advanced_delay",
    "repeat_cycle",
    "inline_script",
    "inline_javascript",
    "form_base",
    "form_consent",
    "form_text_input",
    "form_text_display",
    "form_html"
]

TS_SYSTEM = f'''You're a translator for OpenSesame, a program for developing psychology experiments.

Do not translate technical terms or terms that have a special meaning within OpenSesame, such as sketchpad, keyboard_response, and other item types. Preserve whitespace, capitalization, and punctuation.

I will provide one phrase at a time. Reply with translations in the following languages: {', '.join(l[0] for l in LOCALES)}. Provide translated phrases in that order on separate lines and without any additional text.'''

MD_SYSTEM = f'''You're a translator for OpenSesame, a program for developing psychology experiments.

Do not translate technical terms or terms that have a special meaning within OpenSesame, such as: {', '.join(SPECIAL_TERMS)}, and other similar terms. Preserve whitespace, capitalization, and punctuation.

Reply with a %s translation. Only provide the translated text without adding any additional text. This concludes the instruction. The to be translated text will be provided next.'''
MODEL = 'gpt-4'
TS_FOLDER = Path(args.ts_folder)
QM_FOLDER = Path(args.qm_folder)
TRANSLATABLES = TS_FOLDER / 'translatables.ts'
TRANSLATIONS = Path('translations.json')
TRANSLATIONS_CHECKED = Path('translations-checked.json')
EXCLUDE_FOLDERS = ['build', 'dist', 'deb_dist', 'pgs4a-0.9.4', 'doc',
                   'translation_tools', 'readme.md', '.pytest_cache',
                   'dev-scripts', 'locale', 'tmp.md']
openai.api_key = (Path.home() / '.openai-api-key').read_text().strip()
