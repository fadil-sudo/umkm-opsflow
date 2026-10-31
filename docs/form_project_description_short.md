# Project Description — Form Submission (Versi Singkat)

## 1. Project Overview

UMKM OpsFlow: Agent AI yang mengubah catatan order/pengeluaran berantakan (CSV) jadi laporan operasional harian tervalidasi + daftar tindakan + draf pesan follow-up.

- **Target:** UMKM FnB (kedai kopi, warung) dengan 30-80 transaksi/hari
- **Users:** Pemilik UMKM mikro, tidak punya staf admin, pakai Excel dasar
- **Value:** 30-60 menit manual → <15 detik otomatis. Laporan akurat, jejak audit lengkap, tidak ada tindakan tanpa persetujuan.

---

## 2. Real World Scenario

**Pain points:**
- 64% UMKM Indonesia belum pakai software akuntansi (Kemenkop UKM, 2024)
- Error perhitungan 3-5 kali/hari dengan pencatatan manual
- Order belum bayar sering terlupakan
- Pemilik kerja 12-14 jam/hari, administrasi ditinggalkan

**Problem solved:**
- Data berantakan → CSV parsing otomatis
- Waktu kompilasi lama → <15 detik
- Error manusia → perhitungan deterministik 100% akurat
- Tindak lanjut terlupakan → action items otomatis

---

## 3. Solution Design

**Architecture:** Parse → Validate → Clarify → Compute → Report → Actions → Draft → Human Approval

**Stack:** Python 3.13 stdlib + Streamlit UI + WorkBuddy orchestrator. No external APIs. 100% offline.

**Prompt design:**
- LLM (WorkBuddy): intent classification, report formatting, message drafting
- Python (deterministik): SEMUA perhitungan, validasi, aturan tindakan
- LLM tidak pernah hitung angka. Python tidak pernah menebak konten.

---

## 4. Business Value

| Metric | Manual | Agent |
|--------|--------|-------|
| Laporan harian | 30-60 menit | <15 detik |
| Error perhitungan | 3-5/hari | 0 |
| Unpaid order missed | Sering | Near-zero |

**Impact:** ~25 jam/bulan dihemat. ~Rp 6.6 juta/bulan unpaid order terdeteksi. Kepercayaan data meningkat.
