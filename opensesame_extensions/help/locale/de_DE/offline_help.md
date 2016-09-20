# OpenSesame Hilfe

*Dies ist die Offline-Hilfeseite. Wenn Du mit dem Internet verbunden bist,
findest Du die Online-Dokumentation (Englisch) unter <http://osdoc.cogsci.nl>.*

## Einführung

OpenSesame ist eine Software um Experimente für die Sozialwisseschaften in einer grafischen Bedienoberfläche zu bauen. Mit OpenSesame kannst Du - dank der point-and-click-Oberfläche - ganz leicht Experimente erstellen. Für komplexere Aufgaben unterstützt OpenSesame [Python]-Skripte.

## Loslegen

Die beste Methode anzufangen ist, ein Tutorials durchzugehen. Tutorials und vieles mehr, findest Du online:

- <http://osdoc.cogsci.nl/tutorials/>

## Zitation

Um OpenSesame in Deinen Arbeiten zu zitieren, nutze bitte die folgende Literaturangabe:

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: An open-source, graphical experiment builder for the social sciences. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Oberfläche

Die grafische Oberfläche hat folgende Komponenten. Für kontext-sensitive Hilfe, klicke auf das Hilfe-Symbol in der rechten oberen Ecke jedes Tabs.

- Das *Menü* (am oberen Rand des Fensters) enthält häufig genutzte Befehle, wie das Öffnen und Speichern von Dateien, das Schließen des Programms und das Anzeigen dieser Hilfe.
- Die *Werkzeugleiste* (die großen Knöpfe unterhalb des Menüs) bieten eine Auswahl der wichtigsten Menüpunkte an.
- Die *Item-Werkzeugleiste* (die großen Knöpfe am linken Rand des Fensters) zeigt verfügbare Items. Um ein Item in Dein Experiment einzufügen, ziehe es von der Werkzeugleiste in den Überblicksbereich.
- Der *Überblicksbereich* (Strg + \\) zeigt eine Baumstruktur Deines Experiments.
- Der *Tab-Bereich* enthält die Tabs zur Bearbeitung von Items. Wenn Du auf ein Item im Überblicksbereich klickst, öffnet sich der dazugehörige Tab im Tab-Bereich. Die Hilfe wird ebenfalls im Tab-Bereich angezeigt.
- Die [Dateisammlung](opensesame://help.pool) (Strg + P) zeigt Dateien die an Dein Experiment gebunden sind.
- Der [Variablenassistent](opensesame://help.extension.variable_inspector) (Strg + I) zeigt alle erkannten Variablen.
- Das [Debug-Fenster](opensesame://help.stdout). (Strg + D) ist ein [IPython]-Terminal. Der gesamte Standard-Output (z.B. mittels `print()`) Deines Experiments während des Durchlaufs wird hier angezeigt.

## Items

Items sind die Bausteine Deines Experiments. Zehn Kernitems bieten alle Basis-Funktionen, um ein Experiment zu erstellen. Um Items zu Deinem Experiment hinzuzufügen, ziehe Sie aus der Item-Werkzeugleiste in den Überblicksbereich.

- Das [loop]-Item(opensesame://help.loop) führt andere Items mehrfach aus. Du kannst im LOOP-Item auch unabhängige Variablen definieren.
- Das [sequence]-Item (opensesame://help.sequence) führt mehrere andere Items in einer definierbaren Reihenfolge aus.
- Das [sketchpad]-Item(opensesame://help.sketchpad) zeigt visuelle Stimuli. Mit integrierten Zeichentools kannst Du ganz leicht Deine Stimuli anzeigen.
- Das [feedback]-Item(opensesame://help.feedback) ähnelt dem `sketchpad`-Item, wird aber nicht vor Beginn des experimentellen Durchlaufs vorbereitet. Daher können FEEDBACK-Items genutzt werden um den Teilnehmerinnen und Teilnehmern Feedback zu ihrer aktuellen Leistung geben.
- Das [sampler]-Item (opensesame://help.sampler) spielt eine Sounddatei ab.
- Das [synth]-Item (opensesame://help.synth) erstellt einen Synthesizer-Sound.
- Das [keyboard_response]-Item (opensesame://help.keyboard_response) sammelt Tastendruck-Antworten.
- Das [mouse_response]-Item (opensesame://help.mouse_response) sammelt Mausklick-Antworten.
- Das [logger]-Item (opensesame://help.logger) schreibt Variablen in die Protokolldatei.
- Das [inline_script]-Item (opensesame://help.inline_script) bettet Python-Code in Dein Experiment ein.

Wenn sie installiert sind, bieten Plugin-Items zusätzliche Funktionalität. Plugins erscheinen gemeinsam mit den Kernitems in der Item-Werkzeugleiste.

## Dein Experiment starten

Du kannst Dein Experiment in verscheidenen Modi starten:

- Vollbildmodus (*Strg+R* oder *Starte -> Ausführen im Vollbildmodus*)
- Fenstermodus (*Strg+W* oder *Starte -> Ausführen im Fenstermodus*)
- Schnellstart (*Strg+Shift+W* oder *Starte -> Schnellstart*)

Beim Schnellstart beginnt das Experiment sofort in einem neuen Fenster mit der Protokolldatei `quickrun.csv` und Versuchspersonennummer 999. Das kann während der Entwicklung Deines Experiments sehr hilfreich sein.

Wenn die 'Automatischer Antwortmodus'-Option (*Starte -> Automatischen Antwortmodus aktivieren*) angeschaltet ist, simuliert OpenSesame Tastatur- und Mausklick-Antworten. Das kann während der Entwicklung Deines Experiments sehr hilfreich sein.

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/
