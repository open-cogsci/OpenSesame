# Advanced_delay

De `advanced_delay` plug-in vertraagt het experiment voor een vooraf opgegeven gemiddelde duur plus een willekeurige marge.

- *Duur* is de gemiddelde duur van de vertraging in milliseconden.
- *Jitter* is de grootte van de variatie in de vertraging in milliseconden.
- *Jitter modus* is de manier waarop de jitter wordt berekend:
	- *Standaardafwijking* zal de variatie uit een Gaussische verdeling halen met Jitter als de standaardafwijking.
	- *Uniform* zal de variatie in duur uit een uniforme verdeling halen.