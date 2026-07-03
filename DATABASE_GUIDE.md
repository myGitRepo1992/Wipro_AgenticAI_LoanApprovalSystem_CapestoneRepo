# 🗄️ Database Access & Management Guide

## Overview

Your loan approval system now has **persistent SQL database storage** with multiple ways to access and search application records.

## Database Setup

### Location
```
/home/ubuntu/Desktop/demo/Capstone_Project/loan_applications.db
```

### Tables
- **applications** - Complete loan applications with decisions
- **applicant_cache** - Cached applicant profile data
- **risk_assessments** - Financial risk evaluations
- **decisions** - Loan decision records
- **notifications** - Notification and case tracking

## Access Methods

### 1. 🖥️ Streamlit Web UI (Recommended for Visual Browsing)

#### Launch the UI:
```bash
streamlit run chatbot_ui.py
```

#### Database Viewer Tab Features:
- **🔍 Search** - Find applications by:
  - Application ID (e.g., `APP-XXXXX`)
  - Applicant Name (e.g., `John Doe`)
  - Applicant ID (e.g., `APP-12345`)

- **📊 View Statistics** - See:
  - Total applications
  - Approval/Rejection/Review counts
  - Total loan amounts
  - Average credit scores

- **📋 Detailed View** - Click any application to see:
  - Basic Information (name, ID, status, dates)
  - Financial Details (income, credit score, debt)
  - Analysis Results (profile, risk assessment)
  - Decision Details (status, confidence, factors)

---

### 2. 📡 REST API (Programmatic Access)

#### Start the microservice:
```bash
python microservice.py
```

#### Base URL:
```
http://localhost:8000
```

#### Endpoints:

##### Get All Applications
```bash
GET /applications/all?limit=100&offset=0

Example:
curl http://localhost:8000/applications/all?limit=50
```

##### Search Applications
```bash
GET /search_applications?search_query=John&status_filter=approved&limit=50

Example:
curl "http://localhost:8000/search_applications?search_query=APP-ABC123&status_filter=approved"
```

##### Get Application Details
```bash
GET /application_details/{application_id}

Example:
curl http://localhost:8000/application_details/APP-ABC123
```

##### Get Database Statistics
```bash
GET /database_stats

Example:
curl http://localhost:8000/database_stats
```

#### Response Examples:

**Search Response:**
```json
{
  "status": "success",
  "count": 5,
  "applications": [
    {
      "application_id": "APP-ABC123",
      "applicant_name": "John Doe",
      "status": "approved",
      "loan_amount": 100000.0,
      "credit_score": 720,
      "risk_score": 25.5,
      "created_at": "2026-07-01T10:30:00"
    }
  ]
}
```

**Statistics Response:**
```json
{
  "status": "success",
  "statistics": {
    "total_applications": 15,
    "approved_count": 10,
    "rejected_count": 2,
    "review_count": 3,
    "approval_rate": 66.67,
    "total_loan_amount": 1500000.0,
    "average_credit_score": 695.0
  }
}
```

---

### 3. 🖱️ CLI Tool (Interactive & Command-Line)

#### Interactive Mode:
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

#### Command-Line Mode:

**View all applications (latest 50):**
```bash
python database_cli.py all
python database_cli.py all 100  # Show 100 records
```

**Search by Application ID:**
```bash
python database_cli.py search APP-ABC123
```

**Search by Applicant Name:**
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

### 4. 🔧 Direct Database Query Script

#### View and Query Database:
```bash
# View all applications (default 50)
python query_database.py

# View specific application details
python query_database.py APP-ABC123

# View statistics
python query_database.py stats
```

---

## Data Retrieval Examples

### Using REST API with Python:

```python
import requests

BASE_URL = "http://localhost:8000"

# Search applications
response = requests.get(
    f"{BASE_URL}/search_applications",
    params={
        "search_query": "John",
        "status_filter": "approved",
        "limit": 10
    }
)
applications = response.json()["applications"]
for app in applications:
    print(f"{app['application_id']} - {app['applicant_name']}: {app['status']}")

# Get statistics
stats = requests.get(f"{BASE_URL}/database_stats").json()
print(f"Approval Rate: {stats['statistics']['approval_rate']}%")

# Get detailed application
details = requests.get(f"{BASE_URL}/application_details/APP-ABC123").json()
print(details["application"]["overall_reasoning"])
```

### Using CLI Commands:

```bash
# Find all applications for a specific applicant
python database_cli.py name "Jane Smith"

# Get approval statistics
python database_cli.py stats

# Search specific application
python database_cli.py search APP-XYZ789
```

---

## Search Features

### Supported Search Methods

| Method | Field | Example |
|--------|-------|---------|
| Application ID | `application_id` | `APP-ABC123` |
| Applicant Name | `applicant_name` | `John Doe` |
| Applicant ID | `applicant_id` | `APP-12345` |

### Status Filters

- `approved` - Approved applications
- `rejected` - Rejected applications
- `review` - Applications under review
- `all` - No filtering (default)

### Result Limits

- Default: 50 records
- Maximum: 500 records (API) or system memory limit (CLI)
- Adjustable per request

---

## Database Schema

### Applications Table

```sql
CREATE TABLE applications (
  id VARCHAR PRIMARY KEY,
  applicant_id VARCHAR NOT NULL,
  applicant_name VARCHAR NOT NULL,
  applicant_email VARCHAR,
  annual_income FLOAT,
  credit_score INTEGER,
  loan_amount FLOAT,
  employment_type VARCHAR,
  employment_years INTEGER,
  existing_debt FLOAT,
  applicant_profile JSON,
  financial_risk JSON,
  loan_decision JSON,
  compliance_action JSON,
  overall_reasoning TEXT,
  status VARCHAR DEFAULT 'pending',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

### Key Fields

- **applicant_profile** (JSON)
  - income_stability_score
  - employment_risk
  - credit_history_summary
  - application_completeness_flags

- **financial_risk** (JSON)
  - debt_to_income_ratio
  - credit_score_risk_level
  - loan_amount_risk
  - anomaly_detection

- **loan_decision** (JSON)
  - classification (approved/rejected/review)
  - risk_score (0-100)
  - confidence_level (0-1)
  - key_decision_factors
  - explanation

- **compliance_action** (JSON)
  - action_taken
  - notification_sent
  - case_id
  - timestamp

---

## Performance Tips

### For Large Datasets

1. **Use pagination with API:**
   ```bash
   curl "http://localhost:8000/applications/all?limit=100&offset=0"
   curl "http://localhost:8000/applications/all?limit=100&offset=100"
   ```

2. **Filter before searching:**
   ```bash
   curl "http://localhost:8000/search_applications?status_filter=approved&limit=50"
   ```

3. **Use CLI for local queries (faster):**
   ```bash
   python database_cli.py all 1000  # Faster than API for large datasets
   ```

---

## Exporting Data

### Export to CSV (via Python):

```python
from database import SessionLocal, ApplicationRecord
import csv

db = SessionLocal()
records = db.query(ApplicationRecord).all()

with open('applications.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Name', 'Status', 'Loan Amount', 'Risk Score'])
    for r in records:
        writer.writerow([
            r.id,
            r.applicant_name,
            r.status,
            r.loan_amount,
            r.loan_decision.get('risk_score') if r.loan_decision else 'N/A'
        ])

db.close()
print("✅ Exported to applications.csv")
```

### Export via CLI (to terminal):

```bash
# Pipe to file
python database_cli.py all 1000 > applications.txt

# View and copy
python database_cli.py search APP-ABC123
```

---

## Troubleshooting

### Database Not Found
```bash
# Reinitialize database
python init_database.py
```

### No Records Found
```bash
# Check total count
python query_database.py stats

# Submit a test application first via UI
```

### API Connection Issues
```bash
# Verify microservice is running
curl http://localhost:8000/health

# Check port 8000 is available
netstat -tuln | grep 8000
```

### Slow Queries
```bash
# Use CLI for faster local queries
python database_cli.py all 100

# Add limit parameter
curl "http://localhost:8000/search_applications?limit=50"
```

---

## Summary of Access Methods

| Method | Best For | Speed | Installation |
|--------|----------|-------|--------------|
| **Web UI (Streamlit)** | Visual browsing, quick searches | Fast | Built-in |
| **REST API** | Programmatic access, integrations | Medium | Built-in |
| **CLI Tool** | Command-line, large datasets | Fast | Built-in |
| **Query Script** | Simple queries | Very Fast | Built-in |

---

**Quick Start:**
```bash
# 1. Initialize database
python init_database.py

# 2. Start microservice
python microservice.py &

# 3. Start UI
streamlit run chatbot_ui.py

# 4. Submit applications and search via UI or API
```
