# External_script

L'item `external_script` est une manière alternative d'inclure du code Python dans votre expérimentation. Contraitement à l'item `inline_script` qui permet d'entrer directement du code Pyton, l'item `external_script` exécute le script Python d'un autre fichier.

## Options

- *Script file* est le nom du script Python qui sera exécuté.
- *Prepare function in script* est le nom de la fonction du script appelé (sans paramètres) pendant la phase de préparation.
- *Run function in script* est le nom de la fonction du script appelé (sans paramètres) pendant la phase d'exécution.


## Exécution du script et espace de travail Python

Le script est exécuté dans le même espace de travail Python que celui qui est utilisé pour l'item `inline_script`. Cela veut dire que vous pouvez accéder à tous les objets et fonctions habituels comme pour un item `inline_script`.

Quand le plugin est initialisé pour la première fois(pendant la phase de préparation initiale), le script entier est exécuté.

## Exemple

Dans le script suviant, faisons l'hypothèse que vous utilisez `prepare` and `run` comme les fonctions à exécuter :

~~~ .python
print('This will be shown when the plug-in is initialized')

def prepare():

    print('This will be shown during the prepare phase')
    global c
    c = Canvas()
    c.fixdot()

def run():

    print('This will be shown during the run phase')
    global c
    c.show()
    clock.sleep(1000)
    c.clear()
    c.show()
~~~
