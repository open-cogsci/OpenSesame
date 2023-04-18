# Advanced_delay

El complemento `advanced_delay` retrasa el experimento durante una duración promedio preestablecida más un margen aleatorio.

- *Duración* es la duración promedio del retraso en milisegundos.
- *Jitter* es el tamaño de la variación en el retraso en milisegundos.
- *Modo de Jitter* es cómo se calcula la fluctuación:
    - *Desviación estándar* extraerá la variación de una distribución gaussiana con Jitter como la desviación estándar.
    - *Uniforme* extraerá la variación de duración de una distribución uniforme.