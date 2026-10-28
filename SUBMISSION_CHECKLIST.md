# Submission Checklist — UMKM OpsFlow

**Tencent Cloud Hackathon Indonesia 2026**  
**Deadline: 1 November 2026, 23:59 WIB**  
**Form Submission:** https://forms.gle/y1aHBH4BsrytXDxdA

---

## Wajib Diisi di Form

### Informasi Dasar
- [ ] **Project title:** UMKM OpsFlow
- [ ] **Short blurb:** "Agent laporan harian UMKM dari data berantakan" (7 kata)
- [ ] **Team name:** (isi nama tim Anda)
- [ ] **Team members:** 1-3 orang, semua berbasis di Indonesia
- [ ] **Challenge selected:** B — The Office Agent

### Dokumen Upload
- [ ] **Project description** — Upload/README link
  - Lokasi: `README_GITHUB.md` atau `README.md`
  - Isi: Overview, target user, value, architecture, prompt design, business value
- [ ] **Accountability sheet** — Upload
  - Lokasi: `docs/accountability_sheet.md`
  - Isi: Akses agent, eksekusi otonom, persetujuan manusia, larangan
- [ ] **Test results** — Upload screenshot
  - Lokasi: Screenshot `test_output_final.txt` atau terminal saat `python tests/test_opsflow.py`
  - Hasil: 43 passed, 0 failed
- [ ] **Architecture diagram** — Upload
  - Lokasi: `docs/workflow_diagram.md`
  - Isi: 3 diagram Mermaid (workflow, layer separation, data flow)
- [ ] **Demo video** — Upload/link
  - Lokasi: File video 5-8 menit
  - Isi: Overview, capabilities, refusal/approval demo, reflection
  - Script: `docs/demo_video_script.md`
- [ ] **Product sharing** — Upload
  - Lokasi: `docs/product_sharing.md`
  - Isi: WorkBuddy value add + key insights
- [ ] **Source code** — Link
  - Lokasi: GitHub repo publik atau exported WorkBuddy workflow
  - Pastikan: Kode lengkap, bisa dijalankan, ada instruksi setup

### Opsional
- [ ] **Cover image** — Upload
  - Lokasi: `assets/cover_image.svg`
  - Ukuran: 380×216 px (16:9)
- [ ] **Project link (bonus)** — URL live/demo
  - Jika ada deployment atau demo online

---

## File yang Harus Ada di Repo/Upload

```
umkm-opsflow/
├── README.md                 # atau README_GITHUB.md
├── scripts/
│   ├── opsflow.py           # Entry point
│   ├── parse_input.py       # CSV/XLSX parser
│   ├── validate.py          # Data validation
│   ├── compute.py           # Deterministic metrics
│   ├── actions.py           # Rule-based actions
│   ├── clarify.py           # Ambiguity detection
│   └── export.py            # Report export
├── tests/
│   └── test_opsflow.py      # 43 test assertions
├── data/
│   ├── sample_orders_clean.csv
│   ├── sample_orders_messy.csv
│   ├── sample_orders_empty.csv
│   ├── sample_prompt_injection.csv
│   └── sample_ambiguous.csv
├── docs/
│   ├── accountability_sheet.md
│   ├── product_sharing.md
│   ├── demo_video_script.md
│   ├── short_blurb.md
│   ├── workflow_diagram.md
│   └── audit_final.md
└── assets/
    └── cover_image.svg
```

---

## Langkah Upload ke GitHub

1. Buat akun GitHub (jika belum punya): https://github.com/signup
2. Buat repository baru:
   - Name: `umkm-opsflow` (atau nama yang Anda suka)
   - Visibility: **Public**
   - Add README: No (kita sudah punya)
3. Upload file:
   ```bash
   # Di direktori umkm-opsflow
   git init
   git add .
   git commit -m "Initial commit: UMKM OpsFlow hackathon submission"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/umkm-opsflow.git
   git push -u origin main
   ```
4. Verifikasi: Buka repo di browser, pastikan semua file terlihat
5. Copy URL repo untuk form submission

---

## Langkah Screenshot Test Results

1. Buka terminal di direktori `umkm-opsflow`
2. Jalankan: `python tests/test_opsflow.py`
3. Screenshot bagian:
   ```
   ============================================================
     TEST RESULTS: 43 passed, 0 failed, 43 total
   ============================================================
   ```
4. Simpan sebagai PNG/JPG
5. Upload ke form submission

---

## Langkah Rekam Demo Video

1. Baca script: `docs/demo_video_script.md`
2. Setup screen recorder (OBS Studio / Loom / Windows Game Bar)
3. Resolusi: 1920×1080
4. Rekam 8 scene sesuai script:
   - Scene 1: Hook & masalah (spreadsheet berantakan)
   - Scene 2: Solusi UMKM OpsFlow
   - Scene 3: Demo data bersih
   - Scene 4: Demo data berantakan + validasi
   - Scene 5: Prompt injection resistance
   - Scene 6: Human approval gate
   - Scene 7: Test results
   - Scene 8: Refleksi & closing
5. Edit dan export sebagai MP4
6. Upload ke YouTube (unlisted) atau Google Drive
7. Copy link untuk form submission

---

## Final Review Sebelum Submit

- [ ] Semua field form diisi lengkap
- [ ] Semua dokumen di-upload
- [ ] Link repo/GitHub berfungsi
- [ ] Demo video bisa di-play
- [ ] Test results screenshot jelas
- [ ] Cover image sesuai ukuran (jika di-upload)
- [ ] Informasi tim benar
- [ ] Challenge yang dipilih benar (B — The Office Agent)

---

## Setelah Submit

- Simpan konfirmasi submission (screenshot/email)
- Pantau WhatsApp group untuk update
- Siapkan untuk pengumuman finalis: **10 November 2026**
- Jika lolos, siapkan presentasi live untuk Demo Day: **27 November 2026**

---

**Good luck! 🚀**
