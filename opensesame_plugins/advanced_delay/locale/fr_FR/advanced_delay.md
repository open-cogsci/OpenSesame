# Advanced_delay

Le plugin `advanced_delay` retarde l'expérimentation d'une durée pré-spécifiée ajoutée à une durée aléatoire.
- *Durée* correspond à la durée moyenne du délai en millisecondes.
- *Variabilité* correspond à la taille de la variation du délai en millisecondes.
- *Mode de la variabilité* correspond à la manière dont la variabilité est calculée :
	- *Ecart-type* définira la variation à partir d'une distribution Gaussienne avec la Variabilité comme écart-type.
	- *Uniforme* définira la variation de la durée à partir d'une distribution uniforme.
