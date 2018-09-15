# Repeat_cycle

Este plug-in permite repetir ciclos de un `loop`(bucle). Normalmente, este será para repetir una prueba cuando un o una participante comete un error o es demasiado lento/a.

Por ejemplo, para repetir todas las pruebas cuya respuesta fue más lenta de 3000 ms, puede añadir un objeto `repeat_cycle` tras (típicamente) el objeto `keyboard_response` y añadir la siguiente declaración repetir-si:

	[response_time] > 3000

También puede forzar que se repita un ciclo ajustando la variable `repeat_cycle` a 1 en un objeto `inline_script` de la siguiente forma:

	var.repeat_cycle = 1
