# OpenSesame yardım

*Bu sayfa çevirimdışı yardım sayfasıdır. İnternete bağlı iseniz, çevirimiçi yardım sayfasını linkte bulabilirsiniz <http://osdoc.cogsci.nl>.*

## Giriş

OpenSesame sosyal bilimler için geliştirilmiş görsel bir deney oluşturucu programdır. OpenSesame ile üzerine tıklamalı grafik arayüzü ile hızlıca deney oluşturabilirsiniz. OpenSesame'de kompleks görevler için [Python] programlama dilini desteklemektedir.

## Başlayalım

Başlamak için en iyi yöntem öğreticiyi kullanmaktır. Öğretici ve daha fazlası çevirimiçi olarak bulunabilir:

- <http://osdoc.cogsci.nl/tutorials/>

## Alıntılama

OpenSesame'yi çalışmanızda kullandığınızda için aşağıdaki çalışmayı referans olarak gösteriniz:

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: An open-source, graphical experiment builder for the social sciences. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Kullanıcı arayüzü

Grafik arayüzü aşağıdaki bileşenleri içerir. İçerikle alakalı yardım almak için her bir sekmenin sağ üst köşesinde bulunan yardım simgelerine başvurabilirsiniz.

- *menü* (pencerenin en üstünde) açma, dosya kaydetme, programı kapatma ya da yardım sayfası gibi genel seçenekleri gösterir.
- *ana araç çubuğu* (menünün altındaki büyük butonlar) menüdeki en alakalı seçenekleri sunar.
- *öge araç çubuğu* (sol penceredeki büyük butonlar) kullanılabilir ögeleri gösterir. Deneyinize bir öge eklemek için öge araç çubuğundan bir ögeyi genel bakış bölümüne sürükleyin.
- *genel bakış bölümü* (Control + \\) deneyinizin bir ağaç gibi genel taslağını gösterir
- *sekme bölgesi* ögeleri düzenlemek için sekmeleri içerir. Genel bakış bölümünden bir ögeye tıklarsanız, bu öge bir sekme olarak açılır. Yardım sayfası da sekmelerde gösterilir.
- [dosya havuzu](opensesame://help.pool) (Control + P) deneyinize entegre edilmiş dosyaları gösterir.
- [değişken denetleyicisi](opensesame://help.extension.variable_inspector) (Control + I) saptanan bütün değişkenleri gösterir.
- [hata ayıklama penceresi](opensesame://help.stdout). (Control + D) bir [IPython] terminaldir. Deneyinizin standart bir çıktıya yazdığı herşey (örneğin `print()` komutu ile) burada görülebilir.

##Ögeler

Ögeler deneyinizin yapı taşlarıdır. 10 öz öge deneyinizi oluşturmadaki basit fonksiyonları sağlar. Deneyinize öge eklemek için, öge araç çubuğundan genel bakış alanına istediğiniz ögeyi sürükleyiniz.

- [loop](opensesame://help.loop) ögesi başka ögeleri çoklu çalıştırmanızı sağler. Bağımsız değişkenlerinizi LOOP ögesi içinde tanımlayabilirsiniz.
- [sequence](opensesame://help.sequence) ögesi başka çok ögelerinizi sıralı olarak çalıştırmanızı sağlar.
- [sketchpad](opensesame://help.sketchpad) ögesi görsel uyarıcıları gösterir. Gömülü olan çizim araçları uyarıcılarını kolayca hazırlamanızı sağlar.
- [feedback](opensesame://help.feedback) bu öge `sketchpad` ögesine benzer. Ancak bu öge işin başında hazırlanmaz. Bu nedenle FEEDBACK ögeleri geri bildirim vermek için kullanılabilir.
- [sampler](opensesame://help.sampler) ögesi bir adet ses dosyası çalıştırır.
- [synth](opensesame://help.synth) ögesi bir ses oluşturur.
- [keyboard_response](opensesame://help.keyboard_response) ögesi klavye girdilerini toplar.
- [mouse_response](opensesame://help.mouse_response) ögesi fare girdilerini toplar.
- [logger](opensesame://help.logger) ögesi kayıt dosyasına değişkenleri kaydeder.
- [inline_script](opensesame://help.inline_script) ögesi deneyinize Python kodu gömer.

Eklenti ögeler yüklendiği takdirde ek fonksiyonlar sağlar. Eklentiler, öz ögelerin altında yer alır.
## Deneyinizi çalıştırın

Deneyinizi aşağıdaki seçeneklerde çalıştırabilirsiniz:

- Tam ekran modu(*Control+R* ya da *Run -> Run fullscreen*)
- Pencere modu (*Control+W* ya da *Run -> Run in window*)
- Hızlı çalıştır (*Control+Shift+W* ya da *Run -> Quick run*)

Hızlı çalıştır modunda deney `quickrun.csv` kayıt dosyasını 999 katılımcı numarası ile pencere modunda çalıştırır. Bu özellik deneyinizi geliştirirken kullanışlıdır.

Otomatik tepki (auto-response) modu (*Run -> Enable auto-response*) etkin olduğunda OpenSesame klavye ve fare girdilerini taklit eder. Bu fonksiyon da deneyinizi geliştirirken kullanışlıdır.

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/
