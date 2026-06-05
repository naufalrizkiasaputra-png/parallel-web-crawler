LAPORAN DAN DOKUMENTASI UTAMA PROYEK
IMPLEMENTASI ARSITEKTUR PARALLEL PIPELINE PADA SISTEM WEB CRAWLER DAN TEXT PROCESSING

1. IDENTITAS MAHASISWA
* **Nama Lengkap** : [Naufal Rizkia Saputra]
* **NRP** : [15-2024-050]
* **Kelas** : [CC]
* **Mata Kuliah** : IFB 206 Komputasi Paralel
* **Program Studi** : Informatika
* **Fakultas** : Teknologi Industri
* **Institusi** : Institut Teknologi Nasional (Itenas) Bandung
* **Dosen Pengampu** : Lisa Kristiana Ph.D

---

2. PENGANTAR DAN LATAR BELAKANG PROYEK

Pada era pemrosesan data berskala besar (*Big Data Analytics*), efisiensi waktu eksekusi penambangan data menjadi salah satu tolak ukur utama keberhasilan sebuah sistem. Dua aktivitas yang paling sering dilakukan dalam *Data Engineering* adalah:
1. **Web Crawling / Scraping**: Mengunduh halaman web secara massal.
2. **Text Processing / Mining**: Membersihkan teks dan menganalisis kandungan kata di dalamnya.

Namun, jika kedua proses di atas digabungkan dan dieksekusi menggunakan pendekatan **Sekuensial (Berurutan)**, performa sistem akan menurun drastis (*performance degradation*). Hal ini disebabkan oleh dua jenis bottleneck utama:

A. I/O Bound Bottleneck (Latensi Jaringan)
Saat melakukan *crawling*, program mengirimkan permintaan HTTP ke server target dan harus menunggu respons paket data kembali melalui jaringan internet. Pada model sekuensial, CPU laptop akan berada dalam kondisi *idle* (menganggur/menunggu) selama ratusan milidetik. Waktu tunggu ini membuang-buang daya komputasi yang berharga.

B. CPU Bound Bottleneck (Komputasi Intensif)
Setelah dokumen HTML berhasil diunduh, sistem harus melakukan operasi string yang berat, seperti membuang tag-tag HTML, menghilangkan karakter khusus (*noise removal*), melakukan tokenisasi, hingga menghitung frekuensi kata tunggal. Proses ini menguras daya kerja satu *core* CPU secara terus-menerus.

Solusi: Pipeline Paralelisme
Untuk memecahkan masalah ini, proyek ini mengimplementasikan konsep **Pipeline Paralelisme**. Dengan memecah rangkaian pekerjaan menjadi 3 tahapan independen (*isolated stages*) yang berjalan secara simultan pada *core* prosesor yang berbeda, kita dapat meloverlapping waktu tunggu I/O dengan waktu eksekusi CPU.

---

3. ARSITEKTUR SISTEM DAN ALIRAN DATA

Aplikasi ini menggunakan model arsitektur *Pipeline Layout* di mana data mengalir secara searah melewati tiga stasiun pemrosesan. Setiap stasiun diimplementasikan sebagai proses sistem operasi yang terpisah melalui modul `multiprocessing` Python.

Diagram Aliran Data Pipeline:

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

4. METRIK EVALUASI PERFORMA KOMPUTASI PARALEL

Untuk membuktikan secara ilmiah bahwa arsitektur *Parallel Pipeline* ini memberikan peningkatan performa yang valid dibandingkan dengan eksekusi sekuensial tradisional, sistem ini dilengkapi dengan algoritma kalkulasi performa otomatis. Pengukuran dilakukan dengan melacak durasi waktu menggunakan presisi tinggi dari fungsi `time.time()`.

Berikut adalah penjabaran detail mengenai 4 metrik evaluasi utama yang digunakan dalam sistem ini:

A. Waktu Eksekusi Paralel ($T_p$)
Metrik $T_p$ adalah representasi dari total waktu nyata (*wall-clock time*) yang dihabiskan oleh sistem dari mulai sub-proses pertama (Stage 1) diaktifkan, hingga sub-proses terakhir (Stage 3) selesai menulis berkas laporan akhir (.txt) ke dalam media penyimpanan fisik laptop. 
* **Karakteristik**: Waktu ini mencakup latensi jaringan simulasi, waktu tunggu antrean (*blocking queue*), serta waktu pemrosesan CPU di semua *core*.

B. Estimasi Waktu Sekuensial ($T_s$)
Metrik $T_s$ adalah nilai teoretis yang dihitung berdasarkan akumulasi beban kerja murni dari seluruh tahapan seandainya program dijalankan secara konvensional (berurutan satu per satu) tanpa adanya tumpang-tindih (*overlapping*) pekerjaan. Rumus matematis untuk menghitung nilai $T_s$ pada proyek ini adalah:

$$T_s = (\text{Delay Stage 1} + \text{Delay Stage 2} + \text{Delay Stage 3}) \times \text{Jumlah URL}$$

Sesuai dengan konstanta yang diatur pada kode program:
* Delay Stage 1 (I/O Jaringan) = 0.15 detik
* Delay Stage 2 (CPU Cleaning) = 0.25 detik
* Delay Stage 3 (I/O Storage) = 0.10 detik
* Maka total beban kerja per URL adalah $0.15 + 0.25 + 0.10 = 0.50$ detik. Jika terdapat 5 URL, estimasi waktu sekuensial murni adalah **2.50 detik**.

C. Speedup ($S$)
Speedup merupakan indikator utama dalam komputasi paralel untuk melihat berapa kali lipat program berjalan lebih cepat setelah dioptimalkan menggunakan multi-proses prosesor. Rumus matematisnya mengacu pada Hukum Amdahl dasar:

$$S = \frac{T_s}{T_p}$$

* **Analisis Nilai**: 
  * Jika nilai $S = 1$, maka performa paralel sama dengan sekuensial (tidak ada efisiensi).
  * Jika nilai $S > 1$, maka arsitektur paralel berhasil memangkas waktu produksi secara efektif. Pada sistem *pipeline* ini, nilai $S$ idealnya akan mendekati rasio efisiensi tahapan paling berat (Stage 2).

D. Throughput Sistem
Throughput adalah metrik efisiensi produktivitas yang menunjukkan kapasitas rata-rata sistem dalam menyelesaikan pemrosesan halaman web atau artikel per satu satuan detik. Rumus operasionalnya adalah:

$$\text{Throughput} = \frac{\text{Jumlah URL Target}}{T_p} \text{ (satuan: artikel/detik)}$$

Semakin tinggi nilai throughput, semakin andal sistem dalam menangani lonjakan data besar (*Big Data ingestion*).

💻 5. PENJELASAN DAN BEDAH BLOK KODE PROGRAM

Program ini dibangun menggunakan bahasa pemrograman Python 3 dengan pendekatan objek fungsional dan memanfaatkan arsitektur multi-proses tingkat rendah (*low-level multiprocessing OS binding*). Keunggulan utama dari kode ini adalah sifatnya yang *Zero-Dependency*, sehingga sangat portabel untuk dijalankan di lingkungan macOS, Windows, maupun Linux tanpa memerlukan instalasi pustaka eksternal.

Berikut adalah bedah komponen dan logika baris kode utama yang menyusun sistem *pipeline* ini:

### A. Komunikasi Jalur Pipa Berbasis IPC (Inter-Process Communication)
```python
queue_1_to_2 = multiprocessing.Queue()
queue_2_to_3 = multiprocessing.Queue()