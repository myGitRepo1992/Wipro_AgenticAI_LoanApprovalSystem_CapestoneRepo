#!/usr/bin/env python3
"""
Interactive CLI tool for database operations
"""

from database import SessionLocal, ApplicationRecord
from tabulate import tabulate
import sys
from datetime import datetime


class DatabaseCLI:
    def __init__(self):
        self.db = SessionLocal()

    def close(self):
        self.db.close()

    def view_all_applications(self, limit=50):
        """View all applications"""
        records = self.db.query(ApplicationRecord).order_by(
            ApplicationRecord.created_at.desc()
        ).limit(limit).all()

        if not records:
            print("❌ No applications found in database")
            return

        print(f"\n{'='*120}")
        print(f"{'APPLICATIONS':^120}")
        print(f"{'='*120}\n")

        data = []
        for i, record in enumerate(records, 1):
            data.append([
                i,
                record.id,
                record.applicant_name,
                record.status.upper(),
                f"${record.loan_amount:,.2f}",
                record.credit_score,
                f"{record.loan_decision.get('risk_score', 'N/A'):.1f}" if record.loan_decision else "N/A",
                record.created_at.strftime("%Y-%m-%d %H:%M:%S")
            ])

        headers = ["#", "Application ID", "Applicant", "Status", "Loan Amount", "Credit", "Risk", "Created"]
        print(tabulate(data, headers=headers, tablefmt="grid"))
        print(f"\nTotal: {len(records)} records\n")

    def search_by_id(self, application_id):
        """Search application by ID"""
        record = self.db.query(ApplicationRecord).filter(
            ApplicationRecord.id == application_id
        ).first()

        if not record:
            print(f"❌ Application {application_id} not found")
            return

        self._display_application_details(record)

    def search_by_name(self, name, limit=10):
        """Search applications by applicant name"""
        records = self.db.query(ApplicationRecord).filter(
            ApplicationRecord.applicant_name.ilike(f"%{name}%")
        ).limit(limit).all()

        if not records:
            print(f"❌ No applications found for: {name}")
            return

        print(f"\n{'='*120}")
        print(f"{'SEARCH RESULTS FOR: ' + name:^120}")
        print(f"{'='*120}\n")

        data = []
        for i, record in enumerate(records, 1):
            data.append([
                i,
                record.id,
                record.applicant_name,
                record.status.upper(),
                f"${record.loan_amount:,.2f}",
                record.created_at.strftime("%Y-%m-%d")
            ])

        headers = ["#", "Application ID", "Applicant", "Status", "Loan Amount", "Created"]
        print(tabulate(data, headers=headers, tablefmt="grid"))
        print(f"\nFound: {len(records)} records\n")

    def search_by_status(self, status, limit=50):
        """Search applications by status"""
        valid_statuses = ["approved", "rejected", "review"]
        if status.lower() not in valid_statuses:
            print(f"❌ Invalid status. Use: {', '.join(valid_statuses)}")
            return

        records = self.db.query(ApplicationRecord).filter(
            ApplicationRecord.status == status.lower()
        ).order_by(ApplicationRecord.created_at.desc()).limit(limit).all()

        if not records:
            print(f"❌ No applications found with status: {status}")
            return

        print(f"\n{'='*120}")
        print(f"{'APPLICATIONS - STATUS: ' + status.upper():^120}")
        print(f"{'='*120}\n")

        data = []
        for i, record in enumerate(records, 1):
            data.append([
                i,
                record.id,
                record.applicant_name,
                f"${record.loan_amount:,.2f}",
                record.annual_income,
                record.credit_score,
                record.created_at.strftime("%Y-%m-%d %H:%M:%S")
            ])

        headers = ["#", "App ID", "Applicant", "Loan", "Income", "Credit", "Created"]
        print(tabulate(data, headers=headers, tablefmt="grid"))
        print(f"\nTotal: {len(records)} records\n")

    def _display_application_details(self, record):
        """Display detailed view of a single application"""
        print(f"\n{'='*120}")
        print(f"{'APPLICATION DETAILS':^120}")
        print(f"{'='*120}\n")

        print("📋 BASIC INFORMATION")
        print(f"  Application ID:    {record.id}")
        print(f"  Applicant ID:      {record.applicant_id}")
        print(f"  Applicant Name:    {record.applicant_name}")
        print(f"  Email:             {record.applicant_email}")
        print(f"  Status:            {record.status.upper()}")

        print("\n💼 EMPLOYMENT INFORMATION")
        print(f"  Employment Type:   {record.employment_type}")
        print(f"  Years:             {record.employment_years}")
        print(f"  Company:           {getattr(record, 'employment_company', 'N/A')}")

        print("\n💰 FINANCIAL INFORMATION")
        print(f"  Annual Income:     ${record.annual_income:,.2f}")
        print(f"  Credit Score:      {record.credit_score}")
        print(f"  Existing Debt:     ${record.existing_debt:,.2f}")
        print(f"  Loan Amount:       ${record.loan_amount:,.2f}")

        if record.applicant_profile:
            profile = record.applicant_profile
            print("\n📊 APPLICANT PROFILE")
            print(f"  Income Stability:  {profile.get('income_stability_score', 'N/A')}/100")
            print(f"  Employment Risk:   {profile.get('employment_risk', 'N/A')}")
            print(f"  Credit Summary:    {profile.get('credit_history_summary', 'N/A')}")

        if record.financial_risk:
            risk = record.financial_risk
            print("\n⚠️  FINANCIAL RISK ANALYSIS")
            print(f"  DTI Ratio:         {risk.get('debt_to_income_ratio', 'N/A')}%")
            print(f"  Credit Risk:       {risk.get('credit_score_risk_level', 'N/A')}")
            print(f"  Loan Risk:         {risk.get('loan_amount_risk', 'N/A')}")

        if record.loan_decision:
            decision = record.loan_decision
            print("\n✅ LOAN DECISION")
            print(f"  Decision:          {decision.get('classification', 'N/A').upper()}")
            print(f"  Risk Score:        {decision.get('risk_score', 'N/A')}/100")
            print(f"  Confidence:        {decision.get('confidence_level', 'N/A')*100:.1f}%")
            print(f"  Explanation:       {decision.get('explanation', 'N/A')}")

        print(f"\n⏰ TIMESTAMPS")
        print(f"  Created:           {record.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Updated:           {record.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    def get_statistics(self):
        """Display database statistics"""
        total = self.db.query(ApplicationRecord).count()
        approved = self.db.query(ApplicationRecord).filter(
            ApplicationRecord.status == "approved"
        ).count()
        rejected = self.db.query(ApplicationRecord).filter(
            ApplicationRecord.status == "rejected"
        ).count()
        review = self.db.query(ApplicationRecord).filter(
            ApplicationRecord.status == "review"
        ).count()

        total_loan = sum([r[0] for r in self.db.query(ApplicationRecord.loan_amount).all()]) if total > 0 else 0
        avg_credit = sum([r[0] for r in self.db.query(ApplicationRecord.credit_score).all()]) / total if total > 0 else 0
        avg_income = sum([r[0] for r in self.db.query(ApplicationRecord.annual_income).all()]) / total if total > 0 else 0

        print(f"\n{'='*60}")
        print(f"{'DATABASE STATISTICS':^60}")
        print(f"{'='*60}\n")

        print(f"Total Applications:    {total}")
        print(f"  ✅ Approved:         {approved} ({approved/total*100:.1f}%)" if total > 0 else "  ✅ Approved:         0")
        print(f"  ❌ Rejected:         {rejected} ({rejected/total*100:.1f}%)" if total > 0 else "  ❌ Rejected:         0")
        print(f"  🟡 Under Review:     {review} ({review/total*100:.1f}%)" if total > 0 else "  🟡 Under Review:     0")

        print(f"\nFinancial Metrics:")
        print(f"  Total Loans:         ${total_loan:,.2f}")
        print(f"  Avg Credit Score:    {avg_credit:.0f}")
        print(f"  Avg Annual Income:   ${avg_income:,.2f}")
        print()

    def display_menu(self):
        """Display interactive menu"""
        while True:
            print(f"\n{'='*60}")
            print(f"{'LOAN APPLICATION DATABASE':^60}")
            print(f"{'='*60}")
            print("\n1. View all applications")
            print("2. Search by Application ID")
            print("3. Search by Applicant Name")
            print("4. Filter by Status")
            print("5. View Statistics")
            print("6. Exit")

            choice = input("\nSelect option (1-6): ").strip()

            if choice == "1":
                limit = input("Enter limit (default 50): ").strip()
                try:
                    limit = int(limit) if limit else 50
                    self.view_all_applications(limit)
                except ValueError:
                    print("❌ Invalid limit")

            elif choice == "2":
                app_id = input("Enter Application ID: ").strip()
                if app_id:
                    self.search_by_id(app_id)
                else:
                    print("❌ Please enter an Application ID")

            elif choice == "3":
                name = input("Enter Applicant Name (or part of it): ").strip()
                if name:
                    self.search_by_name(name)
                else:
                    print("❌ Please enter a name")

            elif choice == "4":
                print("Statuses: approved, rejected, review")
                status = input("Enter status: ").strip()
                if status:
                    self.search_by_status(status)
                else:
                    print("❌ Please enter a status")

            elif choice == "5":
                self.get_statistics()

            elif choice == "6":
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid option. Please try again.")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        cli = DatabaseCLI()

        command = sys.argv[1].lower()

        if command == "all":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            cli.view_all_applications(limit)

        elif command == "search":
            if len(sys.argv) < 3:
                print("Usage: python database_cli.py search <application_id>")
                return
            cli.search_by_id(sys.argv[2])

        elif command == "name":
            if len(sys.argv) < 3:
                print("Usage: python database_cli.py name <applicant_name>")
                return
            cli.search_by_name(" ".join(sys.argv[2:]))

        elif command == "status":
            if len(sys.argv) < 3:
                print("Usage: python database_cli.py status <approved|rejected|review>")
                return
            cli.search_by_status(sys.argv[2])

        elif command == "stats":
            cli.get_statistics()

        else:
            print("Usage:")
            print("  python database_cli.py all [limit]           - View all applications")
            print("  python database_cli.py search <app_id>        - Search by Application ID")
            print("  python database_cli.py name <name>            - Search by Applicant Name")
            print("  python database_cli.py status <status>        - Filter by Status")
            print("  python database_cli.py stats                  - View Statistics")
            print("  python database_cli.py interactive             - Interactive mode")

        cli.close()

    else:
        cli = DatabaseCLI()
        try:
            cli.display_menu()
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
        finally:
            cli.close()


if __name__ == "__main__":
    main()
