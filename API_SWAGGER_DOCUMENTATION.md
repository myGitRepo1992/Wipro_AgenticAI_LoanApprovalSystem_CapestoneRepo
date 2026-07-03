# API Swagger Documentation - All Microservices

Complete OpenAPI/Swagger documentation for the Multi-Agent Loan Approval System.

---

## 📋 Table of Contents

1. [Main Microservice (Port 8000)](#main-microservice-port-8000)
2. [ApplicantDB MCP Server (Port 8001)](#applicantdb-mcp-server-port-8001)
3. [RiskRulesDB MCP Server (Port 8002)](#riskrulesdb-mcp-server-port-8002)
4. [DecisionSynthesis MCP Server (Port 8003)](#decisionsynthesis-mcp-server-port-8003)
5. [NotificationSystem MCP Server (Port 8004)](#notificationsystem-mcp-server-port-8004)

---

## Main Microservice (Port 8000)

**Base URL:** `http://localhost:8000`

### 1. Submit Loan Application

**Endpoint:** `POST /submit_application`

**Description:** Submits a loan application and processes it through the multi-agent orchestration engine.

**Request Body:**
```json
{
  "applicant_id": "12345",
  "applicant_name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-555-0001",
  "annual_income": 75000,
  "employment_type": "Full-time",
  "employment_years": 5,
  "employment_company": "TechCorp",
  "credit_score": 720,
  "existing_debt": 15000,
  "loan_amount": 100000,
  "loan_purpose": "Home Purchase",
  "employment_status": "employed",
  "loan_tenure": 10,
  "location": "New York, NY"
}
```

**Response (Success):**
```json
{
  "application_id": "CASE-APP-12345-20260702111939",
  "status": "approved",
  "decision": {
    "classification": "approved",
    "risk_score": 28.5,
    "confidence_level": 0.92,
    "key_decision_factors": [
      "Strong income stability",
      "Stable employment",
      "Good credit score",
      "Healthy DTI ratio"
    ],
    "explanation": "Application approved based on strong financial profile and low risk assessment."
  },
  "financial_risk": {
    "debt_to_income_ratio": 24.5,
    "credit_score_risk_level": "low",
    "loan_amount_risk": "low",
    "anomaly_detection": [],
    "reasoning": "Financial risk assessment indicates low risk profile"
  },
  "applicant_profile": {
    "income_stability_score": 82.5,
    "employment_risk": "low",
    "credit_history_summary": "Excellent credit history with 720 score",
    "application_completeness_flags": []
  },
  "compliance_action": {
    "action_taken": "Approval letter sent",
    "notification_sent": true,
    "case_id": "CASE-APP-12345-20260702111939",
    "timestamp": "2026-07-02T11:19:39Z",
    "summary": "Application approved and applicant notified"
  },
  "overall_reasoning": "Strong financial profile with low risk indicators"
}
```

**Status Codes:**
- `200 OK` - Application processed successfully
- `422 Unprocessable Entity` - Validation error in input
- `500 Internal Server Error` - Processing failed

---

### 2. Get Application Status

**Endpoint:** `GET /application_status/{application_id}`

**Description:** Retrieves the status of a previously submitted application.

**Parameters:**
- `application_id` (path, required): Application case ID (e.g., `CASE-APP-12345-20260702111939`)

**Response:**
```json
{
  "status": "success",
  "application_id": "CASE-APP-12345-20260702111939",
  "data": {
    "applicant_name": "John Doe",
    "loan_status": "approved",
    "decision": {
      "classification": "approved",
      "risk_score": 28.5,
      "confidence_level": 0.92,
      "key_decision_factors": ["Strong income stability", "Stable employment"],
      "explanation": "Application approved"
    },
    "risk_assessment": {
      "debt_to_income_ratio": 24.5,
      "credit_score_risk_level": "low",
      "loan_amount_risk": "low",
      "anomaly_detection": [],
      "reasoning": "Low risk profile"
    },
    "applicant_profile": {
      "income_stability_score": 82.5,
      "employment_risk": "low",
      "credit_history_summary": "Excellent credit",
      "application_completeness_flags": []
    },
    "created_at": "2026-07-02T11:19:39"
  }
}
```

**Status Codes:**
- `200 OK` - Application found
- `404 Not Found` - Application not found
- `500 Internal Server Error` - Server error

---

### 3. List Applications

**Endpoint:** `GET /applications`

**Description:** Lists recent applications.

**Query Parameters:**
- `limit` (optional, default: 10): Number of applications to return (1-100)

**Response:**
```json
{
  "status": "success",
  "count": 5,
  "applications": [
    {
      "id": "CASE-APP-12345-20260702111939",
      "applicant_name": "John Doe",
      "status": "approved",
      "loan_amount": 100000,
      "created_at": "2026-07-02T11:19:39"
    },
    {
      "id": "CASE-APP-54321-20260702110512",
      "applicant_name": "Jane Smith",
      "status": "rejected",
      "loan_amount": 150000,
      "created_at": "2026-07-02T11:05:12"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Applications retrieved
- `500 Internal Server Error` - Server error

---

### 4. Search Applications

**Endpoint:** `GET /search_applications`

**Description:** Search applications by ID or applicant name with optional status filter.

**Query Parameters:**
- `search_query` (optional): Search term (application ID, applicant name, or applicant ID)
- `status_filter` (optional): Filter by status (approved, rejected, review)
- `limit` (optional, default: 50): Maximum results to return

**Example:**
```
GET /search_applications?search_query=John&status_filter=approved&limit=20
```

**Response:**
```json
{
  "status": "success",
  "count": 2,
  "applications": [
    {
      "application_id": "CASE-APP-12345-20260702111939",
      "applicant_id": "12345",
      "applicant_name": "John Doe",
      "email": "john@example.com",
      "status": "approved",
      "loan_amount": 100000,
      "annual_income": 75000,
      "credit_score": 720,
      "created_at": "2026-07-02T11:19:39"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Search completed
- `500 Internal Server Error` - Server error

---

### 5. Get Application Details

**Endpoint:** `GET /application_details/{application_id}`

**Description:** Retrieves complete details of an application.

**Parameters:**
- `application_id` (path, required): Application case ID

**Response:**
```json
{
  "status": "success",
  "application": {
    "application_id": "CASE-APP-12345-20260702111939",
    "applicant_id": "12345",
    "applicant_name": "John Doe",
    "email": "john@example.com",
    "annual_income": 75000,
    "credit_score": 720,
    "loan_amount": 100000,
    "employment_type": "Full-time",
    "employment_years": 5,
    "existing_debt": 15000,
    "loan_tenure": 10,
    "location": "New York, NY",
    "status": "approved",
    "decision": { /* decision details */ },
    "financial_risk": { /* risk assessment */ },
    "applicant_profile": { /* profile analysis */ },
    "compliance_action": { /* compliance details */ },
    "created_at": "2026-07-02T11:19:39",
    "updated_at": "2026-07-02T11:19:45"
  }
}
```

**Status Codes:**
- `200 OK` - Application details retrieved
- `404 Not Found` - Application not found
- `500 Internal Server Error` - Server error

---

### 6. Health Check

**Endpoint:** `GET /health`

**Description:** Service health check.

**Response:**
```json
{
  "status": "healthy",
  "service": "Loan Approval Microservice"
}
```

---

## ApplicantDB MCP Server (Port 8001)

**Base URL:** `http://localhost:8001`

### 1. Analyze Applicant

**Endpoint:** `POST /analyze_applicant`

**Description:** MCP endpoint for analyzing applicant profile.

**Request Body:**
```json
{
  "applicant_id": "12345",
  "query_type": "profile_assessment"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "applicant_id": "12345",
    "income_stability_score": 82.5,
    "employment_risk": "low",
    "credit_history_summary": "Excellent credit history with 720 score",
    "application_completeness_flags": []
  },
  "query_type": "profile_assessment"
}
```

**Response (Not Found):**
```json
{
  "status": "pending",
  "message": "Applicant 12345 profile not found"
}
```

---

### 2. Cache Applicant

**Endpoint:** `POST /cache_applicant`

**Description:** Caches applicant profile data in database.

**Request Body:**
```json
{
  "applicant_id": "12345",
  "income_stability_score": 82.5,
  "employment_risk": "low",
  "credit_history_summary": "Excellent credit history with 720 score",
  "application_completeness_flags": []
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Cached applicant 12345"
}
```

---

### 3. Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "ApplicantDB"
}
```

---

## RiskRulesDB MCP Server (Port 8002)

**Base URL:** `http://localhost:8002`

### 1. Assess Risk

**Endpoint:** `POST /assess_risk`

**Description:** MCP endpoint for financial risk assessment.

**Request Body:**
```json
{
  "dti_ratio": 35.5,
  "credit_score": 720,
  "loan_amount": 100000,
  "annual_income": 75000,
  "query_type": "financial_risk"
}
```

**Response:**
```json
{
  "status": "success",
  "assessment": {
    "dti_risk": "medium",
    "credit_risk": "low",
    "loan_risk": "low",
    "anomalies": []
  }
}
```

**Risk Levels:**
- **DTI Risk:** low (< 35%), medium (35-43%), high (> 43%)
- **Credit Risk:** low (≥ 750), medium-low (700-749), medium (650-699), high (< 650)
- **Loan Risk:** low (≤ 50% of income), medium (50-100%), high (> 100%)

---

### 2. Get Risk Rules

**Endpoint:** `GET /rules`

**Description:** Returns current risk assessment rules.

**Response:**
```json
{
  "rules": {
    "dti_thresholds": {
      "low": 30,
      "medium": 40,
      "high": 50
    },
    "credit_thresholds": {
      "excellent": 750,
      "good": 700,
      "fair": 650,
      "poor": 600
    },
    "loan_limits": {
      "low_income": 50000,
      "medium_income": 150000,
      "high_income": 500000
    }
  }
}
```

---

### 3. Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "RiskRulesDB"
}
```

---

## DecisionSynthesis MCP Server (Port 8003)

**Base URL:** `http://localhost:8003`

### 1. Synthesize Decision

**Endpoint:** `POST /synthesize_decision`

**Description:** MCP endpoint for decision synthesis.

**Request Body:**
```json
{
  "applicant_id": "12345",
  "risk_score": 35.2,
  "income_stability": 82.5,
  "employment_risk": "low",
  "credit_risk": "low",
  "dti_ratio": 24.5
}
```

**Response:**
```json
{
  "status": "success",
  "decision": {
    "applicant_id": "12345",
    "classification": "approved",
    "risk_score": 35.2,
    "confidence": 0.90,
    "factors": [
      "Strong income stability",
      "Stable employment",
      "Good credit",
      "Healthy DTI"
    ]
  }
}
```

**Decision Classifications:**
- `approved` - Risk score < 40
- `review` - Risk score 40-60
- `rejected` - Risk score ≥ 60

---

### 2. Get Cached Decision

**Endpoint:** `GET /decisions/{applicant_id}`

**Description:** Retrieves cached decision for applicant.

**Parameters:**
- `applicant_id` (path, required): Applicant ID

**Response:**
```json
{
  "status": "success",
  "decision": {
    "applicant_id": "12345",
    "classification": "approved",
    "risk_score": 35.2,
    "confidence": 0.90,
    "factors": ["Strong income stability", "Stable employment"]
  }
}
```

**Response (Not Found):**
```json
{
  "status": "not_found"
}
```

---

### 3. Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "DecisionSynthesis"
}
```

---

## NotificationSystem MCP Server (Port 8004)

**Base URL:** `http://localhost:8004`

### 1. Send Notification

**Endpoint:** `POST /send_notification`

**Description:** MCP endpoint for sending notifications.

**Request Body:**
```json
{
  "applicant_id": "12345",
  "applicant_name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-555-0001",
  "case_id": "CASE-APP-12345-20260702111939",
  "decision": "approved",
  "action": "Approval letter sent"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Notification sent for case CASE-APP-12345-20260702111939",
  "notification": {
    "case_id": "CASE-APP-12345-20260702111939",
    "applicant_id": "12345",
    "applicant_name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0001",
    "decision": "approved",
    "action": "Approval letter sent",
    "timestamp": "2026-07-02T11:19:45.123456",
    "status": "sent"
  }
}
```

---

### 2. Get Notification Status

**Endpoint:** `GET /notifications/{case_id}`

**Description:** Retrieves notification status.

**Parameters:**
- `case_id` (path, required): Case ID

**Response:**
```json
{
  "status": "success",
  "notification": {
    "case_id": "CASE-APP-12345-20260702111939",
    "applicant_id": "12345",
    "applicant_name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0001",
    "decision": "approved",
    "action": "Approval letter sent",
    "timestamp": "2026-07-02T11:19:45.123456",
    "status": "sent"
  }
}
```

**Response (Not Found):**
```json
{
  "status": "not_found"
}
```

---

### 3. Get Notification History

**Endpoint:** `GET /notification_history`

**Description:** Retrieves recent notification history.

**Query Parameters:**
- `limit` (optional, default: 10): Number of recent notifications to return

**Response:**
```json
{
  "status": "success",
  "count": 3,
  "notifications": [
    {
      "case_id": "CASE-APP-12345-20260702111939",
      "applicant_id": "12345",
      "applicant_name": "John Doe",
      "decision": "approved",
      "timestamp": "2026-07-02T11:19:45.123456",
      "status": "sent"
    }
  ]
}
```

---

### 4. Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "NotificationSystem"
}
```

---

## Error Handling

### Common Error Responses

**400 Bad Request:**
```json
{
  "detail": "Invalid request parameters"
}
```

**404 Not Found:**
```json
{
  "detail": "Resource not found"
}
```

**422 Unprocessable Entity:**
```json
{
  "detail": [
    {
      "loc": ["body", "annual_income"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Processing failed: [error message]"
}
```

---

## Data Models

### LoanApplication
```json
{
  "applicant_id": "string (required)",
  "applicant_name": "string (required)",
  "email": "string (required)",
  "phone": "string (optional)",
  "annual_income": "float (required)",
  "employment_type": "string (required)",
  "employment_years": "integer (required)",
  "employment_company": "string (required)",
  "credit_score": "integer (required)",
  "existing_debt": "float (required)",
  "loan_amount": "float (required)",
  "loan_purpose": "string (required)",
  "employment_status": "string (required)",
  "loan_tenure": "integer (required)",
  "location": "string (required)"
}
```

### LoanDecision
```json
{
  "classification": "approved | rejected | review",
  "risk_score": "float (0-100)",
  "confidence_level": "float (0-1)",
  "key_decision_factors": "list[string]",
  "explanation": "string"
}
```

### ApplicationStatus
```
- "pending": Application submitted but not yet processed
- "approved": Application approved for funding
- "rejected": Application rejected
- "review": Application requires manual review
```

---

## Testing with cURL

### Submit Application
```bash
curl -X POST http://localhost:8000/submit_application \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "12345",
    "applicant_name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0001",
    "annual_income": 75000,
    "employment_type": "Full-time",
    "employment_years": 5,
    "employment_company": "TechCorp",
    "credit_score": 720,
    "existing_debt": 15000,
    "loan_amount": 100000,
    "loan_purpose": "Home Purchase",
    "employment_status": "employed",
    "loan_tenure": 10,
    "location": "New York, NY"
  }'
```

### Get Application Status
```bash
curl -X GET http://localhost:8000/application_status/CASE-APP-12345-20260702111939
```

### Search Applications
```bash
curl -X GET "http://localhost:8000/search_applications?search_query=John&status_filter=approved"
```

### Assess Risk
```bash
curl -X POST http://localhost:8002/assess_risk \
  -H "Content-Type: application/json" \
  -d '{
    "dti_ratio": 35.5,
    "credit_score": 720,
    "loan_amount": 100000,
    "annual_income": 75000,
    "query_type": "financial_risk"
  }'
```

---

## Version & Status

- **API Version:** 1.0.0
- **Last Updated:** 2026-07-02
- **Status:** Production Ready