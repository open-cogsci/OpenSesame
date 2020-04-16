# Advanced_delay 插件

`advanced_delay` 插件将实验延迟。延迟时间为一个指定的平均时长加上一个随机变化幅度。

- *时长* 为延迟的平均时长（毫秒）。
- *Jitter* 为延迟的变化幅度（毫秒）。
- *Jitter模式* 为jitter的计算方式：
	- *Standard deviation* （标准差） 从以jitter为标准差的高斯分布中得出延迟的变化幅度。
	- *Uniform* （标准）从标准分布中得出变化幅度。
