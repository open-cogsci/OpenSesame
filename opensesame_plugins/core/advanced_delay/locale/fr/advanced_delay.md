# Advanced_delay

Le plug-in `advanced_delay` retarde l'expérience pour une durée moyenne pré-spécifiée plus une marge aléatoire.

- *Duration* est la durée moyenne du retard en millisecondes.
- *Jitter* est la taille de la variation du retard en millisecondes.
- *Jitter mode* est la façon dont le jitter est calculé :
	- *Standard deviation* utilisera une distribution Gaussienne pour calculer la variation avec le Jitter comme écart-type.
	- *Uniform* utilisera une distribution uniforme pour calculer la variation de durée.