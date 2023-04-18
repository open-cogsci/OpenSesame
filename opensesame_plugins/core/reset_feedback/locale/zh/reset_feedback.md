# 重置反馈

*提示：此插件的效果与呈现一个持续时间为 0 毫秒的 FEEDBACK 项目相同。*

如果您不重置反馈变量，可能会将您的反馈与与任务无关的响应混淆。例如，指导阶段期间所做的按键操作可能会影响实验的第一个区块中的反馈。因此，您需要在适当的时刻重置反馈变量。

此插件将将以下变量重置为0：

- `total_response_time`
- `total_response`
- `acc`
- `accuracy`
- `avg_rt`
- `average_response_time`

更多信息，请查看：

- <http://osdoc.cogsci.nl/3.2/manual/stimuli/visual/>