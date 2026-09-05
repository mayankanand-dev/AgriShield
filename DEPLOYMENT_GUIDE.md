# AgriShield Remote Cloud Deployment Plan (100% Free Resources)

This plan covers deploying the entire AgriShield ecosystem remotely so you can disconnect your phone from USB debugging, share the Android APK with anyone, and access the web dashboard worldwide with continuous live syncing.

---

## 1. Architecture & Free Cloud Provider Matrix

| Component | Repository Folder | Recommended Free Cloud Provider | Free Tier Limits & Specs |
| :--- | :--- | :--- | :--- |
| **PostgreSQL + PostGIS Database** | `backend/` DB | **Supabase** | 500 MB DB, full PostGIS extension, SSL connection pooler |
| **Integration Backend API** | `backend/` | **Render.com** (or **Koyeb**) | 512 MB RAM, free SSL (`https://...onrender.com`), automatic git deploy |
| **AI Inference Microservice** | `ai/` | **Hugging Face Spaces** (Docker) or **Render** | 16 GB RAM / 2 vCPU on HF Spaces (CPU Basic, 100% Free) |
| **Web Dashboard** | `web/` | **Vercel** / **Cloudflare Pages** | Unlimited static hosting, free custom domains, instant edge CDN |
| **Flutter Mobile App (APK)** | `app/` | **GitHub Actions Releases** | Free artifact builds & downloadable `.apk` links for any phone |

---

## 2. Step-by-Step Deployment Roadmap

### Phase 1: Managed PostGIS Database (Supabase)
1. Create a free project at [supabase.com](https://supabase.com).
2. Under **Database -> Extensions**, enable `postgis`.
3. In **Project Settings -> Database**, copy the direct URI or Session connection string:
   ```text
   postgresql+asyncpg://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```
4. Run database initialization or seeding once from your local CLI using this remote `DATABASE_URL`:
   ```bash
   cd backend
   python -m db.init_db
   python seed_db.py
   ```

---

### Phase 2: AI Microservice on Hugging Face Spaces (Port 8001)
> [!NOTE]
> PyTorch, YOLO, and EasyOCR require ~1–2 GB of disk and memory. Render's free tier limits RAM to 512MB, whereas **Hugging Face Spaces** provides **16 GB RAM / 2 vCPU for free**.

1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces) with **SDK: Docker**.
2. Add a `Dockerfile` in `ai/`:
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 7860
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
   ```
3. Set environment variables on Space: `MOCK_MODE=false`, `COPERNICUS_CLIENT_ID=...`, `OPENWEATHER_API_KEY=...`.
4. Your free public AI endpoint will be: `https://[your-username]-agrishield-ai.hf.space`.

---

### Phase 3: Integration Backend on Render.com (Port 8000)
1. Sign in to [render.com](https://render.com) using your GitHub account (`mayankanand-dev`).
2. Click **New -> Web Service** and select `AgriShield`.
3. Configure:
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. In **Environment Variables**, add:
   - `DATABASE_URL`: `postgresql+asyncpg://...` (from Supabase)
   - `SECRET_KEY`: `[generate a 32-character random string]`
   - `AI_SERVICE_URL`: `https://[your-username]-agrishield-ai.hf.space`
   - `POLYGON_RPC_URL`: `https://rpc-amoy.polygon.technology`
   - `POLYGON_PRIVATE_KEY`: `[your testnet private key]`
   - `SMART_CONTRACT_ADDRESS`: `0x479c319C22928FF293713e70F24d399220d46876`
5. Click **Create Web Service**. Render provides an HTTPS URL:
   `https://agrishield-api.onrender.com/api/v1`

---

### Phase 4: Web Dashboard on Vercel
1. Connect your repo on [vercel.com](https://vercel.com).
2. Set **Root Directory** to `web`.
3. Add Environment Variables:
   - `VITE_API_BASE_URL`: `https://agrishield-api.onrender.com/api/v1`
   - `VITE_AGMARKNET_API_KEY`: `579b464db66ec23bdd0000017b02f24f1c2140614737c4b2c4c478a8`
4. Deploy! Your admin dashboard is instantly live at `https://agrishield.vercel.app`.

---

### Phase 5: Flutter Android Release APK (Standalone Phone Installation)
To use the app without a computer or USB cable:

1. **Build the Release APK pointing to the Cloud API**:
   ```bash
   cd app
   flutter build apk --release --dart-define=API_BASE_URL=https://agrishield-api.onrender.com/api/v1
   ```
2. The generated standalone APK will be located at:
   `app/build/app/outputs/flutter-apk/app-release.apk`
3. You can transfer this single `.apk` file to your phone via Google Drive, WhatsApp, Telegram, or GitHub Releases, tap **Install**, and the app runs completely standalone.

---

## 3. Immediate Fast-Track Option (Cloudflare Tunnels or ngrok)
If you want to test everything remotely **right now in 2 minutes** without setting up new cloud accounts:
1. Run a free Cloudflare tunnel:
   ```bash
   cloudflared tunnel --url http://localhost:8000
   ```
2. Use the generated `https://xxxx.trycloudflare.com/api/v1` as the `API_BASE_URL` when compiling your Flutter APK or launching the app.
