# Agentic AI Intelligent Loan Approval System

A distributed, microservices-based multi-agent architecture for intelligent loan processing using LangGraph orchestration and Anthropic Claude.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│              Streamlit Chatbot UI (Port 8501)               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Microservice Layer                         │
│         FastAPI REST Endpoints (Port 8000)                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Orchestration Layer                         │
│      LangGraph-based Workflow Engine & State Manager        │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
┌────────────────────┐ ┌──────────────┐ ┌──────────────────┐
│  Applicant Agent   │ │ Financial    │ │ Decision Agent   │
│                    │ │ Risk Agent   │ │                  │
│ • Income Stability │ │              │ │ • Approval Logic │
│ • Employment Risk  │ │ • DTI Ratio  │ │ • Risk Scoring   │
│ • Credit Summary   │ │ • Credit     │ │ • Confidence     │
└────────────────────┘ │   Risk       │ └──────────────────┘
                       │ • Anomalies  │
                       └──────────────┘
            │
            ▼
┌────────────────────────────────────────┐
│      Compliance & Action Agent         │
│  • Notification Management             │
│  • Case Tracking                       │
└────────────────────────────────────────┘
```

## 🔌 MCP Servers

Each domain-specific agent communicates through dedicated MCP servers:

- **ApplicantDB Server** (Port 8001) - Applicant profile data management
- **RiskRulesDB Server** (Port 8002) - Financial risk assessment rules
- **DecisionSynthesis Server** (Port 8003) - Decision aggregation
- **NotificationSystem Server** (Port 8004) - Application notifications

## 📦 Components

### Core Modules

```
├── main.py                          # Main entry point
├── microservice.py                  # FastAPI microservice
├── orchestrator.py                  # LangGraph workflow engine
├── chatbot_ui.py                    # Streamlit chatbot UI
├── schemas.py                       # Data models & validation
├── config.py                        # Configuration management
│
├── agents/                          # Domain-specific agents
│   ├── applicant_agent.py           # Applicant profile analysis
│   ├── financial_risk_agent.py      # Financial risk assessment
│   ├── decision_agent.py            # Decision synthesis
│   └── compliance_agent.py          # Compliance & notifications
│
└── mcp_servers/                     # MCP server implementations
    ├── applicant_db_server.py       # Applicant data MCP
    ├── risk_rules_server.py         # Risk rules MCP
    ├── decision_synthesis_server.py # Decision MCP
    └── notification_server.py       # Notification MCP
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to project directory
cd /home/ubuntu/Desktop/demo/Capstone_Project

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Edit .env and add your Anthropic API key
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 2. Run Full System

```bash
# Method 1: Using main.py (Recommended)
python main.py --mode full

# Method 2: Using shell script
bash run_services.sh

# Method 3: Individual services
# Terminal 1: MCP Servers
python mcp_servers/applicant_db_server.py &
python mcp_servers/risk_rules_server.py &
python mcp_servers/decision_synthesis_server.py &
python mcp_servers/notification_server.py &

# Terminal 2: FastAPI Microservice
python microservice.py

# Terminal 3: Streamlit UI
streamlit run chatbot_ui.py
```

### 3. Demo Mode

```bash
python main.py --mode demo
```

This runs a sample loan application through the entire multi-agent system.

### 4. API-Only Mode

```bash
python main.py --mode api-only
```

Starts backend services for programmatic access via FastAPI (http://localhost:8000/docs).

## 📝 Usage

### Via Streamlit UI

1. Navigate to `http://localhost:8501` in your browser
2. Enter loan application details in the "New Application" tab
3. Click "Submit Application"
4. View real-time multi-agent analysis and decision

### Via REST API

```bash
# Submit application
curl -X POST http://127.0.0.1:8000/submit_application \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "APP-001",
    "applicant_name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-1234",
    "annual_income": 75000,
    "employment_type": "employed",
    "employment_years": 5,
    "credit_score": 720,
    "existing_debt": 15000,
    "loan_amount": 100000,
    "loan_purpose": "Home Purchase",
    "employment_company": "Tech Corp",
    "employment_status": "employed"
  }'

# Check application status
curl http://127.0.0.1:8000/application_status/APP-001

# List all applications
curl http://127.0.0.1:8000/applications
```

## 🤖 Agent Responsibilities

### 1. Applicant Profile Agent
- Analyzes applicant employment history and income stability
- Evaluates credit profile
- Identifies application completeness issues
- **Output:** Income Stability Score, Employment Risk, Credit Summary

### 2. Financial Risk Agent
- Calculates debt-to-income ratio
- Assesses credit score risk
- Evaluates loan-to-income ratio
- Detects financial anomalies
- **Output:** DTI, Credit Risk Level, Loan Risk, Anomalies

### 3. Decision Agent
- Synthesizes risk scores from other agents
- Determines approval/rejection/review classification
- Calculates confidence levels
- Identifies key decision factors
- **Output:** Classification, Risk Score, Confidence, Factors

### 4. Compliance & Action Agent
- Generates case tracking IDs
- Executes compliance actions
- Sends notifications
- Maintains audit trail
- **Output:** Action Taken, Case ID, Notification Status

## 📊 Key Features

### Multi-Agent Orchestration
- **LangGraph Workflow:** Parallel and sequential agent execution
- **State Management:** Shared state across agent pipeline
- **Error Handling:** Graceful failure recovery

### Distributed Architecture
- **Microservices:** Independent scalable services
- **MCP Servers:** Standardized agent communication
- **FastAPI:** RESTful API for external integration

### Explainable AI
- **Decision Factors:** Clear reasoning for each decision
- **Risk Scoring:** Transparent risk calculation
- **Audit Trail:** Complete decision history

### Production-Ready
- **Type Validation:** Pydantic models for data integrity
- **CORS Support:** Cross-origin requests enabled
- **Health Checks:** Service status monitoring
- **Error Handling:** Comprehensive exception management

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Model selection
MODEL = "claude-sonnet-4-20250514"

# Service ports
FASTAPI_PORT = 8000  # Main microservice
# MCP servers: 8001-8004

# API endpoints
ANTHROPIC_API_KEY = "your-key"
```

## 📈 Workflow Pipeline

```
1. Application Submission
   ↓
2. Validation Node (LangGraph)
   ├─→ 3a. Applicant Profile Analysis (Parallel)
   └─→ 3b. Financial Risk Analysis (Parallel)
      ↓
4. Decision Synthesis Node
   ├─→ Calculate Risk Score
   ├─→ Determine Decision (Approve/Reject/Review)
   ├─→ Set Confidence Level
   └─→ Identify Key Factors
      ↓
5. Compliance Node
   ├─→ Generate Case ID
   ├─→ Execute Action
   └─→ Send Notification
      ↓
6. Response to UI/API
```

## 🧪 Testing

### Run Demo
```bash
python main.py --mode demo
```

### Test with Custom Application
```python
from schemas import LoanApplication
from orchestrator import process_loan_application

app = LoanApplication(
    applicant_id="TEST-001",
    applicant_name="Jane Smith",
    email="jane@example.com",
    phone="+1-555-5678",
    annual_income=95000,
    employment_type="employed",
    employment_years=8,
    credit_score=780,
    existing_debt=8000,
    loan_amount=250000,
    loan_purpose="Home Purchase",
    employment_company="Finance Inc",
    employment_status="employed"
)

result = process_loan_application(app, "TEST-001")
print(result)
```

## 📚 API Documentation

Interactive API docs available at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔐 Security Considerations

- API keys should be stored in environment variables
- CORS is configured to allow all origins (adjust in production)
- Input validation via Pydantic models
- Error messages don't leak sensitive information

## 📝 Logging

Logs are printed to console with INFO level. Customize in `microservice.py`:

```python
logging.basicConfig(level=logging.DEBUG)  # For verbose logging
```

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Kill process using the port
kill -9 <PID>
```

### API Connection Error
```bash
# Check if microservice is running
curl http://127.0.0.1:8000/health

# Verify MCP servers are running
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:8002/health
curl http://127.0.0.1:8003/health
curl http://127.0.0.1:8004/health
```

### Streamlit Not Connecting
- Ensure microservice is running on port 8000
- Check firewall settings
- Verify API_BASE_URL in `chatbot_ui.py`

## 📞 Support

For issues or questions:
1. Check application logs for error messages
2. Verify all services are running: `ps aux | grep python`
3. Test API endpoints directly with curl
4. Review CLAUDE.md for additional documentation

## 📄 License

Educational project for demonstrating Agentic AI architecture.

## 🎓 Learning Objectives

This implementation demonstrates:
- ✅ Multi-agent AI system design
- ✅ LangGraph orchestration patterns
- ✅ Microservices architecture
- ✅ MCP server implementation
- ✅ FastAPI REST API design
- ✅ Streamlit UI development
- ✅ State management in distributed systems
- ✅ Explainable AI outputs
- ✅ Production-ready Python code patterns
