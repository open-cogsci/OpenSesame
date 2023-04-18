# Repeat_cycle

このプラグインは、`loop`からサイクルを繰り返すことができます。最も一般的なのは、参加者がミスをしたり、遅すぎた場合に試行を繰り返すことです。

例えば、3000 msより遅い応答があったすべての試行を繰り返すには、（通常は）`keyboard_response`の後に`repeat_cycle`アイテムを追加し、次のようなrepeat-ifステートメントを追加します：

	[response_time] > 3000

また、`inline_script`で変数`repeat_cycle`を1に設定することで、強制的にサイクルを繰り返すこともできます。以下のようにしてください：

	var.repeat_cycle = 1