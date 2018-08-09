# Parallel

El plug-in parallel permite correr múltiples objetos al mismo tiempo, es decir, en paralelo. Esto es conveniente, por ejemplo cuando quiere mostrar estímulos dinámicamente y pedir respuestas al mismo tiempo. 

**Nota:** En algunos sistemas, los hilos (es decir, procesos corriendo en paralelo) no recibirán eventos de teclado. El primer objeto del plug-in parallel es ejecutado en el proceso principal. Por tanto,  si sus objetos no parecen responder a presiones de teclado, trate de colocar su objeto de respuesta de teclado como primer objeto en parallel. 
