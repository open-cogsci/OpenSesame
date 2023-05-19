# Automated translation

## Translation of translatable strings from the source code and UI files

1. `collect-translatables.py` extracts all translatables. Based on this, `translatables.ts` (in `libqtopensesame/resources/ts`) is generated.
2. `translate-ts.py` uses GPT4 to translates all untranslated translatables from `translatables.ts`. The result is stored in `translations.json`.
2. `translate-md.py` uses GPT4 to translates all untranslated Markdown files.
3. `check-ts.py` performs various sanity checks and corrections on the translations. The result is stored in `translations-checked.json`.
4. `generate-ts.py` generates `qm` (in `libqtopensesame/resources/locale`) files for each locale.
