# 重复周期

此插件允许您从`loop`重复周期。最常见的情况是当参与者犯错或反应过慢时重复试验。

例如，要重复所有响应时间超过3000毫秒的试验，您可以在（通常）`keyboard_response`之后添加一个`repeat_cycle`项目，并添加以下重复条件语句：

	[response_time] > 3000

您还可以通过在`inline_script`中将变量`repeat_cycle`设置为1来强制重复一个周期，如下所示：

	var.repeat_cycle = 1