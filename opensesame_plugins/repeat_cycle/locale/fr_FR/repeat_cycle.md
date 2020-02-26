# Repeat_cycle

Ce plug-in vous permet de répéter des cycles à partir d'une `loop'. Le plus souvent, il s'agira de répéter un essai lorsqu'un participant a fait une erreur ou a été trop lent.

Par exemple, pour répéter tous les essais pour lesquels une réponse a été plus lente que 3000 ms, vous pouvez ajouter un item `repeat_cycle` après (généralement) la` keyboard_response` et ajouter le repeat-if statement suivant :

	[response_time] > 3000

Vous pouvez également forcer la répétition d'un cycle en mettrant la variable `repeat_cycle` sur 1 dans un` inline_script`, comme ceci :

	var.repeat_cycle = 1
