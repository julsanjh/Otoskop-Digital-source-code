# Sistem Otoskop Medis V3

Sistem antarmuka pengguna (*User Interface*) berbasis Kiosk-Mode untuk otoskop digital. Perangkat lunak ini dirancang untuk berjalan di lingkungan Linux (seperti pada Raspberry Pi) dan dioptimalkan untuk perangkat keras dengan sumber daya terbatas. Proyek ini dikembangkan di program studi Teknologi Kedokteran ITS sebagai bagian dari pengembangan instrumentasi medis.

## Fitur Utama

- **Layar Pemuatan Interaktif**: Menampilkan status inisialisasi kernel, modul sensor, dan antarmuka X11 saat sistem dinyalakan[cite: 2, 3].
- **Dasbor Menu Utama**: Antarmuka kontrol terpusat yang menampilkan status sistem, jam waktu nyata, dan metrik jumlah total foto observasi.
- **Kamera Medis Latensi Rendah**: Menggunakan mesin grafis `mpv` untuk menayangkan *feed* kamera `v4l2` (`/dev/video0`) tanpa *delay*, dilengkapi dengan fitur tangkapan layar dan kontrol *zoom* digital[cite: 1].
- **Galeri Observasi**: Integrasi mulus dengan `feh` untuk meninjau gambar medis yang telah diambil secara layar penuh[cite: 4].
- **Navigasi Perangkat Keras**: Antarmuka sepenuhnya dikendalikan menggunakan *keyboard* atau tombol fisik mikrokontroler (Tombol Atas, Bawah, dan Enter), menghilangkan kebutuhan akan *mouse*[cite: 1, 4].

## Struktur Direktori

- `start_medis.sh`: Skrip *entry point* yang bertugas mengonfigurasi keamanan X11, mematikan fungsi *screensaver*, memanggil *window manager* `openbox`, dan meluncurkan urutan antarmuka Python[cite: 3].
- `loading_medis.py`: Skrip Tkinter yang mensimulasikan layar *loading* perangkat keras sebelum masuk ke menu utama[cite: 2, 3].
- `ui_medis.py`: Program menu utama sistem yang mengelola navigasi antar mode (Kamera, Galeri, Hapus Data, dan Kontrol Daya)[cite: 3, 4].
- `kamera_medis.py`: Skrip pengendali jendela kamera yang menyatukan *frame* video `mpv` dengan panel kontrol medis di sebelah kanan menggunakan teknik injeksi *Window ID*[cite: 1, 4].

## Persyaratan Sistem (Dependencies)

Pastikan dependensi berikut terpasang di sistem operasi Linux yang digunakan:
- `python3-tk`: Pustaka antarmuka grafis Tkinter.
- `mpv`: Pemutar media untuk *rendering* video latensi rendah dari sensor kamera[cite: 1].
- `socat`: Untuk mengirimkan perintah IPC (Inter-Process Communication) ke *socket* `mpv`[cite: 1].
- `feh`: Penampil gambar ringan yang digunakan untuk membuka galeri foto[cite: 4].
- `openbox`: *Window manager* ringan untuk mengatur jendela layar penuh tanpa desktop *environment* yang berat[cite: 3].

## Instalasi & Penggunaan

1. Kloning repositori ini ke dalam direktori perangkat (disarankan di jalur yang sesuai dengan konfigurasi skrip, misalnya direktori *home* pengguna).
2. Pastikan izin eksekusi diberikan pada *bash script*:
   ```bash
   chmod +x start_medis.sh
