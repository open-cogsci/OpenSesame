# OpenSesame yardım

*Bu çevrimdışı yardım sayfasıdır. İnternete bağlıysanız,
<http://osdoc.cogsci.nl> adresindeki çevrimiçi belgelere ulaşabilirsiniz.*

## Giriş

OpenSesame, sosyal bilimler için grafiksel bir deney oluşturucudur. OpenSesame ile nokta ve tıkla grafiksel arayüz kullanarak kolayca deneyler oluşturabilirsiniz. Karmaşık görevler için OpenSesame, [Python] betiği desteği sunar.

## Başlangıç

Başlamak için en iyi yol, bir öğretici üzerinde çalışmaktır. Öğreticiler ve daha fazlası çevrimiçi olarak bulunabilir:

- <http://osdoc.cogsci.nl/tutorials/>

## Alıntı

OpenSesame'yi çalışmanızda alıntılamak için lütfen aşağıdaki referansı kullanın:

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: Sosyal bilimler için açık kaynaklı, grafiksel bir deney yapılandırıcı. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Arayüz

Grafiksel arayüz aşağıdaki bileşenlere sahiptir. Her sekmenin sağ üst kısmındaki yardım simgelerine tıklayarak
bağlam duyarlı yardım alabilirsiniz.

- *Menü* (pencerenin üst kısmında) dosyaları açma, kaydetme, programı kapatma ve bu yardım sayfasını gösterme gibi ortak seçenekleri gösterir.
- *Ana araç çubuğu* (menünün hemen altındaki büyük düğmeler) menüden en alakalı seçeneklerin bir kısmını sunar.
- *Öğe araç çubuğu* (pencerenin solundaki büyük düğmeler) mevcut öğeleri gösterir. Deneyinize bir öğe eklemek için, öğeyi öğe araç çubuğundan genel bakış alanına sürükleyin.
- *Genel bakış alanı* (Control + \\) deneyinize ağaç benzeri bir genel bakış sunar.
- *Sekme alanı* öğeleri düzenleme sekmelerini içerir. Genel bakış alanında bir öğeye tıklarsanız, sekme alanında ilgili sekme açılır. Yardım da sekme alanında görüntülenir.
- [Dosya havuzu](opensesame://help.pool) (Control + P) deneyinizle birlikte olan dosyaları gösterir.
-   [Değişken denetçisi](opensesame://help.extension.variable_inspector) (Control + I) tespit edilen tüm değişkenleri gösterir.
-   [Hata ayıklama penceresi](opensesame://help.stdout) (Control + D) bir [IPython] terminalidir. Deneyinizin standart çıktısına yazdığı her şey (yani `print()` kullanarak) burada görüntülenir.

## Öğeler

Öğeler, deneyinizin yapı taşlarıdır. On temel öğe, bir deney oluşturmak için temel işlevselliği sağlar. Deneyinize öğeler eklemek için, öğe araç çubuğundaki öğeleri genel bakış alanına sürükleyin.

- [Döngü](opensesame://help.loop) öğesi, başka bir öğeyi birden fazla kez çalıştırır. Ayrıca, bağımsız değişkenleri DÖNGÜ öğesinde tanımlayabilirsiniz.
- [Dizi](opensesame://help.sequence) öğesi, diğer birçok öğeyi sırayla çalıştırır.
- [Sketchpad](opensesame://help.sketchpad) öğesi görsel uyarıcıları sunar. Dahili çizim araçları, uyarıcı ekranlarını kolayca oluşturmanızı sağlar.
- [Geribildirim](opensesame://help.feedback) öğesi, `sketchpad` gibi olsa da, önceden hazırlanmamıştır. Bu nedenle, GERİBİLDİRİM öğeleri katılımcılara geribildirim sağlamak için kullanılabilir.
- [Sampler](opensesame://help.sampler) öğesi tek bir ses dosyasını oynatır.
- [Synth](opensesame://help.synth) öğesi tek bir ses üretir.
- [T_IDtkanuşma_yanıt](opensesame://help.keyboard_response) öğesi tuş basma yanıtlarını toplar.
- [Mouse_response](opensesame://help.mouse_response) öğesi fare tıklama yanıtlarını toplar.
- [Logger](opensesame://help.logger) öğesi değişkenleri log dosyasına yazar.
- [Inline_script](opensesame://help.inline_script) deneyinize Python kodu yerleştirir.

Yüklüyse, eklenti öğeleri ek işlevsellik sağlar. Eklentiler, öğe araç çubuğunda ana öğelerle birlikte görünür.

## Deneyinizi çalıştırma

Deneyinizi şu şekillerde çalıştırabilirsiniz:

- Tam ekran modu (*Control+R* veya *Çalıştır -> Tam ekranda çalıştır*)
- Pencere modu (*Control+W* veya *Çalıştır -> Pencerede çalıştır*)
- Hızlı çalıştırma modu (*Control+Shift+W* veya *Çalıştır -> Hızlı çalıştır*)

Hızlı çalıştırma modunda, deney hemen pencerede başlar, `quickrun.csv` log dosyasını kullanır ve 999 numaralı denek numarasıyla çalışır. Bu, geliştirme sırasında kullanışlıdır.

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/