# Tahap E — Arsitektur & Stack

**Proyek:** UMKM OpsFlow
**Tanggal:** 2026-10-27
**Status:** Selesai

---

## 1. Ikhtisar Stack

```
┌─────────────────────────────────────────────────────┐
│                   ANTARMUKA PENGGUNA                  │
│            WorkBuddy Agent (bahasa natural)          │
│        "Ini data penjualan hari ini"                │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              WORKBUDDY AGENT (ORKESTRATOR)           │
│                                                      │
│  ┌─────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │ Intent  │→ │ Workflow │→ │ Gerbang Persetujuan│  │
│  │ Parse   │  │ Eksekusi │  │ Manusia            │  │
│  └─────────┘  └────┬─────┘  └───────────────────┘  │
│                    │                                 │
│     ┌──────────────┼──────────────────┐            │
│     ▼              ▼                  ▼             │
│  Layer LLM     Layer Deterministik   File I/O      │
│  (formatting,  (parsing, validasi,   (baca input,  │
│   draf teks,   hitung, tindakan)     tulis output) │
│   jelaskan)                                      │   │
└─────┬──────────────┬──────────────────┬───────────┘
      │              │                  │
      ▼              ▼                  ▼
┌──────────┐  ┌───────────────┐  ┌─────────────┐
│ WorkBuddy│  │ Skrip Python  │  │ File System │
│ LLM API  │  │               │  │             │
│          │  │ parse_input.py│  │ data/       │
│          │  │ validate.py   │  │ output/     │
│          │  │ compute.py    │  │ tests/      │
│          │  │ actions.py    │  │             │
│          │  │ export.py     │  │             │
└──────────┘  └───────────────┘  └─────────────┘
```

## 2. Detail Komponen

### 2.1 WorkBuddy Agent (Orkestrator)
- **Peran:** Menerima input pengguna (path file atau unggahan), mengorkestrasi workflow, menyajikan hasil, mengelola gerbang persetujuan manusia
- **Tugas LLM saja:** Memahami intent pengguna, memformat laporan dari data pre-computed, menyusun draf pesan follow-up
- **Tidak pernah melakukan:** Perhitungan numerik, modifikasi file tanpa persetujuan, panggilan API eksternal

### 2.2 Skrip Python (Core Deterministik)
Semua skrip berada di `scripts/` dan dipanggil oleh WorkBuddy agent via Bash tool.

| Skrip | Tujuan | Input | Output |
|-------|--------|-------|--------|
| `opsflow.py` | Skrip orkestrator utama — jalankan pipeline penuh | `--input <file>` `--output-dir <dir>` | File laporan di dir output |
| Modul internal: | | | |
| `parse_input.py` | Parse CSV/XLSX menjadi record ternormalisasi | Path file | List of Record dict |
| `validate.py` | Validasi record, tandai isu | List record | List isu + record tervalidasi |
| `compute.py` | Hitung metrik (pendapatan, pengeluaran, dll) | Record tervalidasi | Dict metrik |
| `actions.py` | Hasilkan item tindakan berbasis aturan | Metrik + record | List item tindakan |
| `export.py` | Ekspor laporan dan draf ke file | Semua hasil | File .md, .csv |

### 2.3 File System
```
umkm-opsflow/
├── data/               # Data demo sintetis (diberi label sintetis)
│   ├── sample_orders_clean.csv
│   ├── sample_orders_messy.csv
│   └── sample_orders_empty.csv
├── scripts/            # Core deterministik Python
│   ├── opsflow.py      # Entry point utama
│   ├── parse_input.py  # Modul parsing
│   ├── validate.py     # Modul validasi
│   ├── compute.py      # Modul komputasi
│   ├── actions.py      # Modul pembuatan tindakan
│   └── export.py       # Modul ekspor
├── tests/              # Test case
│   └── test_opsflow.py
├── output/             # Laporan yang dihasilkan (dibuat saat runtime)
├── docs/               # Dokumentasi
│   ├── 01_research_report.md
│   ├── 02_idea_matrix.md
│   ├── 03_mvp_and_spec.md
│   ├── 04_architecture.md       ← FILE INI
│   └── 05_test_plan.md
└── README.md
```

## 3. Prinsip Desain Utama

### 3.1 Pemisahan Probabilistik vs Deterministik

| Layer | Apa yang dilakukan | Apa yang TIDAK PERNAH dilakukan |
|-------|---------------------|-------------------------------|
| LLM (WorkBuddy) | Pahami intent, format teks, draf pesan, jelaskan hasil | Hitung angka, validasi data, buat keputusan |
| Python (Deterministik) | Parse, validasi, hitung, hasilkan tindakan, ekspor | Hasilkan bahasa natural, buat judgment call |

**LLM menerima angka pre-computed dan memformatnya menjadi teks yang dapat dibaca. LLM tidak pernah menghasilkan angka yang tidak dihitung oleh Python.**

### 3.2 Tanpa Dependensi Eksternal
- Tidak ada LangChain, LangGraph, atau framework agent
- Tidak ada vector database
- Tidak ada orkestrasi multi-agent
- Tidak ada deployment cloud untuk MVP
- Tidak ada panggilan API eksternal
- Hanya pustaka standar Python: `csv`, `json`, `datetime`, `statistics`, `collections`, `pathlib`, `argparse`
- Untuk XLSX: `openpyxl` (diinstall via pip di env terisolasi jika dibutuhkan, atau fallback CSV-only)

### 3.3 Jejak Audit
Setiap angka output menyertakan sumbernya:
- "Total pendapatan: Rp 2.340.000" → "Sumber: 47 record order, baris 2-48 dari file input"
- "Produk teratas: Kopi Susu (25 unit)" → "Sumber: baris 3,7,12,15,22,28,31,35,38,41,43,45"
- "4 order belum bayar" → "Sumber: baris dengan payment_status='unpaid': 5,11,19,27"

### 3.4 Version Pinning
- Python: 3.13.12 (managed runtime)
- Tidak ada dependensi pip untuk fungsi inti (stdlib only)
- openpyxl hanya untuk dukungan XLSX (opsional, pip-installed di env terisolasi)

## 4. Integrasi WorkBuddy

Agent beroperasi sebagai percakapan WorkBuddy:

1. **Pengguna:** "Analisa data penjualan hari ini: [unggah CSV atau berikan path]"
2. **Agent (WorkBuddy):** Panggil `opsflow.py` via Bash → terima hasil JSON terstruktur
3. **Agent:** Format hasil menjadi laporan yang dapat dibaca manusia (formatting LLM, angka deterministik)
4. **Agent:** Sajikan laporan + item tindakan + draf pesan
5. **Agent:** "Apakah Anda ingin saya menyiapkan pesan follow-up? Anda bisa review dulu sebelum kirim."
6. **Pengguna:** Setuju → Agent simpan draf ke file output untuk disalin pengguna

WorkBuddy agent TIDAK diganti oleh skrip Python. Skrip Python adalah **tool** yang digunakan agent. Agent tetap menjadi orkestrator, antarmuka, dan pengambil keputusan untuk formatting dan komunikasi.

## 5. Apa yang Bisa Ditambahkan Nanti (Pasca-MVP)

| Fitur | Cara | Kapan |
|-------|-----|------|
| Pengiriman WhatsApp | Konektor WhatsApp WorkBuddy (jika tersedia) | Pasca-hackathon |
| Penyimpanan cloud | Skill cloud-service WorkBuddy | Jika butuh persistensi data |
| Tren multi-hari | Perluas compute.py untuk handle rentang tanggal | P1 |
| Ekspor PDF | Python reportlab atau markdown→PDF | P2 |
| Dashboard web | Streamlit atau HTML statis | P2 |
| Packaging Skill | Package sebagai WorkBuddy Skill untuk marketplace | Pasca-hackathon |
