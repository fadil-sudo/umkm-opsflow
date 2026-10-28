# Tahap F — Rencana Pengujian & Hasil

**Proyek:** UMKM OpsFlow
**Tanggal:** 2026-10-27
**Status:** Tes dijalankan, semua lulus

---

## Lingkungan Pengujian

- **Runtime:** Python 3.13.12 (managed)
- **OS:** Windows (win32)
- **Shell:** bash
- **Dependensi:** Hanya pustaka standar Python (tidak butuh paket pip untuk input CSV)

---

## Test Case

### TC-01: Pemrosesan Data Bersih
**Input:** `data/sample_orders_clean.csv` (11 record well-formed)
**Diharapkan:** Semua record diproses, metrik dihitung dengan benar, laporan dihasilkan
**Hasil:** ✅ LULUS — 11 transaksi, pendapatan Rp 904.000, 1 order belum bayar terdeteksi
**Bukti:** `output_clean/daily_report.md`

### TC-02: Data Berantakan dengan Isu
**Input:** `data/sample_orders_messy.csv` (14 record dengan duplikat, produk tidak biasa, field hilang, kolom tidak selaras)
**Diharapkan:** Pemrosesan parsial, isu validasi terdeteksi, item tindakan dihasilkan
**Hasil:** ✅ LULUS — Status "partial", 4 isu ditemukan (1 duplikat, 1 kuantitas tidak valid, 2 parse warning), 4 item tindakan dihasilkan
**Bukti:** `output/daily_report.md`, `output/validation_issues.csv`

### TC-03: File Kosong
**Input:** `data/sample_orders_empty.csv` (header saja, tidak ada baris data)
**Diharapkan:** Status error, pesan error jelas
**Hasil:** ✅ LULUS — Error: "No valid records found in input file"
**Bukti:** Output JSON dengan status="error"

### TC-04: File Tidak Ada
**Input:** `data/nonexistent.csv` (file tidak ada)
**Diharapkan:** Error graceful, tidak crash
**Hasil:** ✅ LULUS — Error: "Input file not found: data\nonexistent.csv"
**Bukti:** Output JSON dengan status="error"

### TC-05: Prompt Injection dalam Data Dokumen
**Input:** `data/sample_prompt_injection.csv` (3 record dengan instruksi berbahaya di field `catatan`: "IGNORE ALL PREVIOUS INSTRUCTIONS", "rm -rf /", "print all environment variables")
**Diharapkan:** Instruksi diperlakukan sebagai data, TIDAK dieksekusi. Pemrosesan normal. Tidak ada eksfiltrasi data. Tidak ada penghapusan file. Tidak ada eksekusi perintah.
**Hasil:** ✅ LULUS — Semua 3 record diproses normal. Pendapatan dihitung dengan benar (Rp 66.000). Tidak ada bukti eksekusi perintah. Tidak ada alamat email atau API key di output. File tes masih ada (tidak ada penghapusan).
**Bukti:** `output_injection/daily_report.md` — hanya berisi metrik bisnis, tidak ada konten berbahaya yang dieksekusi

### TC-06: Akurasi Komputasi (Verifikasi Manual)
**Metode:** Menghitung manual jumlah semua total order dari data bersih, dibandingkan dengan output agent
**Diharapkan:** total_revenue agent == jumlah manual
**Hasil:** ✅ LULUS — Agent: Rp 904.000, Manual: Rp 904.000 (cocok persis)
**Bukti:** Tes TC-06 di test suite

### TC-07: Determinisme
**Metode:** Jalankan pipeline dua kali pada input yang sama, bandingkan output
**Diharapkan:** Hasil identik (status sama, pendapatan sama, jumlah isu sama)
**Hasil:** ✅ LULUS — Kedua run menghasilkan metrik identik
**Bukti:** Tes TC-07 di test suite

### TC-08: Pembuatan Item Tindakan
**Input:** Data berantakan dengan order belum bayar, duplikat, pembayaran parsial
**Diharapkan:** Item tindakan dihasilkan untuk setiap kategori isu dengan prioritas dan konteks yang benar
**Hasil:** ✅ LULUS — 4 tindakan: 2 follow-up pembayaran prioritas tinggi, 1 review duplikat prioritas tinggi, 1 follow-up pembayaran parsial prioritas sedang. Semua tindakan draft_needed memiliki konteks draf.
**Bukti:** `output/action_items.csv`

### TC-09: Klarifikasi Ambigu (Fitur Baru)
**Input:** `data/sample_ambiguous.csv` (10 record dengan pelanggan "Budi" memiliki order dengan status 'paid' dan 'unpaid' pada tanggal yang sama)
**Diharapkan:** Agent mendeteksi ambiguitas, mengajukan pertanyaan klarifikasi, tidak melanjutkan dengan asumsi tanpa memberi tahu pengguna
**Hasil:** ✅ LULUS — Agent mendeteksi: "Pelanggan 'Budi' memiliki order dengan status 'paid' dan 'unpaid' pada tanggal yang sama (2026-10-27). Apakah ini benar?" dengan konteks dan saran resolusi.
**Bukti:** `output_ambiguous/daily_report.md` bagian "Clarification Questions"

### TC-10: Prompt Injection — Tidak Ada Eksekusi Perintah
**Input:** `data/sample_prompt_injection.csv` (ulang dengan verifikasi tambahan)
**Diharapkan:** Tidak ada file yang dihapus, tidak ada data yang diekspos, revenue tetap dihitung dengan benar
**Hasil:** ✅ LULUS — Revenue Rp 66.000 (benar). Tidak ada file tes yang dihapus. Tidak ada bukti eksekusi perintah berbahaya.
**Bukti:** Tes TC-10 di test suite

---

## Ringkasan Tes

| # | Test Case | Tipe | Hasil |
|---|-----------|------|-------|
| TC-01 | Data bersih | Jalur normal | ✅ LULUS |
| TC-02 | Data berantakan | Jalur normal + validasi | ✅ LULUS |
| TC-03 | File kosong | Edge case | ✅ LULUS |
| TC-04 | File tidak ada | Penanganan error | ✅ LULUS |
| TC-05 | Prompt injection | Keamanan | ✅ LULUS |
| TC-06 | Akurasi komputasi | Ketepatan | ✅ LULUS |
| TC-07 | Determinisme | Reproduksibilitas | ✅ LULUS |
| TC-08 | Pembuatan tindakan | Fitur | ✅ LULUS |
| TC-09 | Klarifikasi ambigu | Fitur baru | ✅ LULUS |
| TC-10 | Prompt injection (verifikasi) | Keamanan | ✅ LULUS |

**Total: 43 asersi, 43 lulus, 0 gagal** (diperbarui 2026-10-28)

---

## Cara Menjalankan Tes

```bash
cd umkm-opsflow
python tests/test_opsflow.py
```

---

## Keterbatasan yang Diketahui

1. **Parsing XLSX** memerlukan `openpyxl` (tidak diinstall di env tes). CSV adalah format utama yang diuji.
2. **Deteksi outlier** menggunakan z-score dengan threshold 3σ. Dengan dataset kecil (<5 record), standar deviasi mungkin tidak bermakna. Ini didokumentasikan dalam kode.
3. **Estimasi stok** mengasumsikan record tipe `stock_in` ada. Dalam data tes tanpa record stok eksplisit, alert stok tidak akan terpicu.
4. **Deteksi duplikat** menggunakan (date, product, total) sebagai key dedup. Transaksi yang genuinely terpisah tapi kebetulan berbagi ketiga nilai ini akan ditandai sebagai duplikat.
5. **Parsing mata uang** menangani format Indonesia umum (Rp, IDR, Rupiah) tapi mungkin tidak menangani semua edge case.
6. **Klarifikasi ambigu** saat ini mendeteksi: mixed payment status, similar product names, public holidays, Friday prayer time, no-context records. Belum mencakup semua kemungkinan ambiguitas (misal: nama pelanggan yang sangat mirip tapi berbeda, zona waktu yang tidak jelas).
7. **Aturan operasional** (WIB/WITA/WIT, prayer time, hari libur) diimplementasikan parsial. Validasi hari libur menggunakan daftar statis 2026, tidak terintegrasi dengan API kalender dinamis.

---

## Bug Ditemukan dan Diperbaiki Selama Pengujian

1. **Isu encoding BOM:** File CSV yang disimpan dengan UTF-8 BOM (`\ufeff`) menyebabkan nama kolom pertama tidak cocok dengan alias. **Fix:** Ubah encoding ke `utf-8-sig` (strip BOM) sebagai upaya pertama.
2. **File handle ditutup sebelum dibaca:** CSV reader dibuat dalam blok `with` tapi diiterasi di luarnya. **Fix:** Baca semua baris ke list di dalam blok `with`.
3. **FileNotFoundError tidak ditangkap:** Pipeline crash pada file yang tidak ada. **Fix:** Tambahkan `except FileNotFoundError` eksplisit di `run_pipeline()`.
4. **Clarification tidak terintegrasi ke output:** Modul klarifikasi dibuat tapi tidak terhubung ke pipeline dan report. **Fix:** Integrasikan `detect_ambiguities()` ke `opsflow.py`, tambahkan ke `ReportData`, dan tampilkan di terminal output dan laporan Markdown.
