# Reset_feedback （重置反馈）插件

*提示: 此插件与持续时间为0毫秒的feedback（反馈）项有相同的效果.*

若不重置反馈变量，你可能会将反馈和与任务无关的反应混淆。比如，被试在（实验正式开始前的）指导语阶段按下的键可能会影响
实验的第一部分。因此，你需要适时重置反馈变量。

这个插件会将以下变量重置为0:

- `total_response_time`
- `total_response`
- `acc`
- `accuracy`
- `avg_rt`
- `average_response_time`

更多信息请查看:

- <http://osdoc.cogsci.nl/3.2/manual/stimuli/visual/>
