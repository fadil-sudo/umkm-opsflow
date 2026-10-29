# UMKM OpsFlow
### Agent Laporan Operasional Harian untuk UMKM Indonesia

**Short blurb:** *"Agent laporan harian UMKM dari data berantakan"*

**Tencent Cloud Hackathon Indonesia 2026** — Challenge B: The Office Agent (Automate Better)

---

## Apa yang Dilakukan

UMKM OpsFlow mengubah catatan order/pengeluaran yang berantakan (CSV/XLSX) menjadi **laporan operasional harian yang tervalidasi** lengkap dengan daftar tindakan dan draf pesan follow-up — dalam waktu kurang dari 15 detik, bukan 30-60 menit secara manual.

```
Spreadsheet berantakan → Agent membaca → Validasi → Hitung (deterministik) → Laporan + Tindakan
                                                                                  ↓
                                                                   Manusia review sebelum bertindak
```

### Pembeda Utama (Bukan Sekadar Chatbot)

1. **Jejak audit** — setiap angka di laporan dapat ditelusuri ke baris sumber
2. **Penanda ketidakpastian** — agent menandai data yang tidak valid/duplikat/anomali secara eksplisit
3. **Klarifikasi ambigu** — agent bertanya saat menemukan situasi ambigu (misal: pelanggan dengan status pembayaran berbeda pada hari yang sama)
4. **Tindakan berbasis aturan** — item tindakan dihasilkan dari aturan deterministik, bukan tebakan LLM
5. **Gerbang persetujuan manusia** — tidak ada tindakan eksternal tanpa konfirmasi eksplisit
6. **Perhitungan yang dapat direproduksi** — semua matematika adalah kode Python, LLM tidak pernah menghitung angka

---

## Mulai Cepat

### Prasyarat
- Python 3.11+ (diuji pada 3.13.12)
- Tidak perlu dependensi pip untuk CLI (hanya pustaka standar untuk CSV)
- Untuk UI: `pip install streamlit`

### Jalankan dengan UI (Streamlit) — Direkomendasikan untuk Demo

```bash
# Install streamlit
pip install streamlit

# Jalankan UI
streamlit run app.py
```

Buka browser di `http://localhost:8501`. Anda bisa:
- **Upload** file CSV via drag-and-drop
- **Lihat** metrik pendapatan, pengeluaran, net cashflow
- **Periksa** masalah validasi dan pertanyaan klarifikasi
- **Tinjau** item tindakan dan draf pesan
- **Setujui** tindakan sebelum "kirim" (mock)
- **Unduh** laporan dalam format Markdown, JSON, dan CSV

### Jalankan via CLI

```bash
# Proses data berantakan (menunjukkan validasi beraksi)
python scripts/opsflow.py --input data/sample_orders_messy.csv --output-dir output/

# Proses data bersih (menunjukkan jalur normal)
python scripts/opsflow.py --input data/sample_orders_clean.csv --output-dir output_clean/

# Output JSON untuk penggunaan programatik
python scripts/opsflow.py --input data/sample_orders_messy.csv --output-dir output/ --json
```

### Jalankan Tes

```bash
python tests/test_opsflow.py
```

**Hasil yang diharapkan:** 43 asersi, 43 lulus, 0 gagal (diperbarui 2026-10-28)

---

## File Output

Setelah dijalankan, direktori `output/` berisi:

| File | Deskripsi |
|------|-----------|
| `daily_report.md` | Laporan operasional harian lengkap dengan metrik, isu, dan tindakan |
| `draft_messages.md` | Draf pesan follow-up WhatsApp (untuk review manusia) |
| `action_items.csv` | Item tindakan dalam format spreadsheet |
| `validation_issues.csv` | Isu kualitas data dalam format spreadsheet |
| `metrics.json` | Metrik mentah untuk audit/debugging |

---

## Data Demo

Semua data di `data/` adalah **sintetis** dan diberi label jelas. Tidak ada data bisnis nyata yang digunakan.

| File | Deskripsi |
|------|-----------|
| `sample_orders_clean.csv` | Data well-formed (11 record) — demo jalur normal |
| `sample_orders_messy.csv` | Data berantakan (14 record) — menunjukkan validasi, deteksi duplikat, pembuatan tindakan |
| `sample_orders_empty.csv` | File kosong — demo penanganan error |
| `sample_prompt_injection.csv` | Instruksi berbahaya dalam field data — tes keamanan |
| `sample_ambiguous.csv` | Data dengan ambiguitas (pelanggan dengan status berbeda) — demo klarifikasi |

---

## Arsitektur

```
Pengguna (WorkBuddy) → "Ini data penjualan hari ini" → unggah CSV
                          ↓
              WorkBuddy Agent (orkestrator)
                    ↓            ↓            ↓
              LLM (format)  Python (hitung)  File I/O
                    ↓            ↓            ↓
              Teks laporan   Dict metrik     output/*.md
                    ↓            ↓            ↓
              Manusia review → Setujui → Salin/kirim pesan secara manual
```

**Pemisahan tanggung jawab:**
- **LLM** (WorkBuddy agent): Memahami intent, memformat laporan, menyusun draf pesan
- **Python** (deterministik): Parsing, validasi, SEMUA perhitungan numerik, aturan tindakan
- **File system**: Baca input, tulis output (tidak ada panggilan API eksternal)

### Skrip

| Skrip | Tujuan |
|-------|--------|
| `scripts/opsflow.py` | Entry point utama — orkestrasi pipeline lengkap |
| `scripts/parse_input.py` | Parse CSV/XLSX menjadi record ternormalisasi |
| `scripts/validate.py` | Validasi record, tandai isu |
| `scripts/compute.py` | Hitung metrik (deterministik) |
| `scripts/actions.py` | Hasilkan item tindakan berbasis aturan |
| `scripts/export.py` | Ekspor laporan dan draf ke file |

---

## Keamanan

- **Tahan terhadap prompt injection:** Field data di-parse sebagai data, bukan instruksi. LLM hanya melihat metrik yang sudah dihitung, bukan konten sel mentah.
- **Tidak ada panggilan API eksternal:** Tidak ada data yang meninggalkan lingkungan lokal.
- **Tidak ada penyimpanan kredensial:** Tidak ada API key, password, atau token di mana pun.
- **Input read-only:** Agent tidak pernah memodifikasi file sumber.
- **Gerbang persetujuan manusia:** Tidak ada pesan yang dikirim otomatis. Draf disimpan untuk disalin/dikirim manual.
- **Tidak ada operasi destruktif:** Agent tidak dapat menghapus, memodifikasi, atau mengirim apa pun.

---

## Keterbatasan

- Dukungan XLSX memerlukan `openpyxl` (CSV langsung berjalan tanpa dependensi)
- Estimasi stok memerlukan record tipe `stock_in` (tidak ada dalam data demo)
- Deteksi anomali butuh ≥5 record untuk statistik yang bermakna
- Tidak ada analisis tren multi-hari dalam MVP (fokus single-day)
- Tidak ada pengiriman pesan aktual (hanya draf — by design, untuk keamanan)
- Format Rupiah Indonesia menggunakan `.` sebagai pemisah ribuan (konvensi lokal)

---

## Metrik: Baseline vs Agent

| Tugas | Manual (estimasi) | Agent (terukur) | Error Manual | Error Agent |
|-------|-------------------|-----------------|--------------|-------------|
| Kompilasi total harian | ~15 menit | <1 detik | 3-5 per hari | 0 (deterministik) |
| Identifikasi pesanan belum bayar | ~5 menit | <1 detik | Sering terlewat | 0 |
| Tandai isu kualitas data | ~10 menit (kalau dilakukan) | <1 detik | Jarang dilakukan | Komprehensif |
| Siapkan draf follow-up | ~10 menit | <1 detik | Variatif | Draf siap pakai |
| **Total** | **~40 menit** | **<15 detik** | **Tinggi** | **Mendekati nol** |

*Waktu manual adalah estimasi berdasarkan riset persona. Waktu agent adalah waktu eksekusi terukur aktual. Tingkat error manual diestimasi dari riset praktik operasional UMKM.*

---

## Skrip Demo (2-3 menit)

1. **Tunjukkan masalah (30 detik):** Buka `data/sample_orders_messy.csv` — tunjukkan keberantakan: nama pelanggan hilang, "Electric Pulsar XL" yang mencurigakan seharga Rp 50.000, baris supplies campur aduk, duplikat, pembayaran parsial.

2. **Jalankan agent (30 detik):**
   ```
   python scripts/opsflow.py --input data/sample_orders_messy.csv --output-dir output/
   ```
   Tunjukkan output yang dapat dibaca manusia — 14 record diparse, 4 isu ditemukan, 4 tindakan diusulkan.

3. **Tunjukkan laporan (60 detik):** Buka `output/daily_report.md` — tunjukkan:
   - Ringkasan eksekutif dengan pendapatan/pengeluaran/laba bersih
   - Rincian status pembayaran (2 belum bayar, 1 parsial)
   - Produk teratas
   - Isu kualitas data (duplikat, kuantitas tidak valid)
   - Item tindakan dengan prioritas
   - Jejak audit yang menunjukkan baris sumber

4. **Tunjukkan draf pesan (30 detik):** Buka `output/draft_messages.md` — tunjukkan draf follow-up WhatsApp untuk pelanggan yang belum bayar. Tekankan: ini adalah draf, belum dikirim. Manusia harus salin dan kirim manual.

5. **Penutup (30 detik):** "Apa yang butuh 40 menit kerja manual yang rawan error sekarang butuh 15 detik dengan jejak audit lengkap, validasi, dan persetujuan manusia sebelum tindakan apa pun."

---

## Pitch 1 Menit

> Pemilik UMKM Indonesia — 99% dari bisnis kita — mencatat penjualan harian di spreadsheet berantakan atau buku catatan kertas. Menyusun laporan harian butuh 30-60 menit, penuh error, dan biasanya dilewati. UMKM OpsFlow adalah agent yang membaca CSV berantakan itu, memvalidasi data, menghitung metrik harian secara deterministik, menandai isu seperti duplikat dan pesanan belum bayar, menghasilkan item tindakan, dan menyusun draf pesan follow-up — semua dalam 15 detik. Setiap angka dihitung oleh Python, bukan dihalusinasi LLM. Setiap tindakan butuh persetujuan manusia. Agent ini tidak cuma ngobrol — dia kerja nyata: baca, validasi, hitung, dan usulkan tindakan dengan jejak audit penuh.

---

## Lisensi

Proyek ini dibuat untuk Tencent Cloud Hackathon Indonesia 2026. Semua data demo adalah sintetis.

## Kontribusi

Solo builder — mahasiswa Sistem Informasi.
