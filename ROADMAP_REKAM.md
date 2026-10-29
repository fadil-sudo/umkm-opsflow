# Roadmap Rekam Demo & Screenshot — UMKM OpsFlow

**Tujuan:** Hasilkan 2 deliverable: (1) Screenshot test results, (2) Demo video 5-8 menit  
**Estimasi waktu total:** 1-2 jam (tergantung editing video)

---

## Persiapan (10 menit)

### 1.1 Setup Environment

- [x] Buka terminal/command prompt
- [x] Navigate ke folder: `cd C:/Users/User/WorkBuddy AI/2026-10-27-20-34-13/umkm-opsflow`
- [x] Pastikan Python berfungsi: `python --version`
- [ ] Setup screen recorder (pilih salah satu):
  - **Windows Game Bar:** Tekan `Win + G` → klik tombol record (tombol bulat merah)
  - **OBS Studio:** Buka OBS → Add Source → Display Capture → Start Recording
  - **Loom:** Install extension Chrome → klik icon Loom → Start Recording

### 1.2 Siapkan File

- [ ] Buka `docs/demo_video_script.md` di tab/browser (untuk referensi)
- [ ] Siapkan folder `umkm-opsflow` di file explorer (untuk drag-drop file nanti)
- [ ] Kosongkan desktop (tutup aplikasi yang tidak perlu)
- [ ] Set resolusi layar ke 1920×1080 (jika memungkinkan)

---

## Fase 1: Screenshot Test Results (5 menit)

**Tujuan:** Dapatkan gambar bukti 43/43 test passing

### Langkah

1. Di terminal, jalankan:
   ```bash
   python tests/test_opsflow.py
   ```
2. Tunggu sampai selesai (sekitar 10-15 detik)
3. Saat muncul output:
   ```
   ============================================================
     TEST RESULTS: 43 passed, 0 failed, 43 total
   ============================================================
   ```
4. **Screenshot:**
   - Tekan `Win + Shift + S`
   - Pilih area dari "=== TEST 1" sampai 10-15 baris hasil PASS
   - Atau screenshot seluruh terminal window
5. Simpan sebagai `screenshot_test_results.png`

### Tips

- Pastikan font terminal cukup besar (minimal 14px) agar terbaca jelas
- Jika menggunakan Windows Terminal, bisa zoom dengan `Ctrl + +`
- Background terminal gelap lebih mudah dibaca

---

## Fase 2: Rekam Demo Video (30-60 menit)

**Tujuan:** Hasilkan video 5-8 menit yang menunjukkan capabilities agent

### Scene 1: Hook & Masalah (0:00 - 0:45)

**Aksi:**

1. Mulai screen recording
2. Buka file `data/sample_orders_messy.csv` di text editor (Notepad/VS Code)
3. Scroll ke bawah, tunjukkan:
   - Baris dengan kolom kosong
   - "Electric Pulsar XL" Rp 50.000
   - Format tanggal campur
   - Duplikat
   - Pembayaran parsial
4. **Voice over:** "Setiap hari, pemilik UMKM mencatat puluhan transaksi di spreadsheet berantakan seperti ini..."
5. **Pause recording** (jeda untuk editing)

---

### Scene 2: Solusi UMKM OpsFlow (0:45 - 1:30)

**Aksi:**

1. Buka slide sederhana atau tampilkan README
2. Tunjukkan nama proyek: "UMKM OpsFlow"
3. Tunjukkan flow diagram (bisa dari `docs/workflow_diagram.md`)
4. **Voice over:** "UMKM OpsFlow adalah agent AI yang mengubah catatan berantakan ini menjadi laporan tervalidasi dalam hitungan detik..."
5. **Pause recording**

---

### Scene 3: Demo Data Bersih (1:30 - 3:00)

**Aksi:**

1. Buka terminal
2. Ketik dan jalankan:
   ```bash
   python scripts/opsflow.py --input data/sample_orders_clean.csv --output-dir output_clean/
   ```
3. Tunggu output selesai
4. Tunjukkan:
   - "Status: SUCCESS"
   - "Records parsed: 11"
   - "Total Revenue: Rp 483,000"
   - "Unpaid Orders: 1"
5. Buka `output_clean/daily_report.md`
6. Scroll tunjukkan:
   - Executive Summary
   - Payment Status Breakdown
   - Top Products
7. **Voice over:** "Dengan data yang rapi, agent menghasilkan laporan lengkap dengan metrik dan produk terlaris..."
8. **Pause recording**

---

### Scene 4: Demo Data Berantakan + Validasi (3:00 - 4:30)

**Aksi:**

1. Di terminal, jalankan:
   ```bash
   python scripts/opsflow.py --input data/sample_orders_messy.csv --output-dir output_messy/
   ```
2. Tunggu output
3. Highlight:
   - "Status: PARTIAL"
   - "Validation issues: 4"
   - List isu: duplikat, qty = 0, unparseable number
4. **Voice over:** "Tapi yang lebih menarik adalah saat data tidak sempurna. Agent tidak berhenti — dia mendeteksi isu dan tetap menghasilkan laporan..."
5. Buka `output_messy/validation_issues.csv`
6. Tunjukkan isu yang terdeteksi
7. **Pause recording**

---

### Scene 5: Klarifikasi Ambigu (4:30 - 5:15) ⭐ Penting

**Aksi:**

1. Jalankan:
   ```bash
   python scripts/opsflow.py --input data/sample_ambiguous.csv --output-dir output_ambiguous/
   ```
2. Highlight bagian:
   ```
   --- Clarification Questions (1) ---
   🟠 [MEDIUM] Pelanggan 'Budi' memiliki order dengan status 'paid' dan 'unpaid'...
   ```
3. **Voice over:** "Ini yang membedakan agent kami. Saat menemukan ambiguitas — seperti pelanggan dengan status berbeda — agent bertanya, tidak menebak..."
4. **Pause recording**

---

### Scene 6: Prompt Injection Resistance (5:15 - 6:00) ⭐ Penting

**Aksi:**

1. Buka `data/sample_prompt_injection.csv` di text editor
2. Tunjukkan baris dengan catatan berbahaya: "IGNORE ALL PREVIOUS INSTRUCTIONS..."
3. Jalankan:
   ```bash
   python scripts/opsflow.py --input data/sample_prompt_injection.csv --output-dir output_injection/
   ```
4. Tunjukkan:
   - "Status: SUCCESS"
   - Revenue tetap dihitung dengan benar
   - Tidak ada file yang dihapus
5. **Voice over:** "Keamanan adalah prioritas. Bahkan jika ada instruksi berbahaya tersembunyi dalam data, agent memperlakukannya sebagai data, bukan perintah..."
6. **Pause recording**

---

### Scene 7: Human Approval Gate (6:00 - 6:45) ⭐ Penting

**Aksi:**

1. Buka `output_messy/draft_messages.md`
2. Tunjukkan draf pesan untuk pelanggan yang belum bayar
3. Buka WhatsApp Web (atau mockup)
4. Copy-paste draf pesan
5. **Voice over:** "Agent menyusun draf pesan follow-up, tapi ingat — ini hanya draf. Agent tidak pernah mengirim apa pun. Manusia yang memutuskan dan mengirim..."
6. **Pause recording**

---

### Scene 8: Test Results & Closing (6:45 - 7:30)

**Aksi:**

1. Jalankan test:
   ```bash
   python tests/test_opsflow.py
   ```
2. Tunjukkan:
   ```
   TEST RESULTS: 43 passed, 0 failed, 43 total
   ```
3. **Voice over:** "Kami menguji agent dengan 43 test case yang mencakup data bersih, data berantakan, file kosong, prompt injection, dan banyak lagi. Semua lulus..."
4. Tampilkan slide ringkasan:
   - Masalah: Data UMKM berantakan → 30-60 menit manual
   - Solusi: UMKM OpsFlow → <15 detik
   - Akuntabilitas: 5 aturan (SOURCES, PERMISSIONS, APPROVAL, LIMITS, RECORD)
   - Test: 43/43 passing
5. **Voice over closing:** "UMKM OpsFlow — agent yang tidak hanya bekerja, tapi juga dapat dipertanggungjawabkan. Terima kasih."
6. **Stop recording**

---

## Fase 3: Editing (Opsional, 15-30 menit)

**Jika ingin edit video:**

1. Buka video editor (Windows Photos app, Clipchamp, atau DaVinci Resolve)
2. Potong bagian yang tidak perlu (loading lama, typo)
3. Tambahkan text overlay di bagian penting:
   - "43/43 TESTS PASSING"
   - "🛡️ PROMPT INJECTION BLOCKED"
   - "❓ CLARIFICATION ASKED"
4. Export sebagai MP4 (1080p, 30fps)

**Jika tidak mau edit:**

- Video mentah juga bisa diterima
- Pastikan tidak ada informasi pribadi yang terlihat

---

## Fase 4: Upload & Submit (10 menit)

### Upload Video

- **Pilihan 1:** Upload ke YouTube (Unlisted)
  - Buka YouTube Studio → Upload Video
  - Visibility: Unlisted
  - Copy link
- **Pilihan 2:** Upload ke Google Drive
  - Share dengan "Anyone with the link"
  - Copy link

### Isi Form Submission

Buka: <https://forms.gle/y1aHBH4BsrytXDxdA>

Isi dengan:

- **Project title:** UMKM OpsFlow
- **Short blurb:** Agent laporan harian UMKM dari data berantakan
- **GitHub repo:** <https://github.com/fadil-sudo/umkm-opsflow>
- **Demo video:** [Link YouTube/Google Drive]
- **Screenshot test:** Upload file `screenshot_test_results.png`
- **Cover image:** Upload `assets/cover_image.svg`

---

## Checklist Final

- [ ] Screenshot test results (43/43)
- [ ] Demo video 5-8 menit
- [ ] Video di-upload (YouTube/Google Drive)
- [ ] Form submission diisi
- [ ] Semua dokumen di-upload
- [ ] Konfirmasi submission disimpan

---

**Tips Sukses:**

- Rekam di ruangan yang tenang (tidak ada noise)
- Jelaskan dengan suara yang jelas dan tidak terlalu cepat
- Tunjukkan kursor saat menunjukkan sesuatu
- Jeda 2-3 detik antar scene untuk editing
- Jika salah, ulangi scene itu saja (tidak perlu ulang dari awal)

**Selamat merekam! 🎬**
