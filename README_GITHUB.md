# UMKM OpsFlow

**Agent laporan harian UMKM dari data berantakan**

[![Tests](https://img.shields.io/badge/tests-43%2F43%20passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

> **Tencent Cloud Hackathon Indonesia 2026** — Challenge B: The Office Agent (Automate Better)

---

## 🎯 Apa yang Dilakukan

UMKM OpsFlow mengubah catatan order/pengeluaran yang berantakan (CSV/XLSX) menjadi **laporan operasional harian yang tervalidasi** lengkap dengan daftar tindakan dan draf pesan follow-up — dalam waktu kurang dari 15 detik, bukan 30-60 menit secara manual.

```
Spreadsheet berantakan → Agent membaca → Validasi → Hitung (deterministik) → Laporan + Tindakan
                                                                                  ↓
                                                                   Manusia review sebelum bertindak
```

### ✨ Pembeda Utama

1. **Jejak audit** — setiap angka di laporan dapat ditelusuri ke baris sumber
2. **Penanda ketidakpastian** — agent menandai data yang tidak valid/duplikat/anomali secara eksplisit
3. **Klarifikasi ambigu** — agent bertanya saat menemukan situasi ambigu (misal: pelanggan dengan status pembayaran berbeda pada hari yang sama)
4. **Tindakan berbasis aturan** — item tindakan dihasilkan dari aturan deterministik, bukan tebakan LLM
5. **Gerbang persetujuan manusia** — tidak ada tindakan eksternal tanpa konfirmasi eksplisit
6. **Perhitungan yang dapat direproduksi** — semua matematika adalah kode Python, LLM tidak pernah menghitung angka

---

## 🚀 Mulai Cepat

### Prasyarat
- Python 3.11+ (diuji pada 3.13.12)
- Tidak perlu dependensi pip (hanya pustaka standar untuk CSV)

### Jalankan Demo

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

**Hasil:** 43 asersi, 43 lulus, 0 gagal ✅

---

## 📁 File Output

Setelah dijalankan, direktori `output/` berisi:

| File | Deskripsi |
|------|-----------|
| `daily_report.md` | Laporan operasional harian lengkap dengan metrik, isu, dan tindakan |
| `draft_messages.md` | Draf pesan follow-up WhatsApp (untuk review manusia) |
| `action_items.csv` | Item tindakan dalam format spreadsheet |
| `validation_issues.csv` | Isu kualitas data dalam format spreadsheet |
| `metrics.json` | Metrik mentah untuk audit/debugging |

---

## 🧪 Data Demo

Semua data di `data/` adalah **sintetis** dan diberi label jelas.

| File | Deskripsi |
|------|-----------|
| `sample_orders_clean.csv` | Data well-formed (11 record) — demo jalur normal |
| `sample_orders_messy.csv` | Data berantakan (14 record) — validasi, duplikat, tindakan |
| `sample_orders_empty.csv` | File kosong — demo penanganan error |
| `sample_prompt_injection.csv` | Instruksi berbahaya dalam field data — tes keamanan |
| `sample_ambiguous.csv` | Data dengan ambiguitas — demo klarifikasi agent |

---

## 🏗️ Arsitektur

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
- **Python** (deterministik): Parsing, validasi, SEMUA perhitungan numerik, aturan tindakan, deteksi ambiguitas
- **File system**: Baca input, tulis output (tidak ada panggilan API eksternal)

### Skrip

| Skrip | Tujuan |
|-------|--------|
| `scripts/opsflow.py` | Entry point utama — orkestrasi pipeline lengkap |
| `scripts/parse_input.py` | Parse CSV/XLSX menjadi record ternormalisasi |
| `scripts/validate.py` | Validasi record, tandai isu |
| `scripts/compute.py` | Hitung metrik (deterministik) |
| `scripts/actions.py` | Hasilkan item tindakan berbasis aturan |
| `scripts/clarify.py` | Deteksi ambiguitas yang membutuhkan klarifikasi pengguna |
| `scripts/export.py` | Ekspor laporan dan draf ke file |

---

## 🛡️ Keamanan & Akuntabilitas

### Lima Aturan Akuntabilitas

| Aturan | Implementasi |
|--------|--------------|
| **SOURCES** — Tunjukkan sumber | Setiap angka di laporan ditautkan ke baris sumber di file input |
| **PERMISSIONS** — Tetap dalam izin | Hanya membaca file yang diberikan pengguna, tidak ada akses lain |
| **APPROVAL** — Tanya sebelum bertindak | Draf pesan disiapkan, tidak pernah dikirim otomatis |
| **LIMITS** — Akui batasan | Agent menandai outlier, data hilang, dan ketidakpastian secara eksplisit |
| **RECORD** — Simpan catatan | Log audit lengkap: metrics.json + validation_issues.csv + clarification log |

### Fitur Keamanan

- ✅ **Tahan terhadap prompt injection:** Field data di-parse sebagai data, bukan instruksi
- ✅ **Tidak ada panggilan API eksternal:** Semua pemrosesan lokal
- ✅ **Tidak ada penyimpanan kredensial:** Tidak ada API key atau token
- ✅ **Input read-only:** Agent tidak pernah memodifikasi file sumber
- ✅ **Gerbang persetujuan manusia:** Tidak ada pesan yang dikirim otomatis
- ✅ **Tidak ada operasi destruktif:** Agent tidak dapat menghapus, memodifikasi, atau mengirim apa pun

---

## 📊 Metrik: Baseline vs Agent

| Tugas | Manual (estimasi) | Agent (terukur) | Error Manual | Error Agent |
|-------|-------------------|-----------------|--------------|-------------|
| Kompilasi total harian | ~15 menit | <1 detik | 3-5 per hari | 0 (deterministik) |
| Identifikasi pesanan belum bayar | ~5 menit | <1 detik | Sering terlewat | 0 |
| Tandai isu kualitas data | ~10 menit (kalau dilakukan) | <1 detik | Jarang dilakukan | Komprehensif |
| Siapkan draf follow-up | ~10 menit | <1 detik | Variatif | Draf siap pakai |
| **Total** | **~40 menit** | **<15 detik** | **Tinggi** | **Mendekati nol** |

---

## 🎥 Demo Video

Lihat `docs/demo_video_script.md` untuk script lengkap demo video 5-8 menit.

**Scene utama:**
1. Masalah — spreadsheet berantakan
2. Solusi — jalankan agent
3. Validasi — deteksi isu data
4. Klarifikasi — agent bertanya saat ambigu
5. Keamanan — prompt injection diabaikan
6. Approval — draf pesan untuk review manusia

---

## 📚 Dokumentasi

| Dokumen | Isi |
|---------|-----|
| `docs/01_research_report.md` | Verifikasi hackathon, audit tools, riset masalah |
| `docs/02_idea_matrix.md` | Matriks 9 ide, analisis sensitivitas |
| `docs/03_mvp_and_spec.md` | Problem statement, persona, workflow, skema data |
| `docs/04_architecture.md` | Stack, komponen, prinsip desain |
| `docs/05_test_plan.md` | Test cases, hasil pengujian, bug fixes |
| `docs/06_handbook_analysis.md` | Analisis handbook resmi, gap analysis |
| `docs/accountability_sheet.md` | Ringkasan 1 halaman: akses, otonom, persetujuan |
| `docs/product_sharing.md` | Insight WorkBuddy dan pembelajaran |
| `docs/demo_video_script.md` | Script demo video lengkap |
| `docs/short_blurb.md` | Tagline <10 kata |
| `docs/workflow_diagram.md` | Diagram Mermaid workflow |

---

## 🏆 Konteks Hackathon

- **Event:** [Tencent Cloud Hackathon Indonesia 2026](https://tch.tencentcloud.com/contest/47)
- **Challenge:** B — The Office Agent (Automate Better)
- **Platform:** [Tencent WorkBuddy](https://open.workbuddy.cn/)
- **Deadline submission:** 1 November 2026, 23:59 WIB
- **Demo Day:** 27 November 2026

---

## 📄 Lisensi

MIT License — Proyek ini dibuat untuk Tencent Cloud Hackathon Indonesia 2026. Semua data demo adalah sintetis.

---

<p align="center">Built with ❤️ using <strong>Tencent Cloud WorkBuddy</strong></p>
