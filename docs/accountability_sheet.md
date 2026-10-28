# UMKM OpsFlow — Accountability Sheet

**Sesuai persyaratan submission: ringkasan 1 halaman tentang apa yang agent dapat akses, apa yang dieksekusi otonom, apa yang membutuhkan persetujuan manusia, dan apa yang tidak akan pernah dilakukan.**

---

## Apa yang Agent Dapat Akses

| Sumber Data | Cara Akses | Batasan |
|-------------|-----------|---------|
| File CSV/XLSX yang diberikan pengguna | Baca via Python (read-only) | Hanya file yang eksplisit diberikan pengguna. Tidak memindai direktori lain. |
| Tidak ada akses ke sistem eksternal | — | Tidak ada email, chat, kalender, database, atau API eksternal |
| Tidak ada akses ke internet | — | Semua pemrosesan lokal di workspace |

## Apa yang Agent Eksekusi Secara Otonom

| Tindakan | Mengapa Aman | Jejak Audit |
|----------|-------------|-------------|
| Membaca dan mem-parse file input | Read-only, tidak mengubah file | Tercatat di metrics.json |
| Memvalidasi data (field hilang, duplikat, outlier) | Analisis, tidak ada dampak eksternal | Isu tercatat di validation_issues.csv |
| Menghitung metrik (total pendapatan, pengeluaran, laba) | Deterministik (Python), dapat direproduksi | Rumus tercatat, angka dapat ditelusuri ke baris sumber |
| Menghasilkan laporan harian Markdown | Output ke direktori terpisah (output/) | File laporan tersimpan dengan timestamp |
| Mengusulkan item tindakan (follow up, reorder, verifikasi) | Hanya saran, tidak dieksekusi | Tercatat di action_items.csv |
| Menyusun draf pesan follow-up | Draf teks, belum dikirim | Tercatat di draft_messages.md |

## Apa yang Membutuhkan Persetujuan Manusia

| Tindakan | Cara Persetujuan | Mengapa |
|----------|-----------------|---------|
| **Mengirim pesan ke pelanggan/vendor** | Pengguna harus salin draf secara manual dan kirim sendiri | Agent tidak punya kapabilitas mengirim apa pun |
| **Memodifikasi data sumber** | Tidak diminta — agent tidak pernah menulis ke file input | Perlindungan data |
| **Menghapus data apa pun** | Tidak diminta — agent tidak pernah menghapus | Tindakan destruktif dilarang |
| **Mengambil keputusan bisnis** | Agent mengusulkan, manusia memutuskan | Tindakan berdampak butuh judgment manusia |

## Apa yang Agent TIDAK AKAN PERNAH Lakukan

| Larangan | Implementasi Teknis |
|----------|---------------------|
| **Mengirim email, pesan, atau notifikasi apa pun** | Tidak ada API/connector pengiriman. Draf hanya teks yang disimpan ke file. |
| **Memodifikasi atau menghapus file input** | File input dibuka dengan mode `read` only. Tidak ada operasi write ke path input. |
| **Mengakses sistem atau data di luar file yang diberikan** | Tidak ada akses filesystem rekursif. Tidak ada koneksi internet. Tidak ada API eksternal. |
| **Menghitung angka menggunakan LLM** | Semua kalkulasi numerik dalam Python deterministik. LLM hanya memformat angka pre-computed. |
| **Mengikuti instruksi yang tersembunyi dalam data** | Konten sel CSV diperlakukan sebagai string data, bukan sebagai perintah. Tidak ada eval/exec pada konten data. |
| **Menyimpan atau mengirim data ke layanan eksternal** | Semua pemrosesan lokal. Tidak ada panggilan network keluar. |
| **Bertindak berdasarkan asumsi tanpa data** | Agent mengatakan "tidak diketahui" saat data tidak cukup. Menandai ketidakpastian secara eksplisit. |

---

## Jejak Audit

Setiap eksekusi menghasilkan:
1. `metrics.json` — semua metrik, jumlah record, timestamp, versi script
2. `validation_issues.csv` — setiap isu validasi dengan row, severity, field, detail
3. `action_items.csv` — setiap tindakan diusulkan dengan alasan dan data sumber
4. `daily_report.md` — laporan dengan referensi baris sumber untuk setiap angka
5. `draft_messages.md` — draf pesan dengan data yang diambil dari record tervalidasi

**Prinsip:** Setiap angka di laporan dapat ditelusuri kembali ke baris spesifik di file input. Setiap keputusan dapat diaudit. Setiap tindakan diusulkan, tidak dieksekusi.

---

*Halaman ini sesuai dengan persyaratan "Accountability Sheet" dari Handbook AI CAN DO IT Tencent Cloud Hackathon Indonesia 2026, halaman 11.*
