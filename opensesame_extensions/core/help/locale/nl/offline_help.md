# OpenSesame help

*Dit is de offline help-pagina. Als je verbonden bent met het internet, kan je de online documentatie vinden op <http://osdoc.cogsci.nl>.*

## Introductie

OpenSesame is een grafische experimentontwerper voor de sociale wetenschappen. Met OpenSesame kunt u eenvoudig experimenten maken met behulp van een klik-en-sleep grafische interface. Voor complexe taken ondersteunt OpenSesame [Python] scripten.

## Aan de slag

De beste manier om te beginnen is door een tutorial te volgen. Tutorials, en nog veel meer, zijn online te vinden:

- <http://osdoc.cogsci.nl/tutorials/>

## Citatie

Om OpenSesame in uw werk te citeren, gebruik alstublieft de volgende referentie:

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: An open-source, graphical experiment builder for the social sciences. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Interface

De grafische interface heeft de volgende componenten. U kunt contextgevoelige hulp krijgen door op de helpiconen rechtsboven in elk tabblad te klikken.

- Het *menu* (bovenaan het venster) toont algemene opties, zoals het openen en opslaan van bestanden, het sluiten van het programma en het weergeven van deze helppagina.
- De *hoofdwerkbalk* (de grote knoppen onder het menu) biedt een selectie van de meest relevante opties uit het menu.
- De *itemwerkbalk* (de grote knoppen aan de linkerkant van het venster) toont beschikbare items. Om een item aan uw experiment toe te voegen, sleept u het van de itemwerkbalk naar het overzichtsgebied.
- Het *overzichtsgebied* (Control + \\) toont een boomachtig overzicht van uw experiment.
- Het *tabbladgebied* bevat de tabbladen om items te bewerken. Als u op een item in het overzichtsgebied klikt, opent u een overeenkomstig tabblad in het tabbladgebied. Hulp wordt ook weergegeven in het tabbladgebied.
- De [bestandspool](opensesame://help.pool) (Control + P) toont bestanden die bij uw experiment horen.
- De [variabele inspecteur](opensesame://help.extension.variable_inspector) (Control + I) toont alle gedetecteerde variabelen.
- Het [debugvenster](opensesame://help.stdout). (Control + D) is een [IPython] terminal. Alles wat uw experiment naar de standaard uitvoer print (d.w.z. met `print()`) is hier zichtbaar.

## Items

Items zijn de bouwstenen van uw experiment. Tien basiselementen bieden basisfunctionaliteit voor het maken van een experiment. Om items aan uw experiment toe te voegen, sleept u ze van de itemwerkbalk naar het overzichtsgebied.

- Het [loop](opensesame://help.loop) item draait een ander item meerdere keren. U kunt ook onafhankelijke variabelen in het LOOP-item definiëren.
- Het [sequence](opensesame://help.sequence) item draait meerdere andere items in volgorde.
- Het [sketchpad](opensesame://help.sketchpad) item presenteert visuele stimuli. Ingebouwde tekentools maken het eenvoudig om stimulusdisplays te maken.
- Het [feedback](opensesame://help.feedback) item lijkt op de `sketchpad`, maar wordt niet van tevoren voorbereid. Daarom kunnen FEEDBACK-items worden gebruikt om feedback aan deelnemers te geven.
- Het [sampler](opensesame://help.sampler) item speelt een enkel geluidsbestand af.
- Het [synth](opensesame://help.synth) item genereert een enkele toon.
- Het [keyboard_response](opensesame://help.keyboard_response) item verzamelt toetsaanslagreacties.
- Het [mouse_response](opensesame://help.mouse_response) item verzamelt muisklikreacties.
- Het [logger](opensesame://help.logger) item schrijft variabelen naar het logbestand.
- Het [inline_script](opensesame://help.inline_script) bevat Python-code in uw experiment.

Indien geïnstalleerd, bieden plug-in-items extra functionaliteit. Plug-ins verschijnen naast de basiselementen in de itemwerkbalk.

## Uw experiment uitvoeren

U kunt uw experiment uitvoeren in:

- Volledig schermmodus (*Control+R* of *Run -> Run fullscreen*)
- Venstermodus (*Control+W* of *Run -> Run in window*)
- Quick-run-modus (*Control+Shift+W* of *Run -> Quick run*)

In de Quick-run modus start het experiment meteen in een venster, met gebruik van het logbestand `quickrun.csv`, en subjectnummer 999. Dit is handig tijdens de ontwikkeling.

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/