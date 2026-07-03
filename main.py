#!/usr/bin/env python3
"""
Agentic AI Intelligent Loan Approval System
Main entry point for the distributed multi-agent architecture
"""

import sys
import argparse
import subprocess
import time
import requests
from pathlib import Path
import logging


def init_database():
    """Initialize the database."""
    try:
        from database import init_db
        print("\n🗄️  Initializing database...")
        init_db()
        print("   ✅ Database ready at loan_applications.db")
        return True
    except Exception as e:
        print(f"   ⚠️  Database initialization: {str(e)}")
        return False


def check_dependencies():
    """Checks if all required packages are installed."""
    required = ["fastapi", "streamlit", "langgraph", "anthropic", "sqlalchemy"]
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    return missing


def wait_for_service(url: str, max_attempts: int = 30) -> bool:
    """Waits for a service to be ready."""
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False


def start_mcp_servers():
    """Starts all MCP servers."""
    print("\n" + "="*60)
    print("Starting MCP Servers...")
    print("="*60)

    servers = [
        {
            "name": "ApplicantDB",
            "script": "mcp_servers/applicant_db_server.py",
            "port": 8001,
            "url": "http://127.0.0.1:8001/health"
        },
        {
            "name": "RiskRulesDB",
            "script": "mcp_servers/risk_rules_server.py",
            "port": 8002,
            "url": "http://127.0.0.1:8002/health"
        },
        {
            "name": "DecisionSynthesis",
            "script": "mcp_servers/decision_synthesis_server.py",
            "port": 8003,
            "url": "http://127.0.0.1:8003/health"
        },
        {
            "name": "NotificationSystem",
            "script": "mcp_servers/notification_server.py",
            "port": 8004,
            "url": "http://127.0.0.1:8004/health"
        }
    ]

    processes = []

    for server in servers:
        print(f"\n🚀 Starting {server['name']} (Port {server['port']})...")
        process = subprocess.Popen(
            ["python", server["script"]],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes.append(process)

        if wait_for_service(server["url"]):
            print(f"   ✅ {server['name']} ready at {server['url']}")
        else:
            print(f"   ⚠️  {server['name']} startup delayed, continuing...")

    return processes


def start_microservice():
    """Starts the FastAPI microservice."""
    print("\n" + "="*60)
    print("Starting FastAPI Microservice...")
    print("="*60)

    print("\n🚀 Starting microservice on http://127.0.0.1:8000...")

    process = subprocess.Popen(
        ["python", "microservice.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if wait_for_service("http://127.0.0.1:8000/health"):
        print("   ✅ Microservice ready at http://127.0.0.1:8000")
    else:
        print("   ⚠️  Microservice startup delayed")

    return process


def start_streamlit():
    """Starts the Streamlit chatbot UI."""
    print("\n" + "="*60)
    print("Starting Streamlit UI...")
    print("="*60 + "\n")

    print("🚀 Opening Streamlit app in browser...")
    print("   📍 Available at: http://localhost:8501\n")

    subprocess.run(["streamlit", "run", "chatbot_ui.py"])


def demo_mode():
    """Runs a simple demo."""
    print("\n" + "="*60)
    print("Demo Mode - Testing Multi-Agent Architecture")
    print("="*60)

    from schemas import LoanApplication
    from orchestrator import process_loan_application

    sample_app = LoanApplication(
        applicant_id="DEMO-001",
        applicant_name="John Doe",
        email="john@example.com",
        phone="+1-555-1234",
        annual_income=75000,
        employment_type="full-time",
        employment_years=5,
        credit_score=720,
        existing_debt=15000,
        loan_amount=100000,
        loan_purpose="Home Purchase",
        employment_company="Tech Corp",
        employment_status="employed"
    )

    print("\n📋 Sample Application:")
    print(f"  Applicant: {sample_app.applicant_name}")
    print(f"  Income: ${sample_app.annual_income:,.2f}")
    print(f"  Credit Score: {sample_app.credit_score}")
    print(f"  Loan Amount: ${sample_app.loan_amount:,.2f}")

    print("\n⏳ Processing through multi-agent system...")

    result = process_loan_application(sample_app, "DEMO-001")

    print("\n✅ Processing Complete!")
    print(f"\nDecision: {result.status}")
    print(f"Risk Score: {result.decision.risk_score:.2f}/100")
    print(f"Confidence: {result.decision.confidence_level*100:.1f}%")
    print(f"\nExplanation: {result.decision.explanation}")
    print(f"\nOverall Reasoning: {result.overall_reasoning}")


def main():
    parser = argparse.ArgumentParser(
        description="Agentic AI Intelligent Loan Approval System"
    )
    parser.add_argument(
        "--mode",
        choices=["full", "demo", "api-only"],
        default="full",
        help="Running mode: full (all services), demo (test agents), api-only (backend only)"
    )
    parser.add_argument(
        "--skip-dependencies",
        action="store_true",
        help="Skip dependency check"
    )

    args = parser.parse_args()

    print("\n" + "="*60)
    print("AGENTIC AI INTELLIGENT LOAN APPROVAL SYSTEM")
    print("="*60)
    print("Multi-Agent Orchestration with LangGraph")
    print("Distributed Microservices Architecture")

    if not args.skip_dependencies:
        print("\n🔍 Checking dependencies...")
        missing = check_dependencies()
        if missing:
            print(f"\n❌ Missing packages: {', '.join(missing)}")
            print("\nInstall with: pip install -r requirements.txt")
            sys.exit(1)
        print("   ✅ All dependencies available")

    try:
        if args.mode in ["full", "api-only"]:
            init_database()
            mcp_processes = start_mcp_servers()
            microservice_process = start_microservice()

            if args.mode == "api-only":
                print("\n" + "="*60)
                print("API-Only Mode: Backend services running")
                print("="*60)
                print("\n📍 API Documentation: http://127.0.0.1:8000/docs")
                print("   Submit applications to: http://127.0.0.1:8000/submit_application\n")

                try:
                    input("Press Enter to stop services...")
                except KeyboardInterrupt:
                    pass
            else:
                start_streamlit()

        elif args.mode == "demo":
            demo_mode()

    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down services...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
