# Sıfırlama_geribildirimi

*İpucu: Bu eklentinin etkisi, 0 ms süreli bir GERİBİLDİRİM öğesi sunmakla aynıdır.*

Geribildirim değişkenlerini sıfırlamazsanız, geri bildiriminizi görevle ilgisi olmayan yanıtlarla karıştırabilirsiniz. Örneğin, talimat aşamasındaki tuş basmaları deneyin ilk bloğundaki geribildirimi etkileyebilir. Bu nedenle, geribildirim değişkenlerini uygun anlarda sıfırlamanız gerekmektedir.

Bu eklenti, aşağıdaki değişkenleri 0'a sıfırlayacaktır:

- `total_response_time`
- `total_response`
- `acc`
- `accuracy`
- `avg_rt`
- `average_response_time`

Daha fazla bilgi için bkz:

- <http://osdoc.cogsci.nl/3.2/manual/stimuli/visual/>