# Externes Skript

Das `external_script` Item ist eine Alternative um Python Code in Ihr Experiment zu integrieren. Während das `inline_script` Ihnen erlaubt Python Code direkt einzugeben, führt das `external_script` ein Pythonskript von einer Datei aus.

## Optionen

- *Script file*  ist der Name des Pythonskripts, welches ausgeführt wird.
- *Prepare function in script* ist der Name der Funktion im Skript, welches während der Prepare Phase ausgeführt wird (ohne Parameter).
- *Run function in script* ist der Name der Funktion im Skript, welches während der Run Phase ausgeführt wird (ohne Parameter).

## Skriptausführung und Python workspace

Das Skript wird im selben Python Workspace ausgeführt wie `inline_script` Items. Das bedeutet, dass Sie auf alle normalen Objekte und Funktionen zugreifen können, wie Sie es auch von `inline_scripts` könnten.

Wenn das Plug-in zum ersten Mal (während der ersten Prepare Phase) initialisiert wird, wird das gesamte Skript ausgeführt.

## Beispiel

Bei folgendem Skript nehmen wir an, dass Sie `prepare` und `run` als Funktionen haben, die Sie ausführen wollen:

~~~ .python
print('Das wird präsentiert, wenn das Plug-in initialisiert wird')

def prepare():

    print('Das wird während der Prepare Phase gezeigt')
    global c
    c = Canvas()
    c.fixdot()

def run():

    print('Das wird während der Run Phase gezeigt')
    global c
    c.show()
    clock.sleep(1000)
    c.clear()
    c.show()
~~~
