# Repeat_cycle

Bu eklenti bir `loop` dan döngülerin tekrar edilmesini sağlar. Bu katılımcının bir denemede hata yaptığı ya da çok yavaş olduğu durumlarda kullanılır.

Örneğin, 3000 milisaniyeden daha uzun sürede verilen yanıtların bulunduğu deneysel denemelerin (experimetal trial) tekrar edilmesi için  `repeat_cycle`  ögesini `keyboard_response` ögesinden sonra kullanıp aşağıdaki kodu girebilirsiniz:

	[response_time] > 3000

Bir döngünün tekrar edilmesini `inline_script` içerisinde `repeat_cycle` değişkeni aracılığı ile yapabilirsiniz:

	var.repeat_cycle = 1
