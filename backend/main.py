"""
UMKM OpsFlow — FastAPI Backend
Production-grade API for the React frontend.
"""

import os
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Import pipeline modules
from opsflow import run_pipeline

app = FastAPI(
    title="UMKM OpsFlow API",
    description="AI-powered UMKM daily operations report generator",
    version="1.0.0",
)

# CORS for Vercel / local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProcessResponse(BaseModel):
    status: str
    input_file: str
    timestamp: str
    records_count: Optional[int]
    validated_count: Optional[int]
    rejected_count: Optional[int]
    metrics: Optional[dict]
    issues: list
    actions: list
    clarifications: list
    parse_warnings: list
    report_path: Optional[str]
    error: Optional[str]


@app.get("/api/status")
def health_check():
    return {"status": "ok", "service": "umkm-opsflow-api"}


@app.post("/api/process", response_model=ProcessResponse)
async def process_file(file: UploadFile = File(...)):
    """
    Upload a CSV or XLSX file and run the full OpsFlow pipeline.
    Returns validation issues, metrics, action items, and clarifications.
    """
    # Validate file extension
    ext = Path(file.filename).suffix.lower()
    if ext not in [".csv", ".xlsx", ".xls"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: {ext}. Supported: .csv, .xlsx"
        )

    # Save uploaded file to temp directory
    temp_dir = tempfile.mkdtemp(prefix="opsflow_")
    input_path = Path(temp_dir) / file.filename

    try:
        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
    finally:
        await file.close()

    # Run pipeline
    output_dir = Path(temp_dir) / "output"
    try:
        result = run_pipeline(str(input_path), str(output_dir))
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"Pipeline error: {e}")

    # Read generated report content if available
    report_content = None
    if result.get("report_path"):
        report_file = Path(result["report_path"])
        if report_file.exists():
            try:
                with open(report_file, "r", encoding="utf-8") as f:
                    report_content = f.read()
            except Exception:
                pass

    # Clean up temp files (keep in production if you want to serve them)
    shutil.rmtree(temp_dir, ignore_errors=True)

    return ProcessResponse(
        status=result.get("status", "error"),
        input_file=result.get("input_file", file.filename),
        timestamp=result.get("timestamp", datetime.now().isoformat()),
        records_count=result.get("records_count"),
        validated_count=result.get("validated_count"),
        rejected_count=result.get("rejected_count"),
        metrics=result.get("metrics"),
        issues=result.get("issues", []),
        actions=result.get("actions", []),
        clarifications=result.get("clarifications", []),
        parse_warnings=result.get("parse_warnings", []),
        report_path=None,  # Don't expose server paths
        error=result.get("error"),
    )


# Serve static frontend files
app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/favicon.svg")
def favicon():
    return FileResponse("static/favicon.svg")

@app.get("/api/info")
def api_info():
    return {
        "message": "UMKM OpsFlow API",
        "docs": "/docs",
        "health": "/api/health",
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
