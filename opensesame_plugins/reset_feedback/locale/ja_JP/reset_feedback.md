# Reset_feedback: フィードバック初期化

*ヒント: このプラグインはfeedback(フィードバック)アイテムを 0ms 呈示した際と同じ効果があります。*

フィードバック値を初期化しない場合、タスクに関連しない応答でフィードバックを混乱させる可能性があります。 例えば、実験説明フェーズ中に行われたキー押下は、実験の最初のブロックのフィードバックに影響を与える可能性があります。 したがって、適切なタイミングでフィードバック変数をリセットする必要があります。

このプラグインは以下の変数を0にします:

- `total_response_time`
- `total_response`
- `acc`
- `accuracy`
- `avg_rt`
- `average_response_time`

さらに詳しくはこちらをご覧ください:

- <http://osdoc.cogsci.nl/3.2/manual/stimuli/visual/>
