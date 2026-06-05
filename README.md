# Parallel Web Crawler & Text Processing Pipeline Simulation

Proyek mandiri ini dibuat untuk memenuhi Evaluasi 3 Mata Kuliah IFB 206 Komputasi Paralel Informatika Itenas.

## Identitas Mahasiswa
- **Nama:** [Naufal Rizkia Saputra]
- **NRP:** [15-2024-050]
- **Kelas:** [IFB-206 KOMPUTASI PARALEL & SISTEM TERDISTRIBUSI CC]

## Mekanisme Kerja Sistem
Sistem ini menggunakan arsitektur **Pipeline Paralel** yang membagi tugas pemrosesan teks web berskala besar ke dalam 3 tahapan mandiri menggunakan Python `multiprocessing`:
1. **Stage 1 (Web Crawler):** Mengunduh konten teks HTML mentah secara berkala.
2. **Stage 2 (Text Cleaning):** Membersihkan noise teks dan tag HTML yang tidak diperlukan.
3. **Stage 3 (Data Writer):** Menganalisis hasil akhir dan menyimpannya ke dalam sistem penyimpanan.

Dengan metode paralel ini, pemrosesan tidak perlu menunggu satu artikel selesai sepenuhnya untuk mulai mengunduh artikel berikutnya.