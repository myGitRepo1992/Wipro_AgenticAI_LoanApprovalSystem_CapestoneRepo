from langgraph.graph import StateGraph, END
from typing import TypedDict, Any, Optional, Annotated
import json
from schemas import LoanApplication, LoanApplicationResponse, LoanStatus
from agents.applicant_agent import analyze_applicant_profile
from agents.financial_risk_agent import analyze_financial_risk
from agents.decision_agent import make_loan_decision
from agents.compliance_agent import execute_compliance_action
from operator import or_


class LoanProcessingState(TypedDict):
    application_id: str
    case_id: str
    application: LoanApplication
    applicant_profile: Optional[Any]
    financial_risk: Optional[Any]
    loan_decision: Optional[Any]
    compliance_action: Optional[Any]
    error: Annotated[str, lambda a, b: a or b]


def validate_application(state: LoanProcessingState) -> dict:
    """Validates the loan application data."""
    try:
        application = state["application"]

        if not application.applicant_id:
            raise ValueError("Missing applicant ID")

        if application.annual_income <= 0:
            raise ValueError("Invalid annual income")

        if application.credit_score < 300 or application.credit_score > 850:
            raise ValueError("Invalid credit score")

        if application.loan_amount <= 0:
            raise ValueError("Invalid loan amount")

        return {"error": ""}

    except Exception as e:
        return {"error": str(e)}


def applicant_profile_node(state: LoanProcessingState) -> dict:
    """Agent node for applicant profile analysis."""
    try:
        if state.get("error"):
            return {}

        application = state["application"]
        profile = analyze_applicant_profile(application)
        return {"applicant_profile": profile}

    except Exception as e:
        return {"error": f"Applicant profile analysis failed: {str(e)}"}


def financial_risk_node(state: LoanProcessingState) -> dict:
    """Agent node for financial risk analysis."""
    try:
        if state.get("error"):
            return {}

        application = state["application"]
        risk = analyze_financial_risk(application)
        return {"financial_risk": risk}

    except Exception as e:
        return {"error": f"Financial risk analysis failed: {str(e)}"}


def decision_node(state: LoanProcessingState) -> dict:
    """Agent node for loan decision making."""
    try:
        if state.get("error"):
            return {}

        application = state["application"]
        profile = state["applicant_profile"]
        risk = state["financial_risk"]

        decision = make_loan_decision(application, profile, risk)
        return {"loan_decision": decision}

    except Exception as e:
        return {"error": f"Loan decision failed: {str(e)}"}


def compliance_node(state: LoanProcessingState) -> dict:
    """Agent node for compliance and notification."""
    try:
        if state.get("error"):
            return {}

        application = state["application"]
        decision = state["loan_decision"]
        case_id = state["case_id"]

        compliance = execute_compliance_action(application, decision, case_id)
        return {"compliance_action": compliance}

    except Exception as e:
        return {"error": f"Compliance action failed: {str(e)}"}


def create_loan_processing_graph():
    """Creates the LangGraph workflow for loan processing."""
    workflow = StateGraph(LoanProcessingState)

    workflow.add_node("validate", validate_application)
    workflow.add_node("applicant_profile", applicant_profile_node)
    workflow.add_node("financial_risk", financial_risk_node)
    workflow.add_node("decision", decision_node)
    workflow.add_node("compliance", compliance_node)

    workflow.set_entry_point("validate")

    workflow.add_edge("validate", "applicant_profile")
    workflow.add_edge("validate", "financial_risk")

    workflow.add_edge("applicant_profile", "decision")
    workflow.add_edge("financial_risk", "decision")

    workflow.add_edge("decision", "compliance")

    workflow.add_edge("compliance", END)

    return workflow.compile()


def process_loan_application(application: LoanApplication, application_id: str) -> LoanApplicationResponse:
    """
    Main orchestration function that processes a loan application
    through the multi-agent workflow.
    """
    graph = create_loan_processing_graph()

    initial_state = {
        "application_id": application_id,
        "case_id": application_id,
        "application": application,
        "applicant_profile": None,
        "financial_risk": None,
        "loan_decision": None,
        "compliance_action": None,
        "error": ""
    }

    final_state = graph.invoke(initial_state)

    if final_state.get("error"):
        raise Exception(f"Loan processing error: {final_state['error']}")

    overall_reasoning = generate_overall_reasoning(
        final_state["applicant_profile"],
        final_state["financial_risk"],
        final_state["loan_decision"]
    )

    response = LoanApplicationResponse(
        application_id=application_id,
        status=final_state["loan_decision"].classification,
        decision=final_state["loan_decision"],
        financial_risk=final_state["financial_risk"],
        applicant_profile=final_state["applicant_profile"],
        compliance_action=final_state["compliance_action"],
        overall_reasoning=overall_reasoning
    )

    return response


def generate_overall_reasoning(profile, financial_risk, decision):
    """Generates overall reasoning from all agent outputs."""
    reasoning = f"Loan application processed through multi-agent analysis. "
    reasoning += f"Applicant income stability: {profile.income_stability_score}/100. "
    reasoning += f"Employment risk: {profile.employment_risk}. "
    reasoning += f"Debt-to-income ratio: {financial_risk.debt_to_income_ratio}%. "
    reasoning += f"Overall risk score: {decision.risk_score}/100. "
    reasoning += f"Decision: {decision.classification.upper()}. "
    reasoning += decision.explanation

    return reasoning
