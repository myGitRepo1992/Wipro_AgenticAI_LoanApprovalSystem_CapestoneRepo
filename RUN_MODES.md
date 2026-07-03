# 🚀 Running Modes - main.py

## Available Modes

### 1. **Full Mode** (Default - Everything)
```bash
python main.py --mode full
# or
python main.py
```

**Starts:**
- ✅ All 4 MCP Servers (ports 8001-8004)
- ✅ FastAPI Microservice (port 8000)
- ✅ Streamlit Web UI (port 8501)
- ✅ Database initialization

**Access:**
- Web UI: http://localhost:8501
- API Docs: http://localhost:8000/docs
- Submit applications and search via UI

**Best for:** Complete system testing with UI

---

### 2. **Demo Mode** (Fastest - Test Agents)
```bash
python main.py --mode demo
```

**Does:**
- ✅ Creates a sample loan application
- ✅ Processes through all 4 agents
- ✅ Shows decision results
- ✅ No background services running
- ✅ Completes in 2-5 seconds

**Output Example:**
```
📋 Sample Application:
  Applicant: John Doe
  Income: $75,000.00
  Credit Score: 720
  Loan Amount: $100,000.00

✅ Processing Complete!

Decision: APPROVED
Risk Score: 27.27/100
Confidence: 95.0%
```

**Best for:** Quick testing, demos, validation

---

### 3. **API-Only Mode** (Backend Services Only)
```bash
python main.py --mode api-only
```

**Starts:**
- ✅ All 4 MCP Servers (ports 8001-8004)
- ✅ FastAPI Microservice (port 8000)
- ✅ NO Streamlit UI
- ✅ Database initialization

**Access:**
- API Documentation: http://localhost:8000/docs
- Submit via curl/Postman/Python requests

**Best for:** API testing, programmatic access, headless deployment

---

## Mode Comparison

| Feature | Full | Demo | API-Only |
|---------|------|------|----------|
| **Web UI** | ✅ | ❌ | ❌ |
| **API Server** | ✅ | ❌ | ✅ |
| **MCP Servers** | ✅ | ❌ | ✅ |
| **Database** | ✅ | ❌ | ✅ |
| **Agent Testing** | ✅ | ✅ | ✅ |
| **Startup Time** | ~10s | ~2s | ~8s |
| **Persistent Data** | ✅ | ❌ | ✅ |

---

## Usage Examples

### Full Mode Workflow
```bash
# Start all services
python main.py --mode full

# In browser: http://localhost:8501
# 1. Submit application in "📝 New Application" tab
# 2. Note the Application ID
# 3. Go to "🗄️ Database Viewer" tab
# 4. Search by Application ID
# 5. View full details and statistics
```

### Demo Mode Workflow
```bash
# Quick test of multi-agent system
python main.py --mode demo

# Output shows:
# - Sample application details
# - Processing through agents
# - Final decision with confidence
# - Risk analysis and reasoning
```

### API-Only Workflow
```bash
# Start backend services
python main.py --mode api-only

# In another terminal, submit application:
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

# Search applications:
curl "http://localhost:8000/search_applications?search_query=Jane"

# View statistics:
curl http://localhost:8000/database_stats
```

---

## Additional Flags

### Skip Dependency Check
```bash
python main.py --mode full --skip-dependencies
```

Useful when:
- Dependencies already verified
- Running in CI/CD pipelines
- Faster startup needed

---

## Output Examples

### Full Mode Startup
```
============================================================
AGENTIC AI INTELLIGENT LOAN APPROVAL SYSTEM
============================================================

🔍 Checking dependencies...
   ✅ All dependencies available

🗄️  Initializing database...
   ✅ Database ready at loan_applications.db

============================================================
Starting MCP Servers...
============================================================

🚀 Starting ApplicantDB (Port 8001)...
   ✅ ApplicantDB ready at http://127.0.0.1:8001/health

🚀 Starting RiskRulesDB (Port 8002)...
   ✅ RiskRulesDB ready at http://127.0.0.1:8002/health

[... more servers ...]

============================================================
Starting FastAPI Microservice...
============================================================

🚀 Starting microservice on http://127.0.0.1:8000...
   ✅ Microservice ready at http://127.0.0.1:8000

============================================================
Starting Streamlit UI...
============================================================

🚀 Opening Streamlit app in browser...
   📍 Available at: http://localhost:8501
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8000  # Check port 8000

# Kill process
kill -9 <PID>

# Then restart
python main.py --mode full
```

### Database Initialization Failed
```bash
# Reinitialize database manually
python init_database.py

# Then run main.py
python main.py --mode full
```

### Missing Dependencies
```bash
# Install all requirements
pip install -r requirements.txt

# Then run
python main.py --mode full
```

---

## Development vs Production

### Development (Local Testing)
```bash
# Full mode for UI development
python main.py --mode full

# Demo mode for quick validation
python main.py --mode demo
```

### Testing (API Testing)
```bash
# API-only mode for endpoint testing
python main.py --mode api-only

# Then use curl/Postman in another terminal
```

### Production (Headless)
```bash
# Start in API-only mode
python main.py --mode api-only &

# Or use systemd/docker to manage processes
```

---

## Quick Reference

```bash
# Everything (UI + API + Agents)
python main.py --mode full

# Quick test (agents only)
python main.py --mode demo

# API only (for integration)
python main.py --mode api-only

# Skip dependency checks
python main.py --mode full --skip-dependencies
```

---

**The system is now fully operational with database persistence, search capability, and multiple run modes!** 🎉
