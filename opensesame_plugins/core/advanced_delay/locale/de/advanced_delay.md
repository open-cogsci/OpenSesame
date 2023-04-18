# Advanced_delay

Das `advanced_delay` Plug-in verzögert das Experiment um eine vordefinierte durchschnittliche Dauer plus einem zufälligen Spielraum.

- *Dauer* ist die durchschnittliche Dauer der Verzögerung in Millisekunden.
- *Schwankung* ist die Größe der Variation der Verzögerung in Millisekunden.
- *Schwankungsmodus* ist die Art und Weise, wie die Schwankung berechnet wird:
	- *Standardabweichung* zieht die Variation aus einer Gaußschen Verteilung mit der Schwankung als Standardabweichung.
	- *Gleichmäßig* zieht die Variation in der Dauer aus einer gleichmäßigen Verteilung.