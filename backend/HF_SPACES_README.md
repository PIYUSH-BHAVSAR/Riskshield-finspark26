# RiskShield-BFSI-X — Hugging Face Spaces Deployment

## Deploy Backend to Hugging Face Spaces in 5 Minutes

### Step 1: Create Hugging Face Spaces Repository

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in:
   - **Space name:** `riskshield-bfsi-x`
   - **Space type:** Docker (or Gradio for UI)
   - **Visibility:** Public (for demo)
4. Click "Create Space"

### Step 2: Push Code to Hugging Face

```bash
# Clone your Hugging Face space (local)
git clone https://huggingface.co/spaces/YOUR-USERNAME/riskshield-bfsi-x
cd riskshield-bfsi-x

# Copy backend files from your project
cp -r /path/to/finspark26/backend/* .

# Create Dockerfile for Hugging Face
cat > Dockerfile << 'EOF'
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port (Hugging Face uses 7860)
EXPOSE 7860

# Run FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
EOF

# Commit and push
git add .
git commit -m "Deploy RiskShield backend to Hugging Face Spaces"
git push
```

### Step 3: Add Secrets (Environment Variables)

1. Go to **Space settings** → **Secrets and variables**
2. Add these secrets:

```
SUPABASE_URL=https://YOUR-PROJECT-ID.supabase.co
SUPABASE_KEY=YOUR-ANON-KEY
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR-PROJECT-ID.supabase.co:5432/postgres
DATABASE_POOL_MAX=10
FRAUD_THRESHOLD=0.6
SECURITY_TRAP_THRESHOLD=1.0
CORRELATION_WINDOW_SECONDS=900
SECRET_KEY=riskshield-bfsi-x-secure-key
ENVIRONMENT=production
FRONTEND_URL=https://YOUR-VERCEL-DOMAIN.vercel.app
```

3. Click "Save" — Hugging Face will restart your Space with new vars

### Step 4: Access Your Backend

Your API will be live at:
```
https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/api/health
```

**Monitor:** Go to Space → Logs tab to see real-time output

---

## API Endpoints Available

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | Health check |
| POST | `/api/predict` | Score transaction for fraud |
| POST | `/api/security-event` | Ingest security event |
| POST | `/api/run-correlation` | Trigger correlation engine |
| GET | `/api/alerts` | List correlated alerts |
| GET | `/api/alerts/{id}/graph` | Get graph data for alert |
| GET | `/api/analytics` | Get dashboard KPIs |

---

## Hugging Face Spaces Specifics

| Feature | Hugging Face | Detail |
|---------|--------------|--------|
| **Restart on push** | ✅ Auto | Push code → auto rebuild |
| **Secrets management** | ✅ Built-in | Environment vars stored securely |
| **GPU support** | ⚠️ Paid | Free tier uses CPU only |
| **Storage** | ⚠️ Limited | 50GB temp storage, cleared on restart |
| **Persistent DB** | ✅ Via Supabase | Use Supabase for data (not local files) |
| **HTTPS** | ✅ Yes | Auto-provided |
| **Custom domain** | ✅ Paid | Upgrade to use custom domain |
| **Rate limiting** | ✅ Default | 300 requests/hour per IP |

---

## Key Configuration

### Dockerfile for Hugging Face

The `Dockerfile` in this directory is already configured for Hugging Face:
- Uses Python 3.10 slim image (fast, lightweight)
- Installs requirements from `requirements.txt`
- Exposes port **7860** (Hugging Face standard)
- Runs FastAPI with `uvicorn` on `0.0.0.0:7860`

### app.py Configuration

The main `app.py` automatically:
- Reads env vars (Supabase credentials)
- Initializes database on startup
- Sets up CORS for Vercel frontend
- Provides health check for monitoring

---

## Testing Your Deployment

### From command line:

```bash
# Test health endpoint
curl https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/api/health

# Should return:
# {"status":"healthy","service":"RiskShield-BFSI-X","database":"connected"}

# Test from Vercel frontend:
# API_URL=https://YOUR-USERNAME-riskshield-bfsi-x.hf.space
```

### From browser:

1. Go to `https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/docs`
2. You'll see SwaggerUI with all endpoints
3. Click "Try it out" to test endpoints

---

## Troubleshooting

### Space stuck in "Building"?
- Check **Logs** tab → scroll to bottom to see error
- Common: Missing dependency in `requirements.txt`
- Fix: Add missing package, push again

### 500 Error on `/api/health`?
- Check: Supabase credentials in Space secrets
- Check: Database connection string format (URL-encode special chars)
- Fix: Update secrets, Space will restart

### Timeout on request?
- Hugging Face has 300 req/hour limit for free tier
- Paid tier: no limit
- Or scale to multiple instances

### Model file not found?
- Hugging Face clears `/tmp` on restart
- Store models in Supabase or download on startup
- Don't use local file paths

---

## Auto-Deploy from GitHub

(Optional) For continuous deployment:

1. Connect your GitHub repo to Hugging Face
2. Go to Space → **Settings > Linked Repo**
3. Select your repository
4. Space auto-deploys on every GitHub push

---

## Next Steps

1. Push backend to Hugging Face Spaces
2. Copy API URL: `https://YOUR-USERNAME-riskshield-bfsi-x.hf.space`
3. Go to **Frontend Vercel Setup** — paste this URL in `VITE_API_URL`
4. Deploy frontend to Vercel
5. Demo video time!
