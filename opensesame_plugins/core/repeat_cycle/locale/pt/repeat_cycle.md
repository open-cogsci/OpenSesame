# Repeat_cycle

Este plug-in permite que você repita ciclos de um `loop`. Na maioria das vezes, isso será para repetir uma tentativa quando um participante cometeu um erro ou foi muito lento.

Por exemplo, para repetir todas as tentativas em que uma resposta demorou mais de 3000 ms, você pode adicionar um item `repeat_cycle` após (geralmente) o `keyboard_response` e adicionar a seguinte instrução repeat-if:

	[response_time] > 3000

Você também pode forçar a repetição de um ciclo definindo a variável `repeat_cycle` como 1 em um `inline_script`, como a seguir:

	var.repeat_cycle = 1