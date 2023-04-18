# Repeat_cycle

Bu eklenti, bir `loop` içindeki döngüleri tekrarlamanıza olanak tanır. En yaygın olarak, bu, katılımcının bir hata yaptığı veya çok yavaş olduğu denemeleri tekrarlamak için kullanılacaktır.

Örneğin, 3000 ms'den daha yavaş bir yanıt veren tüm denemeleri tekrarlamak için, `repeat_cycle` öğesini (genellikle) `keyboard_response`'un ardından ekleyebilir ve aşağıdaki tekrar-etme-ifadesini ekleyebilirsiniz:

	[response_time] > 3000

Ayrıca, bir `inline_script` içindeki `repeat_cycle` değişkenini 1'e ayarlayarak bir döngünün tekrarlanmasını zorlaştırabilirsiniz, şu şekilde:

	var.repeat_cycle = 1