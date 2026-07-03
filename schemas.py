from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class LoanStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVIEW = "review"


class LoanApplication(BaseModel):
    applicant_id: str
    applicant_name: str
    email: str
    phone: str
    annual_income: float
    employment_type: str
    employment_years: int
    credit_score: int
    existing_debt: float
    loan_amount: float
    loan_purpose: str
    employment_company: str
    employment_status: str
    loan_tenure: int
    location: str


class ApplicantProfileOutput(BaseModel):
    income_stability_score: float = Field(..., ge=0, le=100)
    employment_risk: str
    credit_history_summary: str
    application_completeness_flags: List[str]


class FinancialRiskOutput(BaseModel):
    debt_to_income_ratio: float
    credit_score_risk_level: str
    loan_amount_risk: str
    anomaly_detection: List[str]
    reasoning: str


class LoanDecisionOutput(BaseModel):
    classification: LoanStatus
    risk_score: float = Field(..., ge=0, le=100)
    confidence_level: float = Field(..., ge=0, le=1)
    key_decision_factors: List[str]
    explanation: str


class ComplianceActionOutput(BaseModel):
    action_taken: str
    notification_sent: bool
    case_id: str
    timestamp: str
    summary: str


class LoanApplicationResponse(BaseModel):
    application_id: str
    status: LoanStatus
    decision: LoanDecisionOutput
    financial_risk: FinancialRiskOutput
    applicant_profile: ApplicantProfileOutput
    compliance_action: ComplianceActionOutput
    overall_reasoning: str
