# Ajuda do OpenSesame

*Esta é a página de ajuda offline. Se você estiver conectado à Internet,
pode encontrar a documentação online em <http://osdoc.cogsci.nl>.*

## Introdução

OpenSesame é um criador gráfico de experimentos para as ciências sociais. Com o OpenSesame, você pode criar experimentos facilmente usando uma interface gráfica de apontar e clicar. Para tarefas complexas, o OpenSesame suporta scripts em [Python].

## Primeiros passos

A melhor maneira de começar é seguindo um tutorial. Tutoriais, e muito mais, podem ser encontrados online:

- <http://osdoc.cogsci.nl/tutorials/>

## Citação

Para citar o OpenSesame em seu trabalho, use a seguinte referência:

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: An open-source, graphical experiment builder for the social sciences. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Interface

A interface gráfica possui os seguintes componentes. Você pode obter
ajuda sensível ao contexto clicando nos ícones de ajuda no canto superior direito de
cada guia.

- O *menu* (na parte superior da janela) mostra opções comuns, como abrir e salvar arquivos, fechar o programa e mostrar esta página de ajuda.
- A *barra de ferramentas principal* (os grandes botões abaixo do menu) oferece uma seleção das opções mais relevantes do menu.
- A *barra de ferramentas de itens* (os grandes botões à esquerda da janela) mostra os itens disponíveis. Para adicionar um item ao seu experimento, arraste-o da barra de ferramentas de itens para a área de visão geral.
- A *área de visão geral* (Control + \\) mostra uma visão geral em forma de árvore do seu experimento.
- A *área de guias* contém as guias para editar itens. Se você clicar em um item na área de visão geral, uma guia correspondente abrirá na área de guias. A ajuda também é exibida na área de guias.
- A [pool de arquivos](opensesame://help.pool) (Control + P) mostra os arquivos que estão agrupados com seu experimento.
- O [inspetor de variáveis](opensesame://help.extension.variable_inspector) (Control + I) mostra todas as variáveis detectadas.
- A [janela de depuração](opensesame://help.stdout). (Control + D) é um terminal [IPython]. Tudo o que seu experimento imprimir na saída padrão (ou seja, usando `print()`) é mostrado aqui.

## Itens

Os itens são os blocos de construção do seu experimento. Dez itens principais fornecem funcionalidades básicas para criar um experimento. Para adicionar itens ao seu experimento, arraste-os da barra de ferramentas de itens para a área de visão geral.

- O item [loop](opensesame://help.loop) executa outro item várias vezes. Você também pode definir variáveis independentes no item LOOP.
- O item [sequence](opensesame://help.sequence) executa vários outros itens em sequência.
- O item [sketchpad](opensesame://help.sketchpad) apresenta estímulos visuais. Ferramentas de desenho integradas permitem criar facilmente displays de estímulos.
- O item [feedback](opensesame://help.feedback) é semelhante ao `sketchpad`, mas não é preparado com antecedência. Portanto, os itens FEEDBACK podem ser usados para fornecer feedback aos participantes.
- O item [sampler](opensesame://help.sampler) toca um único arquivo de som.
- O item [synth](opensesame://help.synth) gera um único som.
- O item [keyboard_response](opensesame://help.keyboard_response) coleta respostas de teclas pressionadas.
- O item [mouse_response](opensesame://help.mouse_response) coleta respostas de cliques do mouse.
- O item [logger](opensesame://help.logger) grava variáveis no arquivo de log.
- O item [inline_script](opensesame://help.inline_script) incorpora o código Python no seu experimento.

Se instalados, os itens de plug-in fornecem funcionalidades adicionais. Os plug-ins aparecem junto aos itens principais na barra de ferramentas de itens.

## Executando seu experimento

Você pode executar seu experimento em:

- Modo de tela cheia (*Control+R* ou *Run -> Run fullscreen*)
- Modo de janela (*Control+W* ou *Run -> Run in window*)
- Modo de execução rápida (*Control+Shift+W* ou *Run -> Quick run*)

No modo de execução rápida, o experimento é iniciado imediatamente em uma janela, usando o arquivo de log `quickrun.csv` e o número de participante 999. Isso é útil durante o desenvolvimento.

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/