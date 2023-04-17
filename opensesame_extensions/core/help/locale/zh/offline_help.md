# OpenSesame 帮助

*这是离线帮助页面。如果您连接到互联网，可以在 <http://osdoc.cogsci.nl> 上找到在线文档。*

## 简介

OpenSesame 是一款用于社会科学领域的图形实验构建器。使用 OpenSesame，您可以通过直观的点选式图形界面轻松创建实验。对于复杂数任务，OpenSesame 支持 [Python] 脚本编程。

## 入门

最好的入门方法是通过一个教程入手。对于教程以及其他内容，可以在此处找到：

- <http://osdoc.cogsci.nl/tutorials/>

## 引用

在您的工作中引用 OpenSesame，请使用如下参考：

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: An open-source, graphical experiment builder for the social sciences. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## 接口

图形界面包含以下组件。您可以通过点击每个选项卡右上角的帮助图标获取上下文相关的帮助。

- *菜单*（窗口顶部）显示常用选项，如打开和保存文件、关闭程序和显示此帮助页面。
- *主工具栏*（菜单下方的大按钮）提供了菜单中最相关的选项。
- *项目工具栏*（窗口左侧的大按钮）显示可用的项目。要将项目添加到实验中，请从项目工具栏拖动到概览区域。
- *概览区域*（Control + \\）显示实验的树状概览。
- *选项卡区域* 包含用于编辑项目的选项卡。如果在概览区域单击项目，则在选项卡区域中打开相应的选项卡。帮助也显示在选项卡区域。
- [文件池](opensesame://help.pool)（Control + P）显示与实验捆绑在一起的文件。
-   [变量检查器](opensesame://help.extension.variable_inspector)（Control + I）显示所有检测到的变量。
-   [调试窗口](opensesame://help.stdout)（Control + D）是一个 [IPython] 终端。实验打印到标准输出的所有内容（即使用 `print()`）都将显示在此。

## 项目

项目是构建实验的基础部分。十个核心项目提供了创建实验的基本功能。要将项目添加到实验，请将它们从项目工具栏拖动到概览区域。

- [循环](opensesame://help.loop) 项目多次运行另一个项目。您也可以在 LOOP 项目中定义自变量。
- [序列](opensesame://help.sequence) 项目按顺序运行多个其他项目。
- [草图板](opensesame://help.sketchpad) 项目呈现视觉刺激。内置绘图工具可让您轻松创建刺激显示。
- [反馈](opensesame://help.feedback) 项目类似于 `草图板`，但不是预先准备的。因此，FEEDBACK 项目可以用于向参与者提供反馈。
- [采样器](opensesame://help.sampler) 项目播放单个声音文件。
- [合成器](opensesame://help.synth) 项目生成单个声音。
- [键盘响应](opensesame://help.keyboard_response) 项目收集按键响应。
- [鼠标响应](opensesame://help.mouse_response) 项目收集鼠标点击响应。
- [记录器](opensesame://help.logger) 项目将变量写入日志文件。
- [内联脚本](opensesame://help.inline_script) 项目将 Python 代码嵌入实验中。

如果已安装，插件项目可以提供额外功能。插件会与核心项目一起出现在项目工具栏中。

## 运行实验

您可以在以下模式下运行实验：

- 全屏模式（*Control+R* 或 *运行 -> 全屏运行*）
- 窗口模式（*Control+W* 或 *运行 -> 窗口中运行*）
- 快速运行模式（*Control+Shift+W* 或 *运行 -> 快速运行*）

在快速运行模式下，实验立即以窗口的形式启动，使用日志文件 `quickrun.csv` 和主题编号 999。这在开发过程中非常有用。

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/