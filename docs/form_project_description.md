# Project Description — Form Submission

## Project Overview: Target Scenarios, Users, and Value Proposition

**UMKM OpsFlow** adalah agent AI yang mengubah catatan order dan pengeluaran harian UMKM yang berantakan (CSV, spreadsheet, atau nota) menjadi laporan operasional harian yang tervalidasi, lengkap dengan daftar tindakan dan draf pesan follow-up.

**Target Scenario:**
- UMKM kedai kopi/FnB di Indonesia yang mencatat 30-80 transaksi per hari di buku, WhatsApp, dan spreadsheet
- Pemilik UMKM harus menyusun laporan harian manual di akhir hari
- Data sering berantakan: format tidak konsisten, duplikat, kolom kosong, catatan tersebar di banyak tempat

**Target Users:**
- Pemilik UMKM mikro (1-5 karyawan) seperti Bu Sari (38 tahun, pemilik kedai kopi)
- Tidak punya staf admin khusus
- Menggunakan Excel/spreadsheet dasar, tidak familiar dengan software akuntansi kompleks

**Value Proposition:**
- Dari 30-60 menit kompilasi manual → kurang dari 15 detik otomatis
- Laporan tervalidasi dengan penandaan isu data secara transparan
- Jejak audit: setiap angka bisa ditelusuri ke baris sumber
- Tidak ada tindakan eksternal tanpa persetujuan manusia

---

## Real World Scenario Insights

**Source of Pain Points:**
Berdasarkan riset lapangan dan observasi UMKM FnB Indonesia:
- 64% UMKM Indonesia belum menggunakan software akuntansi digital (Kemenkop UKM, 2024)
- Pencatatan manual menyebabkan error perhitungan 3-5 kali per hari
- Order yang belum dibayar sering terlupakan karena tidak ada sistem reminder
- Pemilik UMKM bekerja 12-14 jam sehari; administrasi sering ditinggalkan

**Target Audience:**
- Pemilik UMKM FnB dengan omzet Rp 5-50 juta per bulan
- Lokasi: kota besar dan menengah di Indonesia
- Tech-savvy dasar (bisa pakai Excel/WhatsApp) tapi tidak familiar dengan ERP/akuntansi software

**Core Problem Solved:**
- **Input berantakan:** CSV dengan kolom kosong, format tanggal campur, duplikat, nilai tidak masuk akal
- **Waktu kompilasi lama:** 30-60 menit per hari untuk merangkum transaksi jadi laporan
- **Error manusia:** Total salah hitung, order unpaid terlewat, duplikat tidak terdeteksi
- **Tindak lanjut terlupakan:** Tidak ada sistem untuk mengingatkan order yang belum dibayar

---

## Comprehensive Solution Design

### Business Architecture

```
Input (CSV/XLSX berantakan)
    ↓
[Parse] → Ekstrak field ke struktur standar
    ↓
[Validate] → Deteksi missing, duplikat, outlier, anomali
    ↓
[Clarify] → Tanya pengguna jika data ambigu
    ↓
[Compute] → Hitung metrik (deterministik Python)
    ↓
[Generate Report] → Laporan harian lengkap
    ↓
[Actions] → Item tindakan berbasis aturan
    ↓
[Draft Messages] → Draf WhatsApp untuk follow-up
    ↓
[Human Approval Gate] → Persetujuan sebelum kirim
    ↓
Output: Laporan + Tindakan + Draf (siap ditinjau manusia)
```

### Technical Architecture

**Stack Minimum:**
- **Frontend:** Streamlit web UI (Python, no JavaScript framework)
- **Backend Core:** Python 3.13 stdlib (no pip dependencies for CLI)
- **Storage:** Local file system (CSV/JSON/Markdown)
- **Integration:** Tencent WorkBuddy as orchestrator (agent calls scripts via Bash tool)
- **No external APIs:** 100% offline processing, no cloud dependency

**Key Components:**
| Module | Function | Deterministic? |
|--------|----------|----------------|
| `parse_input.py` | Parse CSV/XLSX, multi-language column aliases | ✅ Yes |
| `validate.py` | Detect duplicates, outliers, missing fields | ✅ Yes |
| `clarify.py` | Ambiguity detection (mixed payment, similar products) | ✅ Yes |
| `compute.py` | Revenue, expenses, net cashflow, top products | ✅ Yes |
| `actions.py` | Rule-based action items (unpaid orders, low stock) | ✅ Yes |
| `export.py` | Markdown report, CSV, JSON export | ✅ Yes |

**Separation of Probabilistic vs Deterministic:**
- **LLM (WorkBuddy):** Memahami intent pengguna, memformat laporan jadi teks natural, menyusun draf pesan
- **Python (Deterministic):** SEMUA perhitungan numerik, validasi data, aturan tindakan, deteksi ambiguitas
- **Principle:** LLM tidak pernah menghitung angka. Python tidak pernah "menebak" konten.

**How Prompts Drive AI Generation:**
WorkBuddy agent menggunakan prompt untuk:
1. **Intent classification:** "Ini data penjualan hari ini" → trigger pipeline
2. **Report formatting:** Metrik dict → laporan narrative yang mudah dibaca
3. **Message drafting:** Konteks order unpaid → draf pesan WhatsApp yang sopan
4. **Clarification:** Ambiguitas terdeteksi → pertanyaan yang jelas untuk pengguna

Semua output LLM divalidasi: angka dicek ulang dengan Python, draf pesan ditampilkan untuk review manusia.

---

## Business Value

### Quantifiable Metrics (Baseline vs Agent)

| Task | Manual (Baseline) | Agent (UMKM OpsFlow) | Improvement |
|------|-------------------|----------------------|-------------|
| Kompilasi laporan harian | ~30-60 menit | <15 detik | **99% faster** |
| Deteksi order unpaid | ~5 menit (kalau ingat) | <1 detik | Near-zero miss |
| Validasi data quality | ~10 menit (jarang dilakukan) | <1 detik | Komprehensif |
| Siapkan draf follow-up | ~10 menit per pesan | <1 detik | Instan |
| Error perhitungan | 3-5 per hari | 0 (deterministik) | **100% accurate** |

**Monthly Impact (estimasi):**
- Waktu dihemat: ~25 jam/bulan → bisa dialokasikan ke operasional
- Order unpaid terdeteksi: Rp 222.000 per hari (dari demo) → ~Rp 6.6 juta/bulan tidak terlewat
- Error kompilasi: Dihilangkan → kepercayaan data meningkat

### Non-Quantifiable Impact
- **Peace of mind:** Pemilik UMKM tahu laporan akurat dan tervalidasi
- **Audit trail:** Bisa ditelusuri ke baris sumber jika ada dispute
- **Scalability:** Tanpa software mahal, tanpa training karyawan baru
- **Akuntabilitas:** 5 aturan accountability (SOURCES, PERMISSIONS, APPROVAL, LIMITS, RECORD)

---

*Dibuat untuk submission Tencent Cloud Hackathon Indonesia 2026 — Challenge B: The Office Agent*
