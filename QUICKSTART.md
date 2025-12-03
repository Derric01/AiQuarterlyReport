# AI Quarterly Reports - Quick Setup Guide

## 🚀 Quick Start Commands

### 1. Environment Setup
```bash
# Copy environment file
cp .env.example .env

# Edit .env with your OpenAI API key
OPENAI_API_KEY=your_key_here
```

### 2. Backend Setup (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
Backend runs on: http://localhost:8000

### 3. Frontend Setup (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on: http://localhost:3000

## 🎯 Usage Flow

1. **Fetch Data** → Downloads ACWI & S&P 500 data
2. **Compute Metrics** → Calculates quarterly returns & highs
3. **Generate Report** → AI creates professional report
4. **Validate Report** → Dual validation (numeric + semantic)
5. **Style Score** → RAG-based style matching

## 🔧 Troubleshooting

### Backend Issues
- Ensure OpenAI API key is set in `.env`
- Check Python version (3.8+)
- Install dependencies: `pip install -r requirements.txt`

### Frontend Issues
- Ensure Node.js version (18.0+)
- Clear npm cache: `npm cache clean --force`
- Reinstall dependencies: `rm -rf node_modules && npm install`

### API Connection
- Backend must be running on port 8000
- Frontend configured for localhost:8000 backend
- Check CORS settings in main.py

## 📊 Expected Output

### Metrics Example:
```json
{
  "acwi_quarter_return": 8.2,
  "sp500_quarter_return": 10.6,
  "acwi_new_highs": 21,
  "sp500_new_highs": 21
}
```

### Generated Report Example:
> "The strong market momentum continued as global equity markets posted solid gains. The MSCI All-Country World Index (ACWI) gained 8.2% for the quarter, marking 21 new record highs...
>
> The S&P 500 Index delivered strong performance with a 10.6% total return during the quarter. The index reached 21 new record highs, demonstrating continued investor confidence..."

## 🎨 UI Features

- **Enterprise Design**: Professional ShadCN UI components
- **Smooth Animations**: Framer Motion throughout
- **Responsive Layout**: Works on all devices
- **Real-time Feedback**: Loading states and toast notifications
- **Interactive Cards**: Collapsible metrics, copy/download reports

## 🔑 Required API Key

Get your OpenAI API key:
1. Go to https://platform.openai.com
2. Create account or sign in
3. Navigate to API Keys
4. Create new secret key
5. Add to `.env` file

## 📁 Key Files

- `frontend/src/App.jsx` - Main React application
- `backend/main.py` - FastAPI server
- `backend/ai/generator.py` - AI report generator
- `backend/ai/validator.py` - Report validator
- `backend/ai/style_scorer.py` - Style similarity scorer

## 🌟 Success Indicators

✅ Backend health check: http://localhost:8000/health  
✅ Frontend loads with gradient header  
✅ All 5 action buttons visible  
✅ Cards display properly  
✅ Toast notifications work  

---

**Need help?** Check the full README.md for detailed documentation.