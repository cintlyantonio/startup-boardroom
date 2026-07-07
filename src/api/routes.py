import os
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from src.api.schemas import IdeaRequest, RunResponse
from src.orchestrator.orchestrator import run_pipeline
from src.evaluation.debate_quality import count_specific_cross_references

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/download/{filename}")
async def download_pdf(filename: str):
    # Prevent path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
        
    file_path = os.path.join("generated_plans", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    return FileResponse(path=file_path, media_type="application/pdf", filename=filename)

@router.post("/run", response_model=RunResponse)
async def run_analysis(request: IdeaRequest):
    try:
        state = await run_pipeline(request.idea)
        cross_ref_count = count_specific_cross_references(state.get("debate", []))
        
        # If pdf_path is absolute or relative, just return the filename so the frontend can hit /download
        pdf_url = None
        if state.get("pdf_path"):
            pdf_filename = os.path.basename(state["pdf_path"])
            pdf_url = f"/download/{pdf_filename}"
        
        return RunResponse(
            idea=state["idea"],
            analysis=state["analysis"],
            debate=state["debate"],
            final_plan=state.get("final_plan"),
            pdf_path=pdf_url,
            warnings=state.get("warnings", []),
            cross_reference_count=cross_ref_count
        )
    except Exception as e:
        logger.exception("Pipeline failed during /run")
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline execution failed: {str(e)}"
        )
