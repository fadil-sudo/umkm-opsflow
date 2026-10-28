# Tahap A — Laporan Riset: Lanskap Masalah & Teknologi

**Proyek:** UMKM OpsFlow — Tencent Cloud Hackathon Indonesia 2026
**Tanggal:** 2026-10-27
**Penulis:** Builder (mahasiswa Sistem Informasi)
**Status:** Selesai

---

## 1. Verifikasi Hackathon

### 1.1 Sumber Resmi yang Diperiksa

| Sumber | URL | Tanggal Akses | Tipe | Temuan Utama |
|--------|-----|---------------|------|--------------|
| Portal Kontes Tencent | https://tch.tencentcloud.com/contest/47 | 2026-10-27 | Resmi | Konfirmasi tanggal, challenge, hadiah |
| Halaman Event AIClub | https://aiclub.id/tencent-cloud-hackathon | 2026-10-27 | Komunitas/Penyelenggara | Konfirmasi tanggal yang sama, detail tambahan tentang Demo Day |
| **Handbook Resmi (PDF)** | `AI CAN DO IT Tencent Cloud Hackathon Indonesia 2026 Handbook.pdf` | 2026-10-28 | **Resmi (Otoritatif)** | 19 halaman: aturan lengkap, timeline, persyaratan submission, dimensi penilaian, contoh tes |
| Dokumentasi WorkBuddy Skills | https://open.workbuddy.cn/en/docs/skill | 2026-10-27 | Dokumentasi Resmi | Struktur Skill: SKILL.md + references/ + scripts/ + templates/ |
| Dokumentasi WorkBuddy Connector | https://open.workbuddy.cn/en/docs/connector | 2026-10-27 | Dokumentasi Resmi | MCP + Skill atau CLI + Skill; satu MCP server per connector |

### 1.2 Tanggal Penting yang Dikonfirmasi

| Event | Tanggal | Tingkat Kepercayaan Sumber |
|-------|---------|-----------------------------|
| Pendaftaran Dibuka & Kick-off | 15 Okt 2026 | Tinggi — handbook resmi (hal. 13) |
| Online Training (Sumopod & AiClub.ID) | 15 Okt – 1 Nov 2026 | Tinggi — handbook resmi (hal. 13) |
| **Deadline Submission** | **1 Nov 2026** | Tinggi — handbook resmi (hal. 13) |
| **Pengumuman Finalis** | **10 Nov 2026** | Tinggi — handbook resmi (hal. 13) (KOREKSI: sebelumnya 14 Nov dari web) |
| Demo Day & Award Ceremony | 27 Nov 2026 | Tinggi — handbook resmi (hal. 13) |

**Catatan koreksi:** Riset awal dari web menyebut pengumuman finalis 14 Nov. Handbook resmi (hal. 13) menyebut **10 November 2026**. Kami menggunakan tanggal handbook sebagai sumber otoritatif. Form submission resmi: https://forms.gle/y1aHBH4BsrytXDxdA

### 1.3 Tiga Challenge (dari Handbook Resmi, Hal. 3)

| Challenge | Untuk Siapa | Masalah Nyata | Yang Harus Dibangun |
|-----------|-------------|---------------|---------------------|
| A: The Workplace Brain | HR, operasi, team lead, pegawai negeri | Pengetahuan perusahaan terpencar di chat, drive, task board. AI yang membaca semua bisa juga membocorkan semua. | Asisten yang menjawab pertanyaan staf, mengutip sumber, tidak pernah menampilkan info yang tidak diizinkan |
| B: The Office Agent | Admin, finance, founder, pemilik UMKM | Permintaan kantor datang sebagai chat panjang/voice note dengan banyak tugas. Agent otonom bisa kirim ke orang salah atau jadwal salah. | Agent yang menafsirkan permintaan tidak terstruktur, minta klarifikasi saat ambigu, tidak pernah kirim/jadwalkan/modifikasi tanpa persetujuan manusia |
| C: The Creator Agent | Marketer, kreator, edukator, penjual online | Konten harus dibuat cepat, tapi kesalahan fakta/klaim berlebihan bisa mahal (regulasi BPOM, halal). | Tim AI agent (Planner, Writer, Reviewer) yang menghasilkan konten multi-platform, menolak yang melanggar aturan, remediasi sampai lulus |

### 1.3.1 Lima Aturan Akuntabilitas (Berlaku untuk SEMUA Challenge)

Handbook (hal. 2) menetapkan 5 aturan yang dinilai untuk semua challenge:

1. **Menunjukkan sumbernya** (SOURCES) — mengatribusikan setiap jawaban ke sumbernya
2. **Tetap dalam izin** (PERMISSIONS) — hanya melihat/menggunakan apa yang diizinkan pengguna
3. **Bertanya sebelum bertindak** (APPROVAL) — manusia menyetujui apa pun yang dikirim/dipesan/diubah/dipublikasikan
4. **Mengakui batasannya** (LIMITS) — mengatakan "saya tidak tahu" alih-alih berhalusinasi, menandai masalah
5. **Menyimpan catatan** (RECORD) — mencatat apa yang dilihat, diputuskan, dilakukan, sehingga dapat diperiksa

### 1.3.2 Konteks Regulasi

> "Dari 16 Januari 2027, PP 33/2026 Indonesia mewajibkan data-protection impact assessment saat AI memproses data pribadi. Perusahaan hanya akan menggunakan agent jika mereka dapat memeriksa apa yang agent lakukan." — Handbook hal. 3

### 1.4 Hadiah (dari Handbook Resmi, Hal. 17)

| Hadiah | Jumlah Tim | Prize |
|--------|-----------|-------|
| First Prize | 1 | USD 1.200 + 3.000 WorkBuddy credits |
| Second Prize | 1 | USD 800 + 2.000 WorkBuddy credits |
| Third Prize | 1 | USD 500 + 1.000 WorkBuddy credits |

**Total: USD 2.500.** Semua peserta yang berhasil submit menerima sertifikat resmi Tencent Cloud. Pendaftaran: 1.000 WorkBuddy credits per orang.

### 1.5 Persyaratan Platform & Partisipasi

- Platform utama: **Tencent WorkBuddy** — "Build an AI agent that solves a real problem at work and can be held accountable for what it does." (Handbook hal. 2)
- Tim: 1-3 anggota, semua peserta harus berbasis di Indonesia
- Pendaftaran: https://qdrl.qq.com/fc97Jrkr
- Submission: https://forms.gle/y1aHBH4BsrytXDxdA
- "No deep coding required. Build with Tencent Cloud WorkBuddy. The hard part is designing an agent people can rely on." — Handbook hal. 2

---

## 2. Audit Platform WorkBuddy — Tools yang Tersedia di Sesi Ini

### 2.1 Kapabilitas Bawaan yang Tersedia

| Kapabilitas | Status | Catatan |
|-------------|--------|---------|
| Baca/Tulis/Edit File | Tersedia | Akses filesystem penuh di workspace |
| Eksekusi Bash/PowerShell | Tersedia | Python 3.13.12, Node 22.22.2 |
| Web Search | Tersedia | Pencarian web real-time |
| Web Fetch | Tersedia | Pengambilan konten URL |
| Task Management | Tersedia | Pelacakan tugas bawaan |
| Visualizer (show_widget) | Tersedia | Diagram SVG/HTML inline |
| Sistem Memory | Tersedia | Level pengguna + level workspace |

### 2.2 Skills yang Tersedia di Sesi

| Skill | Tujuan |
|-------|--------|
| workbuddy-sheetagent | Baca/tulis/analisis file Excel/xlsx/csv |
| workbuddy-sheet-generation | Hasilkan workbook Excel baru |
| workbuddy-pptx | Buat/edit file PowerPoint |
| workbuddy-docx | Buat/edit dokumen Word |
| workbuddy-office-routing | Rutekan ke skill Office yang benar |
| workbuddy-local-office-edit | Edit file Office/WPS lokal |
| tencent-docs | Integrasi Tencent Docs |
| cloud-service | Backend-as-a-service (DB, auth, storage, LLM) |
| sites (publish) | Deploy proyek sebagai link online |
| pdf | Membaca/memproses PDF |
| agent-browser | Otomasi browser |
| recommend-connectors | Cari/rekomendasikan konektor |
| recommend-experts | Cari/rekomendasikan expert |

### 2.3 Tools Deferred (tersedia via ToolSearch)

| Tool | Tujuan |
|------|--------|
| ImageGen | Generasi gambar dari teks |
| VideoGen | Generasi video dari teks |
| mcp__sheetagent | Manipulasi spreadsheet penuh |
| connect_cloud_service | Kredensial cloud service |
| conversation_search | Pencarian percakapan historis |

### 2.4 Konektor Tidak Terikat

Tidak ada konektor eksternal yang terikat saat ini. Konektor WeCom dimatikan secara eksplisit. Tidak ada API key berbayar yang tersedia. Demo harus berjalan dengan input berbasis file dan data sintetis saja.

### 2.5 Batasan Utama

**Tidak ada API key eksternal, tidak ada layanan berbayar, tidak ada cloud credits yang dikonfirmasi.** MVP harus dapat didemokan sepenuhnya dengan:
- File lokal (CSV/XLSX)
- Skrip Python (parsing, validasi, kalkulasi)
- WorkBuddy agent sebagai orkestrator workflow
- Data demo sintetis yang diberi label jelas

---

## 3. Riset Pola Agentic AI

### 3.1 Pola Berulang dari Proyek Hackathon dan Industri

Berdasarkan web search (2026-10-27) dan review dokumentasi, pola berulang dalam proyek agentic AI:

1. **Orkestrasi tool-use** — Agent memilih dan memanggil tool deterministik (bukan menghasilkan angka via LLM). Sumber: Microsoft AI Agents Hack series, laporan otomasi agentic Genpact (2025-02-28). URL: https://www.genpact.com/insight/agentic-process-automation-the-future-of-intelligent-automation

2. **Human-in-the-loop untuk tindakan destruktif** — Agent yang memerlukan konfirmasi sebelum mengirim, memodifikasi, atau menghapus. Ini adalah best practice eksplisit dalam dokumentasi konektor WorkBuddy (aturan konfirmasi untuk operasi berisiko tinggi).

3. **Pemisahan probabilistik vs deterministik** — LLM menangani pemahaman, ekstraksi, dan penalaran; kode deterministik menangani kalkulasi, validasi, dan penyimpanan. Sumber: berbagai situs vendor agentic AI (CodeTiburon, NxtAspect, ChubbyDeveloper — semua diakses 2026-10-27).

4. **Jejak audit** — Agent sukses mencatat sumber, asumsi, dan hasil intermediate sehingga output dapat diverifikasi. Ini adalah pembeda dari chatbot "black box".

5. **Validasi data sebelum tindakan** — Agent memvalidasi kualitas data input (field hilang, duplikat, outlier) sebelum melanjutkan ke kalkulasi atau tindakan.

### 3.2 Apa yang Gagal atau Dikritik

- Agent yang "berhalusinasi angka" — menggunakan LLM untuk menghasilkan angka finansial alih-alih menghitungnya secara deterministik.
- Agent yang mengambil tindakan tanpa persetujuan manusia — mengirim email, memodifikasi database tanpa persetujuan.
- Agent yang tidak dapat menjelaskan penalarannya — tidak ada jejak audit.
- Stack yang terlalu direkayasa — menambah LangChain, vector DB, orkestrasi multi-agent ketika workflow sederhana sudah cukup.

### 3.3 Pola yang Akan Kami Ikuti

**Input → Parse → Validasi → Hitung (deterministik) → Laporan → Persetujuan Manusia → Tindakan**

LLM menangani: memahami intent pengguna, mengekstrak data terstruktur dari input semi-terstruktur, menyusun draf pesan, menjelaskan hasil. Python menangani: semua kalkulasi numerik, aturan validasi, penegakan skema data. WorkBuddy menangani: orkestrasi workflow, interaksi pengguna, file I/O.

---

## 4. Riset Masalah — 5-8 Pain Point Kerja Nyata

### 4.1 Konteks UMKM Indonesia

Berdasarkan sumber akademik (diakses 2026-10-27):
- ~99% unit bisnis Indonesia adalah UMKM (usaha mikro/kecil/menengah) — Sumber: journal.uad.ac.id, jom.unri.ac.id
- tantangan utama: kualitas SDM rendah, adopsi IT terbatas, pencatatan manual, kurangnya pelaporan keuangan
- Banyak pemilik UMKM mencatat order/pengeluaran via buku catatan kertas, pesan WhatsApp, atau spreadsheet sederhana
- Pelaporan operasional harian jarang dilakukan — pemilik "merasakan" bisnisnya alih-alih mengukurnya

### 4.2 Pain Point yang Teridentifikasi

| # | Pain Point | Frekuensi | Target Pengguna | Dapat Didemo? | Cocok Challenge |
|---|-----------|-----------|-----------------|---------------|-----------------|
| 1 | Pemilik UMKM kompilasi penjualan/pengeluaran harian dari catatan terpencar | Harian | Pemilik UMKM | Ya — input CSV → laporan | B (Office Agent) |
| 2 | Karyawan kantor mengkonsolidasi laporan pengeluaran multi-departemen | Mingguan | Staf admin/finance | Ya — multi CSV → laporan gabungan | B (Office Agent) |
| 3 | Karyawan baru kesulitan menemukan pengetahuan/dok internal lintas tool | Mingguan | Karyawan baru | Ya — Q&A atas dok | A (Workplace Brain) |
| 4 | Kreator mengelola kalender konten dan draf lintas platform | Harian | Kreator solo | Ya — input rencana → jadwal + draf | C (Creator Agent) |
| 5 | Tim kecil melacak action item meeting yang hilang | Mingguan | Tim lead | Ya — transkrip → action items | B (Office Agent) |
| 6 | Freelancer mengirim faktur berulang dan lacak status pembayaran | Bulanan | Freelancer | Ya — daftar klien → faktur + tracker | B (Office Agent) |
| 7 | Tim marketing menghasilkan brief konten SEO dari data tren | Mingguan | Content marketer | Ya — keyword → brief | C (Creator Agent) |
| 8 | Admin kantor mengekstrak data dari faktur/resi PDF ke record terstruktur | Harian | Staf admin | Ya — PDF → CSV | B (Office Agent) |

### 4.3 Fokus yang Direkomendasikan

**Pain Point #1 (pelaporan operasional harian UMKM)** direkomendasikan karena:
- Frekuensi tertinggi (harian)
- Target pengguna paling jelas (pemilik UMKM — populasi besar di Indonesia)
- Nilai paling nyata (waktu yang dihemat pada pelaporan harian)
- Alur demo paling bersih (CSV berantakan → laporan tervalidasi + item tindakan)
- Cocok paling kuat dengan Challenge B (The Office Agent — Automate Better)
- Tidak butuh API eksternal — berbasis file, menggunakan data sintetis
- Native WorkBuddy: agent mengorkestrasi seluruh workflow

---

## 5. Ringkasan Temuan

| Pertanyaan | Jawaban | Kepercayaan | Bukti |
|-----------|---------|-------------|-------|
| Deadline dikonfirmasi? | 1 Nov 2026, 23:59 WIB | Tinggi | Dua sumber independen setuju |
| Demo Day dikonfirmasi? | 27 Nov 2026, Jakarta Selatan | Tinggi | Kedua sumber setuju |
| WorkBuddy adalah platform wajib? | Ya | Tinggi | Dinyatakan eksplisit di portal kontes |
| API eksternal tersedia? | Tidak | Tinggi | Tidak ada konektor terikat, tidak ada API key di sesi |
| Bisakah kami bangun demo berbasis file? | Ya | Tinggi | Python + file I/O + WorkBuddy agent |
| Apakah pelaporan operasional UMKM masalah nyata? | Ya | Sedang-Tinggi | Sumber akademik mengkonfirmasi tantangan IT UMKM; frekuensi self-evident |
| Bisakah agent melakukan tindakan nyata? | Ya — baca, validasi, hitung, usulkan | Tinggi | Python deterministik + orkestrasi LLM |

---

## 6. Langkah Selanjutnya

1. Buat matriks 9 ide (Tahap B) → **BERJALAN di file selanjutnya**
2. Pilih dan definisikan MVP (Tahap C)
3. Tulis spesifikasi produk (Tahap D)
4. Desain arsitektur (Tahap E)
5. Bangun vertical slice (Tahap F)
6. Siapkan paket submission (Tahap G)
