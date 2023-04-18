# Repeat_cycle

Dieses Plug-in ermöglicht es Ihnen, Zyklen aus einer `loop` zu wiederholen. Meistens wird dies verwendet, um einen Versuch zu wiederholen, wenn ein Teilnehmer einen Fehler gemacht hat oder zu langsam war.

Zum Beispiel, um alle Versuche zu wiederholen, bei denen eine Antwort langsamer als 3000 ms war, können Sie ein `repeat_cycle`-Element nach (typischerweise) dem `keyboard_response` hinzufügen und die folgende Wiederhole-Wenn-Aussage verwenden:

	[response_time] > 3000

Sie können auch erzwingen, dass ein Zyklus wiederholt wird, indem Sie die Variable `repeat_cycle` in einem `inline_script` auf 1 setzen, wie folgt:

	var.repeat_cycle = 1