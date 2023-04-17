# Bantuan OpenSesame

*Ini adalah halaman bantuan offline. Jika Anda terhubung ke Internet,
Anda dapat menemukan dokumentasi online di <http://osdoc.cogsci.nl>.*

## Pengantar

OpenSesame adalah pembuat eksperimen grafis untuk ilmu sosial. Dengan OpenSesame, Anda dapat dengan mudah membuat eksperimen menggunakan antarmuka grafis berbasis klik. Untuk tugas yang kompleks, OpenSesame mendukung [Python] scripting.

## Memulai

Cara terbaik untuk memulai adalah dengan menjalani tutorial. Tutorial, dan masih banyak lagi, dapat ditemukan secara online:

- <http://osdoc.cogsci.nl/tutorials/>

## Sitasi

Untuk mengutip OpenSesame dalam karya Anda, silakan gunakan referensi berikut:

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: Pembuat eksperimen sumber terbuka, grafis untuk ilmu sosial. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Antarmuka

Antarmuka grafis memiliki komponen berikut. Anda dapat memperoleh
bantuan yang kontekstual dengan mengklik pada ikon bantuan di bagian kanan atas
setiap tab.

- *Menu* (di bagian atas jendela) menampilkan opsi umum, seperti membuka dan menyimpan file, menutup program, dan menampilkan halaman bantuan ini.
- *Bilah alat utama* (tombol besar di bawah menu) menawarkan pilihan opsi yang paling relevan dari menu.
- *Bilah alat item* (tombol besar di sebelah kiri jendela) menampilkan item yang tersedia. Untuk menambahkan item ke eksperimen Anda, seret dari bilah alat item ke area ringkasan.
- *Area ringkasan* (Control + \\) menampilkan ikhtisar berbentuk pohon dari eksperimen Anda.
- *Area tab* berisi tab untuk mengedit item. Jika Anda mengklik item di area ringkasan, tab yang sesuai terbuka di area tab. Bantuan juga ditampilkan di area tab.
- [Kolam file](opensesame://help.pool) (Control + P) menampilkan file yang digabungkan dengan eksperimen Anda.
-   [Pemeriksa variabel](opensesame://help.extension.variable_inspector) (Control + I) menampilkan semua variabel yang terdeteksi.
-   [Jendela debug](opensesame://help.stdout). (Control + D) adalah terminal [IPython]. Semua yang mencetak eksperimen Anda ke output standar (yaitu dengan menggunakan `print()`) ditampilkan di sini.

## Item

Item adalah blok bangunan eksperimen Anda. Sepuluh item inti menyediakan fungsionalitas dasar untuk membuat eksperimen. Untuk menambahkan item ke eksperimen Anda, seret mereka dari item toolbar ke area ringkasan.

- Item [loop](opensesame://help.loop) menjalankan item lain beberapa kali. Anda juga dapat mendefinisikan variabel independen dalam item LOOP.
- Item [sequence](opensesame://help.sequence) menjalankan beberapa item lain secara berurutan.
- Item [sketchpad](opensesame://help.sketchpad) menyajikan rangsangan visual. Alat gambar bawaan memungkinkan Anda untuk dengan mudah membuat tampilan stimulus.
- Item [feedback](opensesame://help.feedback) mirip dengan `sketchpad`, tetapi tidak disiapkan sebelumnya. Oleh karena itu, item FEEDBACK dapat digunakan untuk memberikan umpan balik kepada peserta.
- Item [sampler](opensesame://help.sampler) memutar satu file suara.
- Item [synth](opensesame://help.synth) menghasilkan satu suara.
- Item [keyboard_response](opensesame://help.keyboard_response) mengumpulkan respons penekanan tombol.
- Item [mouse_response](opensesame://help.mouse_response) mengumpulkan respons klik mouse.
- Item [logger](opensesame://help.logger) menulis variabel ke file log.
- Item [inline_script](opensesame://help.inline_script) menyematkan kode Python dalam eksperimen Anda.

Jika diinstal, item-plugin menyediakan fungsionalitas tambahan. Plugin muncul bersama dengan item inti di bilah alat item.

## Menjalankan eksperimen Anda

Anda dapat menjalankan eksperimen Anda dalam:

- Mode layar penuh (*Control+R* atau *Run -> Run fullscreen*)
- Mode Jendela (*Control+W* atau *Run -> Run in window*)
- Mode Quick-Run (*Control+Shift+W* atau *Run -> Quick run*)

Dalam mode quick-run, eksperimen dimulai segera dalam jendela, menggunakan file log `quickrun.csv`, dan nomor subjek 999. Ini berguna selama pengembangan.

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/