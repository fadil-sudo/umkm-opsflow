# Tahap B — Matriks Perbandingan 9 Ide

**Proyek:** UMKM OpsFlow — Tencent Cloud Hackathon Indonesia 2026
**Tanggal:** 2026-10-27
**Status:** Selesai

---

## Metodologi Skor

Setiap kandidat dinilai 1-5 pada 9 kriteria. Skor **bukan fakta objektif** — mereka mewakili penilaian builder berdasarkan bukti riset dan batasan kelayakan. Catatan pembobotan disediakan per kriteria.

| Kriteria | Bobot | Rasional |
|----------|-------|----------|
| Frekuensi & tingkat kesakitan masalah | Tinggi | Masalah harian > mingguan > bulanan untuk dampak demo |
| Kejelasan target pengguna | Tinggi | Harus menyebut persona spesifik, bukan "semua orang" |
| Potensi penghematan waktu/biaya | Sedang | Harus dapat diukur dalam demo |
| Agent melakukan tindakan nyata | Tinggi | Harus menggunakan tool, bukan sekadar chat — persyaratan hackathon |
| Kelayakan MVP dalam waktu | Tinggi | 5 hari ke deadline (27 Okt → 1 Nov) |
| Ketersediaan data uji | Sedang | Harus memiliki atau menghasilkan data uji valid |
| Kejelasan demo sebelum/sesudah | Tinggi | Juri perlu melihat perbedaan secara visual |
| Risiko privasi/keamanan | Sedang | Risiko lebih rendah lebih baik untuk MVP |
| Kesesuaian eksplisit challenge | Sedang | Harus jelas cocok dengan satu deskripsi challenge |

**Total maksimal: 45 poin.** Semakin tinggi semakin baik.

---

## Challenge A: The Workplace Brain (Learn Anywhere)

### A1: Onboarding Buddy — "90 Hari Pertama"
Agent yang membantu karyawan baru menemukan dok internal, SOP, dan orang selama onboarding.

| Kriteria | Skor | Catatan |
|----------|------|---------|
| Frekuensi & kesakitan masalah | 4 | Umum, tapi bervariasi per perusahaan |
| Kejelasan target pengguna | 4 | Karyawan baru di UKM |
| Penghematan waktu/biaya | 4 | Jam dihemat per minggu |
| Agent melakukan tindakan nyata | 3 | Sebagian besar search + summarize, tool use terbatas |
| Kelayakan MVP | 3 | Butuh korpus pengetahuan — sulit tanpa data nyata |
| Ketersediaan data uji | 2 | Butuh dok perusahaan nyata atau knowledge base sintetis |
| Demo sebelum/sesudah | 3 | Sulit memvisualisasikan dampak "pengetahuan ditemukan" |
| Risiko privasi/keamanan | 2 | Dok internal mungkin sensitif |
| Kesesuaian challenge | 5 | Cocok sempurna untuk "Learn Anywhere" |
| **Total** | **30** | |

### A2: Meeting Knowledge Extractor
Agent yang mengambil transkrip/catatan meeting dan mengekstrak keputusan, action item, dan knowledge nugget ke format yang dapat dicari.

| Kriteria | Skor | Catatan |
|----------|------|---------|
| Frekuensi & kesakitan masalah | 4 | Meeting terjadi harian di kantor |
| Kejelasan target pengguna | 4 | Semua pekerja kantor |
| Penghematan waktu/biaya | 4 | Hemat 15-30 menit per meeting |
| Agent melakukan tindakan nyata | 4 | Parse → ekstrak → struktur → simpan → notifikasi |
| Kelayakan MVP | 4 | Teks transkrip → output terstruktur, tanpa API eksternal |
| Ketersediaan data uji | 4 | Dapat menghasilkan transkrip meeting sintetis |
| Demo sebelum/sesudah | 4 | Jelas: transkrip mentah → action item bersih |
| Risiko privasi/keamanan | 2 | Konten meeting mungkin sensitif |
| Kesesuaian challenge | 4 | Cocok — "temukan pengetahuan di tempat kerja" |
| **Total** | **34** | |

### A3: SOP Builder dari Kerja yang Diamati
Agent yang membantu pekerja mendokumentasikan proses mereka sendiri dengan menjawab pertanyaan tentang apa yang mereka lakukan.

| Kriteria | Skor | Catatan |
|----------|------|---------|
| Frekuensi & kesakitan masalah | 3 | Pembuatan SOP menyakitkan tapi tidak harian |
| Kejelasan target pengguna | 3 | Pekerja yang diminta mendokumentasikan proses |
| Penghematan waktu/biaya | 3 | Hemat jam tapi jarang |
| Agent melakukan tindakan nyata | 3 | Q&A → hasilkan dok SOP |
| Kelayakan MVP | 2 | Butuh pemahaman pekerjaan aktual pekerja |
| Ketersediaan data uji | 2 | Butuh skenario domain-spesifik |
| Demo sebelum/sesudah | 3 | Q&A → SOP terformat |
| Risiko privasi/keamanan | 3 | Proses internal mungkin rahasia |
| Kesesuaian challenge | 4 | "Learn Anywhere" — mendokumentasikan pengetahuan |
| **Total** | **25** | |

---

## Challenge B: The Office Agent (Automate Better)

### B1: UMKM OpsFlow — Agent Laporan Operasional Harian ★ DIREKOMENDASIKAN
Agent yang mengubah catatan order/pengeluaran yang terpencar menjadi laporan operasional harian yang tervalidasi dengan item tindakan.

| Kriteria | Skor | Catatan |
|----------|------|---------|
| Frekuensi & kesakitan masalah | 5 | Harian untuk pemilik UMKM — ~99% bisnis Indonesia |
| Kejelasan target pengguna | 5 | Pemilik UMKM / operator bisnis kecil |
| Penghematan waktu/biaya | 5 | Menggantikan 30-60 menit kerja manual harian |
| Agent melakukan tindakan nyata | 5 | Baca CSV → parse → validasi → hitung → laporan → draf pesan |
| Kelayakan MVP | 5 | Berbasis file, Python + WorkBuddy, tanpa API eksternal |
| Ketersediaan data uji | 5 | CSV order/pengeluaran sintetis — mudah dibuat realistis |
| Demo sebelum/sesudah | 5 | Spreadsheet berantakan → laporan tervalidasi bersih + daftar tindakan |
| Risiko privasi/keamanan | 4 | Tidak butuh PII nyata; data sintetis; file lokal saja |
| Kesesuaian challenge | 5 | Sempurna: "otomasi pekerjaan kantor yang berulang" |
| **Total** | **44** | |

### B2: Konsolidator Pengeluaran Multi-Sumber
Agent yang menggabungkan laporan pengeluaran dari multiple departemen/format menjadi satu laporan bulanan terpadu.

| Kriteria | Skor | Catatan |
|----------|------|---------|
| Frekuensi & kesakitan masalah | 4 | Bulanan, tapi sangat menyakitkan saat terjadi |
| Kejelasan target pengguna | 4 | Staf finance/admin |
| Penghematan waktu/biaya | 4 | Hemat jam konsolidasi manual |
| Agent melakukan tindakan nyata | 4 | Baca multi file → normalisasi → gabung → hitung → laporan |
| Kelayakan MVP | 4 | Multi CSV → satu laporan |
| Ketersediaan data uji | 4 | Dapat buat file pengeluaran departemen sintetis |
| Demo sebelum/sesudah | 4 | 5 file berantakan → satu laporan konsolidasi bersih |
| Risiko privasi/keamanan | 3 | Data finansial sensitif |
| Kesesuaian challenge | 5 | "Otomasi pekerjaan kantor yang berulang" |
| **Total** | **36** | |

### B3: Ekstraktor Data Faktur/Resi PDF
Agent yang membaca faktur/resi PDF dan mengekstrak data terstruktur ke CSV untuk akuntansi.

| Kriteria | Skor | Catatan |
|----------|------|---------|
| Frekuensi & kesakitan masalah | 4 | Harian untuk admin/akuntansi |
| Kejelasan target pengguna | 4 | Staf admin/akuntansi |
| Penghematan waktu/biaya | 4 | Hemat entry data manual |
| Agent melakukan tindakan nyata | 4 | PDF → ekstrak → validasi → CSV |
| Kelayakan MVP | 3 | Parsing PDF tidak stabil; ekstraksi teks bervariasi |
| Ketersediaan data uji | 3 | Butuh resi PDF realistis |
| Demo sebelum/sesudah | 4 | PDF → CSV terstruktur |
| Risiko privasi/keamanan | 3 | Resi berisi data finansial |
| Kesesuaian challenge | 5 | "Otomasi pekerjaan kantor yang berulang" |
| **Total** | **30** | |

---

## Challenge C: The Creator Agent (Create Bolder)

### C1: Agent Kalender & Draf Konten
Agent yang mengambil tema/rencana konten dan menghasilkan kalender konten mingguan dengan draf post untuk multiple platform.

| Kriteria | Skor | Catatan |
|----------|------|---------|
| Frekuensi & kesakitan masalah | 4 | Harian untuk kreator solo |
| Kejelasan target pengguna | 4 | Kreator konten solo / social media manager |
| Penghematan waktu/biaya | 4 | Hemat waktu planning + drafting |
| Agent melakukan tindakan nyata | 4 | Input rencana → kalender + draf post + hashtag |
| Kelayakan MVP | 4 | Input teks → output teks, tanpa API eksternal |
| Ketersediaan data uji | 4 | Mudah buat brief konten |
| Demo sebelum/sesudah | 3 | Rencana → draf (lebih sulit tunjukkan peningkatan "kualitas") |
| Risiko privasi/keamanan | 5 | Tidak ada data sensitif |
| Kesesuaian challenge | 5 | "Bantu kreator berkarya lebih berani" |
| **Total** | **37** | |

### C2: Generator Brief Konten SEO
Agent yang mengambil keyword/topik dan menghasilkan brief konten terstruktur dengan heading, poin utama, dan meta description.

| Kriteria | Skor | Catatan |
|----------|------|---------|
| Frekuensi & kesakitan masalah | 3 | Mingguan, tidak harian |
| Kejelasan target pengguna | 3 | Content marketer |
| Penghematan waktu/biaya | 3 | Hemat waktu riset |
| Agent melakukan tindakan nyata | 3 | Sebagian besar generasi, tool use terbatas |
| Kelayakan MVP | 3 | Butuh data keyword/tren untuk bermakna |
| Ketersediaan data uji | 3 | Keyword mudah tapi data tren tidak |
| Demo sebelum/sesudah | 3 | Keyword → brief |
| Risiko privasi/keamanan | 5 | Tidak ada data sensitif |
| Kesesuaian challenge | 4 | "Create Bolder" |
| **Total** | **27** | |

### C3: Multi-Format Repurposer
Agent yang mengambil satu konten (misal: blog post) dan merepurpose ke multiple format (social post, email, outline slide).

| Kriteria | Skor | Catatan |
|----------|------|---------|
| Frekuensi & kesakitan masalah | 3 | Mingguan untuk kreator |
| Kejelasan target pengguna | 3 | Kreator konten |
| Penghematan waktu/biaya | 4 | Hemat jam reformatting |
| Agent melakukan tindakan nyata | 3 | Transformasi teks → multiple output |
| Kelayakan MVP | 4 | Teks → transformasi teks |
| Ketersediaan data uji | 4 | Mudah buat konten sumber |
| Demo sebelum/sesudah | 3 | Blog → 5 output format |
| Risiko privasi/keamanan | 5 | Tidak ada data sensitif |
| Kesesuaian challenge | 4 | "Create Bolder" |
| **Total** | **29** | |

---

## Peringkat Ringkasan

| Rank | Ide | Challenge | Total Skor | Kekuatan Utama |
|------|-----|-----------|------------|----------------|
| 1 | **B1: UMKM OpsFlow** | B | **44/45** | Kelayakan maksimum + tindakan nyata + frekuensi harian |
| 2 | C1: Kalender Konten | C | 37/45 | Demo bersih, tanpa risiko |
| 3 | B2: Konsolidator Pengeluaran | B | 36/45 | Kuat tapi kurang frequent |
| 4 | A2: Meeting Extractor | A | 34/45 | Bagus tapi butuh korpus pengetahuan |
| 5 | B3: Ekstraktor Resi PDF | B | 30/45 | Risiko parsing PDF |
| 6 | A1: Onboarding Buddy | A | 30/45 | Kelemahan ketersediaan data |
| 7 | C3: Multi-Format Repurposer | C | 29/45 | Tool use terbatas |
| 8 | C2: Generator Brief SEO | C | 27/45 | Butuh data tren |
| 9 | A3: SOP Builder | A | 25/45 | Paling sulit didemokan |

---

## Analisis Sensitivitas

### Bagaimana jika bobot "Kelayakan MVP" digandakan?

Jika kita memberi bobot tinggi pada kelayakan (mengingat deadline 5 hari), keunggulan B1 semakin besar. B1 skor 5 untuk kelayakan vs kebanyakan lainnya skor 2-4.

### Bagaimana jika bobot "Agent melakukan tindakan nyata" digandakan?

B1 dan B2 keduanya skor 5 dan 4, melebarkan keunggulan atas ide tipe A (yang sebagian besar search/summarize).

### Bagaimana jika kita hapus konteks spesifik UMKM?

Tanpa konteks UMKM Indonesia, "frekuensi masalah" B1 turun ke 4 (masih harian untuk bisnis kecil secara global). Akan seri dengan C1 di ~43. Sudut UMKM adalah pembeda, bukan tongkat.

### Risiko B1 "terlalu umum"?

**Diminimalisir oleh pembeda yang terukur:**
1. **Jejak audit** — setiap angka di laporan dapat ditelusuri ke baris sumber
2. **Penanda ketidakpastian** — agent menandai data tidak pasti/tidak valid secara eksplisit
3. **Tindakan berbasis aturan** — item tindakan dari aturan deterministik, bukan tebakan LLM
4. **Gerbang persetujuan manusia** — tidak ada tindakan eksternal tanpa konfirmasi eksplisit
5. **Perhitungan dapat direproduksi** — semua matematika adalah kode Python, bukan generasi LLM

Lima pembeda ini membedakan UMKM OpsFlow dari "chatbot generik yang merangkum spreadsheet."

---

## Keputusan

**Terpilih: B1 — UMKM OpsFlow (Challenge B: The Office Agent)**

Rasional: Total skor tertinggi (44/45), kesesuaian challenge sempurna, kelayakan MVP maksimum dalam deadline, tanpa dependensi eksternal, narasi demo jelas, dan pembeda kuat dari solusi generik.

**Alternatif yang ditolak dan alasannya:**
- C1 (Kalender Konten): Bagus tapi lebih sulit tunjukkan "tindakan nyata" — sebagian besar generasi teks
- B2 (Konsolidator Pengeluaran): Kuat tapi frekuensi bulanan kurang compelling dibanding harian
- A2 (Meeting Extractor): Butuh korpus pengetahuan yang tidak kita miliki
