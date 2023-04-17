import json
import re
import warnings
from pathlib import Path
from bs4 import BeautifulSoup, Tag
from translation_utils import *


def extract_formatting_chars(text):
    formatting_chars = re.findall(r'%\w|%\.\d\w|{(?:\d*:)?[\w\s]*}', text)
    return set(formatting_chars)


def html_structure_equal(html1, html2):
    soup1 = BeautifulSoup(html1, 'html.parser')
    soup2 = BeautifulSoup(html2, 'html.parser')
    def tag_structure(tag):
        if isinstance(tag, Tag):
            return (tag.name, [tag_structure(child) for child in tag.contents])
        return None
    structure1 = tag_structure(soup1)
    structure2 = tag_structure(soup2)
    return structure1 == structure2


def fix_whitespace(original, translation):
    leading_whitespace = re.search(r'^\s*', original).group()
    trailing_whitespace = re.search(r'\s*$', original).group()
    fixed_translation = re.sub(r'^\s*', leading_whitespace, translation)
    fixed_translation = re.sub(r'\s*$', trailing_whitespace, fixed_translation)
    return fixed_translation


def fix_french_spacing(text):
    fixed_text = re.sub(r'(?<=[^\s])([?!:;])', r' \1', text)
    return fixed_text


def check_special_terms(original, translation):
    for term in SPECIAL_TERMS:
        if term in original and term not in translation:
            return False
    return True


def check_translations(file_path):
    with file_path.open('r', encoding='utf-8') as f:
        translations = json.load(f)
    for key, values in translations.items():
        original_formatting_chars = extract_formatting_chars(key)
        contains_html = "<" in key and ">" in key
        if values is None:
            warnings.warn(f"No translations for '{key}'")
            continue
        untranslated_count = sum(1 for translation in values.values() if translation == key)
        if 0 < untranslated_count < len(values):
            warnings.warn(f"Most translations for '{key}' are the same as the original: "
                          f"Untranslated count: {untranslated_count}")
        for lang, translation in values.items():
            fixed_translation = fix_whitespace(key, translation)
            if fixed_translation != translation:
                warnings.warn(f"Fixed whitespace for '{key}' in {lang}: "
                              f"Updated translation: {fixed_translation}")
                translation = fixed_translation            
            if lang == 'fr':
                fixed_translation = fix_french_spacing(translation)
                if fixed_translation != translation:
                    warnings.warn(f"Fixed spacing for '{key}' in {lang}: "
                                  f"Updated translation: {fixed_translation}")
                    translation = fixed_translation
            translated_formatting_chars = extract_formatting_chars(translation)
            if original_formatting_chars != translated_formatting_chars:
                warnings.warn(f"Error: Translation for '{key}' in {lang} is incorrect (formatting_chars):\n"
                              f"  Original: {key}\n"
                              f"  Translation: {translation}")
                values[lang] = None
            elif contains_html and not html_structure_equal(key, translation):
                warnings.warn(f"Error: Translation for '{key}' in {lang} is incorrect (html_structure):\n"
                              f"  Original: '{key}'\n"
                              f"  Translation: '{translation}'")
                values[lang] = None
            elif not check_special_terms(key, translation):
                warnings.warn(f"Error: Translation for '{key}' in {lang} is incorrect (special_terms):\n"
                              f"  Original: {key}\n"
                              f"  Translation: {translation}")
                values[lang] = None
        if 'jp' in values:
            values['ja'] = values['jp']
            del values['jp']
    return translations


updated_translations = check_translations(TRANSLATIONS)
with TRANSLATIONS_CHECKED.open('w', encoding='utf-8') as f:
    json.dump(updated_translations, f, ensure_ascii=False, indent=2)
