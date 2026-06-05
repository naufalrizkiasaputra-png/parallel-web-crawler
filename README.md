# LAPORAN DAN DOKUMENTASI UTAMA PROYEK
## IMPLEMENTASI ARSITEKTUR PARALLEL PIPELINE PADA SISTEM WEB CRAWLER DAN TEXT PROCESSING

---

## 👤 1. IDENTITAS MAHASISWA
* **Nama Lengkap** : [Naufal Rizkia Saputra]
* **NRP** : [15-2024-050]
* **Kelas** : [CC]
* **Mata Kuliah** : IFB 206 Komputasi Paralel
* **Program Studi** : Informatika
* **Fakultas** : Teknologi Industri
* **Institusi** : Institut Teknologi Nasional (Itenas) Bandung
* **Dosen Pengampu** : Lisa Kristiana Ph.D

---

## 📌 2. PENGANTAR DAN LATAR BELAKANG PROYEK

Pada era pemrosesan data berskala besar (*Big Data Analytics*), efisiensi waktu eksekusi penambangan data menjadi salah satu tolak ukur utama keberhasilan sebuah sistem. Dua aktivitas yang paling sering dilakukan dalam *Data Engineering* adalah:
1. **Web Crawling / Scraping**: Mengunduh halaman web secara massal.
2. **Text Processing / Mining**: Membersihkan teks dan menganalisis kandungan kata di dalamnya.

Namun, jika kedua proses di atas digabungkan dan dieksekusi menggunakan pendekatan **Sekuensial (Berurutan)**, performa sistem akan menurun drastis (*performance degradation*). Hal ini disebabkan oleh dua jenis bottleneck utama:

### A. I/O Bound Bottleneck (Latensi Jaringan)
Saat melakukan *crawling*, program mengirimkan permintaan HTTP ke server target dan harus menunggu respons paket data kembali melalui jaringan internet. Pada model sekuensial, CPU laptop akan berada dalam kondisi *idle* (menganggur/menunggu) selama ratusan milidetik. Waktu tunggu ini membuang-buang daya komputasi yang berharga.

### B. CPU Bound Bottleneck (Komputasi Intensif)
Setelah dokumen HTML berhasil diunduh, sistem harus melakukan operasi string yang berat, seperti membuang tag-tag HTML, menghilangkan karakter khusus (*noise removal*), melakukan tokenisasi, hingga menghitung frekuensi kata tunggal. Proses ini menguras daya kerja satu *core* CPU secara terus-menerus.

### Solusi: Pipeline Paralelisme
Untuk memecahkan masalah ini, proyek ini mengimplementasikan konsep **Pipeline Paralelisme**. Dengan memecah rangkaian pekerjaan menjadi 3 tahapan independen (*isolated stages*) yang berjalan secara simultan pada *core* prosesor yang berbeda, kita dapat meloverlapping waktu tunggu I/O dengan waktu eksekusi CPU.

---

## 🏗️ 3. ARSITEKTUR SISTEM DAN ALIRAN DATA

Aplikasi ini menggunakan model arsitektur *Pipeline Layout* di mana data mengalir secara searah melewati tiga stasiun pemrosesan. Setiap stasiun diimplementasikan sebagai proses sistem operasi yang terpisah melalui modul `multiprocessing` Python.

### Diagram Aliran Data Pipeline:

```text
  [ START ]
      │
      ▼
┌──────────────┐
│   STAGE 1    │
│ Web Crawler  │ ──► Mengunduh dokumen HTML mentah dari internet (I/O Bound)
└──────────────┘
      │
      ▼ [ multiprocess.Queue 1 ] -> Jalur pipa transfer data mentah
      │
┌──────────────┐
│   STAGE 2    │
│ Text Cleaner │ ──► Parsing HTML, eliminasi noise, pembersihan string (CPU Bound)
└──────────────┘
      │
      ▼ [ multiprocess.Queue 2 ] -> Jalur pipa transfer data bersih
      │
┌──────────────┐
│   STAGE 3    │
│Text Analyzer │ ──► Tokenisasi, hitung frekuensi kata, tulis laporan (I/O Bound)
└──────────────┘
      │
      ▼
  [ EXITS ] ──► Pembuatan laporan berkas teks (.txt) selesai