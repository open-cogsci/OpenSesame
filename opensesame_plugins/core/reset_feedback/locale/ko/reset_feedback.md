# Reset_feedback

*Tip: 이 플러그인은 0ms의 지속 시간을 가진 FEEDBACK 항목을 제시하는 것과 같은 효과를 갖습니다.*

피드백 변수를 재설정하지 않으면, 작업과 관련이 없는 반응과 피드백이 혼동될 수 있습니다. 예를 들어, 안내 단계 동안의 키 입력이 실험의 첫 번째 블록 동안 피드백에 영향을 줄 수 있습니다. 따라서 적절한 시기에 피드백 변수를 재설정해야 합니다.

이 플러그인은 다음 변수를 0으로 재설정합니다:

- `total_response_time`
- `total_response`
- `acc`
- `accuracy`
- `avg_rt`
- `average_response_time`

자세한 정보는 다음을 참조하십시오:

- <http://osdoc.cogsci.nl/3.2/manual/stimuli/visual/>