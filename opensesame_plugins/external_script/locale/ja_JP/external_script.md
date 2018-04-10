# External_script: 外部スクリプト

`external_script (外部スクリプト)` アイテムはあなたの実験でPythonスクリプトを実行するもう一つの方法です。`inline_script (インラインスクリプト)` では直接Pythonコードを入力するのに対して、`external_script (外部スクリプト)` ではPythonのスクリプトを外部ファイルから読み込みます。

## オプション

- *Script file (スクリプトファイル)* は実行されるPythonスクリプトのファイル名です。
- *Prepare function in script (事前読み込み関数)* ではスクリプトに記入されている関数をprepare phase(事前フェーズ)で読み込むことができます。(引数は渡されません)
- *Run function in script (スクリプトで関数を実行)* 実行フェーズ中に(引数なしで)呼び出されるスクリプト内の関数の名前です。

## スクリプトの実行とPythonのワークスペース

読み込まれたスクリプトは、`inline_script (インラインスクリプト)`アイテムに使用されるのと同じPythonワークスペースで実行されます。 つまり、`inline_script (インラインスクリプト)`と同様に、すべてのオブジェクトや関数にアクセスするできます。

最初のprepare phase(事前フェーズ)中にプラグインが初期化されると、スクリプト全体が実行されます。

## 例

実行する関数に`prepare`と`run`を使うと仮定して、次のスクリプトを考えてみましょう:

~~~ .python
print('This will be shown when the plug-in is initialized')

def prepare():

    print('This will be shown during the prepare phase')
    global c
    c = Canvas()
    c.fixdot()

def run():

    print('This will be shown during the run phase')
    global c
    c.show()
    clock.sleep(1000)
    c.clear()
    c.show()
~~~
