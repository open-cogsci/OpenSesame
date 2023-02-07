# Advanced_delay

The `advanced_delay` plug-in delays the experiment for a pre-specified average duration plus a random margin.

- *Duration* ist die Durchschnittsdauer des Delays (Verzögerung) in Millisekunden.
- *Jitter* ist die Größe der Variation des Delays in Millisekunden.
- *Jitter mode* ist wie der Jitter (Variation) berechnet wird:
	- *Standard deviation* nimmt die Variation von einer Gausschen Verteilung mit Jitter als Standardabweichung.
	- *Uniform* nimmt die Variation der Dauer von einer Uniformen Verteilung.
