# Repeat_cycle

Ce plug-in vous permet de répéter des cycles à partir d'une `loop`. Le plus souvent, cela sera pour répéter un essai lorsque le participant a commis une erreur ou était trop lent.

Par exemple, pour répéter tous les essais lorsqu'une réponse a été plus lente que 3000 ms, vous pouvez ajouter un élément `repeat_cycle` après (typiquement) le `keyboard_response` et ajouter la déclaration repeat-if suivante:

	[response_time] > 3000

Vous pouvez également forcer un cycle à être répété en définissant la variable `repeat_cycle` sur 1 dans un `inline_script`, comme ceci:

	var.repeat_cycle = 1