# Ripeti_ciclo

Questo plug-in ti permette di ripetere cicli da un `loop`. Più comunemente, ciò avverrà per ripetere un tentativo quando un partecipante ha commesso un errore o è stato troppo lento.

Ad esempio, per ripetere tutti i tentativi in cui una risposta è stata più lenta di 3000 ms, è possibile aggiungere un elemento `repeat_cycle` dopo (tipicamente) il `keyboard_response` e aggiungere la seguente istruzione ripeti-se:

	[response_time] > 3000

Puoi anche forzare la ripetizione di un ciclo impostando la variabile `repeat_cycle` su 1 in un `inline_script`, in questo modo:

	var.repeat_cycle = 1