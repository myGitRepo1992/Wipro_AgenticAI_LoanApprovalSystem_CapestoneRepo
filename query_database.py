#!/usr/bin/env python3
"""Query and display data from the database"""

from database import SessionLocal, ApplicationRecord, ApplicantCacheRecord
import json
from tabulate import tabulate


def view_applications():
    """View all applications stored in database"""
    db = SessionLocal()
    try:
        records = db.query(ApplicationRecord).all()

        if not records:
            print("No applications found in database")
            return

        print(f"\n{'='*100}")
        print(f"APPLICATIONS ({len(records)} total)")
        print(f"{'='*100}\n")

        data = []
        for record in records:
            data.append([
                record.id,
                record.applicant_name,
                record.status,
                f"${record.loan_amount:,.2f}",
                record.created_at.strftime("%Y-%m-%d %H:%M:%S")
            ])

        headers = ["Application ID", "Applicant", "Status", "Loan Amount", "Created"]
        print(tabulate(data, headers=headers, tablefmt="grid"))

    finally:
        db.close()


def view_application_details(app_id: str):
    """View detailed information about a specific application"""
    db = SessionLocal()
    try:
        record = db.query(ApplicationRecord).filter(
            ApplicationRecord.id == app_id
        ).first()

        if not record:
            print(f"Application {app_id} not found")
            return

        print(f"\n{'='*100}")
        print(f"APPLICATION DETAILS: {app_id}")
        print(f"{'='*100}\n")

        print(f"Applicant Information:")
        print(f"  Name: {record.applicant_name}")
        print(f"  Email: {record.applicant_email}")
        print(f"  ID: {record.applicant_id}")
        print(f"\nFinancial Information:")
        print(f"  Annual Income: ${record.annual_income:,.2f}")
        print(f"  Credit Score: {record.credit_score}")
        print(f"  Loan Amount: ${record.loan_amount:,.2f}")
        print(f"  Existing Debt: ${record.existing_debt:,.2f}")
        print(f"\nEmployment Information:")
        print(f"  Type: {record.employment_type}")
        print(f"  Years: {record.employment_years}")

        print(f"\nDecision Details:")
        decision = record.loan_decision
        if decision:
            print(f"  Status: {decision.get('classification', 'N/A').upper()}")
            print(f"  Risk Score: {decision.get('risk_score', 'N/A')}/100")
            print(f"  Confidence: {decision.get('confidence_level', 'N/A')}")
            print(f"  Explanation: {decision.get('explanation', 'N/A')}")

        print(f"\nFinancial Risk:")
        risk = record.financial_risk
        if risk:
            print(f"  DTI Ratio: {risk.get('debt_to_income_ratio', 'N/A')}%")
            print(f"  Credit Risk: {risk.get('credit_score_risk_level', 'N/A')}")
            print(f"  Loan Risk: {risk.get('loan_amount_risk', 'N/A')}")

        print(f"\nProcessed At: {record.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    finally:
        db.close()


def view_statistics():
    """View database statistics"""
    db = SessionLocal()
    try:
        total_apps = db.query(ApplicationRecord).count()
        approved = db.query(ApplicationRecord).filter(
            ApplicationRecord.status == "approved"
        ).count()
        rejected = db.query(ApplicationRecord).filter(
            ApplicationRecord.status == "rejected"
        ).count()
        review = db.query(ApplicationRecord).filter(
            ApplicationRecord.status == "review"
        ).count()

        total_loan = db.query(ApplicationRecord).with_entities(
            ApplicationRecord.loan_amount
        ).all()
        total_loan_amount = sum([l[0] for l in total_loan]) if total_loan else 0

        print(f"\n{'='*100}")
        print(f"DATABASE STATISTICS")
        print(f"{'='*100}\n")

        print(f"Total Applications: {total_apps}")
        print(f"  - Approved: {approved} ({approved/total_apps*100:.1f}%)" if total_apps > 0 else "  - Approved: 0")
        print(f"  - Rejected: {rejected} ({rejected/total_apps*100:.1f}%)" if total_apps > 0 else "  - Rejected: 0")
        print(f"  - Under Review: {review} ({review/total_apps*100:.1f}%)" if total_apps > 0 else "  - Under Review: 0")
        print(f"\nTotal Loan Amount: ${total_loan_amount:,.2f}")
        print()

    finally:
        db.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "stats":
            view_statistics()
        else:
            view_application_details(sys.argv[1])
    else:
        view_applications()
