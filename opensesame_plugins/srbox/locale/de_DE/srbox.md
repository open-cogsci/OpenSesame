# SR Box

Das SR (serial response) box Item sammelt Reaktionen von einer Tastenbox, die mit einem seriellen Port oder via USB zu einem "virtuellen seriellen Port" verbunden ist. Dieses Item kann mit der SR Box (Psychology Software Tools. Inc.) und kompatiblen Geräten benutzt werden. 

## Dummymodus

Im Dummymodus wird die SR Box mittels den Nummertasten auf der Tastatur simuliert. Dies ist nützlich um ihr Experiment ohne eine SR Box zu testen.

## Ignoriere Tasten, die schon gedrückt sind

Falls Sie die Option 'Ignoriere Tasten, die schon gedrückt sind' aktiviert haben, wird das Plug-in nur solche Reaktionen berücksichtigen, die von nicht-gedrückt ihren Status zu gedrückt veränderen. Dies ist normalerweise was Sie möchten, weil es verhindert das eine einzelner Tastendruck eine Vielzahl von Reaktionen verursacht. Diese Option ist aus Rückwärtskompatibilitätsgründen jedoch deaktiviert.

## Name von Tasten und Lichter

Tasten und Lichter werden durch eine einzelne Nummer zwischen 1 und 8 identifiziert. Wieviele Tasten es gibt und welche Tasten zu welchen Nummern gehören ist von Ihrer speziellen Tastenbox abhängig. Auf der SR Box, die von Psychology Software Tools, Inc. vertrieben wird, gibt es 5 Tasten und 5 Lichter, wobei sich Taste 1 und Licht 1 auf der linken Seite befinden. Auf anderen SR Boxen könnten Lichter nicht verfügbar sein. In diesem Fall wird die Lichteingabe ignoriert.

## Mehr Informationen

Auf der Seite von Psychology Software Tools:

- <http://www.pstnet.com/hardware.cfm?ID=102>.

Auf der OpenSesame Dokumentationsseite:

- <http://osdoc.cogsci.nl/3.1/manual/response/srbox/>
