import json
from datetime import datetime
from schemas import ComplianceActionOutput, LoanDecisionOutput, LoanApplication


def execute_compliance_action(
    application: LoanApplication,
    decision: LoanDecisionOutput,
    case_id: str = None
) -> ComplianceActionOutput:
    """
    Executes compliance checks and sends notifications
    based on loan decision.
    """

    if not case_id:
        case_id = generate_case_id(application.applicant_id)

    action = determine_compliance_action(decision.classification)

    notification_sent = send_notification(
        application,
        decision,
        action,
        case_id
    )

    summary = generate_compliance_summary(
        decision.classification,
        action,
        application
    )

    timestamp = datetime.now().isoformat()

    return ComplianceActionOutput(
        action_taken=action,
        notification_sent=notification_sent,
        case_id=case_id,
        timestamp=timestamp,
        summary=summary,
    )


def generate_case_id(applicant_id: str) -> str:
    """Generates a unique case ID for tracking."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"CASE-{applicant_id}-{timestamp}"


def determine_compliance_action(classification: str) -> str:
    """Determines the compliance action based on decision."""

    action_map = {
        "approved": "Loan approved - send approval letter and funding instructions",
        "rejected": "Loan rejected - send rejection letter with appeal process info",
        "review": "Application queued for manual compliance review by underwriter",
        "pending": "Application received - initial compliance check passed"
    }

    return action_map.get(classification.lower(), "Under compliance review")


def send_notification(
    application: LoanApplication,
    decision: LoanDecisionOutput,
    action: str,
    case_id: str
) -> bool:
    """Sends notification to applicant (simulated)."""
    try:
        notification_data = {
            "applicant_id": application.applicant_id,
            "applicant_name": application.applicant_name,
            "email": application.email,
            "phone": application.phone,
            "case_id": case_id,
            "decision": decision.classification,
            "risk_score": decision.risk_score,
            "confidence": decision.confidence_level,
            "action": action,
            "timestamp": datetime.now().isoformat()
        }

        return True
    except Exception as e:
        print(f"Notification error: {e}")
        return False


def generate_compliance_summary(
    classification: str,
    action: str,
    application: LoanApplication
) -> str:
    """Generates compliance action summary."""

    summary = f"Compliance processing for {application.applicant_name} ({application.applicant_id}). "
    summary += f"Decision: {classification.upper()}. "
    summary += f"Action: {action}. "
    summary += f"Loan amount: ${application.loan_amount:,.2f}. "
    summary += f"Annual income: ${application.annual_income:,.2f}."

    return summary
