from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import uvicorn
from typing import Optional
from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import SessionLocal, ApplicantCacheRecord, init_db

app = FastAPI(title="ApplicantDB MCP Server")


class ApplicantQuery(BaseModel):
    applicant_id: str
    query_type: str


class ApplicantData(BaseModel):
    applicant_id: str
    income_stability_score: float
    employment_risk: str
    credit_history_summary: str
    application_completeness_flags: list


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/analyze_applicant")
def analyze_applicant(query: ApplicantQuery, db: Session = Depends(get_db)):
    """MCP endpoint for analyzing applicant profile."""
    try:
        record = db.query(ApplicantCacheRecord).filter(
            ApplicantCacheRecord.applicant_id == query.applicant_id
        ).first()

        if not record:
            return {
                "status": "pending",
                "message": f"Applicant {query.applicant_id} profile not found"
            }

        return {
            "status": "success",
            "data": {
                "applicant_id": record.applicant_id,
                "income_stability_score": record.income_stability_score,
                "employment_risk": record.employment_risk,
                "credit_history_summary": record.credit_history_summary,
                "application_completeness_flags": record.application_completeness_flags
            },
            "query_type": query.query_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cache_applicant")
def cache_applicant(data: ApplicantData, db: Session = Depends(get_db)):
    """Caches applicant profile data in database."""
    try:
        record = db.query(ApplicantCacheRecord).filter(
            ApplicantCacheRecord.applicant_id == data.applicant_id
        ).first()

        if record:
            record.income_stability_score = data.income_stability_score
            record.employment_risk = data.employment_risk
            record.credit_history_summary = data.credit_history_summary
            record.application_completeness_flags = data.application_completeness_flags
        else:
            record = ApplicantCacheRecord(
                id=f"applicant_{data.applicant_id}",
                applicant_id=data.applicant_id,
                income_stability_score=data.income_stability_score,
                employment_risk=data.employment_risk,
                credit_history_summary=data.credit_history_summary,
                application_completeness_flags=data.application_completeness_flags
            )
            db.add(record)

        db.commit()
        return {
            "status": "success",
            "message": f"Cached applicant {data.applicant_id}"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ApplicantDB"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
