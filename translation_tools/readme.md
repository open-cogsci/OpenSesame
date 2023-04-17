# Automated translation

## Translation of translatable strings from the source code and UI files

1. `collect-translatables.py` extracts all translatables. Based on this, `translatables.ts` (in `libqtopensesae/resources/ts`) is generated.
2. `translate-translatables.py` uses GPT4 to translates all untranslated translatables from `translatables.ts`. The result is stored in `translations.json`.
3. `check-ts.py` performs various sanity checks and corrections on the translations. The result is stored in `translations-checked.json`.
4. `generate-ts.py` generates `qm` (in `libqtopensesae/resources/locale`) files for each locale.

## Translation of Markdown templates

1. 
