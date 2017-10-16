# External_script

`external_script` deneyinize Python kodu eklemek için alternatif bir yöntemdir. `inline_script` Python kodlarını direkt olarak girmenize izin verirken, `external_script` ögesi Python kodlarını bir komut dizisi dosyasından çalıştır.

## Seçenekler

- *Script file* Python kodlarının okunacağı dosyayı seçmenizi sağlar.
- *Prepare function in script* hazırlanma evresinde python komut dizisinden çağrılacak olan fonksiyonun adıdır.
- *Run function in script* çalıştırma evresinde python komut dizisinden çalıştırılacak fonksiyonu seçer.

## Komut dizisi çalıştırma ve Python çalışma alanı

Komut dizisi `inline_script` ögeleri için kullanılan Python çalışma alanında kullanılır. Bu nedenle olagan nesneleri, fonksiyonları aynı `inline_script` te kullandığınız gibi kullanabilirsiniz.

Eklenti başlatıldığında, kullanılan Python komut dizisi dosyasını çalıştırır.

## Örnek

Aşağıdaki komut dizisinde, sizin çalıştırma fonksiyonu olarak  `prepare` ve `run` komutlarını kullandığınızı düşünelim:

~~~ .python
print('This will be shown when the plug-in is initialized')

def prepare():

    print('This will be shown during the prepare phase')
    global c
    c = canvas()
    c.fixdot()

def run():

    print('This will be shown during the run phase')
    global c
    c.show()
    clock.sleep(1000)
    c.clear()
    c.show()
~~~
