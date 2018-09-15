# Plug-in port_reader

El plug-in port_reader (lector de puerto) lee entradas de un puerto arbitrario, tanto paralelo como puerto en serie, e interpreta el valor en retorno como una respuesta del participante (es decir, una presión de botón).

- **Modo dummy** -- Si lo ajusta a sí, se usará teclado en su lugar. 
Útil para propósitos de prueba. 
- **Número de puerto** -- El número del puerto que quiere usar. 
- **Valor de estado de reposo** -- El valor que debe interpretarse como 'botón no presionado'.
- **Respuesta correcta** -- La respuesta esperada.
- **Tiempo de expiración** -- El tiempo máximo permitido, tras el cual un 
tiempo de expiración se señalará.
