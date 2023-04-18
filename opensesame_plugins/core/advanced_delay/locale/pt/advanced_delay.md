# Advanced_delay

O plug-in `advanced_delay` atrasa o experimento por uma duração média pré-especificada mais uma margem aleatória.

- *Duração* é a duração média do atraso em milissegundos.
- *Jitter* é o tamanho da variação no atraso em milissegundos.
- *Modo Jitter* é como o jitter é calculado:
	- *Desvio padrão* extrairá a variação de uma distribuição Gaussiana com o Jitter como desvio padrão.
	- *Uniforme* extrairá a variação na duração de uma distribuição uniforme.