# ✅ Complete Setup & Running Guide

## What's Included

Your loan approval system now has:

1. ✅ **Multi-Agent Orchestration** (LangGraph)
   - Applicant Profile Agent
   - Financial Risk Agent
   - Decision Agent
   - Compliance Agent

2. ✅ **SQL Database** (SQLite)
   - Persistent application storage
   - Search and filtering
   - Statistics dashboard

3. ✅ **REST API** (FastAPI)
   - 8+ endpoints for searching and retrieving data
   - JSON responses
   - Full CORS support

4. ✅ **Web UI** (Streamlit)
   - New Application submission
   - Application Status lookup
   - Analytics dashboard
   - Database Viewer & Search

5. ✅ **CLI Tools**
   - Interactive database browser
   - Command-line search
   - Quick data export

6. ✅ **Multiple Run Modes**
   - Full (UI + API + Agents)
   - Demo (Quick test)
   - API-Only (Headless)

---

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database
```bash
python init_database.py
```

You'll see:
```
✓ Database initialized successfully!
✓ Database location: sqlite:///./loan_applications.db
✓ Tables created: applications, applicant_cache, risk_assessments, decisions, notifications
```

### Step 3: Run the System
```bash
# Full mode (UI + API + All Services)
python main.py --mode full

# or Quick demo
python main.py --mode demo

# or API-only
python main.py --mode api-only
```

---

## Running Modes

### 🎨 Full Mode (Recommended)
```bash
python main.py --mode full
```

Opens **http://localhost:8501** with:
- 📝 New Application form
- 📊 Application Status lookup
- 📈 Analytics dashboard
- 🗄️ Database Viewer & Search

**Features:**
- Submit new applications
- Search by Application ID, Name, or Status
- View approval statistics
- See detailed application breakdown
- All data persists to database

---

### ⚡ Demo Mode (Quick Test)
```bash
python main.py --mode demo
```

Runs a sample application through all agents instantly:
- No services running
- No UI needed
- Output shows decision and reasoning
- Good for validation

**Output:**
```
✅ Processing Complete!
Decision: APPROVED
Risk Score: 27.27/100
Confidence: 95.0%
```

---

### 🔧 API-Only Mode (Backend)
```bash
python main.py --mode api-only
```

Starts backend services at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

Use with curl, Postman, or your own frontend.

---

## Accessing the System

### Web UI
```
http://localhost:8501
```

**Tabs:**
1. **📝 New Application** - Submit applications
2. **📊 Application Status** - Lookup by ID
3. **📈 Analytics** - View statistics
4. **🗄️ Database Viewer** - Search & filter records

---

### REST API

#### Submit Application
```bash
curl -X POST http://localhost:8000/submit_application \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "TEST-001",
    "applicant_name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "+1-555-5678",
    "annual_income": 85000,
    "employment_type": "Full-time",
    "employment_years": 7,
    "credit_score": 750,
    "existing_debt": 5000,
    "loan_amount": 150000,
    "loan_purpose": "Home Purchase",
    "employment_company": "Finance Corp",
    "employment_status": "employed"
  }'
```

#### Search Applications
```bash
curl "http://localhost:8000/search_applications?search_query=Jane&status_filter=approved"
```

#### Get Application Details
```bash
curl http://localhost:8000/application_details/APP-ABC123
```

#### View Statistics
```bash
curl http://localhost:8000/database_stats
```

#### API Documentation
```
http://localhost:8000/docs
```

---

### Command-Line Tools

#### Interactive Mode
```bash
python database_cli.py
```

Menu options:
```
1. View all applications
2. Search by Application ID
3. Search by Applicant Name
4. Filter by Status
5. View Statistics
6. Exit
```

#### Quick Commands
```bash
# View all applications (latest 50)
python database_cli.py all

# Search by Application ID
python database_cli.py search APP-ABC123

# Search by Name
python database_cli.py name "John Doe"

# Filter by Status
python database_cli.py status approved

# View Statistics
python database_cli.py stats
```

---

## Database Features

### Search Capabilities
- **Application ID**: `APP-XXXXX`
- **Applicant Name**: Full or partial name
- **Applicant ID**: Original applicant ID
- **Status**: approved, rejected, review

### Data Stored
For each application:
- ✅ Applicant information
- ✅ Financial details
- ✅ Employment info
- ✅ Agent analysis results
- ✅ Final decision with confidence
- ✅ Compliance actions
- ✅ Audit trail with timestamps

### Accessing Data

**Via UI:** 🗄️ Database Viewer tab
**Via API:** `/search_applications`, `/application_details/{id}`, `/database_stats`
**Via CLI:** `python database_cli.py`
**Via Python:** Import `database.py` and query directly

---

## Example Workflow

### 1. Submit Application (UI)
```
1. Open http://localhost:8501
2. Fill out "📝 New Application" form
3. Click "🚀 Submit Application"
4. Note the Application ID (e.g., APP-ABC123)
5. See decision immediately
```

### 2. Search Database (UI)
```
1. Go to "🗄️ Database Viewer" tab
2. Enter Application ID in search box
3. Click "🔍 Search Database"
4. View application in results table
5. Click to see detailed breakdown
```

### 3. View Statistics (UI)
```
1. Click "📊 View Statistics" button
2. See:
   - Total applications
   - Approval rate
   - Average credit score
   - Total loan amount
```

### 4. Export Data (CLI)
```bash
python database_cli.py all 100 > applications.txt
python database_cli.py stats > statistics.txt
```

---

## Files Overview

### Core System
- `main.py` - Entry point (supports 3 modes)
- `orchestrator.py` - LangGraph workflow
- `microservice.py` - FastAPI server
- `chatbot_ui.py` - Streamlit UI

### Agents
- `agents/applicant_agent.py`
- `agents/financial_risk_agent.py`
- `agents/decision_agent.py`
- `agents/compliance_agent.py`

### Database
- `database.py` - SQLAlchemy configuration
- `database_cli.py` - CLI tool
- `init_database.py` - Initialization
- `query_database.py` - Query script

### Configuration
- `config.py` - Settings
- `schemas.py` - Data models
- `requirements.txt` - Dependencies

### Documentation
- `CLAUDE.md` - Architecture guide
- `DATABASE_GUIDE.md` - Database features
- `QUICK_START_DATABASE.md` - Quick reference
- `RUN_MODES.md` - Running modes
- `COMPLETE_SETUP.md` - This file

---

## Configuration

### Edit Settings
```python
# config.py
FASTAPI_HOST = "127.0.0.1"
FASTAPI_PORT = 8000
ANTHROPIC_API_KEY = "your-key"
```

### Database Location
```
/home/ubuntu/Desktop/demo/Capstone_Project/loan_applications.db
```

To change:
```python
# database.py
DATABASE_URL = "sqlite:///./custom_location.db"
```

---

## Troubleshooting

### Port Already in Use
```bash
# Kill process using port 8000
lsof -i :8000
kill -9 <PID>
```

### Database Error
```bash
# Reinitialize
python init_database.py
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### API Connection Issues
```bash
# Verify microservice
curl http://localhost:8000/health

# Check port
netstat -tuln | grep 8000
```

---

## Next Steps

### For Development
```bash
# 1. Full mode for feature testing
python main.py --mode full

# 2. Demo mode for validation
python main.py --mode demo

# 3. API-only for backend work
python main.py --mode api-only
```

### For Deployment
```bash
# 1. Initialize database
python init_database.py

# 2. Start in API-only mode
python main.py --mode api-only &

# 3. Deploy your frontend separately
```

### For Data Analysis
```bash
# Use CLI for batch queries
python database_cli.py all 1000 > all_applications.txt

# Or export via Python
python -c "
from database import SessionLocal, ApplicationRecord
db = SessionLocal()
apps = db.query(ApplicationRecord).all()
print(f'Total: {len(apps)}, Approved: {sum(1 for a in apps if a.status==\"approved\")}')
"
```

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────┐
│         Streamlit Web UI (Port 8501)                │
│  - New Application  - Status Lookup                 │
│  - Analytics        - Database Viewer               │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│      FastAPI Microservice (Port 8000)               │
│  - /submit_application                              │
│  - /search_applications                             │
│  - /application_details                             │
│  - /database_stats                                  │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│        LangGraph Orchestrator                       │
│  - Validate → Applicant Profile & Financial Risk   │
│  - Merge → Decision Synthesis → Compliance          │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│           4 MCP Servers (Ports 8001-8004)           │
│  - ApplicantDB      - RiskRulesDB                   │
│  - DecisionSynthesis - NotificationSystem           │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│       SQLite Database (loan_applications.db)        │
│  - applications  - applicant_cache                  │
│  - risk_assessments - decisions - notifications    │
└─────────────────────────────────────────────────────┘
```

---

## Summary

You now have a **complete, production-ready loan approval system** with:

✅ Multi-agent AI orchestration
✅ Persistent SQL database
✅ Full-featured REST API
✅ Beautiful web UI
✅ Command-line tools
✅ Comprehensive documentation
✅ Multiple run modes
✅ Search and analytics

**Ready to use!** 🚀

---

**Questions?** See:
- `DATABASE_GUIDE.md` - Database operations
- `RUN_MODES.md` - Running modes
- `CLAUDE.md` - Architecture details
- API Docs: http://localhost:8000/docs
