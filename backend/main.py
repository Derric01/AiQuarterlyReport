from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os
from pathlib import Path
from dotenv import load_dotenv

from fetch_data import fetch_market_data
from compute_metrics import compute_quarterly_metrics
from ai.generator_simple import ReportGenerator
from ai.validator_simple import ReportValidator
from ai.style_scorer_simple import StyleScorer
from ai.memory_loader import MemoryLoader

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Quarterly Reports API",
    description="AI-powered quarterly equity market report generation system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI components
report_generator = ReportGenerator()
report_validator = ReportValidator()
style_scorer = StyleScorer()
memory_loader = MemoryLoader()

# Load memory on startup
@app.on_event("startup")
def startup_event():
    """Load past reports into memory/vector database"""
    try:
        memory_loader.load_past_reports()
        print("✅ Past reports loaded into vector database")
    except Exception as e:
        print(f"⚠️ Warning: Failed to load past reports: {e}")

# Request models
class GenerateReportRequest(BaseModel):
    metrics: dict

class ValidateReportRequest(BaseModel):
    report: str
    metrics: dict

class StyleScoreRequest(BaseModel):
    report: str

@app.get("/")
async def root():
    return {
        "message": "AI Quarterly Reports API", 
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/fetch")
async def fetch_data():
    """Fetch ACWI and S&P 500 market data"""
    try:
        result = fetch_market_data()
        return JSONResponse(content={
            "status": "success",
            "message": "Market data fetched successfully",
            "files": result.get("files", [])
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")

@app.get("/metrics")
async def get_metrics():
    """Compute quarterly metrics from fetched data"""
    try:
        metrics = compute_quarterly_metrics()
        return JSONResponse(content=metrics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to compute metrics: {str(e)}")

@app.post("/report-ai")
def generate_report_ai(request: GenerateReportRequest):
    """Generate AI-powered quarterly report"""
    try:
        report = report_generator.generate(request.metrics)
        return JSONResponse(content={
            "report": report,
            "status": "success"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@app.post("/validate-ai")
def validate_report_ai(request: ValidateReportRequest):
    """Validate report using deterministic and AI methods"""
    try:
        validation_result = report_validator.validate(request.report, request.metrics)
        return JSONResponse(content=validation_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to validate report: {str(e)}")

@app.post("/style-score-ai")
def get_style_score_ai(request: StyleScoreRequest):
    """Get style similarity score using RAG"""
    try:
        style_result = style_scorer.score_sync(request.report)
        return JSONResponse(content=style_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to compute style score: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_components": {
            "generator": "ready",
            "validator": "ready", 
            "style_scorer": "ready",
            "memory_loader": "ready"
        }
    }

# Serve frontend static files in production
frontend_dist_path = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist_path.exists():
    # Mount static assets
    app.mount("/assets", StaticFiles(directory=str(frontend_dist_path / "assets")), name="assets")
    
    # Serve index.html for all non-API routes (SPA fallback)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend for all non-API routes"""
        # If requesting a specific file that exists, serve it
        file_path = frontend_dist_path / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        
        # Otherwise serve index.html (SPA fallback)
        index_path = frontend_dist_path / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        
        raise HTTPException(status_code=404, detail="Not found")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port, 
        reload=False,
        log_level="info"
    )