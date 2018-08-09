# Ayuda de OpenSesame

*Esta es la página de ayuda offline. Si tiene conexión a internet, 
puede encontrar documentación (en inglés) en línea en <http://osdoc.cogsci.nl>.*

## Introducción

OpenSesame es un constructor de experimentos gráficos para ciencias sociales. Con OpenSesame puede crear experimentos fácilmente con una interfaz gráfica. Para tareas complejas, OpenSesame permite scripts en [Python].

## Empezar

La mejor manera de empezar es a través de un tutorial. Puede encontrar tutoriales y más en línea: 

- <http://osdoc.cogsci.nl/tutorials/>

## Citas

Para citar OpenSesame en sus trabajos, utilice la siguiente referencia: 

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: An open-source, graphical experiment builder for the social sciences. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Interfaz

La interfaz gráfica cuenta con los siguientes componentes. Puede obtener 
ayuda más específica haciendo click en los iconos de ayuda en los iconos de ayuda en la parte superior derecha de 
cada pestaña.

- El *menú* (en la parte superior de la ventana) muestra opciones comunes, como abrir y guardar archivos, cerrar el programa y mostrar esta página de ayuda. 
- La *barra de herramientas principal* (los botones grandes bajo el menú) ofrece una selección de las opciones más relevantes del menú. 
- La *barra de herramientas de objetos* (los botones grandes a la izquierda de la ventana) muestra los objetos disponibles. Para añadir un objeto a su experimento, arrástrelo de dicha barra de herramientas al área de vista general.
- El *área de vista general* (Control + \\) muestra una vista general en una estructura de árnpñ de su experimento. 
- El *área de pestañas* contiene las pestañas para editar sus objetos. Si hace click en un objeto en el área de vista general, una pestaña correspondiente se abrirá en el área de pestañas. También se mostrará ayuda en el área de pesteañas.
- El [grupo de archivos](opensesame://help.pool) (Control + P) muestra los archivos que están incorporados en su experimento. 
-   El [inspector de variables](opensesame://help.extension.variable_inspector) (Control + I) muestra todas las variables detectadas
-   La [vebtana de depuración](opensesame://help.stdout). (Control + D) es una terminal de [IPython]. Todo lo que su experimento imprima is an [IPython] terminal. Todo lo que su experimento imprima (en otras palabras, usando `print()`) se mostrará aquí.

## Objetos

Los objetos son los ladrillos de su experimento. Diez objetos principales ofrecen funcionalidad básica para crear un experimentos. Para añadir objetos a su experimento, arrástrelos de la barra de herramientas de objetos al área de vista general. 

- El objeto [loop (bucle)](opensesame://help.loop) corre otro objeto múltiples veces. Puede también definir variables independientes en dicho objeto.
- El objeto [sequence(secuencia)](opensesame://help.sequence) corre múltiples objetos distintos en secuencia. 
- El objeto [sketchpad (bloc de dibujo)](opensesame://help.sketchpad) presenta un estímulo visual. Cuenta con herramientas de dibujo para crear estímulos visuales fácilmente.
- El objeto [feedback](opensesame://help.feedback) es similar a `sketchpad`, pero no está preparado de antemano. Por tanto, puede usarse para proporcionar feedback a los participantes.
- El objeto [sampler (mezclador)](opensesame://help.sampler) reproduce un archivo de sonido
- El objeto [synth](opensesame://help.synth) genera un sonido.
- El objeto [keyboard_response (respuesta de teclado)](opensesame://help.keyboard_response) recoje respuestas de presión de teclado.
- El objeto [mouse_response (respuesta de ratón)](opensesame://help.mouse_response) recoje respuestas de click de ratón. 
- El objeto [logger (registrador)](opensesame://help.logger) escribe los valores de variables al archivo de registro. 
- El objeto [inline_script (script interno)](opensesame://help.inline_script) incorpora código en Python a su experimento. 

También puede obtener objetos con funcionalidades extra si se instalan mediante plug-ins. Estos aparecerán junto a los objetos principales en su barra de herramientas. 

## Correr su experimetno

Puede correr su experimento en:

- Modo de pantalla completa (*Control+R* or *Correr -> Correr en pantalla completa*)
- Modo en ventana (*Control+W* or *Correr -> Correr en ventana*)
- Modo de correr rápido (*Control+Shift+W* or *Correr -> Correr rápido*)

En el modo de correr rápido, el experimento inicia inmediatamente en una ventana, usando como registro el archivo `quickrun.csv` y con el número de sujeto 999. Esto es útil durante el desarrollo del experimento. 

Cuando la opción 'respuesta automática' (*Correr -> Activar respuesta automática*) está habilitada, OpenSesame simula presiones de tecla y ratón, lo cuál es útil durante el desarrollo del experimento. 

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/
