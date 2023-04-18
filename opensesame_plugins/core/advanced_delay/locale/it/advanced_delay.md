# Advanced_delay

Il plug-in `advanced_delay` ritarda l'esperimento per una durata media pre-specificata più un margine casuale.

- *Duration* è la durata media del ritardo in millisecondi.
- *Jitter* è la dimensione della variazione del ritardo in millisecondi.
- *Jitter mode* è il modo in cui viene calcolato il jitter:
	- *Standard deviation* preleverà la variazione da una distribuzione gaussiana con il Jitter come deviazione standard.
	- *Uniform* preleverà la variazione di durata da una distribuzione uniforme.