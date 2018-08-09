# Plugin de reproductor de medios basado en Moviepy

Copyright 2010-2016 Daniel Schreij (<d.schreij@vu.nl>)

El plugin media_player_mpy plug-in añade la capacidad de reproducir medio al [editor de experimentos de OpenSesame][opensesame]. Este plugin usa [Moviepy][mpy_home] como base. Debería ser capaz de manejar la mayoría de los formatos de vídeo y audio modernos, aunque es importante que sus fuentes no esten corruptas. Si un archivo no parece funcionar, trate de encontrar una versión mejor o recodifíquelo en un formato distinto. 

La mejor reproducción se consigue emdiante la aceleración de hardware proporcionada por una base Psychopy o Expyriment. El resultado puede ser peor cuando se utiliza una base anticuada o el medio tiene una alta resolución o número de fotogramas por segundo.

## Ajustes del plugin
El plugin ofrece las siguientes opciones de configuración en la GUI: 

- *Archivo de video* - el archivo a reproducirse. Este campo permite incluir variables como [video_file], las cuales se pueden especificar su valor en ítems de bucle.
- *Reproducir audio* - especifica si el video debe ser reproducido con sonido o no (silenciado).
- *Ajustar video a pantalla* - especifica si el video debe ser reproducicido en su tamaño original, o si debe ser escalado para encajar en la ventana/pantalla. El proceso de reescalado mantiene la proporción original del vídeo. 
- *Bucle* - especifica si el video debe ser reproducido en bucle, es decir, que vuelva a reproducir desde el principio una vez llegue al final. 
- *Duración* - Establece qué longitud debe tener el vídeo a mostrar. Se espera un valor en segundos, 'keypress' o 'mouseclick'. Si tiene uno de los últimos dos valores, la reproducción terminará si se pulsa una tecla o se hace clic con el ratón respectivamente. 

## Código Python personalizado para manejar eventos de pulsaciones de teclas y de clic de ratón 
Este plugin también ofrece funcionalidad para ejecutar código propio para ejecutar eventos tras cada fotograma, o tras una presión de tecla o se hace clic con el ratón (Tenga en cuenta que la ejecucuón de código tras cada fotograma nulifica la opción 'keypress' en el campo de duración; si bien se responderá a presiones de la tecla Escape). Esto es útil, por ejemplo, si uno quiere contar cuántas veces un participante ha presionado una tecla (por ejemplo espacio) durante la reproducción del vídeo.

Hay algunas variables accessibles en el script que puede introducir aquí: 

- `continue_playback` (True o False) - Determina si el vídeo debe continuar reproduciéndose. Esta variable está ajustada a True por predeterminado mientras el vídeo se reproduce. Si quiere detener la reproducción desde su script, ajuste esta variable a False y se detendrá. 
- `exp` - Una variable de conveniencia apuntando al objeto self.experiment
- `frame` - El número del fotograma mostrándose actualmente
- `mov_width` - El ancho del vídeo en px
- `mov_height` - El alto del vídeo en px
- `paused` - *True* cuando la reproducción está pausada, *False* si se está reproduciendo actualmente 
- `event` - Esta variable es un tanto especial, ya que sus contenidos dependen en si una tecla se está pulsando o se hace click con el ratón durante el último fotograma. Si no es el caso, la variable simplemente apuntará a *None*. Si se pulsó una tecla, el evento contendrá un tuple con la primera posición diciendo "key" y en la segunda el valor de la tecla pulsada, como por ejemplo ("key", "space") para espacio. Si se hizo clic con el ratón, el tuple contendrá "mouse" en su primera posición y en la segunda el número del botón pulsado, como por ejemplo ("mouse", 2). En el raro caso que múltiples botones  o teclas se pulsen, la variable contendrá una lista de estos eventos, como por ejemplo [("key","space"),("key", "x"),("mouse",2)]. En este caso, deberá traspasar la lista a su código y extraer todos los eventos que le sean relevantes. 

Junto a estas variables también tiene las siguientes funciones disponibles: 

- `pause()` - Pausa la reproducción cuando el vídeo se reproduce, y despausa en el caso contrario (puede verlo como un interruptor de pausa/despausar) 

[opensesame]: http://www.cogsci.nl/opensesame
[mpy_home]: http://zulko.github.io/moviepy/

