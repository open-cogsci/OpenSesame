# Pengulangan_siklus

Pengaya ini memungkinkan Anda mengulangi siklus dari `loop`. Biasanya, ini akan digunakan untuk mengulangi percobaan jika peserta membuat kesalahan atau terlalu lambat.

Sebagai contoh, untuk mengulangi semua percobaan di mana respon lebih lambat dari 3000 ms, Anda dapat menambahkan item `repeat_cycle` setelah (biasanya) `keyboard_response` dan tambahkan pernyataan pengulangan- jika berikut:

	[response_time] > 3000

Anda juga dapat memaksa siklus untuk diulang dengan mengatur variabel `repeat_cycle` menjadi 1 dalam `inline_script`, seperti ini:

	var.repeat_cycle = 1