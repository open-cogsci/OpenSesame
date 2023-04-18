# Advanced_delay

`advanced_delay` 插件使实验延迟预设的平均持续时间加上一个随机幅度。

- *Duration* 是延迟的平均持续时间，单位为毫秒。
- *Jitter* 是延迟变化的大小，单位为毫秒。
- *Jitter mode* 是计算抖动的方式：
	- *Standard deviation* 将从具有Jitter标准差的高斯分布中抽取变化。
	- *Uniform* 将从均匀分布中抽取持续时间的变化。