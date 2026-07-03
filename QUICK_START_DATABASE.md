# ⚡ Quick Start - Database & Search

## One-Time Setup

```bash
# Install dependencies
pip install sqlalchemy tabulate

# Initialize database
python init_database.py

# You'll see:
# ✓ Database initialized successfully!
# ✓ Database location: sqlite:///./loan_applications.db
# ✓ Tables created: applications, applicant_cache, risk_assessments, decisions, notifications
```

---

## Running the System

### Terminal 1 - Start Microservice (API)
```bash
python microservice.py
```

### Terminal 2 - Start Streamlit UI
```bash
streamlit run chatbot_ui.py
```

### Open Browser
```
http://localhost:8501
```

---

## Using Database Features

### In Streamlit UI (Easiest)
1. Open the **"🗄️ Database Viewer"** tab
2. Search by:
   - **Application ID**: `APP-XXXXX`
   - **Applicant Name**: `John Doe`
   - **Status**: Approved / Rejected / Review
3. Click **View Statistics** to see:
   - Total applications
   - Approval rate
   - Average credit score
   - Total loan amount
4. Click on any application to see **full details** across 4 tabs

---

## Command-Line Tools

### Interactive Mode (Menu-Driven)
```bash
python database_cli.py
```

### Quick Commands

**View all applications:**
```bash
python database_cli.py all
python database_cli.py all 100  # Show 100 records
```

**Search by Application ID:**
```bash
python database_cli.py search APP-ABC123
```

**Search by Name:**
```bash
python database_cli.py name "John Doe"
```

**Filter by Status:**
```bash
python database_cli.py status approved
python database_cli.py status rejected
python database_cli.py status review
```

**View Statistics:**
```bash
python database_cli.py stats
```

---

## REST API Endpoints

### Search Applications
```bash
curl "http://localhost:8000/search_applications?search_query=John&status_filter=approved&limit=50"
```

### Get Application Details
```bash
curl http://localhost:8000/application_details/APP-ABC123
```

### Get All Applications
```bash
curl http://localhost:8000/applications/all?limit=50&offset=0
```

### Get Statistics
```bash
curl http://localhost:8000/database_stats
```

---

## Sample Workflow

### 1️⃣ Submit Application (UI)
- Open Streamlit at `http://localhost:8501`
- Fill out **New Application** form
- Click **Submit Application**
- Note the **Application ID** (e.g., `APP-ABC123`)

### 2️⃣ Search Database
**Via UI:**
- Go to **🗄️ Database Viewer** tab
- Enter Application ID in search box
- Click **🔍 Search Database**
- View full application details

**Via CLI:**
```bash
python database_cli.py search APP-ABC123
```

### 3️⃣ View Statistics
**Via UI:**
- Click **📊 View Statistics** button

**Via CLI:**
```bash
python database_cli.py stats
```

**Via API:**
```bash
curl http://localhost:8000/database_stats | python -m json.tool
```

---

## Data Stored

For each application:
- ✅ Applicant information (name, email, ID)
- ✅ Financial data (income, credit score, debt, loan amount)
- ✅ Employment details (type, years, company)
- ✅ Agent analysis results (income stability, employment risk, financial risk)
- ✅ Final decision (approved/rejected/review + risk score + confidence)
- ✅ Compliance actions (case ID, notifications)
- ✅ Timestamps (created, updated)

---

## Database Files

```
/home/ubuntu/Desktop/demo/Capstone_Project/
├── loan_applications.db          ← SQLite database file
├── database.py                   ← Database configuration
├── database_cli.py               ← CLI tool for queries
├── query_database.py             ← Quick query script
├── init_database.py              ← Database initialization
└── DATABASE_GUIDE.md             ← Full documentation
```

---

## Useful Queries

### Python Script - Export Approved Applications
```python
from database import SessionLocal, ApplicationRecord

db = SessionLocal()
approved_apps = db.query(ApplicationRecord).filter(
    ApplicationRecord.status == "approved"
).all()

print(f"Total Approved: {len(approved_apps)}")
for app in approved_apps:
    print(f"  {app.id}: {app.applicant_name} - ${app.loan_amount:,.2f}")

db.close()
```

### Python Script - Get Average Risk Score
```python
from database import SessionLocal, ApplicationRecord

db = SessionLocal()
records = db.query(ApplicationRecord).all()

risk_scores = [
    r.loan_decision.get('risk_score')
    for r in records if r.loan_decision
]

avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0
print(f"Average Risk Score: {avg_risk:.1f}/100")

db.close()
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **"Application not found"** | Submit an application first or check the ID spelling |
| **"Connection refused"** | Start microservice: `python microservice.py` |
| ****No database file** | Run: `python init_database.py` |
| **API too slow** | Use CLI tool instead: `python database_cli.py` |

---

## Next Steps

1. ✅ Initialize database: `python init_database.py`
2. ✅ Start microservice: `python microservice.py`
3. ✅ Start UI: `streamlit run chatbot_ui.py`
4. ✅ Submit test applications
5. ✅ Search and view via UI or CLI

**All data is now persistent and searchable!** 🎉
