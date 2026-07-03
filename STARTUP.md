# Quick Start Guide

## 🚀 Getting Started (5 minutes)

### Step 1: Install Dependencies

```bash
cd /home/ubuntu/Desktop/demo/Capstone_Project

# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import fastapi, streamlit, langgraph; print('✅ Dependencies installed')"
```

### Step 2: Set Environment Variables

```bash
# Edit .env file and add your Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-xxx..."

# Verify it's set
echo $ANTHROPIC_API_KEY
```

### Step 3: Run Tests (Optional)

```bash
# Test all agents with sample data
python test_agents.py
```

**Expected Output:**
```
✅ Testing Complete Workflow...
  Testing: Strong Applicant
  ✅ Processing successful
     Decision: approved
     Risk Score: 25.3/100
     ...
```

### Step 4: Start the System

#### Option A: Full System with UI (Recommended)

```bash
python main.py --mode full
```

This will:
1. Start ApplicantDB server (Port 8001)
2. Start RiskRulesDB server (Port 8002)
3. Start DecisionSynthesis server (Port 8003)
4. Start NotificationSystem server (Port 8004)
5. Start FastAPI microservice (Port 8000)
6. Launch Streamlit UI (Port 8501)

#### Option B: API-Only Mode

```bash
python main.py --mode api-only
```

API will be available at: http://localhost:8000/docs

#### Option C: Demo Mode

```bash
python main.py --mode demo
```

Tests the system with a sample application.

### Step 5: Access the System

#### UI (Full Mode)
- **URL:** http://localhost:8501
- **Tabs:**
  - 📝 **New Application** - Submit loan applications
  - 📊 **Application Status** - Look up existing applications
  - 📈 **Analytics** - View system analytics

#### API (All Modes)
- **Swagger Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **API Base:** http://localhost:8000

#### API Endpoints

```bash
# Submit a loan application
curl -X POST http://localhost:8000/submit_application \
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
curl http://localhost:8000/application_status/APP-001

# List applications
curl http://localhost:8000/applications

# Service health check
curl http://localhost:8000/health
```

## 📝 Using the Streamlit UI

### 1. **New Application Tab**

Fill in the form fields:
- **Personal Info:** Name, ID, Email, Phone
- **Employment:** Type, Years, Company
- **Financial:** Income, Credit Score, Debt, Loan Amount, Purpose

Click **"🚀 Submit Application"**

Results display instantly with:
- ✅ Decision (Approved/Rejected/Review)
- 📊 Risk Score & Confidence Level
- 📈 Detailed Analysis breakdown
- 📋 Compliance Information

### 2. **Status Lookup Tab**

Enter an application ID (e.g., `APP-001`) to view previous results.

### 3. **Analytics Tab**

View system statistics:
- Total applications processed
- Approval/Rejection/Review counts
- Recent applications list

## 🧪 Test Applications

Try these pre-built test scenarios:

### Strong Applicant (Should Approve)
```json
{
  "applicant_name": "Alice Johnson",
  "applicant_id": "TEST-STRONG",
  "annual_income": 120000,
  "employment_years": 8,
  "credit_score": 780,
  "existing_debt": 5000,
  "loan_amount": 200000
}
```

### Borderline Applicant (Should Review)
```json
{
  "applicant_name": "Bob Smith",
  "applicant_id": "TEST-BORDER",
  "annual_income": 65000,
  "employment_years": 3,
  "credit_score": 680,
  "existing_debt": 25000,
  "loan_amount": 150000
}
```

### Weak Applicant (Should Reject)
```json
{
  "applicant_name": "Charlie Brown",
  "applicant_id": "TEST-WEAK",
  "annual_income": 35000,
  "employment_years": 1,
  "credit_score": 580,
  "existing_debt": 40000,
  "loan_amount": 100000
}
```

## 🔍 Monitoring

### Check Service Status

```bash
# Microservice
curl http://localhost:8000/health

# ApplicantDB
curl http://localhost:8001/health

# RiskRulesDB
curl http://localhost:8002/health

# DecisionSynthesis
curl http://localhost:8003/health

# NotificationSystem
curl http://localhost:8004/health
```

### View Running Processes

```bash
ps aux | grep python
```

### Check Logs

Each service prints logs to console. Look for:
- `INFO` - Normal operation
- `ERROR` - Problems to investigate

## 🆘 Troubleshooting

### Port Already in Use

```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port (edit config.py)
```

### "Connection refused" Error

```bash
# Check if services are running
curl http://localhost:8000/health

# If not, restart the system
python main.py --mode full
```

### Streamlit Not Loading

```bash
# Ensure microservice is running on 8000
curl http://localhost:8000/health

# Try refreshing the page or clearing browser cache
# Try: http://localhost:8501/?session_id=xxx
```

### API Returns 500 Error

1. Check console logs for error message
2. Verify all MCP servers are running
3. Check that ANTHROPIC_API_KEY is set
4. Restart the system

## 📚 Project Structure

```
Capstone_Project/
├── main.py                    # Main entry point
├── microservice.py            # FastAPI backend
├── chatbot_ui.py             # Streamlit UI
├── orchestrator.py           # LangGraph workflow
├── schemas.py                # Data models
├── config.py                 # Configuration
│
├── agents/                   # Agent implementations
│   ├── applicant_agent.py
│   ├── financial_risk_agent.py
│   ├── decision_agent.py
│   └── compliance_agent.py
│
├── mcp_servers/              # MCP server implementations
│   ├── applicant_db_server.py
│   ├── risk_rules_server.py
│   ├── decision_synthesis_server.py
│   └── notification_server.py
│
├── test_agents.py            # Test suite
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── README.md                 # Full documentation
├── CLAUDE.md                 # Technical documentation
└── STARTUP.md               # This file
```

## 🎯 Next Steps

1. **Explore the Code**
   - Read `CLAUDE.md` for architecture details
   - Review agent implementations in `agents/`
   - Study `orchestrator.py` for workflow logic

2. **Modify and Experiment**
   - Change risk scoring weights in `decision_agent.py`
   - Adjust decision thresholds in `decision_agent.py`
   - Add new anomaly detection rules in `financial_risk_agent.py`

3. **Deploy**
   - Follow deployment guidelines in `CLAUDE.md`
   - Set up Docker containers for each service
   - Configure database and caching layers

## ✅ Verification Checklist

- [ ] Dependencies installed (`pip list | grep fastapi`)
- [ ] API key configured (`echo $ANTHROPIC_API_KEY`)
- [ ] Services starting without errors
- [ ] UI accessible at localhost:8501
- [ ] Sample application processing successfully
- [ ] Decision output makes sense
- [ ] Multiple applications showing different decisions

## 📞 Support

- **Documentation:** See `README.md` and `CLAUDE.md`
- **API Reference:** http://localhost:8000/docs
- **Issues:** Check console logs for error messages

---

**You're all set!** 🎉 The Agentic AI Loan Approval System is ready to use.

For evaluation purposes:
- Demonstrate the system with the test applications
- Show how agents are orchestrated in real-time
- Discuss the architecture and design decisions
- Modify code live during the evaluation session
