# Gelişmiş_gecikme

`gelişmiş_gecikme` eklentisi, deneyi önceden belirlenmiş ortalama süre ve rastgele bir marj ekleyerek geciktirir.

- *Süre*, gecikmenin milisaniye cinsinden ortalama süresidir.
- *Titreşim*, gecikmedeki değişimin milisaniye cinsindendir.
- *Titreşim modu*, titreşimin nasıl hesaplandığıdır:
	- *Standart sapma*, Titreşimi standart sapma olarak kullanan Gaussian dağılımından varyasyon çeker.
	- *Düzgün*, süre varyasyonunu düzgün bir dağılımdan çeker.