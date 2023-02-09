# repeat cycle 插件

这个插件允许您在 `loop` 中重复循环。最常用于的情境是，当被试反应错误或太慢时，重复当前测试。

比如，要重复所有反应速度超过3000毫秒的测试，（通常）可以在 `keyboard_response`后面添加项目 `repeat_cycle` ，并加入以下repeat-if语句：

	[response_time] > 3000

你也可以通过在 `inline_script` 中将变量 `repeat_cycle`设置为1来强制重复循环，比如：

	var.repeat_cycle = 1
