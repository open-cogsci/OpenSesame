# Aide d'OpenSesame

*Ceci est la page d'aide hors-ligne. Si vous êtes connecté à Internet, vous pouvez trouver la documentation en ligne sur <http://osdoc.cogsci.nl>.*

## Introduction

OpenSesame est un outil de construction d'expérimentations pour les sciences humaines et sociales. Avec OpenSesame, vous pouvez facilement créer des expérimentations en utilisant une interface graphique "pointer et cliquer". Pour des tâches complexes, il est possible d'utiliser des scripts en python dans OpenSesame.

## Pour commencer

La meilleure manière de commencer est de suivre un tutoriel. Vous trouverez les tutoriels et d'autres informations en ligne sur : 
- <http://osdoc.cogsci.nl/tutorials/>

## Citation

Voici la citation à utiliser pour citer OpenSesame dans votre travail :

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: An open-source, graphical experiment builder for the social sciences. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Interface

L'interface graphique comprend les items suivants. Vous pouvez obtenir de l'aide spécifique en cliquant sur les icônes d'aide en haut à droite de chaque onglet.

- Le *menu* (en haut de la fenêtre) contient les options principales comme ouvrir et sauvegarder des fichiers, fermer le programme et accéder à cette page d'aide.
- La *barre d'outils principale* (les boutons gris positionnés horizontalement sous le menu) contient une sélection des options du menu qui sont le plus couramment utilisées.
- La *barre d'items* (positionnée verticalement à gauche de la fenêtre) contient les items disponibles. Pour ajouter un item à votre expérience, faite-le glisser de la barre d'items jusqu'à la zone de vue d'ensemble.
- La *vue d'ensemble* (Control + \\) contient un aperçu arborescent de votre expérience.
- La *zone d'onglets* contient les onglets pour éditer des items. Si vous cliquer sur un item dans la vue d'ensemble, l'onglet correspondant àcet item sera ouvert dans la zone d'onglets. Vous y trouverez également de l'aide.
- Le [groupe de fichiers](opensesame://help.pool) (Control + P) contient les fichiers qui sont regroupés dans votre expérimentation. 
- L'[inspecteur de variables](opensesame://help.extension.variable_inspector) (Control + I) contient toutes les variables détectées.
- La [fenêtre de débogage](opensesame://help.stdout) (Control + D) est un terminal [IPython]. Everything that your experiment prints to the standard output (i.e. using `print()`) is shown here.

## Items

Les items sont les éléments constitutifs de votre expérimentation. Dix items fournissent les fonctionnalités basiques pour créer une expérimentation. Pour ajouter des items à votre expérimentation, faites-les glisser de la barre d'items jusqu'à la vue d'ensemble.

- L'item [loop](opensesame://help.loop) permet de lancer d'autres items plusieurs fois au sein d'une boucle. Vous pouvez aussi définir des variables indépendantes dans la LOOP.
- L'item [sequence](opensesame://help.sequence) lance différents items au sein d'une même séquence.
- L'item [sketchpad](opensesame://help.sketchpad) présente des stimuli visuels. Vous pouvez facilement créer des stimuli visuels en utilisant les outils de construction disponibles.
- L'item [feedback](opensesame://help.feedback) est similaire au `sketchpad`, mais il n'est pas préparé à l'avance. Par conséquent, vous pouvez utiliser le FEEDBACK pour fournir un retour au participant.
- L'item [sampler](opensesame://help.sampler) permet de jouer un fichier son unique.
- L'item [synth](opensesame://help.synth) permet de créer un son.
- L'item [keyboard_response](opensesame://help.keyboard_response) collecte des réponses au clavier.
- L'item [mouse_response](opensesame://help.mouse_response) collecte les réponses au clic de la souris
- L'item [logger](opensesame://help.logger) inscrit des variables dans le fichier d'enregistrement des données.
- L'item [inline_script](opensesame://help.inline_script) intègre du code Python dans votre expérimentation.

Le plug-in items, s'il est installé, fournit des fonctionnalités supplémentaires. Les plug-ins apparaîssent le long des items dans la barre d'items.

## Lancer votre expérimentation

Vous pouvez exécuter votre expérimentation en mode :
- Plein-écran(*Ctrl+R* or *Exécuter -> Exécuter en plein écran*)
- Fenêtre (*Ctrl+W* or *Exécuter -> Exécuter en fenêtre*)
- Exécution rapide (*Ctrl+Shift+W* or *Exécuter -> Exécution rapide*)

Dans le mode exécution rapide, les expérimentations démarrent immédiatement dans une fenêtre, en utilisant un fichier d'enregistrement `quickrun.csv` avec le numéro de sujet 999. Ce mode peut être pratique lors du développement de l'expérimentation.

Lorsque l'option "autoriser la réponse automatique" (*Exécuter -> Autoriser la réponse automatique*) est disponible, OpenSesame simule les réponses au clavier ou à la souris ce qui peut être utile pendant le développement de l'expérimentation.

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/
