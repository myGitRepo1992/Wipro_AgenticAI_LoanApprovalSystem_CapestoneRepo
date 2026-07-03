import json
from typing import Any
from schemas import ApplicantProfileOutput, LoanApplication


def analyze_applicant_profile(application: LoanApplication) -> ApplicantProfileOutput:
    """
    Analyzes applicant profile to determine income stability,
    employment risk, and application completeness.
    """

    employment_risk_map = {
        "employed": "low",
        "self-employed": "medium",
        "contract": "medium-high",
        "unemployed": "high",
        "retired": "medium",
    }

    employment_risk = employment_risk_map.get(
        application.employment_status.lower(), "medium"
    )

    income_stability_score = calculate_income_stability(
        application.employment_years,
        application.employment_status,
        application.annual_income
    )

    credit_summary = generate_credit_summary(application.credit_score)

    completeness_flags = check_application_completeness(application)

    return ApplicantProfileOutput(
        income_stability_score=income_stability_score,
        employment_risk=employment_risk,
        credit_history_summary=credit_summary,
        application_completeness_flags=completeness_flags,
    )


def calculate_income_stability(years: int, status: str, income: float) -> float:
    """Calculates income stability score based on tenure and employment status."""
    base_score = 50.0

    tenure_bonus = min(years * 5, 30)

    if status.lower() == "employed":
        status_bonus = 20
    elif status.lower() in ["self-employed", "contract"]:
        status_bonus = 10
    else:
        status_bonus = 5

    if income > 100000:
        income_bonus = 10
    elif income > 50000:
        income_bonus = 5
    else:
        income_bonus = 0

    total_score = base_score + tenure_bonus + status_bonus + income_bonus
    return min(total_score, 100.0)


def generate_credit_summary(credit_score: int) -> str:
    """Generates credit history summary based on credit score."""
    if credit_score >= 750:
        return "Excellent credit history. Low risk profile."
    elif credit_score >= 700:
        return "Good credit history. Acceptable risk profile."
    elif credit_score >= 650:
        return "Fair credit history. Moderate risk profile."
    elif credit_score >= 600:
        return "Poor credit history. Higher risk profile."
    else:
        return "Very poor credit history. Very high risk profile."


def check_application_completeness(application: LoanApplication) -> list:
    """Checks for missing or incomplete application fields."""
    flags = []

    if not application.applicant_name or len(application.applicant_name) < 2:
        flags.append("Incomplete applicant name")

    if application.annual_income <= 0:
        flags.append("Invalid or missing income information")

    if application.employment_years < 0:
        flags.append("Invalid employment duration")

    if application.credit_score < 300 or application.credit_score > 850:
        flags.append("Credit score out of valid range")

    if not application.employment_company:
        flags.append("Missing employer information")

    if not application.email or "@" not in application.email:
        flags.append("Invalid email address")

    return flags
