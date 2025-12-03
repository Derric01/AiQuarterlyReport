# Deployment Guide - AI Quarterly Reports

## 🚀 Render Deployment (Single Service)

This application is configured to deploy as a **single web service** on Render, with the FastAPI backend serving the React frontend as static files.

### Prerequisites

1. **GitHub Repository**: Push your code to GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Environment Variables**: Prepare your API keys

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### Step 2: Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ai-quarterly-reports`
   - **Environment**: `Python 3`
   - **Build Command**: (Auto-detected from `render.yaml`)
   - **Start Command**: (Auto-detected from `Procfile`)

### Step 3: Environment Variables

Add these in Render dashboard under "Environment":

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

**Important**: Never commit API keys to git!

### Step 4: Deploy

Click **"Create Web Service"** - Render will:
1. Install Python dependencies (requirements.txt)
2. Install Node.js and npm
3. Build frontend (npm run build)
4. Start backend server serving frontend

### Deployment Architecture

```
Render Web Service (Single Container)
│
├─ Backend (FastAPI - Port 8000)
│  ├─ API Endpoints (/fetch, /metrics, /report-ai, /validate-ai, /style-score-ai)
│  ├─ ChromaDB Vector Store
│  └─ Static File Serving
│
└─ Frontend (React Production Build)
   ├─ Served from /frontend/dist
   ├─ Accessed via root URL (/)
   └─ API calls use relative URLs
```

## 🧪 Testing Locally in Production Mode

Before deploying, test the production setup locally:

### 1. Build Frontend

```bash
cd frontend
npm run build
cd ..
```

### 2. Set Environment Variable

**Windows PowerShell:**
```powershell
$env:GOOGLE_API_KEY="your_api_key"
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="your_api_key"
```

### 3. Start Backend (Serves Frontend)

```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Test

Open browser to `http://localhost:8000` - you should see the full application.

## 📁 Project Structure

```
ai-quarterly-reports/
├── backend/
│   ├── main.py              # FastAPI app with static file serving
│   ├── requirements.txt      # Python dependencies
│   ├── ai/
│   │   ├── generator_simple.py
│   │   ├── validator_simple.py
│   │   └── style_scorer_simple.py
│   └── data/
│       └── market_data.csv
├── frontend/
│   ├── dist/                 # Production build (served by backend)
│   ├── src/
│   └── package.json
├── package.json              # Root build scripts
├── render.yaml               # Render deployment config
├── Procfile                  # Start command
└── .gitignore

```

## 🔧 Configuration Files

### render.yaml
Defines infrastructure as code:
- Python 3.11.0, Node 20.0.0
- Build commands (pip install, npm install, build frontend)
- Environment variables
- Health check endpoint

### Procfile
Defines start command:
```
web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

### package.json (Root)
Build script runs frontend build:
```json
{
  "scripts": {
    "build": "cd frontend && npm install && npm run build"
  }
}
```

## 🌐 Production URLs

After deployment, Render provides:
- **Application URL**: `https://ai-quarterly-reports.onrender.com`
- **API Base**: Same URL (relative paths)
- **Health Check**: `https://ai-quarterly-reports.onrender.com/health`

## 🐛 Troubleshooting

### Build Fails
- Check Render build logs
- Verify all dependencies in requirements.txt
- Ensure Node.js version compatibility (18+)

### 502 Bad Gateway
- Check if backend is listening on `$PORT` (Render sets this)
- Verify uvicorn starts successfully in logs

### API Calls Fail
- Check GOOGLE_API_KEY is set in Render environment
- Verify API endpoints return 200 in health check

### Frontend Not Loading
- Ensure frontend/dist exists after build
- Check main.py mounts StaticFiles correctly
- Verify SPA fallback returns index.html

## 📊 Performance

**Expected Cold Start**: 30-60 seconds (first request after idle)
**Response Time**: 
- Market data fetch: 2-5s
- AI report generation: 15-30s (Gemini API)
- Style scoring: 8-15s (embeddings + Gemini)

## 🔒 Security

- ✅ CORS configured for production domain
- ✅ API keys stored as environment variables
- ✅ No sensitive data in git
- ✅ ChromaDB data persists in container

## 💰 Cost Estimate (Render Free Tier)

- **Web Service**: Free (spins down after 15 min idle)
- **Bandwidth**: 100 GB/month free
- **Build Minutes**: 500 min/month free

**Gemini API**: Pay per request (see Google pricing)

## 🚀 Next Steps After Deployment

1. **Custom Domain**: Add in Render settings
2. **Monitoring**: Enable Render metrics dashboard
3. **Scaling**: Upgrade to paid tier for 24/7 uptime
4. **Database**: Add persistent PostgreSQL for production data
5. **CI/CD**: Auto-deploy on git push (already configured)

## 📝 Maintenance

### Update Application
```bash
git add .
git commit -m "Update feature"
git push
```
Render auto-deploys on push to main branch.

### View Logs
Render Dashboard → Your Service → Logs (real-time)

### Rollback
Render Dashboard → Your Service → Deploys → Redeploy previous version

---

**Ready to deploy?** Push to GitHub and create your Render service! 🎉
