# Guida di OpenSesame

*Questa è la pagina della guida offline. Se sei connesso a Internet,
puoi trovare la documentazione online all'indirizzo <http://osdoc.cogsci.nl>.*

## Introduzione

OpenSesame è un programma grafico per la creazione di esperimenti nelle scienze sociali. Con OpenSesame puoi creare facilmente esperimenti utilizzando un'interfaccia grafica point-and-click. Per compiti complessi, OpenSesame supporta lo scripting [Python].

## Come iniziare

Il modo migliore per iniziare è seguire un tutorial. I tutorial, e molto altro, possono essere trovati online:

- <http://osdoc.cogsci.nl/tutorials/>

## Citazione

Per citare OpenSesame nel tuo lavoro, utilizza il seguente riferimento:

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: Un programma open-source, grafico per la creazione di esperimenti nelle scienze sociali. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Interfaccia

L'interfaccia grafica ha i seguenti componenti. Puoi ottenere
aiuto sensibile al contesto facendo clic sulle icone di aiuto in alto a destra di
ciascuna scheda.

- Il *menu* (in alto nella finestra) mostra le opzioni comuni, come aprire e salvare file, chiudere il programma e mostrare questa pagina di aiuto.
- La *barra degli strumenti principale* (i grandi pulsanti sotto il menu) offre una selezione delle opzioni più pertinenti dal menu.
- La *barra degli strumenti degli elementi* (i grandi pulsanti sulla sinistra della finestra) mostra gli elementi disponibili. Per aggiungere un elemento al tuo esperimento, trascinalo dalla barra degli strumenti degli elementi nell'area panoramica.
- L'*area riepilogativa* (Control + \\) mostra una panoramica ad albero del tuo esperimento.
- L'*area delle schede* contiene le schede per la modifica degli elementi. Se fai clic su un elemento nell'area di panoramica, una scheda corrispondente si apre nell'area delle schede. L'aiuto viene visualizzato anche nell'area delle schede.
- La [riserva di file](opensesame://help.pool) (Control + P) mostra i file che vengono raggruppati con il tuo esperimento.
- Il [controllore delle variabili](opensesame://help.extension.variable_inspector) (Control + I) mostra tutte le variabili rilevate.
- La [finestra di debug](opensesame://help.stdout). (Control + D) è un terminale [IPython]. Tutto ciò che il tuo esperimento stampa sull'output standard (cioè usando `print()`) viene mostrato qui.

## Elementi

Gli elementi sono i mattoni del tuo esperimento. Dieci elementi principali offrono funzionalità di base per creare un esperimento. Per aggiungere elementi al tuo esperimento, trascinali dalla barra degli strumenti degli elementi nell'area panoramica.

- L'elemento [loop](opensesame://help.loop) esegue un altro elemento più volte. Puoi anche definire variabili indipendenti nell'elemento LOOP.
- L'elemento [sequence](opensesame://help.sequence) esegue più altri elementi in sequenza.
- L'elemento [sketchpad](opensesame://help.sketchpad) presenta stimoli visivi. Gli strumenti di disegno integrati ti permettono di creare facilmente schermate di stimoli.
- L'elemento [feedback](opensesame://help.feedback) è simile allo `sketchpad`, ma non viene preparato in anticipo. Pertanto, gli elementi FEEDBACK possono essere utilizzati per fornire feedback ai partecipanti.
- L'elemento [sampler](opensesame://help.sampler) riproduce un singolo file audio.
- L'elemento [synth](opensesame://help.synth) genera un singolo suono.
- L'elemento [keyboard_response](opensesame://help.keyboard_response) raccoglie risposte con i tasti premuti.
- L'elemento [mouse_response](opensesame://help.mouse_response) raccoglie risposte con i clic del mouse.
- L'elemento [logger](opensesame://help.logger) scrive le variabili nel file di log.
- L'elemento [inline_script](opensesame://help.inline_script) integra il codice Python nel tuo esperimento.

Se installati, gli elementi plug-in forniscono funzionalità aggiuntive. I plug-in appaiono accanto agli elementi principali nella barra degli strumenti degli elementi.

## Esecuzione del tuo esperimento

Puoi eseguire il tuo esperimento in:

- Modalità a schermo intero (*Control+R* o *Esegui -> Esegui a schermo intero*)
- Modalità a finestra (*Control+W* o *Esegui -> Esegui in finestra*)
- Modalità di esecuzione rapida (*Control+Shift+W* o *Esegui -> Esecuzione rapida*)

In modalità di esecuzione rapida, l'esperimento parte immediatamente in una finestra, utilizzando il file di log `quickrun.csv` e il numero di soggetto 999. Questo è utile durante lo sviluppo.

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/