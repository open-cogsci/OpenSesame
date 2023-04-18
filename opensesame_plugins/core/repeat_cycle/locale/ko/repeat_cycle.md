# Repeat_cycle

이 플러그인은 `loop`에서 주기를 반복할 수 있게 해줍니다. 대부분 참가자가 실수했거나 너무 느렸을 때 시행을 반복하는 경우가 일반적입니다.

예를 들어, 응답 시간이 3000ms보다 느렸던 모든 시행을 반복하려면, (일반적으로) `keyboard_response` 다음에 `repeat_cycle` 항목을 추가하고 다음과 같은 반복 조건을 설정할 수 있습니다:

	[response_time] > 3000

또한 `inline_script`에서 변수 `repeat_cycle`을 1로 설정하여 강제로 주기를 반복하도록 설정할 수 있습니다:

	var.repeat_cycle = 1