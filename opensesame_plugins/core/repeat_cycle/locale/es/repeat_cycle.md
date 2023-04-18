# Repeat_cycle

Este complemento te permite repetir ciclos desde un `loop`. Lo más común es para repetir un ensayo cuando un participante cometió un error o fue demasiado lento.

Por ejemplo, para repetir todos los ensayos en los que una respuesta fue más lenta que 3000 ms, puedes agregar un elemento `repeat_cycle` después (típicamente) de la `keyboard_response` y agregar la siguiente declaración de repetir si:

	[response_time] > 3000

También puedes forzar la repetición de un ciclo estableciendo la variable `repeat_cycle` en 1 en un `inline_script`, de la siguiente manera:

	var.repeat_cycle = 1