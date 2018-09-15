# Extensión para Open Science Framework

Esta extensión conecta OpenSesame a la [Open Science Framework](https://osf.io) (OSF), una plataforma web para compartir, conectar y desarrollar trabajos científicos. Para usarla deberá [crear una cuenta](https://osf.io/login/?sign_up=True) en la web de OSF. Puede entonces iniciar sesión con su cuenta OSF dentro de OpenSesame.

Con esta extensión puede enlazar un experimento en su ordenador a una localización en uno de sus repositorios en OSF. Cada vez que guarde su experimento, éste (bajo su permiso) Every time you save your experiment, it will (with your permission) será también subido a su localización correspondiente. De forma similar, puede elegir una carpeta en OSF para subir archivos de datos automáticamente tras completar experimentos. Además también puede abrir directamente experimentos que están almacenados en OSF desde OpenSesame. Al hacer esto, estos experimentos se conectarán automáticamente a su localización en OSF correspondiente si no lo estaban ya. Aparte de estas caracterísitcas, la extensión ofrece la posibilidad de interactuar con sus repositorios OSF para crear o eliminar carpetas, así como subir, bajar y eliminar archivos.

La web de OSF también ofrece posibilidades para conectar sus proyectos a otros servicios en la nube, como Dropbox, Google Drive o Github. Si conecta su proyecto OSF a uno de estos servicios, también podrá accederlos desde esta extensión e interactuar con ellos como si estuvieran en los repoositorios estándares de OSF. Muy cómodo, ¿no cree?

##Iniciar sesión en OSF

Para iniciar sesión en OSF, haga click en el botón de iniciar sesión en la barra de objetos de OpenSesame. Necesita tener una cuenta registrada en <https://osf.io> ya que no puede hacerlo desde OpenSesame. Una vez iniciada la sesión, puede abrir el explorador de OSF haciendo click en su nombre donde el botón de iniciar sesión estaba, y entonces seleccionar *Mostrar explorador*. Entonces verá un listado de todos sus proyectos y repositorios/servicios en la nube que ha enlazado a ellos. 

##Enlazar un experimento

Para enlazar un experimento, deberá primero asegurarse de que lo ha guardado primero en su ordenador. Abra el explorador de OSF y seleccione una carpeta o repositorio donde quiera guardar su experimento en OSF. Puede o bien hacer click derecho en la carpeta y seleccionar *Sincronizar experimento a esta carpeta* o también hacer click en *Enlazar experimento* en la barra de botones en la parte inferior mientras la carpeta deseada esté seleccionada. 

Si todo ha ido bien, el experimento será subido a la localización elegida (le saldrá un aviso con una elección sobre qué hacer si ya existe) y el nodo de OSF al cual el experimento ha sido enlazado se mostrará en la parte superior del explorador. Puede desenlazar el experimento haciendo click en el botón de desenlazar. También puede elegir subir automáticamente el experimento al guardar al seleccionar la opción *Subir siempre el experimento al guardar*. Al hacer esto, no longer se le pedirán permisos cada vez que suba el experimento.

Cuando abra en su ordenador un experimento que ha sido enlazado a OSF, OpenSesame revisará si la versión en su ordenador es y la que está en OSF son las mismas. Si encuentra que son distintas, se le mostrará un diálogo pregundando cómo proceder. Puede elegir entre seguir usando la versión en su ordenador, o bien continuar usando la versión almacenada en OSF. Esta versión puede ser entonces descargada y sobreescribirá el experimento en su ordenador. Sin embargo, antes de hacer esto se le preguntará si quiere guardar una copia de su archivo local con un nombre diferente. 

##Enlazar una carpeta a la que subir archivos

Para enlazar una carpeta a la que subir archivos, su experimento debe estar ya guardado en su ordenador. Abra el explorador de OSF, haga click derecho en la carpeta que quiera enlazar y seleccione *Sincronizar datos a esta carpeta* o seleccione la carpeta y haga click en *Enlazar datos* en la barra de botones inferior. 

Si rodo ha ido bien, el nodo de OSF representando la carpeta enlazada en OSF se mostrará en la parte superior del explorador. Puede desenlazar la carpeta de datos haciendo click en el botón de desenlazar junto a ella. Puede también subir los datos automáticamente eligiendo la opción *Subir siempre los datos recogidos*. Al hacer esto, no se le pedirá permisos cada vez que suba datos. 

##Abrir en experimento en OSF

Para abrir un experimento ya almacenado en OSF, puede buscar el exerimento en el explorador de OSF, hacer click derecho en él y seleccionar *Abrir experimento*. Alternativamente puede seleccionar el experimento y hacer click en *Abrir* en la barra de botones en la parte inferior. 
Sólo los experimentos con la nueva extensión .osexp (de OpenSesame 3 en adelante) pueden abrirse directamente en OSF.


