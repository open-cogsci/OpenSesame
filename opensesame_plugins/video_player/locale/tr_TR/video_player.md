# Video_player

`video_player` eklentisi bir vidyo dosyası çalıştırır. Bu eklenti sadece resimlerden oluşan vidyo dosyalarını çalıştırır ve arka plan dosyalarını çalıştırmak için `legacy` kullanır. Eğer daha detaylı bir vidyo oynatma fonksiyonu kullanmak isterseniz `media_player_vlc` eklentisini kullanmak isteyebilirsiniz.

Aşağıdaki seçenekleri kullanabilirsiniz:

- *Video file*: Dosya havuzundan bir vidyo dosyası. Platforma göre hangi vidyo formatının desteklendiği değişmekle birlikte en yaygın formatlar (`.avi` ve `.mpeg` gibi)heryerde desteklenir.
- *Resize to fit screen*: vidyonun bütün ekranı kaplaması için yeniden boyutlandırılmasını sağlar. Eğer bu seçenek işaretlenmezse, vidyo ekranın ortasında gösterilir.
- *Duration*: Milisaniye olarak, tuşa basma ya da fare tıklaması olarak girilebilir.
- *Frame duration*: Bu vidyonun yalnızca bir karesinin ne kadar süre gösterileceğini milisaniye olarak gösterir. Maksimum oynatma hızı bilgisayarın hızına göre değişir.
