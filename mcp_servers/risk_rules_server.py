from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="RiskRulesDB MCP Server")


class RiskQuery(BaseModel):
    dti_ratio: float
    credit_score: int
    loan_amount: float
    annual_income: float
    query_type: str


class RiskAssessment(BaseModel):
    dti_ratio: float
    credit_risk: str
    loan_risk: str
    anomalies: list


risk_rules = {
    "dti_thresholds": {
        "low": 30,
        "medium": 40,
        "high": 50
    },
    "credit_thresholds": {
        "excellent": 750,
        "good": 700,
        "fair": 650,
        "poor": 600
    },
    "loan_limits": {
        "low_income": 50000,
        "medium_income": 150000,
        "high_income": 500000
    }
}


@app.post("/assess_risk")
def assess_risk(query: RiskQuery):
    """MCP endpoint for financial risk assessment."""
    try:
        dti_risk = "low" if query.dti_ratio < 35 else \
                   "medium" if query.dti_ratio < 43 else "high"

        credit_risk = "low" if query.credit_score >= 750 else \
                      "medium-low" if query.credit_score >= 700 else \
                      "medium" if query.credit_score >= 650 else "high"

        loan_to_income = (query.loan_amount / query.annual_income) * 100
        loan_risk = "low" if loan_to_income <= 50 else \
                    "medium" if loan_to_income <= 100 else "high"

        anomalies = []
        if query.dti_ratio > 43:
            anomalies.append("DTI exceeds 43%")
        if query.loan_amount > query.annual_income * 2:
            anomalies.append("Loan > 2x income")

        return {
            "status": "success",
            "assessment": {
                "dti_risk": dti_risk,
                "credit_risk": credit_risk,
                "loan_risk": loan_risk,
                "anomalies": anomalies
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/rules")
def get_rules():
    """Returns current risk assessment rules."""
    return {"rules": risk_rules}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "RiskRulesDB"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
