import multiprocessing
import time

# Stage 1: Simulasi Web Crawler (Mengunduh Konten Web)
def stage_download_web(num_urls, out_queue):
    for i in range(1, num_urls + 1):
        time.sleep(0.15)  # Simulasi latensi jaringan (150ms)
        print(f"[Stage 1] Sukses mengunduh HTML dari artikel-{i}")
        out_queue.put(f"HTML_Raw_Data_{i}")
    out_queue.put(None)  # Penanda bahwa proses download selesai

# Stage 2: Simulasi Text Cleaning (Pembersihan Tag HTML)
def stage_clean_text(in_queue, out_queue):
    while True:
        raw_data = in_queue.get()
        if raw_data is None:
            out_queue.put(None)
            break
        time.sleep(0.25)  # Simulasi beban CPU membersihkan teks (250ms)
        print(f"  [Stage 2] {raw_data} berhasil dibersihkan dari tag HTML.")
        out_queue.put(f"Clean_Text_{raw_data[-1]}")

# Stage 3: Simulasi Analisis & Penyimpanan Hasil
def stage_analyze_and_save(in_queue):
    while True:
        clean_data = in_queue.get()
        if clean_data is None:
            break
        time.sleep(0.1)  # Simulasi menulis hasil ke file teks (100ms)
        print(f"    [Stage 3] Frekuensi kata untuk {clean_data} sukses disimpan.")

if __name__ == "__main__":
    TOTAL_URLS = 5
    
    # Jalur pipa komunikasi antar-proses
    queue_1_to_2 = multiprocessing.Queue()
    queue_2_to_3 = multiprocessing.Queue()
    
    start_time = time.time()
    
    # Inisialisasi Proses Paralel untuk setiap Tahapan
    p1 = multiprocessing.Process(target=stage_download_web, args=(TOTAL_URLS, queue_1_to_2))
    p2 = multiprocessing.Process(target=stage_clean_text, args=(queue_1_to_2, queue_2_to_3))
    p3 = multiprocessing.Process(target=stage_analyze_and_save, args=(queue_2_to_3,))
    
    print("=== MEMULAI SIMULASI PARALLEL WEB CRAWLER PIPELINE ===\n")
    p1.start()
    p2.start()
    p3.start()
    
    p1.join()
    p2.join()
    p3.join()
    
    total_time = time.time() - start_time
    sequential_time_est = (0.15 + 0.25 + 0.1) * TOTAL_URLS
    speedup = sequential_time_est / total_time
    
    print("\n=== EVALUASI PERFORMA PIPELINE ===")
    print(f"Waktu Eksekusi Paralel : {total_time:.4f} detik")
    print(f"Estimasi Waktu Sekuensial : {sequential_time_est:.4f} detik")
    print(f"Peningkatan Speedup   : {speedup:.2f}x lebih cepat")