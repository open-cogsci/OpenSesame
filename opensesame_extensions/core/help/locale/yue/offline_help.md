# OpenSesame 説明

*這是離線説明頁。如果您已連接互聯網，可以在 <http://osdoc.cogsci.nl> 找到在線文檔。*

## 介紹

OpenSesame 是一個為社會科學專門設計的圖形實驗構建器。用 OpenSesame，您可以通過點擊和拖動的圖形界面輕鬆創建實驗。對於複雜的任務，OpenSesame 支持 [Python] 腳本編程。

## 入門

最好的入門方法是閲讀教程。許多教程以及其他資源都可以在線找到:

- <http://osdoc.cogsci.nl/tutorials/>

## 引用

要在您的工作中引用 OpenSesame，請使用以下參考資料:

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: An open-source, graphical experiment builder for the social sciences. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## 界面

圖形界面包括以下組件。您可以通過單擊每個標籤上部右側的説明圖示來獲得與上下文相關的幫助。

- *菜單*（窗口頂部）顯示常用選項，如打開和保存文件、關閉程序以及顯示此説明頁等；
- *主工具欄*（菜單下方的大按鈕）提供了菜單中的部分常用選項；
- *項目工具欄*（窗口左側的大按鈕）顯示可用項目。要向您的實驗添加項目，請將其從項目工具欄拖到概覽區域；
- *概覽區域*（Control + \\）顯示實驗的樹狀概覽；
- *標籤區域*包含了用於編輯項目的標籤。如果您單擊概覽區域中的某個項目，標籤區域中會打開相應的標籤。在此區域也可顯示説明；
- [文件池](opensesame://help.pool)（Control + P）顯示與您的實驗捆綁在一起的文件；
- [變量檢查器](opensesame://help.extension.variable_inspector)（Control + I）顯示所有檢測到的變量;
- [調試窗口](opensesame://help.stdout) (Control + D) 是一個 [IPython] 終端。您的實驗輸出到標准輸出（如使用 `print()`）的所有內容均顯示在此處。

## 項目

項目是您實驗的構建部件。十個核心項目為創建實驗提供了基本功能。要向您的實驗添加項目，請將它們從項目工具欄拖到概覽區域。

- [loop](opensesame://help.loop) 項目多次運行另一個項目。您還可以在 LOOP 項目中定義獨立變量。
- [sequence](opensesame://help.sequence) 項目依次運行多個其他項目。
- [sketchpad](opensesame://help.sketchpad) 項目呈現視覺刺激。內置的繪圖工具使您可以輕鬆創建刺激顯示。
- [feedback](opensesame://help.feedback) 項目與 `sketchpad` 類似，但未提前準備。因此，FEEDBACK 項目可用於向參與者提供反饋。
- [sampler](opensesame://help.sampler) 項目播放單個聲音文件。
- [synth](opensesame://help.synth) 項目產生單個聲音。
- [keyboard_response](opensesame://help.keyboard_response) 項目收集按鍵響應。
- [mouse_response](opensesame://help.mouse_response) 項目收集鼠標單擊響應。
- [logger](opensesame://help.logger) 項目將變量寫入日誌文件。
- [inline_script](opensesame://help.inline_script) 將 Python 代碼嵌入到您的實驗中。

如果安裝了插件項目，它們將提供其他功能。插件將與核心項目一起顯示在項目工具欄中。

## 運行實驗

您可以在以下模式下運行實驗：

- 全屏模式（*Control+R* 或 *運行->全屏運行*）
- 窗口模式（*Control+W* 或 *運行->窗口運行*）
- 快速運行模式（*Control+Shift+W* 或 *運行->快速運行*）

在快速運行模式下，實驗將立即在窗口中使用日誌文件 `quickrun.csv` 和主題號999啟動。這在開發過程中非常有用。

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/