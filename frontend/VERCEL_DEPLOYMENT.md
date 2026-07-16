# RiskShield-BFSI-X Frontend — Vercel Deployment

## Deploy Frontend to Vercel in 3 Minutes

### Step 1: Push to GitHub

```bash
cd /path/to/finspark26/frontend

# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit - RiskShield frontend"

# Create new repo on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/riskshield-frontend.git
git push -u origin main
```

### Step 2: Connect to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "Import Project"
3. Select "From Git" → Connect GitHub
4. Search & select `riskshield-frontend` repository
5. Click "Import"

### Step 3: Configure Environment Variables

**In Vercel Dashboard:**

1. Go to **Project Settings → Environment Variables**
2. Add these variables:

```
VITE_API_URL=https://YOUR-USERNAME-riskshield-bfsi-x.hf.space
VITE_SUPABASE_URL=https://YOUR-PROJECT-ID.supabase.co
VITE_SUPABASE_ANON_KEY=YOUR-ANON-KEY
VITE_ENVIRONMENT=production
```

3. Click "Save & Deploy"

### Step 4: Deploy

Vercel will automatically:
- Detect `vite.config.js`
- Install dependencies: `npm install`
- Build: `npm run build`
- Deploy to CDN

**Your frontend is live at:**
```
https://riskshield-frontend.vercel.app
```

---

## Vite Configuration for Vercel

The `vite.config.js` should look like:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser'
  },
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  }
})
```

---

## Package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0",
    "react-router-dom": "^6.18.0",
    "d3": "^7.8.0",
    "recharts": "^2.10.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0"
  }
}
```

---

## API Client Setup

**Create `src/api/client.js`:**

```javascript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add auth token if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default apiClient;
```

---

## React Components for API Integration

### Example: Alerts Page

```jsx
import { useEffect, useState } from 'react';
import apiClient from '../api/client';

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await apiClient.get('/alerts?limit=50');
        setAlerts(response.data.alerts);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
  }, []);

  if (loading) return <div>Loading alerts...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h1>Correlated Alerts</h1>
      <table>
        <thead>
          <tr>
            <th>Alert ID</th>
            <th>Customer ID</th>
            <th>Risk Level</th>
            <th>Score</th>
            <th>Explanation</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map(alert => (
            <tr key={alert.id}>
              <td>{alert.id}</td>
              <td>{alert.customer_id}</td>
              <td>{alert.risk_level}</td>
              <td>{alert.correlated_score.toFixed(2)}</td>
              <td>{alert.explanation}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

---

## Continuous Deployment

**Automatic:** Every push to GitHub main branch:
```bash
git push origin main
# → Vercel automatically rebuilds and deploys
```

**Manual deploy:**
```bash
npm run build
vercel deploy
```

---

## Custom Domain (Optional)

1. Go to Vercel Dashboard → **Project Settings > Domains**
2. Add your custom domain (e.g., `riskshield.yourdomain.com`)
3. Update DNS records as instructed
4. Vercel auto-provisions SSL certificate

---

## Monitoring & Logs

**In Vercel Dashboard:**
1. Go to **Deployments** → Select latest
2. View **Build Logs** and **Runtime Logs**
3. Monitor **Performance** metrics
4. Set up alerts in **Settings > Alerts**

---

## Environment Variables by Stage

### Production (Vercel)
```
VITE_API_URL=https://YOUR-USERNAME-riskshield-bfsi-x.hf.space
VITE_ENVIRONMENT=production
```

### Development (Local)
```
VITE_API_URL=http://localhost:8000
VITE_ENVIRONMENT=development
```

### Testing (Preview)
```
VITE_API_URL=https://YOUR-USERNAME-riskshield-bfsi-x.hf.space
VITE_ENVIRONMENT=staging
```

---

## Troubleshooting

### Build fails with "Module not found"?
```bash
# Local fix:
npm install
npm run build

# Push and retry:
git push origin main
```

### Environment variables not working?
- Confirm variables added in Vercel **Settings > Environment Variables**
- Prefix with `VITE_` for Vite to inject them
- Redeploy after adding variables

### API calls return 404?
- Check `VITE_API_URL` matches your Hugging Face Spaces URL
- Ensure Hugging Face backend is running (check logs)
- Test: `curl https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/api/health`

### CORS errors?
- Backend must allow Vercel domain in CORS middleware
- Update in `backend/app.py`:
```python
allow_origins=[
    "https://riskshield-frontend.vercel.app",
    "https://*.vercel.app"
]
```

---

## Performance Tips

1. **Code splitting:** Vite auto-splits chunks
2. **Image optimization:** Use `<img loading="lazy">`
3. **Bundle analysis:** `npm run build -- --analyze`
4. **Caching:** Set cache headers in `vercel.json`

**vercel.json:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "headers": [
    {
      "source": "/assets/:path*",
      "headers": [
        {
          "key": "cache-control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

---

## Deployment Checklist

- [ ] GitHub repo created and connected to Vercel
- [ ] All environment variables added in Vercel dashboard
- [ ] `npm run build` works locally
- [ ] `package.json` has correct build script
- [ ] `vite.config.js` configured for Vercel
- [ ] API client points to Hugging Face backend URL
- [ ] CORS enabled on backend for Vercel domain
- [ ] Frontend deployed and accessible
- [ ] Test `/api/health` endpoint from frontend
- [ ] Demo video recorded

---

**Your frontend is now live on Vercel!**
