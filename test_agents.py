#!/usr/bin/env python3
"""
Test suite for Agentic AI Loan Approval System
Tests individual agents and the complete workflow
"""

import sys
from schemas import LoanApplication
from agents.applicant_agent import (
    analyze_applicant_profile,
    calculate_income_stability,
    generate_credit_summary
)
from agents.financial_risk_agent import (
    analyze_financial_risk,
    calculate_debt_to_income,
    detect_anomalies
)
from agents.decision_agent import make_loan_decision
from agents.compliance_agent import execute_compliance_action
from orchestrator import process_loan_application


def test_income_stability_scoring():
    """Tests income stability calculation."""
    print("\n🧪 Testing Income Stability Scoring...")

    test_cases = [
        {"years": 10, "status": "employed", "income": 150000, "expected": ">80"},
        {"years": 2, "status": "employed", "income": 50000, "expected": "50-60"},
        {"years": 0, "status": "unemployed", "income": 0, "expected": "<40"},
    ]

    for case in test_cases:
        score = calculate_income_stability(case["years"], case["status"], case["income"])
        print(f"  Years: {case['years']}, Status: {case['status']}, Income: ${case['income']:,}")
        print(f"    → Score: {score:.1f}/100 (Expected: {case['expected']})")


def test_dti_calculation():
    """Tests debt-to-income ratio calculation."""
    print("\n🧪 Testing DTI Calculation...")

    test_cases = [
        {
            "income": 60000,
            "debt": 10000,
            "loan": 100000,
            "description": "Lower income, higher loan"
        },
        {
            "income": 150000,
            "debt": 20000,
            "loan": 300000,
            "description": "Higher income, proportional loan"
        },
    ]

    for case in test_cases:
        dti = calculate_debt_to_income(case["income"], case["debt"], case["loan"])
        print(f"  {case['description']}")
        print(f"    Income: ${case['income']:,}, Debt: ${case['debt']:,}, Loan: ${case['loan']:,}")
        print(f"    → DTI: {dti:.2f}%")


def test_credit_summary():
    """Tests credit summary generation."""
    print("\n🧪 Testing Credit Summary...")

    scores = [800, 750, 700, 650, 600, 550]

    for score in scores:
        summary = generate_credit_summary(score)
        print(f"  Score {score}: {summary}")


def test_anomaly_detection():
    """Tests anomaly detection in financial risk agent."""
    print("\n🧪 Testing Anomaly Detection...")

    test_app = LoanApplication(
        applicant_id="TEST-ANOMALY",
        applicant_name="Test Applicant",
        email="test@example.com",
        phone="+1-555-1234",
        annual_income=30000,
        employment_type="employed",
        employment_years=0,
        credit_score=550,
        existing_debt=50000,
        loan_amount=200000,
        loan_purpose="Business",
        employment_company="Startup",
        employment_status="employed"
    )

    anomalies = detect_anomalies(test_app)
    print(f"  Applicant with risky profile:")
    print(f"    Income: ${test_app.annual_income:,}")
    print(f"    Debt: ${test_app.existing_debt:,}")
    print(f"    Loan: ${test_app.loan_amount:,}")
    print(f"    Credit Score: {test_app.credit_score}")
    print(f"  → Anomalies Detected:")
    for anomaly in anomalies:
        print(f"    • {anomaly}")


def test_complete_workflow():
    """Tests the complete multi-agent workflow."""
    print("\n🧪 Testing Complete Workflow...")

    test_cases = [
        {
            "name": "Strong Applicant",
            "app": LoanApplication(
                applicant_id="TEST-STRONG",
                applicant_name="Alice Johnson",
                email="alice@example.com",
                phone="+1-555-0001",
                annual_income=120000,
                employment_type="employed",
                employment_years=8,
                credit_score=780,
                existing_debt=5000,
                loan_amount=200000,
                loan_purpose="Home Purchase",
                employment_company="TechCorp",
                employment_status="employed"
            )
        },
        {
            "name": "Borderline Applicant",
            "app": LoanApplication(
                applicant_id="TEST-BORDERLINE",
                applicant_name="Bob Smith",
                email="bob@example.com",
                phone="+1-555-0002",
                annual_income=65000,
                employment_type="employed",
                employment_years=3,
                credit_score=680,
                existing_debt=25000,
                loan_amount=150000,
                loan_purpose="Auto Purchase",
                employment_company="RetailCo",
                employment_status="employed"
            )
        },
        {
            "name": "Weak Applicant",
            "app": LoanApplication(
                applicant_id="TEST-WEAK",
                applicant_name="Charlie Brown",
                email="charlie@example.com",
                phone="+1-555-0003",
                annual_income=35000,
                employment_type="self-employed",
                employment_years=1,
                credit_score=580,
                existing_debt=40000,
                loan_amount=100000,
                loan_purpose="Debt Consolidation",
                employment_company="Freelance",
                employment_status="self-employed"
            )
        },
    ]

    for test_case in test_cases:
        print(f"\n  Testing: {test_case['name']}")
        print(f"  {'='*50}")

        try:
            result = process_loan_application(test_case["app"], test_case["app"].applicant_id)

            print(f"  ✅ Processing successful")
            print(f"     Decision: {result.status}")
            print(f"     Risk Score: {result.decision.risk_score:.1f}/100")
            print(f"     Confidence: {result.decision.confidence_level*100:.1f}%")
            print(f"     Income Stability: {result.applicant_profile.income_stability_score:.1f}/100")
            print(f"     DTI Ratio: {result.financial_risk.debt_to_income_ratio:.2f}%")

            if result.decision.key_decision_factors:
                print(f"     Key Factors:")
                for factor in result.decision.key_decision_factors[:3]:
                    print(f"       • {factor}")

        except Exception as e:
            print(f"  ❌ Processing failed: {str(e)}")


def test_applicant_profile_agent():
    """Tests the applicant profile agent."""
    print("\n🧪 Testing Applicant Profile Agent...")

    app = LoanApplication(
        applicant_id="TEST-PROFILE",
        applicant_name="John Doe",
        email="john@example.com",
        phone="+1-555-1234",
        annual_income=85000,
        employment_type="employed",
        employment_years=6,
        credit_score=720,
        existing_debt=15000,
        loan_amount=150000,
        loan_purpose="Home Purchase",
        employment_company="TechCorp",
        employment_status="employed"
    )

    profile = analyze_applicant_profile(app)

    print(f"  Applicant: {app.applicant_name}")
    print(f"  → Income Stability Score: {profile.income_stability_score:.1f}/100")
    print(f"  → Employment Risk: {profile.employment_risk}")
    print(f"  → Credit History: {profile.credit_history_summary}")

    if profile.application_completeness_flags:
        print(f"  → Completeness Flags:")
        for flag in profile.application_completeness_flags:
            print(f"    • {flag}")
    else:
        print(f"  → ✅ Application is complete")


def test_financial_risk_agent():
    """Tests the financial risk agent."""
    print("\n🧪 Testing Financial Risk Agent...")

    app = LoanApplication(
        applicant_id="TEST-RISK",
        applicant_name="Jane Smith",
        email="jane@example.com",
        phone="+1-555-5678",
        annual_income=95000,
        employment_type="employed",
        employment_years=7,
        credit_score=700,
        existing_debt=20000,
        loan_amount=250000,
        loan_purpose="Home Purchase",
        employment_company="Finance Inc",
        employment_status="employed"
    )

    risk = analyze_financial_risk(app)

    print(f"  Applicant: {app.applicant_name}")
    print(f"  → DTI Ratio: {risk.debt_to_income_ratio:.2f}%")
    print(f"  → Credit Risk Level: {risk.credit_score_risk_level}")
    print(f"  → Loan Amount Risk: {risk.loan_amount_risk}")

    if risk.anomaly_detection:
        print(f"  → Anomalies:")
        for anomaly in risk.anomaly_detection:
            print(f"    • {anomaly}")
    else:
        print(f"  → ✅ No anomalies detected")


def test_decision_agent():
    """Tests the decision synthesis agent."""
    print("\n🧪 Testing Decision Agent...")

    app = LoanApplication(
        applicant_id="TEST-DECISION",
        applicant_name="Michael Brown",
        email="michael@example.com",
        phone="+1-555-9999",
        annual_income=110000,
        employment_type="employed",
        employment_years=10,
        credit_score=760,
        existing_debt=8000,
        loan_amount=200000,
        loan_purpose="Home Purchase",
        employment_company="Tech Giant",
        employment_status="employed"
    )

    profile = analyze_applicant_profile(app)
    risk = analyze_financial_risk(app)
    decision = make_loan_decision(app, profile, risk)

    print(f"  Applicant: {app.applicant_name}")
    print(f"  → Decision: {decision.classification}")
    print(f"  → Risk Score: {decision.risk_score:.1f}/100")
    print(f"  → Confidence: {decision.confidence_level*100:.1f}%")
    print(f"  → Key Factors:")
    for factor in decision.key_decision_factors:
        print(f"    • {factor}")


def run_all_tests():
    """Runs all tests in sequence."""
    print("\n" + "="*60)
    print("AGENTIC AI LOAN APPROVAL SYSTEM - TEST SUITE")
    print("="*60)

    try:
        test_income_stability_scoring()
        test_dti_calculation()
        test_credit_summary()
        test_anomaly_detection()
        test_applicant_profile_agent()
        test_financial_risk_agent()
        test_decision_agent()
        test_complete_workflow()

        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*60 + "\n")

        return 0

    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
