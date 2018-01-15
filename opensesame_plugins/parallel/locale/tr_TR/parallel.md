# Parallel

paralel eklentisi birden fazla ögeyi aynı anda çalıştırmanızı sağlar, örneğin paralel olarak. Dinamik bir uyarıcı gösterip katılımcılardan aynı anda tepki/yanıt alıp bunu kaydetmek istediğinizde bu yöntem kullanışlıdır.

**Not:** Bazı sistemlerde iş parçacıkları (threads) klavye girdilerini kabul etmez. parallel eklentisindeki ilk öge genel işlem olarak çalıştırılır. Bu nedenle, ögeleriniz tuşa basılması sonucunda ekranda görünmüyorsa, klavye tepkilerini/yanıtlarını parallel'in içinde ilk öge olarak koymayı deneyin.
