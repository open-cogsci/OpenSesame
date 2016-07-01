# Video_player

Das `video_player` Plug-in spielt eine Videodatei ab. Dieses Plug-in ist gedacht für einfache nur-Bild Videos und benötigt den `legacy` back-end. Falls Sie eine fortgeschrittene Video-abspiel Funktionalität benötigen, sollten Sie das `media_player_vlc` plug-in benutzen.

Folgende Optionen sind verfügbar:

- *Video file*:  Eine Videodatei aus der Dateisammlung. Welche Formate unterstützt werden hängt von ihrem System ab, but die meisten Formate (wie z.B. `.avi`und `.mpeg`) werden überall unterstützt.
- *Resize to fit screen*: Gibt an ob die Größe des Videos angepasst werden muss um den gesamten Bildschirm zu bedecken. Falls nicht, wird das Video in der Mitte des Bildschirms abgespielt. 
- *Duration*: Eine Dauer in Millisekunden, 'keypres' (um zu stoppen, sobald eine Taste gedrückt wird) oder 'mouseclick' (um zu stoppen, sobald eine Maustaste geklickt wird).
- *Frame duration*: Eine Dauer in Millisekunden eines einzelnen Bildframes. Im Grunde legt diese Option die Wiedergabegeschwindigkeit fest. Die maximale Geschwindigkeit hängt von der Geschwindigkeit Ihres Computers ab.


