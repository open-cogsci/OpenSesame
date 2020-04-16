# OpenSesame 帮助

*这是一个离线帮助页面。如果你已连接网络，可以在这里找到更多相关文件： <http://osdoc.cogsci.nl>.*

## 简介

OpenSesame是一个针对社会科学实验，提供图形化搭建实验的平台。在OpenSesame上，你可以用点击式的图形化交互界面轻松创建实验。针对复杂实验，OpenSesame支持 [Python] 脚本。

## 开始吧

开始使用OpenSesame最简单有效的方式是教程。教程和更多实用功能可以在这里找到：

- <http://osdoc.cogsci.nl/tutorials/>

## 引用

若在论文中引用OpenSesame，请引用：

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: An open-source, graphical experiment builder for the social sciences. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## 交互界面

图形化交互界面有以下组成元素。点击右上方帮助图标获取上下文相关的帮助。

- *菜单* （在窗口最上端） 显示通用选项，如打开、保存文档，关闭软件，或显示帮助页面。
- *主工具栏* （菜单下方的图标按钮） 提供了从菜单中筛选出的几个最相关和实用的选项。
- *项目工具栏* (窗口左端的图标按钮) 显示可用项目。将项目从*项目工具栏*拖到*概览区*，以将该项目用于你的实验。
- *概览区* (Control + \\) 显示实验的树状概览。
- *标签页区域* 包含编辑各项目的标签页. 若点击概览区的项目，对应的标签页则会在这个区域打开。帮助也会在标签页区域中显示。
- [文件池](opensesame://help.pool) (Control + P) 显示与你的实验绑定在一起的文件。
- [变量检索器](opensesame://help.extension.variable_inspector) (Control + I) 显示所有检测到的变量。
- [debug窗口](opensesame://help.stdout). (Control + D) 是一个[IPython]终端。实验(用 `print()`)列出到标准输出的所有内容都会显示在这里。

## 项目

项目是用于构建实验的基础元素，其中有十个主要项目为创建新实验的基本功能。将你需要的项目从左边的项目工具栏拖到概览区，以将它们添加到你的实验。

- [loop](opensesame://help.loop) 允许其他项目运行多次。你也可以在loop中定义自变量。
- [sequence](opensesame://help.sequence) 按顺序运行其他多个项目。
- [sketchpad](opensesame://help.sketchpad) 显示视觉刺激。 内置绘图工具允许您轻松创建实验中需要的视觉刺激。
- [feedback](opensesame://help.feedback) 与 `sketchpad`相似，但无内置工具。FEEDBACK可用于提供被试反馈。
- [sampler](opensesame://help.sampler) 播放单个声音文件。
- [synth](opensesame://help.synth) 创建声音文件。
- [keyboard_response](opensesame://help.keyboard_response) 收集键盘反应。

- [mouse_response](opensesame://help.mouse_response) 收集鼠标反应。
- [logger](opensesame://help.logger) 将变量记录到日志文件中。
- [inline_script](opensesame://help.inline_script) 在实验中嵌入Python代码。

如果你安装了插件，这些插件项将提供附加功能。插件会出现在项目工具栏的核心项目旁边。


## 运行实验

你可以用以下模式运行实验:

- 全屏模式 (*Control+R* 或 *运行 -> 全屏运行*)
- 窗口模式 (*Control+W* 或 *运行 -> 在窗口中运行*)
- 快速运行模式 (*Control+Shift+W* or *运行 -> 快速运行*)

在快速运行模式中，实验会在窗口中开始，并保存在日志文件 `quickrun.csv`中, 被试编号（subject_nr）为999。

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/
