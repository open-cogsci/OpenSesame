# 重覆週期

呢個插件可以幫你喺`loop`度重覆週期。最普遍嘅情況,就係當參與者出錯或者慢咗嘅時候，會重覆一次試驗。

例如，如果要重覆所有回應時間超過3000毫秒嘅試驗, 你可以喺嗰個（通常係）`keyboard_response`之後加入一個`repeat_cycle`項目，然後加入以下嘅重覆-if陳述：

	[response_time] > 3000

你亦都可以喺`inline_script`度將變數`repeat_cycle`設置為1，以強制重覆一個週期，咁樣：

	var.repeat_cycle = 1