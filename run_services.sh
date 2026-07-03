#!/bin/bash

echo "Starting Agentic AI Loan Approval System..."
echo "============================================"

echo ""
echo "[1/5] Starting ApplicantDB MCP Server (Port 8001)..."
python mcp_servers/applicant_db_server.py &
APPLICANT_PID=$!
sleep 2

echo "[2/5] Starting RiskRulesDB MCP Server (Port 8002)..."
python mcp_servers/risk_rules_server.py &
RISK_PID=$!
sleep 2

echo "[3/5] Starting DecisionSynthesis MCP Server (Port 8003)..."
python mcp_servers/decision_synthesis_server.py &
DECISION_PID=$!
sleep 2

echo "[4/5] Starting NotificationSystem MCP Server (Port 8004)..."
python mcp_servers/notification_server.py &
NOTIFICATION_PID=$!
sleep 2

echo "[5/5] Starting FastAPI Microservice (Port 8000)..."
python microservice.py &
MICROSERVICE_PID=$!
sleep 3

echo ""
echo "✅ All backend services started!"
echo ""
echo "Process IDs:"
echo "  ApplicantDB: $APPLICANT_PID"
echo "  RiskRulesDB: $RISK_PID"
echo "  DecisionSynthesis: $DECISION_PID"
echo "  NotificationSystem: $NOTIFICATION_PID"
echo "  FastAPI Microservice: $MICROSERVICE_PID"
echo ""
echo "🚀 Starting Streamlit UI..."
streamlit run chatbot_ui.py

trap "kill $APPLICANT_PID $RISK_PID $DECISION_PID $NOTIFICATION_PID $MICROSERVICE_PID" EXIT
