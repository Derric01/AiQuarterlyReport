# AI Quarterly Report Generator

An automated system that generates quarterly equity market reports using real financial data and AI validation.

## Features

- **Data Collection**: Fetches ACWI and S&P 500 market data
- **Report Generation**: Creates quarterly reports using Google Gemini AI
- **Validation System**: Validates reports with deterministic and AI-powered checks
- **Style Matching**: Compares report style against historical examples using RAG

## Technology Stack

- **Frontend**: React, Tailwind CSS, ShadCN UI
- **Backend**: FastAPI, Python
- **AI**: Google Gemini, ChromaDB, SentenceTransformers
- **Data**: yfinance for market data

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Derric01/AiQuarterlyReport.git
cd ai-quarterly-reports
```

2. Set up backend:
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your GEMINI_API_KEY
python main.py
```

3. Set up frontend:
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `GET /fetch` - Fetch market data
- `GET /metrics` - Compute quarterly metrics
- `POST /report-ai` - Generate AI report
- `POST /validate-ai` - Validate report
- `POST /style-score-ai` - Score report style

## Environment Variables

```env
GEMINI_API_KEY=your_gemini_api_key_here
PORT=8000
```

## License

MIT License

## 📁 Project Structure

```
ai-quarterly-reports/
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── ui/         # ShadCN UI components
│   │   │   ├── Header.jsx
│   │   │   ├── ActionButtons.jsx
│   │   │   ├── MetricsCard.jsx
│   │   │   ├── ReportCard.jsx
│   │   │   ├── ValidationCard.jsx
│   │   │   └── StyleScoreCard.jsx
│   │   ├── lib/            # Utilities
│   │   │   ├── api.js      # API client
│   │   │   ├── queryClient.js
│   │   │   ├── utils.js
│   │   │   └── toast.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── backend/                  # Python FastAPI backend
│   ├── ai/                  # AI modules
│   │   ├── generator.py     # LLM report generator
│   │   ├── validator.py     # Report validator
│   │   ├── style_scorer.py  # Style similarity scorer
│   │   └── memory_loader.py # ChromaDB loader
│   ├── memory/
│   │   └── past_reports.txt # Historical reports
│   ├── data/               # Auto-created for market data
│   ├── main.py             # FastAPI application
│   ├── fetch_data.py       # Market data fetcher
│   ├── compute_metrics.py  # Metrics calculator
│   └── requirements.txt
├── .env.example            # Environment template
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** (18.0+)
- **Python** (3.8+)
- **Google Gemini API Key** (for AI features)

### Option A: Automated Setup (Recommended)

```bash
# Navigate to project directory
cd ai-quarterly-reports/backend

# Install Python dependencies
pip install -r requirements.txt

# Run automated setup script
python setup.py

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=AIzaSyBQWLpud9-WlsCG7FLpS-mbIu1TwFiviB4

# Start backend
uvicorn main:app --reload

# In a new terminal, start frontend
cd ../frontend
npm install && npm run dev
```

### Option B: Manual Setup

#### 1. Environment Setup

```bash
# Copy environment template
cp .env.example .env
```

Edit `.env` file:
```bash
GEMINI_API_KEY=AIzaSyBQWLpud9-WlsCG7FLpS-mbIu1TwFiviB4
```

#### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create sample data (optional)
python create_sample_data.py

# Start FastAPI server
uvicorn main:app --reload
```

The backend will be available at: `http://localhost:8000`

#### 3. Frontend Setup

```bash
# Open new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at: `http://localhost:3000`

## 📖 Usage Guide

### Step 1: Fetch Market Data
Click **"Fetch Data"** to download the latest ACWI and S&P 500 market data using yfinance.

### Step 2: Compute Metrics
Click **"Compute Metrics"** to calculate:
- Quarterly returns for ACWI and S&P 500
- Year-to-date (YTD) performance
- Number of new market highs

### Step 3: Generate AI Report
Click **"Generate Report (AI)"** to create a professional two-paragraph quarterly report using Google Gemini 1.5 Pro. The AI uses only the computed metrics and follows the style of historical reports.

### Step 4: Validate Report
Click **"Validate Report (AI)"** to run dual validation:
- **Deterministic**: Checks if all numbers match computed metrics
- **Semantic**: AI validates for fabricated facts or inconsistencies

### Step 5: Style Analysis
Click **"Style Score (AI)"** to get a similarity score based on:
- SentenceTransformers embeddings comparison with historical reports
- RAG-based retrieval of similar past reports
- Cosine similarity scoring (0-100%)

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API status |
| GET | `/fetch` | Fetch market data |
| GET | `/metrics` | Compute financial metrics |
| POST | `/report-ai` | Generate AI report |
| POST | `/validate-ai` | Validate report |
| POST | `/style-score-ai` | Style similarity score |
| GET | `/health` | Health check |

## 🧠 AI Components

### 1. Report Generator (`ai/generator.py`)
- Uses Google Gemini 1.5 Pro
- Generates exactly two paragraphs
- Strict adherence to provided metrics
- Professional financial writing style

### 2. Report Validator (`ai/validator.py`)
- **Deterministic Validation**: Number matching with tolerance
- **Semantic Validation**: AI-powered fact checking
- Error detection and reporting

### 3. Style Scorer (`ai/style_scorer.py`)
- Generates embeddings using SentenceTransformers
- Stores in ChromaDB vector database
- Cosine similarity calculation
- Returns top 3 similar historical reports

### 4. Memory Loader (`ai/memory_loader.py`)
- Loads historical reports into ChromaDB
- Automatic text splitting and embedding
- Persistent vector storage

## 📊 Sample Metrics Output

```json
{
  "acwi_quarter_return": 8.2,
  "sp500_quarter_return": 10.6,
  "acwi_ytd_return": 8.2,
  "sp500_ytd_return": 10.6,
  "acwi_new_highs": 21,
  "sp500_new_highs": 21,
  "quarter": "Q1 2024",
  "period_start": "2024-01-01",
  "period_end": "2024-03-31"
}
```

## 🛠️ Development

### Frontend Development
```bash
cd frontend
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
```

### Backend Development
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Variables
- `GEMINI_API_KEY`: Required for all AI features
- `GEMINI_MODEL`: Optional, defaults to gemini-1.5-pro
- `GEMINI_TEMPERATURE`: Optional, defaults to 0.3

## 🎨 UI Components

### Built with ShadCN UI
- **ActionButtons**: Five main action buttons with loading states
- **MetricsCard**: JSON metrics viewer with collapsible display
- **ReportCard**: Generated report with copy, download, regenerate options
- **ValidationCard**: Color-coded validation results with error details
- **StyleScoreCard**: Style similarity percentage with retrieved examples

### Styling Features
- Gradient backgrounds and text
- Smooth Framer Motion animations
- Responsive grid layouts
- Professional color schemes
- Loading skeletons
- Toast notifications

## 🚀 Deployment

### Frontend Deployment
```bash
cd frontend
npm run build
# Deploy 'dist' folder to your hosting service
```

### Backend Deployment
```bash
cd backend
# Install dependencies
pip install -r requirements.txt
# Run with production ASGI server
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

For questions or support:
- Create an issue in the repository
- Check the API documentation at `http://localhost:8000/docs`
- Review the health check endpoint at `http://localhost:8000/health`

## 🌟 Acknowledgments

- **Google Gemini** for advanced LLM capabilities
- **SentenceTransformers** for semantic embeddings
- **ShadCN/UI** for beautiful React components
- **ChromaDB** for vector database functionality
- **yfinance** for market data access
- **FastAPI** for the high-performance backend
- **React** and **Vite** for the modern frontend

---

Built with ❤️ by AI Engineers for Financial Professionals