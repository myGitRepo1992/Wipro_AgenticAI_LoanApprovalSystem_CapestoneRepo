from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import uuid
from datetime import datetime
from schemas import LoanApplication, LoanApplicationResponse
from orchestrator import process_loan_application
from config import FASTAPI_HOST, FASTAPI_PORT
from database import SessionLocal, ApplicationRecord, init_db
from sqlalchemy.orm import Session
import logging
import json

app = FastAPI(
    title="Loan Approval Microservice",
    description="Agentic AI-powered loan approval system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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


@app.post("/submit_application", response_model=LoanApplicationResponse)
async def submit_application(application: LoanApplication, db: Session = Depends(get_db)):
    """
    Submits a loan application and processes it through the
    multi-agent orchestration engine.
    """
    try:
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        unique_id = f"CASE-APP-{application.applicant_id}-{timestamp}"

        logger.info(f"Processing application {unique_id} for {application.applicant_name}")

        response = process_loan_application(application, unique_id)

        record = ApplicationRecord(
            id=unique_id,
            applicant_id=application.applicant_id,
            applicant_name=application.applicant_name,
            applicant_email=application.email,
            annual_income=application.annual_income,
            credit_score=application.credit_score,
            loan_amount=application.loan_amount,
            employment_type=application.employment_type,
            employment_years=application.employment_years,
            existing_debt=application.existing_debt,
            loan_tenure=application.loan_tenure,
            location=application.location,
            applicant_profile=response.applicant_profile.dict(),
            financial_risk=response.financial_risk.dict(),
            loan_decision=response.decision.dict(),
            compliance_action=response.compliance_action.dict(),
            overall_reasoning=response.overall_reasoning,
            status=response.status.value
        )
        db.add(record)
        db.commit()

        logger.info(f"Application {unique_id} processed with status: {response.status}")

        return response

    except Exception as e:
        db.rollback()
        logger.error(f"Application processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.get("/application_status/{application_id}")
async def get_application_status(application_id: str, db: Session = Depends(get_db)):
    """Retrieves the status of a previously submitted application."""
    try:
        record = db.query(ApplicationRecord).filter(
            ApplicationRecord.id == application_id
        ).first()

        if not record:
            raise HTTPException(status_code=404, detail="Application not found")

        return {
            "status": "success",
            "application_id": application_id,
            "data": {
                "applicant_name": record.applicant_name,
                "loan_status": record.status,
                "decision": record.loan_decision,
                "risk_assessment": record.financial_risk,
                "applicant_profile": record.applicant_profile,
                "created_at": record.created_at.isoformat()
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/applications")
async def list_applications(limit: int = 10, db: Session = Depends(get_db)):
    """Lists recent applications."""
    try:
        records = db.query(ApplicationRecord).order_by(
            ApplicationRecord.created_at.desc()
        ).limit(limit).all()

        applications = []
        for record in records:
            applications.append({
                "id": record.id,
                "applicant_name": record.applicant_name,
                "status": record.status,
                "loan_amount": record.loan_amount,
                "created_at": record.created_at.isoformat()
            })

        return {
            "status": "success",
            "count": len(applications),
            "applications": applications
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search_applications")
async def search_applications(
    search_query: str = None,
    status_filter: str = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Search applications by ID or applicant name with optional status filter."""
    try:
        query = db.query(ApplicationRecord)

        if search_query:
            search_query = f"%{search_query}%"
            query = query.filter(
                (ApplicationRecord.id.ilike(search_query)) |
                (ApplicationRecord.applicant_name.ilike(search_query)) |
                (ApplicationRecord.applicant_id.ilike(search_query))
            )

        if status_filter and status_filter.lower() in ["approved", "rejected", "review"]:
            status_val = status_filter.lower()
            query = query.filter(
                (ApplicationRecord.status == status_val) |
                (ApplicationRecord.status.like(f"%{status_val}%"))
            )

        records = query.order_by(
            ApplicationRecord.created_at.desc()
        ).limit(limit).all()

        applications = []
        for record in records:
            applications.append({
                "application_id": record.id,
                "applicant_id": record.applicant_id,
                "applicant_name": record.applicant_name,
                "email": record.applicant_email,
                "status": record.status,
                "loan_amount": record.loan_amount,
                "annual_income": record.annual_income,
                "credit_score": record.credit_score,
                "created_at": record.created_at.isoformat(),
                "risk_score": record.loan_decision.get("risk_score") if record.loan_decision else None
            })

        return {
            "status": "success",
            "count": len(applications),
            "query": search_query,
            "filter": status_filter,
            "applications": applications
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/application_details/{application_id}")
async def get_application_details(application_id: str, db: Session = Depends(get_db)):
    """Get complete details of an application."""
    try:
        record = db.query(ApplicationRecord).filter(
            ApplicationRecord.id == application_id
        ).first()

        if not record:
            raise HTTPException(status_code=404, detail="Application not found")

        return {
            "status": "success",
            "application": {
                "application_id": record.id,
                "applicant_id": record.applicant_id,
                "applicant_name": record.applicant_name,
                "email": record.applicant_email,
                "phone": getattr(record, 'applicant_phone', 'N/A'),
                "annual_income": record.annual_income,
                "credit_score": record.credit_score,
                "loan_amount": record.loan_amount,
                "loan_purpose": getattr(record, 'loan_purpose', 'N/A'),
                "existing_debt": record.existing_debt,
                "employment_type": record.employment_type,
                "employment_years": record.employment_years,
                "employment_company": getattr(record, 'employment_company', 'N/A'),
                "loan_status": record.status,
                "applicant_profile": record.applicant_profile,
                "financial_risk": record.financial_risk,
                "loan_decision": record.loan_decision,
                "compliance_action": record.compliance_action,
                "overall_reasoning": record.overall_reasoning,
                "created_at": record.created_at.isoformat(),
                "updated_at": record.updated_at.isoformat()
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/applications/all")
async def get_all_applications(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    """Get all applications with pagination."""
    try:
        total_count = db.query(ApplicationRecord).count()

        records = db.query(ApplicationRecord).order_by(
            ApplicationRecord.created_at.desc()
        ).offset(offset).limit(limit).all()

        applications = []
        for record in records:
            applications.append({
                "application_id": record.id,
                "applicant_id": record.applicant_id,
                "applicant_name": record.applicant_name,
                "status": record.status,
                "loan_amount": record.loan_amount,
                "risk_score": record.loan_decision.get("risk_score") if record.loan_decision else None,
                "created_at": record.created_at.isoformat()
            })

        return {
            "status": "success",
            "total_count": total_count,
            "returned_count": len(applications),
            "limit": limit,
            "offset": offset,
            "applications": applications
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/database_stats")
async def get_database_stats(db: Session = Depends(get_db)):
    """Get database statistics."""
    try:
        total_apps = db.query(ApplicationRecord).count()

        # Handle both enum format (LoanStatus.approved) and string format (approved)
        approved = db.query(ApplicationRecord).filter(
            (ApplicationRecord.status == "approved") |
            (ApplicationRecord.status.like("%approved%"))
        ).count()
        rejected = db.query(ApplicationRecord).filter(
            (ApplicationRecord.status == "rejected") |
            (ApplicationRecord.status.like("%rejected%"))
        ).count()
        review = db.query(ApplicationRecord).filter(
            (ApplicationRecord.status == "review") |
            (ApplicationRecord.status.like("%review%"))
        ).count()

        total_loan = db.query(ApplicationRecord).with_entities(
            ApplicationRecord.loan_amount
        ).all()
        total_loan_amount = sum([l[0] for l in total_loan]) if total_loan else 0

        avg_credit_score = db.query(ApplicationRecord).with_entities(
            ApplicationRecord.credit_score
        ).all()
        avg_credit = sum([c[0] for c in avg_credit_score]) / len(avg_credit_score) if avg_credit_score else 0

        return {
            "status": "success",
            "statistics": {
                "total_applications": total_apps,
                "approved_count": approved,
                "rejected_count": rejected,
                "review_count": review,
                "approval_rate": round(approved / total_apps * 100, 2) if total_apps > 0 else 0,
                "total_loan_amount": round(total_loan_amount, 2),
                "average_credit_score": round(avg_credit, 2)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Loan Approval Microservice",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Agentic AI Loan Approval System",
        "version": "1.0.0",
        "endpoints": {
            "submit": "/submit_application",
            "status": "/application_status/{application_id}",
            "search": "/search_applications?search_query=&status_filter=",
            "details": "/application_details/{application_id}",
            "all_applications": "/applications/all",
            "statistics": "/database_stats",
            "list": "/applications",
            "health": "/health"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=FASTAPI_HOST,
        port=FASTAPI_PORT,
        log_level="info"
    )
