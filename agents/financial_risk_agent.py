from schemas import FinancialRiskOutput, LoanApplication


def analyze_financial_risk(application: LoanApplication) -> FinancialRiskOutput:
    """
    Analyzes financial risk based on debt-to-income ratio,
    credit score, loan amount, and anomaly detection.
    """

    debt_to_income = calculate_debt_to_income(
        application.annual_income,
        application.existing_debt,
        application.loan_amount
    )

    credit_risk = assess_credit_risk(application.credit_score)

    loan_amount_risk = assess_loan_amount_risk(
        application.loan_amount,
        application.annual_income
    )

    anomalies = detect_anomalies(application)

    reasoning = generate_reasoning(
        debt_to_income,
        credit_risk,
        loan_amount_risk,
        anomalies,
        application
    )

    return FinancialRiskOutput(
        debt_to_income_ratio=debt_to_income,
        credit_score_risk_level=credit_risk,
        loan_amount_risk=loan_amount_risk,
        anomaly_detection=anomalies,
        reasoning=reasoning,
    )


def calculate_debt_to_income(income: float, existing_debt: float, loan_amount: float) -> float:
    """Calculates debt-to-income ratio including new loan."""
    if income <= 0:
        return 0.0

    monthly_income = income / 12
    monthly_debt = existing_debt / 12
    monthly_loan_payment = (loan_amount * 0.005)

    total_monthly_debt = monthly_debt + monthly_loan_payment
    dti_ratio = (total_monthly_debt / monthly_income) * 100

    return round(min(dti_ratio, 100.0), 2)


def assess_credit_risk(credit_score: int) -> str:
    """Assesses credit risk level based on credit score."""
    if credit_score >= 750:
        return "low"
    elif credit_score >= 700:
        return "low-medium"
    elif credit_score >= 650:
        return "medium"
    elif credit_score >= 600:
        return "medium-high"
    else:
        return "high"


def assess_loan_amount_risk(loan_amount: float, annual_income: float) -> str:
    """Assesses loan amount risk relative to income."""
    if annual_income <= 0:
        return "high"

    loan_to_income = (loan_amount / annual_income) * 100

    if loan_to_income <= 50:
        return "low"
    elif loan_to_income <= 75:
        return "low-medium"
    elif loan_to_income <= 100:
        return "medium"
    elif loan_to_income <= 150:
        return "medium-high"
    else:
        return "high"


def detect_anomalies(application: LoanApplication) -> list:
    """Detects anomalies in the application."""
    anomalies = []

    if application.loan_amount > application.annual_income * 2:
        anomalies.append("Loan amount exceeds 2x annual income")

    if application.existing_debt > application.annual_income:
        anomalies.append("Existing debt exceeds annual income")

    if application.employment_years == 0 and application.employment_status == "employed":
        anomalies.append("Recently employed with no job history")

    if application.credit_score < 600 and application.loan_amount > 100000:
        anomalies.append("Low credit score with large loan request")

    dti = calculate_debt_to_income(
        application.annual_income,
        application.existing_debt,
        application.loan_amount
    )
    if dti > 43:
        anomalies.append("Debt-to-income ratio exceeds 43%")

    return anomalies


def generate_reasoning(dti: float, credit_risk: str, loan_risk: str, anomalies: list, application: LoanApplication) -> str:
    """Generates detailed reasoning for financial risk assessment."""
    reasoning_parts = []

    reasoning_parts.append(
        f"DTI ratio of {dti}% with monthly obligations of "
        f"${(application.existing_debt + application.loan_amount * 0.005) / 12:.2f}"
    )

    reasoning_parts.append(f"Credit risk profile: {credit_risk}")

    reasoning_parts.append(f"Loan amount risk: {loan_risk}")

    if anomalies:
        reasoning_parts.append(f"Detected {len(anomalies)} anomalies requiring review")

    return ". ".join(reasoning_parts)
