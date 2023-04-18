# Advanced_delay

Pengaya `advanced_delay` menunda eksperimen selama durasi rata-rata yang ditentukan sebelumnya ditambah margin acak.

- *Duration* adalah durasi rata-rata penundaan dalam milidetik.
- *Jitter* adalah besaran variasi penundaan dalam milidetik.
- *Jitter mode* adalah cara menghitung jitter:
	- *Standard deviation* akan mengambil variasi dari distribusi Gaussian dengan Jitter sebagai deviasi standar.
	- *Uniform* akan mengambil variasi durasi dari distribusi seragam.