# 重設回饋

*提示：此插件的效果與呈現持續時間為 0 毫秒的 FEEDBACK 項相同。*

如果您不重置回饋變量，則可能將您的反饋與與任務無關的響應混淆。 例如，在操作說明階段中進行的按鍵操作可能會影響到實驗的第一個阻塊期間的回饋。 因此，您需要在適當的時刻重置回饋變量。

此插件將以下變量重置為0：

- `total_response_time`
- `total_response`
- `acc`
- `accuracy`
- `avg_rt`
- `average_response_time`

更多資訊，請參見：

- <http://osdoc.cogsci.nl/3.2/manual/stimuli/visual/>