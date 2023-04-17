# OpenSesame Hilfe

*Dies ist die Offline-Hilfeseite. Wenn Sie mit dem Internet verbunden sind,
finden Sie die Online-Dokumentation unter <http://osdoc.cogsci.nl>.*

## Einführung

OpenSesame ist ein grafischer Experiment-Builder für die Sozialwissenschaften. Mit OpenSesame können Sie einfach Experimente erstellen, indem Sie eine grafische Benutzeroberfläche mit Drag-and-Drop verwenden. Für komplexe Aufgaben unterstützt OpenSesame [Python]-Skripterstellung.

## Erste Schritte

Der beste Weg, um anzufangen, besteht darin, ein Tutorial zu durchlaufen. Tutorials und vieles mehr finden Sie online:

- <http://osdoc.cogsci.nl/tutorials/>

## Zitat

Um OpenSesame in Ihrer Arbeit zu zitieren, verwenden Sie bitte die folgende Referenz:

- Mathôt, S., Schreij, D. & Theeuwes, J. (2012). OpenSesame: Ein quelloffener, grafischer Experiment-Builder für die Sozialwissenschaften. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Benutzeroberfläche

Die grafische Benutzeroberfläche hat die folgenden Komponenten. Sie können kontextsensitive Hilfe erhalten, indem Sie auf die Hilfesymbole oben rechts auf jeder Registerkarte klicken.

- Das *Menü* (oben im Fenster) zeigt häufig verwendete Optionen, z.B. Öffnen und Speichern von Dateien, Schließen des Programms und Anzeigen dieser Hilfeseite.
- Die *Hauptwerkzeugleiste* (die großen Schaltflächen unterhalb des Menüs) bietet eine Auswahl der wichtigsten Optionen aus dem Menü.
- Die *Element-Werkzeugleiste* (die großen Schaltflächen links im Fenster) zeigt verfügbare Elemente. Um ein Element zu Ihrem Experiment hinzuzufügen, ziehen Sie es von der Element-Werkzeugleiste in den Übersichtsbereich.
- Der *Übersichtsbereich* (Strg + \\) zeigt eine baumartige Übersicht Ihres Experiments.
- Der *Registerkartenbereich* enthält die Registerkarten zum Bearbeiten von Elementen. Wenn Sie auf ein Element im Übersichtsbereich klicken, wird eine entsprechende Registerkarte im Registerkartenbereich geöffnet. Hilfe wird auch im Registerkartenbereich angezeigt.
- Der [Datei-Pool](opensesame://help.pool) (Strg+P) zeigt Dateien, die Ihrem Experiment beigefügt sind.
- Der [Variablen-Inspektor](opensesame://help.extension.variable_inspector) (Strg + I) zeigt alle erkannten Variablen.
- Das [Debug-Fenster](opensesame://help.stdout) (Strg + D) ist ein [IPython]-Terminal. Alles, was Ihr Experiment auf der Standardausgabe ausgibt (d.h. mit `print()`), wird hier angezeigt.

## Elemente

Elemente sind die Bausteine Ihres Experiments. Zehn Kernelemente bieten grundlegende Funktionen für die Erstellung eines Experiments. Um Elemente zu Ihrem Experiment hinzuzufügen, ziehen Sie sie aus der Element-Werkzeugleiste in den Übersichtsbereich.

- Das [loop](opensesame://help.loop) Element führt ein anderes Element mehrere Male aus. Sie können auch unabhängige Variablen im LOOP-Element definieren.
- Das [sequence](opensesame://help.sequence) Element führt mehrere andere Elemente in einer Sequenz aus.
- Das [sketchpad](opensesame://help.sketchpad) Element präsentiert visuelle Reize. Integrierte Zeichenwerkzeuge ermöglichen es Ihnen, Reizdarstellungen einfach zu erstellen.
- Das [feedback](opensesame://help.feedback) Element ähnelt dem `sketchpad`, wird jedoch nicht im Voraus vorbereitet. Daher können FEEDBACK-Elemente verwendet werden, um Rückmeldungen an die Teilnehmer zu geben.
- Das [sampler](opensesame://help.sampler) Element spielt eine einzelne Sounddatei ab.
- Das [synth](opensesame://help.synth) Element erzeugt einen einzelnen Ton.
- Das [keyboard_response](opensesame://help.keyboard_response) Element erfasst Tastendruck-Antworten.
- Das [mouse_response](opensesame://help.mouse_response) Element erfasst Mausklick-Antworten.
- Das [logger](opensesame://help.logger) Element schreibt Variablen in die Protokolldatei.
- Das [inline_script](opensesame://help.inline_script) Element bettet Python-Code in Ihr Experiment ein.

Wenn installiert, bieten Plug-in-Elemente zusätzliche Funktionen. Plug-ins erscheinen neben den Kernelementen in der Element-Werkzeugleiste.

## Ihr Experiment ausführen

Sie können Ihr Experiment in folgenden Modi ausführen:

- Vollbildmodus (*Strg+R* oder *Run -> Run fullscreen*)
- Fenstermodus (*Strg+W* oder *Run -> Run in window*)
- Schnellstartmodus (*Strg+Umschalt+W* oder *Run -> Quick run*)

Im Schnellstartmodus startet das Experiment sofort in einem Fenster und verwendet die Protokolldatei `quickrun.csv` und die Probandennummer 999. Dies ist während der Entwicklung nützlich.

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/