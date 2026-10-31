# Panduan Deploy UMKM OpsFlow

## Ringkasan Arsitektur

- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: Python FastAPI + Pipeline OpsFlow
- **Database**: Tidak diperlukan (stateless processing)

---

## 1. Deploy Backend ke Render (Gratis)

### Langkah-langkah:

1. Buka [render.com](https://render.com) dan login dengan GitHub
2. Klik **New +** → **Blueprint**
3. Pilih repo `fadil-sudo/umkm-opsflow`
4. Render akan otomatis membaca `render.yaml`
5. Klik **Apply**
6. Tunggu deploy selesai (2-3 menit)
7. Catat URL backend, contoh: `https://umkm-opsflow-api.onrender.com`

### Atau deploy manual (Web Service):
1. **New +** → **Web Service**
2. Pilih repo dan branch `main`
3. Settings:
   - **Name**: `umkm-opsflow-api`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Klik **Create Web Service**

---

## 2. Deploy Frontend ke GitHub Pages (Gratis)

### Langkah-langkah:

1. Buka repo di GitHub → **Settings** → **Pages**
2. **Source**: GitHub Actions
3. Workflow sudah dibuat di `.github/workflows/deploy-frontend.yml`
4. Push ke `main` akan otomatis trigger deploy
5. URL akan muncul di Settings → Pages, contoh:
   `https://fadil-sudo.github.io/umkm-opsflow/`

### Atau deploy ke Vercel (Alternatif):
1. Buka [vercel.com](https://vercel.com) dan import repo GitHub
2. **Root Directory**: `frontend`
3. **Framework Preset**: `Vite`
4. Klik **Deploy**
5. URL akan otomatis dibuat

---

## 3. Konfigurasi API URL

Setelah backend deploy, update API URL di frontend:

### Opsi A: GitHub Pages
Edit file `frontend/src/App.jsx` baris pertama:
```js
const API_URL = 'https://umkm-opsflow-api.onrender.com/api'
```
Lalu push ulang untuk trigger redeploy.

### Opsi B: Vercel
Tambahkan Environment Variable di dashboard Vercel:
- **Name**: `VITE_API_URL`
- **Value**: `https://umkm-opsflow-api.onrender.com/api`

---

## 4. Verifikasi Deploy

### Test Backend:
```bash
curl https://umkm-opsflow-api.onrender.com/api/health
# Expected: {"status":"ok","service":"umkm-opsflow-api"}
```

### Test Frontend:
Buka URL frontend di browser, upload file CSV, dan pastikan pipeline berjalan.

---

## Catatan Penting

- **Render free tier**: Sleep setelah 15 menit idle. First request setelah sleep akan lambat (30 detik).
- **GitHub Pages**: Static hosting, cocok untuk React SPA.
- **CORS**: Sudah dikonfigurasi di backend (`allow_origins=["*"]`). Batasi di production.
