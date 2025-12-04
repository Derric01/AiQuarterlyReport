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

# Initialize AI components lazily
report_generator = None
report_validator = None
style_scorer = None
memory_loader = None

def get_report_generator():
    """Lazy initialization of report generator"""
    global report_generator
    if report_generator is None:
        try:
            from ai.generator_simple import ReportGenerator
            report_generator = ReportGenerator()
        except Exception as e:
            print(f"⚠️ Warning: Failed to initialize ReportGenerator: {e}")
            report_generator = False
    return report_generator if report_generator is not False else None

def get_report_validator():
    """Lazy initialization of report validator"""
    global report_validator
    if report_validator is None:
        try:
            from ai.validator_simple import ReportValidator
            report_validator = ReportValidator()
        except Exception as e:
            print(f"⚠️ Warning: Failed to initialize ReportValidator: {e}")
            report_validator = False
    return report_validator if report_validator is not False else None

def get_style_scorer():
    """Lazy initialization of style scorer"""
    global style_scorer
    if style_scorer is None:
        try:
            from ai.style_scorer_simple import StyleScorer
            style_scorer = StyleScorer()
        except Exception as e:
            print(f"⚠️ Warning: Failed to initialize StyleScorer: {e}")
            style_scorer = False
    return style_scorer if style_scorer is not False else None

def get_memory_loader():
    """Lazy initialization of memory loader"""
    global memory_loader
    if memory_loader is None:
        try:
            from ai.memory_loader import MemoryLoader
            memory_loader = MemoryLoader()
            memory_loader.load_past_reports()
            print("✅ Past reports loaded into vector database")
        except Exception as e:
            print(f"⚠️ Warning: Failed to initialize MemoryLoader: {e}")
            memory_loader = False
    return memory_loader if memory_loader is not False else None

# Light startup
@app.on_event("startup")
def startup_event():
    """Light startup - no heavy AI loading"""
    print("🚀 AI Quarterly Reports API started successfully")

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
        generator = get_report_generator()
        if generator is None:
            raise HTTPException(status_code=503, detail="AI service unavailable - API key not configured")
        
        report = generator.generate(request.metrics)
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
        validator = get_report_validator()
        if validator is None:
            raise HTTPException(status_code=503, detail="AI service unavailable - API key not configured")
        
        validation_result = validator.validate(request.report, request.metrics)
        return JSONResponse(content=validation_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to validate report: {str(e)}")

@app.post("/style-score-ai")
def get_style_score_ai(request: StyleScoreRequest):
    """Get style similarity score using RAG"""
    try:
        scorer = get_style_scorer()
        if scorer is None:
            raise HTTPException(status_code=503, detail="AI service unavailable - API key not configured")
        
        style_result = scorer.score_sync(request.report)
        return JSONResponse(content=style_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to compute style score: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_components": {
            "generator": "lazy_loaded" if report_generator is None else ("ready" if report_generator else "failed"),
            "validator": "lazy_loaded" if report_validator is None else ("ready" if report_validator else "failed"),
            "style_scorer": "lazy_loaded" if style_scorer is None else ("ready" if style_scorer else "failed"),
            "memory_loader": "lazy_loaded" if memory_loader is None else ("ready" if memory_loader else "failed")
        }
    }

# Serve frontend static files in production
frontend_dist_path = Path(__file__).parent / "static"  # Changed to use backend/static
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
else:
    print(f"⚠️ Warning: Frontend static files not found at {frontend_dist_path}")
    
    # Fallback: try original path for local development
    fallback_path = Path(__file__).parent.parent / "frontend" / "dist"
    if fallback_path.exists():
        print(f"✅ Found frontend files at fallback path: {fallback_path}")
        app.mount("/assets", StaticFiles(directory=str(fallback_path / "assets")), name="assets")
        
        @app.get("/{full_path:path}")
        async def serve_frontend_fallback(full_path: str):
            file_path = fallback_path / full_path
            if file_path.is_file():
                return FileResponse(file_path)
            
            index_path = fallback_path / "index.html"
            if index_path.exists():
                return FileResponse(index_path)
            
            raise HTTPException(status_code=404, detail="Not found")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting server on port {port}")
    print(f"Environment PORT variable: {os.getenv('PORT', 'Not set')}")
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port, 
        reload=False,
        log_level="info"
    )