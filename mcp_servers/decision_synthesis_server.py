from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="DecisionSynthesis MCP Server")


class DecisionRequest(BaseModel):
    applicant_id: str
    risk_score: float
    income_stability: float
    employment_risk: str
    credit_risk: str
    dti_ratio: float


class DecisionResult(BaseModel):
    classification: str
    risk_score: float
    confidence: float
    factors: list


decision_cache = {}


@app.post("/synthesize_decision")
def synthesize_decision(request: DecisionRequest):
    """MCP endpoint for decision synthesis."""
    try:
        if request.risk_score < 40:
            decision = "approved"
            confidence = 0.90
        elif request.risk_score < 60:
            decision = "review"
            confidence = 0.70
        else:
            decision = "rejected"
            confidence = 0.85

        factors = []
        if request.income_stability > 70:
            factors.append("Strong income stability")
        if request.employment_risk == "low":
            factors.append("Stable employment")
        if request.credit_risk == "low":
            factors.append("Good credit")
        if request.dti_ratio < 35:
            factors.append("Healthy DTI")

        result = {
            "applicant_id": request.applicant_id,
            "classification": decision,
            "risk_score": request.risk_score,
            "confidence": confidence,
            "factors": factors
        }

        decision_cache[request.applicant_id] = result

        return {
            "status": "success",
            "decision": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/decisions/{applicant_id}")
def get_decision(applicant_id: str):
    """Retrieves cached decision for applicant."""
    if applicant_id in decision_cache:
        return {"status": "success", "decision": decision_cache[applicant_id]}
    return {"status": "not_found"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "DecisionSynthesis"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8003)
