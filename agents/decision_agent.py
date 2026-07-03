from schemas import (
    LoanDecisionOutput,
    LoanStatus,
    LoanApplication,
    ApplicantProfileOutput,
    FinancialRiskOutput,
)


def make_loan_decision(
    application: LoanApplication,
    applicant_profile: ApplicantProfileOutput,
    financial_risk: FinancialRiskOutput,
) -> LoanDecisionOutput:
    """
    Makes the final loan decision based on applicant profile
    and financial risk analysis.
    """

    risk_score = calculate_risk_score(
        applicant_profile,
        financial_risk,
        application
    )

    decision, confidence = determine_decision(
        risk_score,
        applicant_profile,
        financial_risk,
        application
    )

    key_factors = identify_key_factors(
        applicant_profile,
        financial_risk,
        application,
        risk_score
    )

    explanation = generate_decision_explanation(
        decision,
        risk_score,
        applicant_profile,
        financial_risk
    )

    return LoanDecisionOutput(
        classification=decision,
        risk_score=risk_score,
        confidence_level=confidence,
        key_decision_factors=key_factors,
        explanation=explanation,
    )


def calculate_risk_score(
    profile: ApplicantProfileOutput,
    risk: FinancialRiskOutput,
    application: LoanApplication
) -> float:
    """Calculates overall risk score (0-100, higher = riskier)."""

    income_stability_factor = (100 - profile.income_stability_score) * 0.25

    employment_risk_map = {"low": 10, "medium": 30, "medium-high": 50, "high": 80}
    employment_factor = employment_risk_map.get(profile.employment_risk, 50) * 0.20

    credit_risk_map = {
        "low": 5,
        "low-medium": 20,
        "medium": 40,
        "medium-high": 65,
        "high": 85
    }
    credit_factor = credit_risk_map.get(risk.credit_score_risk_level, 40) * 0.25

    loan_risk_map = {
        "low": 10,
        "low-medium": 25,
        "medium": 45,
        "medium-high": 70,
        "high": 90
    }
    loan_factor = loan_risk_map.get(risk.loan_amount_risk, 45) * 0.15

    anomaly_penalty = len(risk.anomaly_detection) * 5

    dti_factor = min(risk.debt_to_income_ratio / 43 * 15, 15)

    total_risk = (
        income_stability_factor +
        employment_factor +
        credit_factor +
        loan_factor +
        anomaly_penalty +
        dti_factor
    )

    return min(round(total_risk, 2), 100.0)


def determine_decision(
    risk_score: float,
    profile: ApplicantProfileOutput,
    risk: FinancialRiskOutput,
    application: LoanApplication
) -> tuple:
    """Determines approval decision and confidence level."""

    completeness_penalty = len(profile.application_completeness_flags)

    if risk_score < 30 and completeness_penalty == 0:
        decision = LoanStatus.APPROVED
        confidence = 0.95
    elif risk_score < 50 and completeness_penalty <= 1:
        decision = LoanStatus.APPROVED
        confidence = 0.85
    elif risk_score < 60 and completeness_penalty == 0:
        decision = LoanStatus.REVIEW
        confidence = 0.7
    elif risk_score < 70 and len(risk.anomaly_detection) <= 1:
        decision = LoanStatus.REVIEW
        confidence = 0.6
    elif risk_score >= 75 or completeness_penalty > 2:
        decision = LoanStatus.REJECTED
        confidence = 0.9
    else:
        decision = LoanStatus.REVIEW
        confidence = 0.65

    return decision, confidence


def identify_key_factors(
    profile: ApplicantProfileOutput,
    risk: FinancialRiskOutput,
    application: LoanApplication,
    risk_score: float
) -> list:
    """Identifies key factors influencing the decision."""
    factors = []

    if profile.income_stability_score >= 80:
        factors.append("Strong income stability")
    elif profile.income_stability_score < 40:
        factors.append("Low income stability concern")

    if profile.employment_risk == "low":
        factors.append("Stable employment")
    elif profile.employment_risk == "high":
        factors.append("High employment risk")

    if risk.credit_score_risk_level in ["low", "low-medium"]:
        factors.append("Good credit profile")
    elif risk.credit_score_risk_level in ["medium-high", "high"]:
        factors.append("Credit risk concerns")

    if risk.debt_to_income_ratio < 35:
        factors.append("Healthy debt-to-income ratio")
    elif risk.debt_to_income_ratio > 43:
        factors.append("High debt-to-income ratio")

    if risk.loan_amount_risk == "low":
        factors.append("Reasonable loan amount")
    elif risk.loan_amount_risk == "high":
        factors.append("High loan-to-income ratio")

    if risk.anomaly_detection:
        factors.append(f"Flagged anomalies: {len(risk.anomaly_detection)}")

    if profile.application_completeness_flags:
        factors.append("Incomplete application data")

    return factors[:5]


def generate_decision_explanation(
    decision: LoanStatus,
    risk_score: float,
    profile: ApplicantProfileOutput,
    risk: FinancialRiskOutput
) -> str:
    """Generates explanation for the loan decision."""

    explanation = f"Based on comprehensive financial analysis with risk score {risk_score}/100, "

    if decision == LoanStatus.APPROVED:
        explanation += "the applicant demonstrates strong financial credentials. "
        explanation += f"Income stability score of {profile.income_stability_score} and "
        explanation += f"{risk.credit_score_risk_level} credit risk indicate favorable approval prospects."

    elif decision == LoanStatus.REJECTED:
        explanation += "the applicant does not meet approval criteria. "
        explanation += f"Key concerns include {risk.credit_score_risk_level} credit risk, "
        explanation += f"DTI ratio of {risk.debt_to_income_ratio}%, and employment risk of {profile.employment_risk}."

    else:
        explanation += "the application requires manual review. "
        explanation += "While some positive factors exist, certain metrics warrant expert evaluation before final approval."

    return explanation
