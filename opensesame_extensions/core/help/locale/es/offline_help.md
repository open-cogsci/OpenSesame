# Ayuda de OpenSesame

*Esta es la página de ayuda sin conexión. Si está conectado a Internet,
puede encontrar la documentación en línea en <http://osdoc.cogsci.nl>.*

## Introducción

OpenSesame es un creador de experimentos gráficos para las ciencias sociales. Con OpenSesame puedes crear fácilmente experimentos utilizando una interfaz gráfica de apuntar y hacer clic. Para tareas complejas, OpenSesame admite secuencias de comandos [Python].

## Empezando

La mejor manera de comenzar es haciendo un tutorial. Los tutoriales y mucho más se pueden encontrar en línea:

- <http://osdoc.cogsci.nl/tutorials/>

## Citación

Para citar OpenSesame en su trabajo, por favor utilice la siguiente referencia:

- Mathôt, S., Schreij, D., y Theeuwes, J. (2012). OpenSesame: An open-source, graphical experiment builder for the social sciences. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Interfaz

La interfaz gráfica tiene los siguientes componentes. Puede obtener
ayuda contextual haciendo clic en los íconos de ayuda en la parte superior derecha de
cada pestaña.

- El *menú* (en la parte superior de la ventana) muestra opciones comunes, como abrir y guardar archivos, cerrar el programa y mostrar esta página de ayuda.
- La *barra de herramientas principal* (los botones grandes debajo del menú) ofrece una selección de las opciones más relevantes del menú.
- La *barra de herramientas de elementos* (los botones grandes a la izquierda de la ventana) muestra los elementos disponibles. Para agregar un elemento a su experimento, arrástrelo desde la barra de herramientas de elementos al área de descripción general.
- El *área de descripción general* (Control + \\) muestra una descripción general en forma de árbol de su experimento.
- El *área de pestañas* contiene las pestañas para editar elementos. Si hace clic en un elemento en el área de descripción general, se abre una pestaña correspondiente en el área de pestañas. La ayuda también se muestra en el área de pestañas.
- El [grupo de archivos](opensesame://help.pool) (Control + P) muestra los archivos que se incluyen con su experimento.
-   El [inspector de variables](opensesame://help.extension.variable_inspector) (Control + I) muestra todas las variables detectadas.
-   La [ventana de depuración](opensesame://help.stdout). (Control + D) es un terminal [IPython]. Todo lo que su experimento imprime en la salida estándar (es decir, usando `print()`) se muestra aquí.

## Elementos

Los elementos son los bloques de construcción de su experimento. Diez elementos básicos proporcionan funcionalidad básica para crear un experimento. Para agregar elementos a su experimento, arrástrelos desde la barra de herramientas de elementos al área de descripción general.

- El elemento [loop](opensesame://help.loop) ejecuta otro elemento varias veces. También puede definir variables independientes en el elemento LOOP.
- El elemento [sequence](opensesame://help.sequence) ejecuta otros elementos en secuencia.
- El elemento [sketchpad](opensesame://help.sketchpad) presenta estímulos visuales. Las herramientas de dibujo incorporadas le permiten crear fácilmente pantallas de estímulos.
- El elemento [feedback](opensesame://help.feedback) es similar al `sketchpad`, pero no se prepara con anticipación. Por lo tanto, los elementos FEEDBACK se pueden utilizar para proporcionar comentarios a los participantes.
- El elemento [sampler](opensesame://help.sampler) reproduce un solo archivo de sonido.
- El elemento [synth](opensesame://help.synth) genera un único sonido.
- El elemento [keyboard_response](opensesame://help.keyboard_response) recopila respuestas de teclas presionadas.
- El elemento [mouse_response](opensesame://help.mouse_response) recopila respuestas de clics del mouse.
- El elemento [logger](opensesame://help.logger) escribe variables en el archivo de registro.
- El elemento [inline_script](opensesame://help.inline_script) incrusta código Python en su experimento.

Si están instalados, los elementos del complemento proporcionan funcionalidad adicional. Los complementos aparecen junto a los elementos básicos en la barra de herramientas de elementos.

## Ejecutando su experimento

Puede ejecutar su experimento en:

- Modo de pantalla completa (*Control+R* o *Ejecutar -> Ejecutar en pantalla completa*)
- Modo de ventana (*Control+W* o *Ejecutar -> Ejecutar en ventana*)
- Modo de ejecución rápida (*Control+Shift+W* o *Ejecutar -> Ejecución rápida*)

En el modo de ejecución rápida, los experimentos comienzan de inmediato en una ventana, utilizando el archivo de registro `quickrun.csv` y el número de sujeto 999. Esto es útil durante el desarrollo.

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/