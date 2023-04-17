# Aide OpenSesame

*Ceci est la page d'aide hors ligne. Si vous êtes connecté à Internet,
vous pouvez trouver la documentation en ligne à l'adresse <http://osdoc.cogsci.nl>.*

## Introduction

OpenSesame est un créateur d'expériences graphiques pour les sciences sociales. Avec OpenSesame, vous pouvez facilement créer des expériences en utilisant une interface graphique point-and-click. Pour les tâches complexes, OpenSesame prend en charge les scripts [Python].

## Pour commencer

La meilleure façon de commencer est de suivre un tutoriel. Des tutoriels, et bien plus encore, peuvent être trouvés en ligne:

- <http://osdoc.cogsci.nl/tutorials/>

## Citation

Pour citer OpenSesame dans votre travail, veuillez utiliser la référence suivante :

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: Un créateur d'expériences open-source et graphique pour les sciences sociales. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Interface

L'interface graphique comporte les éléments suivants. Vous pouvez obtenir
une aide contextuelle en cliquant sur les icônes d'aide en haut à droite de
chaque onglet.

- Le *menu* (en haut de la fenêtre) affiche les options courantes, telles que l'ouverture et l'enregistrement de fichiers, la fermeture du programme et l'affichage de cette page d'aide.
- La *barre d'outils principale* (les gros boutons sous le menu) propose une sélection des options les plus pertinentes du menu.
- La *barre d'outils d'éléments* (les gros boutons sur la gauche de la fenêtre) montre les éléments disponibles. Pour ajouter un élément à votre expérience, faites-le glisser depuis la barre d'outils d'éléments jusqu'à la zone de présentation générale.
- La *zone de présentation générale* (Control + \\) affiche une vue d'ensemble en arborescence de votre expérience.
- La *zone à onglets* contient les onglets pour modifier les éléments. Si vous cliquez sur un élément dans la zone de présentation générale, un onglet correspondant s'ouvre dans la zone des onglets. L'aide s'affiche également dans la zone des onglets.
- La [réserve de fichiers](opensesame://help.pool) (Control + P) montre les fichiers joints à votre expérience.
-   L'[inspecteur de variables](opensesame://help.extension.variable_inspector) (Control + I) montre toutes les variables détectées.
-   La [fenêtre de débogage](opensesame://help.stdout). (Control + D) est un terminal [IPython]. Tout ce que votre expérience imprime sur la sortie standard (c'est-à-dire en utilisant `print()`) est affiché ici.

## Éléments

Les éléments sont les éléments constitutifs de votre expérience. Dix éléments principaux offrent des fonctionnalités de base pour créer une expérience. Pour ajouter des éléments à votre expérience, faites-les glisser depuis la barre d'outils d'éléments dans la zone de présentation générale.

- L’élément [loop](opensesame://help.loop) exécute un autre élément plusieurs fois. Vous pouvez également définir des variables indépendantes dans l'élément LOOP.
- L’élément [sequence](opensesame://help.sequence) exécute plusieurs autres éléments en séquence.
- L’élément [sketchpad](opensesame://help.sketchpad) présente des stimuli visuels. Les outils de dessin intégrés vous permettent de créer facilement des écrans de stimuli.
- L’élément [feedback](opensesame://help.feedback) est similaire au `sketchpad`, mais n'est pas préparé à l'avance. Par conséquent, les éléments FEEDBACK peuvent être utilisés pour fournir un retour d'information aux participants.
- L’élément [sampler](opensesame://help.sampler) lit un seul fichier sonore.
- L’élément [synth](opensesame://help.synth) génère un seul son.
- L’élément [keyboard_response](opensesame://help.keyboard_response) collecte les réponses par pression de touche.
- L’élément [mouse_response](opensesame://help.mouse_response) collecte les réponses par clic de souris.
- L’élément [logger](opensesame://help.logger) écrit les variables dans le fichier journal.
- L’élément [inline_script](opensesame://help.inline_script) intègre du code Python dans votre expérience.

Les éléments plug-in supplémentaires fournissent des fonctionnalités supplémentaires si installés. Les plug-ins apparaissent à côté des éléments principaux dans la barre d'outils d'éléments.

## Exécuter votre expérience

Vous pouvez exécuter votre expérience en :

- Mode plein écran (*Control+R* ou *Run -> Exécuter en plein écran*)
- Mode fenêtre (*Control+W* ou *Run -> Exécuter dans une fenêtre*)
- Mode exécution rapide (*Control+Shift+W* ou *Run -> Exécution rapide*)

En mode d'exécution rapide, l'expérience démarre immédiatement dans une fenêtre, en utilisant le fichier journal `quickrun.csv` et le numéro de sujet 999. Ceci est utile pendant le développement.

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/