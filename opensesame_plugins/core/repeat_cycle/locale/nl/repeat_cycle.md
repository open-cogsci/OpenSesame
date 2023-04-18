# Herhaal_cyclus

Deze plug-in stelt je in staat om cycli van een `loop` te herhalen. Meestal zal dit gebeuren als een deelnemer een fout heeft gemaakt of te langzaam was.

Om bijvoorbeeld alle trials te herhalen waarbij de reactietijd langer dan 3000 ms was, kun je een `repeat_cycle` item toevoegen na (meestal) de `keyboard_response` en de volgende herhaal-als instructie invoeren:

	[response_time] > 3000

Je kunt ook een cyclus forceren om te herhalen door de variabele `repeat_cycle` op 1 te zetten in een `inline_script`, op deze manier:

	var.repeat_cycle = 1